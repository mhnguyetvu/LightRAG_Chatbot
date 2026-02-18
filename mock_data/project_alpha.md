# DỰ ÁN ALPHA — CRM SYSTEM CHO KHÁCH HÀNG FINTECH

## THÔNG TIN CHUNG

| Thông tin | Chi tiết |
|---|---|
| **Tên dự án** | Alpha CRM Platform |
| **Khách hàng** | MoneySmart Vietnam JSC |
| **Loại hợp đồng** | Fixed-price, T&M phần mở rộng |
| **Ngân sách** | 850,000,000 VND |
| **Thời gian** | 01/09/2024 – 28/02/2025 |
| **Trạng thái** | 🟡 In Progress (đang Sprint 6/10) |

## TEAM DỰ ÁN

| Vai trò | Họ tên | Email | Slack |
|---|---|---|---|
| Project Manager | Lê Văn Dũng | dung.le@techviet.vn | @dung.le |
| Tech Lead | Nguyễn Minh Quân | quan.nguyen@techviet.vn | @quan.nguyen |
| Backend Dev | Phạm Thị Hương | huong.pham@techviet.vn | @huong.pham |
| Backend Dev | Trần Đức Anh | anh.tran@techviet.vn | @anh.tran |
| Frontend Dev | Đỗ Thị Mai | mai.do@techviet.vn | @mai.do |
| QA Engineer | Nguyễn Văn Hùng | hung.nguyen@techviet.vn | @hung.nguyen |
| BA | Lê Thị Thu | thu.le@techviet.vn | @thu.le |

## TECH STACK
- **Backend:** Python FastAPI, PostgreSQL 16, Redis, Celery
- **Frontend:** React 18, TypeScript, TailwindCSS, Ant Design
- **Infrastructure:** AWS (ECS, RDS, ElastiCache, S3), Terraform
- **CI/CD:** GitHub Actions → ECR → ECS
- **Monitoring:** Datadog, Sentry

## TIẾN ĐỘ HIỆN TẠI (tính đến tuần 07/01/2025)

### Sprint 6 (06/01 – 17/01/2025) — Đang chạy
**Sprint Goal:** Hoàn thành module Loan Management + fix bugs Sprint 5

**Đang làm:**
- [ALPHA-142] API tính toán điểm tín dụng — Anh Tran (In Progress, 70%)
- [ALPHA-145] UI màn hình quản lý khoản vay — Mai Do (In Progress, 50%)
- [ALPHA-147] Fix bug: race condition khi approve loan đồng thời — Quan Nguyen (In Progress)
- [ALPHA-149] Viết test case module Payment — Hung Nguyen (Todo)

**Đã xong Sprint 6:**
- [ALPHA-141] API CRUD khách hàng vay — Huong Pham ✅
- [ALPHA-143] Tích hợp CIC API lấy lịch sử tín dụng — Anh Tran ✅

### Sprint 5 — Completed (23/12 – 03/01/2025)
- ✅ Module Customer Management (CRUD + search + filter)
- ✅ Authentication & Authorization (JWT + RBAC)
- ✅ Dashboard analytics cơ bản
- ⚠️ Performance issue: Query báo cáo tổng hợp chạy chậm (~8s) — chuyển sang Sprint 6

## VẤN ĐỀ ĐANG TỒN ĐỌNG

### 🔴 Critical
1. **[ALPHA-147] Race condition approve loan:** Khi 2 user approve cùng lúc, hệ thống tạo 2 bản ghi disbursement. Quan đang fix, dự kiến done 09/01.

### 🟡 Medium
2. **Performance query báo cáo:** Query phức tạp trên bảng transactions (~5M records) chạy 8 giây. Cần add index + optimize. Assign Anh.
3. **CIC API timeout:** Môi trường staging CIC hay timeout sau 30s. Đã báo MoneySmart, đang chờ họ xử lý.

### 🟢 Low
4. **UI/UX feedback từ client:** MoneySmart muốn thêm màu sắc trạng thái khoản vay. BA đang update wireframe.

## MILESTONES

| Milestone | Due Date | Status |
|---|---|---|
| M1: Core Infrastructure + Auth | 31/10/2024 | ✅ Done |
| M2: Customer Management Module | 29/11/2024 | ✅ Done (trễ 3 ngày) |
| M3: Loan Origination Module | 17/01/2025 | 🟡 In Progress |
| M4: Payment & Collection Module | 14/02/2025 | ⏳ Upcoming |
| M5: Reporting & Analytics | 21/02/2025 | ⏳ Upcoming |
| M6: UAT & Go-live | 28/02/2025 | ⏳ Upcoming |

## RỦI RO DỰ ÁN

| Rủi ro | Xác suất | Tác động | Biện pháp |
|---|---|---|---|
| CIC API không ổn định | Cao | Cao | Mock CIC + fallback manual review |
| Trễ deadline M3 | Trung bình | Cao | Tăng cường Anh support Backend |
| Client thay đổi yêu cầu | Trung bình | Trung bình | Change request process chặt chẽ |
| Mất nhân sự giữa dự án | Thấp | Cao | Knowledge sharing, document đầy đủ |

## MEETING SCHEDULE
- **Daily Standup:** 9:00 sáng, kênh Slack #alpha-standup
- **Sprint Planning:** Thứ Hai đầu sprint, 10:00-12:00, Phòng họp A
- **Sprint Review + Retro:** Thứ Sáu cuối sprint, 15:00-17:00
- **Weekly sync với MoneySmart:** Thứ Tư, 14:00-15:00 (Google Meet)
