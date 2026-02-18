# LightRAG Chatbot

Chatbot nội bộ sử dụng **LightRAG** để xây dựng knowledge graph từ tài liệu công ty, hỗ trợ truy vấn thông minh bằng ngôn ngữ tự nhiên.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI + LightRAG (HKU) |
| **Frontend** | Next.js 16 + TailwindCSS |
| **LLM** | Your choice |
| **Embeddings** | `BAAI/bge-small-en-v1.5` (local, CPU) |
| **Storage** | JSON files (Knowledge Graph) |

## Cấu trúc project

```
LightRAG_Chatbot/
├── backend/
│   ├── app/
│   │   ├── api/chat.py              # API endpoints
│   │   ├── core/
│   │   │   ├── config.py            # Settings
│   │   │   ├── vnpay_llm.py         # VNPay AI Gateway wrapper
│   │   │   └── openrouter_llm.py    # OpenRouter wrapper (fallback)
│   │   ├── services/
│   │   │   └── lightrag_service.py  # LightRAG integration
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   └── src/app/                     # Next.js pages
├── scripts/
│   ├── ingest.py                    # Load documents vào LightRAG
│   └── query.py                     # CLI query tool
├── mock_data/                       # Sample documents
├── config/
│   └── .env.example                 # Template biến môi trường
└── lightrag_cache/                  # Knowledge graph (auto-generated, gitignored)
```

## Cài đặt

### 1. Clone & setup backend

```bash
git clone <repo-url>
cd LightRAG_Chatbot

# Tạo virtual environment
cd backend
python3 -m venv rag_venv
source rag_venv/bin/activate
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

```bash
cp config/.env.example backend/.env
```

Chỉnh sửa `backend/.env`:

```env
# LLM Provider
LLM_PROVIDER=vnpay

# VNPay AI Gateway
VNPAY_API_KEY=<your-token>
VNPAY_BASE_URL=https://genai.vnpay.vn/aigateway/llm_v4/v1
VNPAY_MODEL=v_chat4

# Working directory (dùng absolute path)
WORKING_DIR=/absolute/path/to/LightRAG_Chatbot/lightrag_cache
```

> **LLM_PROVIDER** hỗ trợ: `vnpay` | `openrouter` | `gemini` | `openai`

### 3. Setup frontend

```bash
cd frontend
npm install
```

## Chạy ứng dụng

### Bước 1: Ingest documents

```bash
cd LightRAG_Chatbot
source backend/rag_venv/bin/activate
python scripts/ingest.py
```

Quá trình này sẽ:
- Đọc tất cả files trong `mock_data/` (`.md`, `.json`, `.txt`)
- Chunk text → tạo embeddings (local CPU)
- Extract entities & relationships qua LLM
- Lưu knowledge graph vào `lightrag_cache/`

> ⏱️ Lần đầu mất ~5-10 phút tùy số lượng documents

### Bước 2: Chạy backend

```bash
cd backend
source rag_venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Bước 3: Chạy frontend

```bash
cd frontend
npm run dev
```

Truy cập: **http://localhost:3000**

## Query modes

LightRAG hỗ trợ 4 chế độ tìm kiếm:

| Mode | Mô tả | Dùng khi |
|------|-------|----------|
| `local` | Tìm trong context cục bộ | Câu hỏi cụ thể về entity |
| `global` | Tìm toàn bộ knowledge graph | Câu hỏi tổng quan |
| `hybrid` | Kết hợp local + global | Mặc định, tốt nhất |
| `naive` | Tìm kiếm đơn giản | Debug |

## Thêm documents mới

Thêm file vào `mock_data/` (hỗ trợ `.md`, `.json`, `.txt`), sau đó chạy lại:

```bash
python scripts/ingest.py
```

> Không cần xóa cache cũ - LightRAG tự detect documents mới.

## CLI Query

```bash
source backend/rag_venv/bin/activate
python scripts/query.py "câu hỏi của bạn"
python scripts/query.py "câu hỏi" --mode hybrid
```

## API

```
POST /api/v1/chat/query
{
  "question": "công ty tên gì?",
  "mode": "local"
}
```

## Lưu ý

- `backend/.env` chứa API key → **không commit lên git** (đã có trong `.gitignore`)
- `lightrag_cache/` là database → **không commit** (gitignored)
- `WORKING_DIR` phải là **absolute path** để backend tìm đúng cache
- VNPay token có thể expire → cần lấy token mới khi bị lỗi 401
