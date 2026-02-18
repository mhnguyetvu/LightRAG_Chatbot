# DỰ ÁN BETA — AI CHATBOT CHO ECOMMERCE

## THÔNG TIN CHUNG

| Thông tin | Chi tiết |
|---|---|
| **Tên dự án** | Beta SmartBot |
| **Khách hàng** | ShopNow Vietnam (nội bộ — sản phẩm tự phát triển) |
| **Loại dự án** | Internal Product |
| **Ngân sách** | 400,000,000 VND (R&D budget) |
| **Thời gian** | 01/11/2024 – 30/04/2025 |
| **Trạng thái** | 🟢 On Track (Sprint 4/8) |

## TEAM DỰ ÁN

| Vai trò | Họ tên | Slack |
|---|---|---|
| Product Owner | Vũ Thị Linh | @linh.vu |
| Tech Lead / AI Lead | Hoàng Minh Đức | @duc.hoang |
| AI Engineer | Nguyễn Thị Phương | @phuong.nguyen |
| Backend Dev | Bùi Văn Nam | @nam.bui |
| Frontend Dev | Trần Thị Hà | @ha.tran |
| DevOps | Lý Văn Khải | @khai.ly |

## TECH STACK
- **AI/ML:** LangChain, OpenAI GPT-4o, LightRAG (Knowledge Base), Chroma DB
- **Backend:** Python FastAPI, Redis (session), PostgreSQL
- **Frontend:** React + WebSocket (real-time chat)
- **Infrastructure:** RunPod (GPU inference), GCP (Cloud Run, Cloud SQL)
- **Model:** Fine-tuned GPT-4o-mini cho domain ecommerce VN

## TIẾN ĐỘ (tính đến 07/01/2025)

### Sprint 4 (06/01 – 17/01/2025) — Đang chạy
**Sprint Goal:** Tích hợp LightRAG Knowledge Base + cải thiện độ chính xác câu trả lời

**Tasks:**
- [BETA-67] Setup LightRAG với dữ liệu sản phẩm 10k items — Duc Hoang (In Progress, 60%)
- [BETA-68] API endpoint /chat với conversation history — Nam Bui (In Progress, 80%)
- [BETA-69] UI chat widget embed được vào website — Ha Tran (In Progress, 40%)
- [BETA-70] Optimize embedding model cho tiếng Việt — Phuong Nguyen (Todo)
- [BETA-71] Setup monitoring latency + cost tracking — Khai Ly (In Progress)

### Sprint 3 — Completed
- ✅ Intent classification (14 intent classes, accuracy 87%)
- ✅ Slot filling cho order tracking
- ✅ Kết nối API đơn hàng ShopNow
- ✅ Fallback to human agent khi confidence < 0.6
- ⚠️ Tiếng Việt có dấu đặc biệt gây lỗi tokenizer — đã có workaround

## KẾT QUẢ HIỆN TẠI (Metrics Sprint 3)
- **Intent Accuracy:** 87.3% (target: 90%)
- **Response Latency P95:** 2.3s (target: <3s) ✅
- **Fallback Rate:** 18% (target: <15%) — cần cải thiện
- **User Satisfaction (beta test 50 users):** 3.8/5 (target: 4.0)

## VẤN ĐỀ ĐANG TỒN ĐỌNG
1. **Tiếng lóng / từ địa phương:** Bot không hiểu "ib" (inbox), "oke bro", "giá đẹp chưa anh ơi"
2. **Context window:** Hội thoại dài >10 turns bị mất context — cần sliding window
3. **Latency spike:** Đôi khi GPT-4o bị 6-8s do rate limit → đang test song song claude-3-haiku

## UPCOMING SPRINTS
- **Sprint 5:** Multilingual support (Anh-Việt mixed), nâng accuracy lên 90%+
- **Sprint 6:** A/B test với human agent, đo conversion rate
- **Sprint 7:** Scale test 1000 concurrent users
- **Sprint 8:** Beta launch cho 5 shop đối tác

## NOTES QUAN TRỌNG
- RunPod GPU (RTX 4090) được dùng để chạy BGE-M3 embedding, giảm 70% chi phí so với OpenAI embedding
- Linh (PO) họp với ShopNow mỗi thứ Tư 10:00 để review demo
- Duc đang research thêm về GraphRAG để tăng chất lượng KB
