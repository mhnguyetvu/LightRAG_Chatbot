# 🐿️ SQUIRREL MINI — SETUP GUIDE
## Phân chia Local (M1 Pro) vs RunPod (RTX 4090)

---

## TỔNG QUAN CHI PHÍ

| Giai đoạn | Chạy ở đâu | Thời gian bật RunPod | Chi phí RunPod |
|---|---|---|---|
| Phase 1: Setup môi trường | Local | 0 | $0 |
| Phase 2: Chuẩn bị mock data | Local | 0 | $0 |
| Phase 3: Indexing vào LightRAG | **RunPod** | ~2-3 giờ | ~$1.5-2 |
| Phase 4: Dev & Test features | Local + OpenAI API | 0 | ~$3-5 tổng API |
| Phase 5: Demo | Local serve | 0 | $0 |
| **TỔNG** | | **~3 giờ RunPod** | **~$5-7** |

> 💡 **Chiến lược chính:** Chỉ bật RunPod để index data (nặng, cần GPU cho embedding nhanh).
> Sau khi index xong, data lưu vào storage local → query bình thường qua OpenAI API (rẻ hơn).

---

## PHASE 1 — SETUP LOCAL (M1 Pro)

### 1.1 Install dependencies

```bash
# Tạo virtual environment
python -m venv .venv
source .venv/bin/activate

# Install LightRAG
pip install "lightrag-hku[api]"

# Install thêm
pip install fastapi uvicorn streamlit python-dotenv textract
```

### 1.2 Setup PostgreSQL local (dùng Docker)

```bash
# Pull và chạy PostgreSQL với pgvector + AGE
docker run -d \
  --name squirrel-postgres \
  -e POSTGRES_USER=squirrel \
  -e POSTGRES_PASSWORD=squirrel123 \
  -e POSTGRES_DB=squirrel_rag \
  -p 5432:5432 \
  gzdaniel/postgres-for-rag:latest

# Verify
docker ps
```

### 1.3 Tạo file .env

```bash
# .env
LLM_BINDING=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-xxx-your-key

EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIM=1536

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=squirrel
POSTGRES_PASSWORD=squirrel123
POSTGRES_DATABASE=squirrel_rag

# Storage backends (dùng PostgreSQL all-in-one)
KV_STORAGE=PGKVStorage
VECTOR_STORAGE=PGVectorStorage
GRAPH_STORAGE=PGGraphStorage
DOC_STATUS_STORAGE=PGDocStatusStorage

# Vietnamese language
LIGHTRAG_LANGUAGE=Vietnamese
```

### 1.4 Start LightRAG Server (test)

```bash
lightrag-server --host 0.0.0.0 --port 9621
# Truy cập: http://localhost:9621 để xem Web UI
```

---

## PHASE 2 — SETUP RUNPOD (Chỉ khi cần index)

### 2.1 Tạo RunPod Pod

Trên RunPod dashboard:
- **GPU:** RTX 4090 (24GB)
- **Template:** RunPod PyTorch 2.x (hoặc Ollama template)
- **Disk:** 50GB (đủ chứa Qwen2.5:32B ~20GB + BGE-M3 ~1.5GB)
- **Expose ports:** 11434 (Ollama), 8888 (Jupyter nếu cần)

### 2.2 Setup Ollama trên RunPod

```bash
# SSH vào RunPod
ssh -i ~/.ssh/id_rsa root@<runpod-ip> -p <port>

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models (chạy background, tốn 15-30 phút)
ollama pull qwen2.5:32b &        # ~20GB — LLM chính
ollama pull bge-m3 &              # ~1.5GB — Embedding tiếng Việt

# Expose Ollama ra ngoài (mặc định chỉ localhost)
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

### 2.3 Test kết nối từ Local

```bash
# Test từ máy local
curl http://<runpod-ip>:<exposed-port>/api/tags
# Phải thấy list models: qwen2.5:32b, bge-m3
```

### 2.4 Chạy ingest script từ Local → RunPod

```bash
# Clone project về local (nếu chưa có)
cd squirrel_mini

# Chạy ingest với Ollama trên RunPod
OLLAMA_BASE_URL=http://<runpod-ip>:<port> python scripts/ingest.py \
  --llm ollama \
  --ollama-url http://<runpod-ip>:<port> \
  --data-dir ./squirrel_mock_data

# Hoặc nếu muốn nhanh hơn, dùng OpenAI:
OPENAI_API_KEY=sk-xxx python scripts/ingest.py --llm openai
```

> ⏱️ **Ước tính thời gian indexing mock data này:**
> - Với OpenAI GPT-4o-mini: ~15-20 phút (~$0.30-0.50)
> - Với Qwen2.5:32B trên 4090: ~45-60 phút (free sau khi setup)

### 2.5 Tắt RunPod sau khi index xong!

Data đã lưu vào PostgreSQL local → RunPod không cần nữa cho dev phase.

```bash
# Trên RunPod dashboard → Stop pod
# Hoặc: dùng RunPod CLI
runpodctl stop pod <pod-id>
```

---

## PHASE 3 — BUILD FEATURES (Local)

Sau khi có data trong LightRAG, build các tính năng:

### 3.1 Tóm tắt tin nhắn chưa đọc

```python
# feature/summarize.py
async def summarize_unread(channel: str, messages: list[dict], user: str, rag: LightRAG):
    # Insert tin nhắn mới vào RAG trước (để cập nhật KB)
    text = format_messages(messages)
    await rag.ainsert(text, ids=[f"chat_{channel}_{today}"])

    # Query tóm tắt
    return await rag.aquery(
        f"Tóm tắt các tin nhắn chưa đọc trong kênh {channel}. "
        f"Highlight: quyết định quan trọng, task được giao, deadline, vấn đề cần xử lý.",
        param=QueryParam(
            mode="naive",  # naive đủ dùng cho recent messages
            user_prompt="Trả lời bằng tiếng Việt. Format: [Tóm tắt 2-3 câu] + [Bullet points: actions/decisions]"
        )
    )
```

### 3.2 Báo cáo công việc theo ngày

```python
async def daily_report(user: str, date: str, rag: LightRAG):
    return await rag.aquery(
        f"Tổng hợp toàn bộ công việc của {user} trong ngày {date}: "
        f"tasks đã hoàn thành, đang làm, gặp vấn đề gì, được giao task mới nào.",
        param=QueryParam(
            mode="hybrid",
            user_prompt="Trả lời tiếng Việt. Format báo cáo EOD: ✅ Done / 🔄 In Progress / ❌ Blocked / 📌 New Tasks"
        )
    )
```

### 3.3 Q&A nội bộ

```python
async def internal_qa(question: str, rag: LightRAG):
    return await rag.aquery(
        question,
        param=QueryParam(
            mode="local",
            user_prompt=(
                "Trả lời dựa trên tài liệu nội bộ công ty TechViet. "
                "Nếu không có thông tin đủ, hãy nói rõ và gợi ý liên hệ ai. "
                "Trả lời bằng tiếng Việt."
            )
        )
    )
```

### 3.4 Chạy Streamlit UI

```bash
streamlit run app.py
```

---

## QUICK COMMANDS CHEATSHEET

```bash
# Bật PostgreSQL (mỗi lần restart Mac)
docker start squirrel-postgres

# Start LightRAG server
source .venv/bin/activate
lightrag-server --port 9621

# Chạy Streamlit
streamlit run app.py --server.port 8501

# Ingest thêm data mới (không cần RunPod nếu dùng OpenAI)
python scripts/ingest.py --llm openai --data-dir ./new_data

# Xem logs LightRAG
tail -f lightrag.log

# Connect RunPod khi cần re-index lớn
runpodctl start pod <pod-id>
ssh root@<runpod-ip> -p <port>
```

---

## LƯU Ý QUAN TRỌNG

1. **Embedding model phải nhất quán:** Chọn 1 model từ đầu (OpenAI `text-embedding-3-small` hoặc `bge-m3`). Nếu đổi model → phải xóa toàn bộ vector data và re-index.

2. **Tiếng Việt:** Đã set `language: Vietnamese` trong `addon_params` → LightRAG sẽ extract entities bằng tiếng Việt.

3. **Context window:** Qwen2.5:32B cần `num_ctx: 32768` (32k tokens), không phải 8k mặc định.

4. **RunPod cost:** RTX 4090 trên RunPod ~$0.44/giờ. Chỉ bật khi cần, **nhớ tắt** sau khi xong!

5. **Data privacy:** Mock data này an toàn. Khi dùng data thật, cân nhắc dùng Ollama local 100% để không gửi data ra ngoài.
