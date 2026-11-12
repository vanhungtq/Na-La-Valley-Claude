---
name: ho-so-quay
description: Dựng hồ sơ quay in được (production-book.html) và shotlist.csv cho một tập Nà Lạ Valley từ shots.json. Dùng khi chủ dự án nói "xuất hồ sơ quay", "in shot list", "/ho-so-quay 01", hoặc sau khi shots.json thay đổi.
argument-hint: "<số tập>"
---

1. `python3 scripts/validate_episode.py episodes/epNN` — nếu CHƯA ĐẠT, liệt kê lỗi và hỏi chủ dự án có muốn xuất bản nháp không.
2. `python3 scripts/build_production_book.py episodes/epNN`
3. Báo đường dẫn hai file và nhắc: mở HTML bằng trình duyệt → In → Lưu PDF (khổ A4 ngang cho bảng storyboard). Ảnh storyboard tham chiếu bằng đường dẫn tương đối nên phải giữ thư mục `06-storyboard/` cạnh file HTML.
4. Nếu chủ dự án cần xem trên điện thoại trong phiên cloud, gửi file HTML cho họ bằng công cụ gửi file nếu có.

Hồ sơ gồm: lịch quay gom theo khung giờ ánh sáng của Bible, danh sách đạo cụ, bảng shot kèm hình theo cảnh, kế hoạch âm thanh từng cảnh, danh sách thu foley.
