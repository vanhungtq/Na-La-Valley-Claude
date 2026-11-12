---
name: phan-tich-reference
description: Đưa một video mẫu (Lý Tử Thất, Điền Tây Tiểu Ca, kênh slow living khác) vào thư viện kiến thức Nà Lạ Valley dưới dạng phân tích có timecode. Claude không xem được video nên skill này tạo prompt để Gemini xem, rồi chuẩn hóa kết quả. Dùng khi chủ dự án nói "phân tích video này", "học từ video mẫu", "/phan-tich-reference <url>".
argument-hint: "<url YouTube> [điều muốn học]"
---

# Phân tích video mẫu

**Sự thật cần nói thẳng:** Claude không xem được video YouTube. Gemini (ứng dụng, gói Pro của chủ dự án) nhận link YouTube và xem được. Vì vậy quy trình có một bước tay.

## Bước 1 — Đưa prompt cho chủ dự án dán vào Gemini

Hiển thị khối sau (thay `<URL>` và `<điều muốn học>`):

```text
Watch this YouTube video in full: <URL>

I am a filmmaker studying its craft to make my own original rural slow-living
videos in northern Vietnam. Analyse only what is actually visible/audible.
If you cannot access part of the video, say so instead of guessing.

Return, in Vietnamese:
1. Bảng cấu trúc theo timecode (mm:ss–mm:ss | phần | chuyện gì xảy ra | ghi chú hình/tiếng), mỗi dòng 20–60 giây.
2. Số liệu quan sát: ước số shot và độ dài shot trung bình ở 3 đoạn (mở đầu, lao động, nấu ăn); tỷ lệ máy tĩnh/máy động; cỡ cảnh chiếm ưu thế; đoạn nào có nhạc, đoạn nào im nhạc; có chữ trên hình không.
3. Hook: 30 giây đầu gồm những shot nào, theo thứ tự.
4. 5 kỹ thuật kể chuyện/quay/âm thanh đáng học, mỗi kỹ thuật có timecode ví dụ.
5. Những chi tiết là "chữ ký" riêng của kênh này mà người khác không nên bắt chước.
6. Phần nào bạn chắc chắn (đã thấy), phần nào là suy đoán.
Trọng tâm tôi muốn học: <điều muốn học>
```

## Bước 2 — Nhận kết quả

Chủ dự án dán câu trả lời của Gemini vào phiên. Nếu họ tự xem và ghi chú tay thì cũng dùng được.

## Bước 3 — Chuẩn hóa

Giao agent `thu-thu` (loại việc 2) với URL và văn bản đã dán, lưu vào `knowledge/references/`.

## Bước 4 — Báo lại

Tên file đã lưu, 3–5 nguyên tắc rút ra áp dụng được với A6400 + 18-105 F4, và lời nhắc: số liệu do model ước lượng, nên xem lại vài timecode để kiểm.

Mục tiêu khởi đầu hợp lý: 5–8 video mẫu thuộc 3 loại (dựng/sửa nhà, nấu ăn từ vườn, thủ công) trước khi viết tập đầu.
