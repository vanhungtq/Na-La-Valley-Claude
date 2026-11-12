---
name: tien-trinh
description: Cho chủ dự án xem tiến trình của xưởng Nà Lạ Valley - agent nào đang làm gì, tập đang ở bước nào, việc nào đang chờ. Dùng khi chủ dự án nói "xem tiến trình", "agents đang làm gì", "mở dashboard", "/tien-trinh".
---

Bảng tiến trình nằm trong app: tab **Agents** (toàn xưởng, hàng việc) và tab **Tiến trình** của từng tập. Đưa chủ dự án link trong `studio/app.json` (thêm `#agents`).

App chỉ hiện những gì đã được ghi lên. Nếu chủ dự án thấy app không khớp việc đang chạy: ghi ngay tài liệu `episodes/<ep>` theo mục 4 của skill `studio`, và nói thật là bước trước đó chưa được đẩy lên.

Không có mạng tới app: `python3 scripts/progress.py build` dựng `dashboard.html` cục bộ từ `status.json`.
