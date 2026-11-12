---
name: tien-trinh
description: Mở bảng tiến trình (dashboard) của xưởng Nà Lạ Valley - các bước của từng tập, agent nào đang làm gì, nhật ký, tiến độ ảnh thực tế, số liệu thư viện. Dùng khi chủ dự án nói "xem tiến trình", "agents đang làm gì", "mở dashboard", "/tien-trinh".
---

1. `python3 scripts/progress.py build` — dựng lại `dashboard.html` ở gốc repo từ `episodes/*/status.json` và `shots.json`.
2. Muốn xem **trực tiếp** trong lúc agents chạy: khởi động máy chủ tĩnh ở gốc repo, chạy nền:

   ```
   python3 -m http.server 8765
   ```

   Mở `http://localhost:8765/dashboard.html`; trang tự làm mới mỗi 5 giây. Trong phiên cloud, báo cổng 8765 cho ứng dụng bằng công cụ báo cổng xem trước nếu có; không có thì gửi file `dashboard.html` cho chủ dự án.
3. Không cần máy chủ: mở thẳng file `dashboard.html` (ảnh chụp tại thời điểm dựng).

Dashboard chỉ phản ánh những gì đã được ghi bằng `scripts/progress.py`. Nếu chủ dự án thấy nó không khớp việc đang diễn ra, nói thật là một bước nào đó đã không ghi tiến trình, rồi ghi bổ sung.
