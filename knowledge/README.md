# Thư viện kiến thức Nà Lạ Valley

Mọi agent đọc thư viện này trước khi làm việc. Thứ tự ưu tiên khi có mâu thuẫn: **lời chủ dự án trong phiên > brief của tập > Project Bible > các file còn lại**.

| Nơi | Nội dung | Ai viết |
|---|---|---|
| `00-project-bible.md` | Bible gốc (nguyên văn, chỉ bỏ một dấu ``` thừa ở dòng cuối). **Không agent nào được sửa.** | Chủ dự án |
| `01-nguyen-tac-ke-chuyen.md` | Cách kể chuyện không lời, cấu trúc tập, nhịp dựng | Claude (khởi điểm) |
| `02-thiet-bi-va-rang-buoc.json` | Ràng buộc máy/ống kính/ngữ pháp, script kiểm tra đọc file này | Từ Bible |
| `03-nhan-vat-va-prompt-anh.md` | Ảnh tham chiếu đi vào đâu, prompt ảnh được lắp ghép thế nào | Claude |
| `04-khan-gia-quoc-te-youtube.md` | Tiêu đề, thumbnail, giữ chân, phụ đề cho khán giả nước ngoài | Claude (khởi điểm) |
| `05-rubric-kich-ban.md` | Thang chấm kịch bản 10 tiêu chí | Claude |
| `06-rubric-storyboard.md` | Chuẩn storyboard, cách nhận xét ảnh thực tế | Claude |
| `video-mau/` | Clip mẫu chủ dự án tải lên **Thư viện trong app** (khung hình, ghi chú), tải về phiên để phân tích; không commit | Thủ thư |
| `kien-thuc/` | Tài liệu chủ dự án tải lên app; không commit | Thủ thư |
| `chu-de/` | Nghiên cứu có nguồn do Thủ thư tra cứu (mùa vụ, món ăn, kỹ thuật thủ công) | Thủ thư |
| `ky-thuat/` | Thẻ kỹ thuật chưng cất từ thư viện, có bằng chứng | `/hoc-tu-thu-vien`, bạn duyệt |
| `so-tay/` | Sổ tay riêng của từng agent, đọc trước mỗi lần làm việc | `/hoc-tu-thu-vien` |
| `visual-refs/` | Ảnh thật dùng cho mọi tập (nhân vật, chòi) | Chủ dự án |

## Vòng học

```
bạn thêm clip + ghi chú vào Thư viện trong app  →  "Phân tích mục mới"  →  phân tích hiện trong app
   →  "Rút kỹ thuật & nâng cấp agents"  →  thẻ KT-xxx đề xuất hiện trong app  →  bạn bấm Duyệt / Bỏ
   →  thẻ đã duyệt ghi vào so-tay/<agent>.md  →  agent đọc sổ tay trước khi viết  →  shot ghi "technique": ["KT-xxx"]
```

## Ba loại dữ kiện — luôn ghi nhãn

- **[ĐÃ XEM]** — agent đã tự đọc file/ảnh trong repo.
- **[CHỦ DỰ ÁN]** — chủ dự án nói trong brief hoặc trong phiên.
- **[GIẢ ĐỊNH]** — suy đoán sáng tạo, cần xác nhận trước khi quay.

Tên file hoặc URL không chứng minh nội dung. Claude không xem được video: nhưng xem được chuỗi khung hình app trích từ clip bạn tải lên.

## Thêm kiến thức mới

Thêm trong tab Thư viện của app. Bài học sau mỗi tập quay xong được ghi vào `so-tay/`.
