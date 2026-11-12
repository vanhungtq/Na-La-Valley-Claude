# Hộp thư đến của thư viện

Thả **bất cứ thứ gì** bạn muốn hệ thống học vào đây, rồi nói với Claude `/nap-thu-vien`. Không cần đặt tên chuẩn hay sắp xếp trước.

## Video mẫu của kênh khác — tạo một thư mục cho mỗi video

```
inbox/ly-tu-that-lam-ban-tre/
  noi-dung.txt      nội dung / lời bình / ghi chú của bạn về video (tùy chọn)
  timeline.txt      mốc thời gian: "0:00–0:25 hook: chặt tre..." (tùy chọn)
  shots/            ảnh chụp màn hình từng cú máy
     001_0m05.jpg   tên file nên có số thứ tự; có thêm timecode càng tốt
     002_0m12.jpg
  link.txt          đường dẫn video gốc (tùy chọn)
```

Thiếu phần nào cũng được. Chỉ có ảnh các cú máy vẫn học được: Claude tự xem từng ảnh và mô tả cỡ cảnh, góc máy, bố cục, ánh sáng. Điều Claude **không** làm được là xem video; muốn có timeline tự động thì dùng Gemini (lệnh `/nap-thu-vien` sẽ đưa prompt).

## Kiến thức khác

File `.md`, `.txt`, `.pdf`, ảnh sơ đồ ánh sáng, ghi chú quay, bài viết bạn lưu lại… cứ thả thẳng vào `inbox/`.

Ảnh nên thu nhỏ còn cạnh dài khoảng 1600 px trước khi thả vào để repo không phình.
