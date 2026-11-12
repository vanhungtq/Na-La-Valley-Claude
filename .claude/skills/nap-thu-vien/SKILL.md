---
name: nap-thu-vien
description: Nhập những gì chủ dự án đã thả vào knowledge/inbox của Nà Lạ Valley vào thư viện kiến thức - video mẫu của kênh khác (văn bản nội dung, timeline, ảnh từng cú máy), tài liệu, ghi chú. Dùng khi chủ dự án nói "tôi vừa tải video mẫu lên", "nạp thư viện", "phân tích video này", "/nap-thu-vien".
argument-hint: "[tên thư mục trong inbox] [url video]"
---

# Nhập thư viện

## 1. Xem inbox có gì

Liệt kê `knowledge/inbox/` (bỏ qua README.md). Trống thì chỉ cho chủ dự án cách thả file theo `knowledge/inbox/README.md` và dừng.

Nói lại ngắn gọn: mấy video mẫu (mỗi video bao nhiêu ảnh cú máy, có timeline/nội dung không), mấy tài liệu.

## 2. Giao Thủ thư

Giao agent `thu-thu` loại việc 2, **mỗi video mẫu một lần giao** (video nhiều ảnh cần trọn ngữ cảnh). Nhắc: mở từng ảnh; điều không thấy được từ ảnh tĩnh thì để trống.

## 3. Nếu chủ dự án chỉ có link video, chưa có timeline

Claude không xem được video. Đưa chủ dự án prompt này để dán vào **ứng dụng Gemini** (xem được YouTube), rồi lưu câu trả lời thành `inbox/<tên>/timeline.txt`:

```text
Watch this YouTube video in full: <URL>

I am a filmmaker studying its craft to make my own original rural slow-living
videos. Describe only what is actually visible/audible; if you cannot access
part of the video, say so instead of guessing.

Trả lời bằng tiếng Việt:
1. Bảng timeline (mm:ss–mm:ss | phần | chuyện gì xảy ra | ghi chú hình/tiếng), mỗi dòng 20–60 giây.
2. Danh sách 25–40 cú máy tiêu biểu: timecode | cỡ cảnh | góc máy | máy tĩnh hay động | ánh sáng | hành động.
3. Ước số shot và độ dài shot trung bình ở 3 đoạn (mở đầu, lao động, nấu ăn); đoạn nào có nhạc, đoạn nào im nhạc; có chữ trên hình không.
4. 30 giây đầu gồm những shot nào, theo thứ tự.
5. Những chi tiết là chữ ký riêng của kênh này.
6. Phần nào bạn chắc chắn đã thấy, phần nào là suy đoán.
```

Ảnh từng cú máy vẫn do chủ dự án chụp màn hình tại các timecode đáng học và thả vào `inbox/<tên>/shots/`. Ảnh là thứ làm thư viện có giá trị nhất, vì Claude tự xem được.

## 4. Báo lại

Mỗi video: thư mục đã tạo trong `knowledge/video-mau/`, số cú máy đã mô tả, 3 điều đáng học nhất, và phần còn trống (không có timeline, không có âm thanh…). Chạy `python3 scripts/progress.py build` để dashboard cập nhật số liệu thư viện.

Gợi ý bước tiếp: khi thư viện có từ 2–3 video trở lên, chạy `/hoc-tu-thu-vien` để chưng cất thành thẻ kỹ thuật và nâng cấp sổ tay các agent.
