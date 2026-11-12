# Video mẫu đã phân tích

Mỗi video một thư mục `<kenh>-<ten-ngan>/`, do Thủ thư tạo từ `knowledge/inbox/` qua lệnh `/nap-thu-vien`.

```
<kenh>-<ten-ngan>/
  reference.json   dữ liệu có cấu trúc (xem _mau/reference.json)
  phan-tich.md     bài phân tích đọc được: cấu trúc, số liệu, kỹ thuật đáng học, điều không sao chép
  noi-dung.md      văn bản gốc chủ dự án cung cấp (giữ nguyên)
  frames/          ảnh từng cú máy, đánh số 001.jpg, 002.jpg…
```

## Nhãn nguồn bắt buộc trong `reference.json`

Mỗi shot có trường `nguon`:

- `da-xem-anh` — Claude đã mở ảnh cú máy đó và tự mô tả.
- `chu-du-an` — mô tả do chủ dự án ghi.
- `gemini` — do Gemini xem video rồi viết; số liệu là ước lượng của model.

Không có nhãn thứ tư. Claude không xem video nên không được ghi như thể đã xem.

Các thẻ kỹ thuật trong `knowledge/ky-thuat/` trỏ về shot ở đây làm bằng chứng (`<thư-mục>#<số shot>`).
