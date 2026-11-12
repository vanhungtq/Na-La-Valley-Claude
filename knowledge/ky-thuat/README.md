# Thẻ kỹ thuật

Mỗi thẻ là **một** kỹ thuật kể chuyện, quay, âm thanh hoặc đóng gói đã được chưng cất từ thư viện, viết sao cho agent áp dụng được ngay. Thẻ do lệnh `/hoc-tu-thu-vien` tạo; chủ dự án duyệt trước khi thẻ có hiệu lực.

Tên file: `KT-001-ten-ngan.md`. Trong `shots.json`, shot áp dụng kỹ thuật ghi `"technique": ["KT-001"]` và thẻ đó hiện trên báo cáo.

## Mẫu thẻ

```markdown
# KT-001 · <Tên kỹ thuật>

- **Loại:** kể chuyện / quay / ánh sáng / âm thanh / dựng / đóng gói
- **Dành cho:** bien-kich, quay-phim (agent nào cần đọc)
- **Trạng thái:** đề xuất / đã duyệt <ngày> / đã thử ở tập NN
- **Độ tin cậy:** thấp (1 nguồn) / vừa (2–3 nguồn) / cao (nhiều nguồn + đã thử thực địa)

## Là gì
Hai ba câu, mô tả thứ nhìn thấy/nghe thấy trên màn hình.

## Vì sao hiệu quả
Tác động lên người xem. Ghi rõ đây là nhận định hay có số liệu.

## Bằng chứng
- `video-mau/<thư-mục>#<số shot>` (timecode) — mô tả ngắn
- …

## Cách làm với Sony A6400 + 18-105 F4
Tiêu cự, khoảng cách, chiều cao máy, giờ quay, thiết bị phụ. Điều không làm được với bộ máy này và cách thay thế.

## Khi nào dùng / khi nào không
…

## Không sao chép
Phần nào là chữ ký của kênh gốc cần biến đổi.
```

## Quy tắc

- Một thẻ chỉ có hiệu lực khi có ít nhất một bằng chứng trỏ được tới file trong thư viện. Không có bằng chứng thì đó là ý kiến, ghi vào sổ tay với nhãn [GIẢ ĐỊNH].
- Sau khi quay, cập nhật mục Trạng thái: kỹ thuật có chạy được ngoài thực địa không.
