# Thư viện kiến thức Nà Lạ Valley

Mọi agent đọc thư viện này trước khi làm việc. Thứ tự ưu tiên khi có mâu thuẫn: **lời chủ dự án trong phiên > brief của tập > Project Bible > các file còn lại**.

| File | Nội dung | Ai dùng |
|---|---|---|
| `00-project-bible.md` | Bible gốc của chủ dự án (nguyên văn, chỉ bỏ một dấu ``` thừa ở dòng cuối). **Không agent nào được sửa.** | Tất cả |
| `01-nguyen-tac-ke-chuyen.md` | Cách kể chuyện không lời, cấu trúc tập, nhịp dựng | Biên kịch, Giám sát |
| `02-thiet-bi-va-rang-buoc.json` | Ràng buộc máy/ống kính/ngữ pháp dạng máy đọc được | Quay phim, script kiểm tra |
| `03-nhan-vat-va-prompt-anh.md` | Mô tả nhân vật cố định + khối prompt chuẩn cho ảnh storyboard | Họa sĩ storyboard |
| `04-khan-gia-quoc-te-youtube.md` | Tiêu đề, thumbnail, giữ chân, phụ đề cho khán giả nước ngoài | Chiến lược YouTube |
| `chu-de/` | Nghiên cứu theo chủ đề có nguồn (mùa vụ, món ăn, kỹ thuật thủ công) do Thủ thư viết | Biên kịch, Chiến lược YouTube |
| `references/` | Phân tích video mẫu có timecode (mỗi video một file) | Biên kịch, Quay phim |
| `visual-refs/` | Ảnh thật của bối cảnh/nhân vật/đạo cụ và model sheet | Họa sĩ storyboard |

## Ba loại dữ kiện — luôn ghi nhãn

- **[ĐÃ XEM]** — agent đã tự đọc file/ảnh trong repo.
- **[CHỦ DỰ ÁN]** — chủ dự án nói trong brief hoặc trong phiên.
- **[GIẢ ĐỊNH]** — suy đoán sáng tạo, cần xác nhận trước khi quay.

Tên file hoặc URL không chứng minh nội dung. Claude không xem được video: phân tích video mẫu phải đi qua `/phan-tich-reference` (Gemini xem, người dán kết quả vào `references/`).

## Thêm kiến thức mới

- Video mẫu → `/phan-tich-reference <url>`.
- Ảnh khảo sát hiện trường → thả vào `visual-refs/` theo quy ước trong `visual-refs/README.md`.
- Bài học sau mỗi tập quay xong → thêm mục vào `01-nguyen-tac-ke-chuyen.md` phần "Bài học thực địa" (ghi tập và ngày).
