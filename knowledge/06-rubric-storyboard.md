# Chuẩn storyboard

Một khung storyboard đạt khi **người cầm máy đọc xong là đặt được chân máy** mà không phải hỏi lại. Chuẩn này rút từ thực hành storyboard quay thật và từ cơ chế giữ nhất quán của StoryGen-Atelier (mô tả chủ thể cố định, ảnh tham chiếu, liên tục với khung trước, liên kết nhân quả).

## Mỗi shot phải có

| Trường | Viết gì | Ví dụ |
|---|---|---|
| `action` | Hành động nhìn thấy được, một câu | Chị đẩy lưỡi bào trên vách ván; phoi vàng bay trong nắng |
| `link` | Vì sao shot này đi sau shot trước | Nhìn xong thì làm: việc đầu tiên là bào lớp gỗ mốc |
| `composition` | Chủ thể ở đâu trong khung (thirds), tiền/trung/hậu cảnh, đường dẫn, hướng chuyển động vào/ra khung | Chị 1/3 phải, đường bào chéo về máy, phoi bay vào vùng nắng 1/3 trái |
| `light` | Hướng, chất, nguồn sáng thật tại giờ quay | Nắng xiên 45° từ sau lưng làm phoi sáng lên |
| `direction` | Lệnh cho người quay: vị trí máy, chiều cao, khoảng cách, tiêu cự, diễn viên làm gì, quay mấy lượt, lưu ý an toàn | Máy nghiêng 45° so với vách, 50mm, ngang tay bào. Gắn ND. Đẩy 6–8 đường liên tục |
| `cut` | Cắt sang shot sau thế nào: theo hành động, theo tiếng, theo hướng mắt | Cắt giữa một đường bào sang bản cận 105mm |
| `frame_en` | **Một khoảnh khắc đóng băng** bằng tiếng Anh cho model ảnh: ai, đang ở tư thế nào, vật gì ở đâu. Không viết chuyển động kéo dài, không viết cảm xúc trừu tượng | The older sister pushes a hand plane in a long stroke…; curls of golden shavings catch the backlight |
| `composition_en`, `angle_en` | Bản tiếng Anh ngắn của bố cục và vị trí máy | Subject on the right third… / 45 degrees to the wall, at hand height |

Shot có `"key": true` (chủ chốt) bắt buộc đủ các trường trên; validator báo LỖI nếu thiếu. Shot thường thiếu thì chỉ cảnh báo.

## Chọn shot chủ chốt

Mỗi vị trí đặt máy (setup) ít nhất một; mọi shot Micro Cut; shot mở và shot kết của mỗi cảnh; ứng viên thumbnail. Thường 30–40% số shot.

## Giữ nhất quán — không viết prompt tự do

Prompt ảnh do `scripts/build_prompt_pack.py` **lắp ghép** từ:

1. `visual-bible.json` → `style`, `negative` (giống nhau mọi khung)
2. `locations[location_id].desc_en` + ảnh bối cảnh thật
3. `subjects[...]` của các nhân vật trong shot + ảnh nhân vật thật — mô tả cố định, viết một lần từ ảnh thật
4. `props[...]` của `prop_ids`
5. Thông số máy của shot → ngôn ngữ ảnh (bảng tiêu cự, bảng giờ quay)
6. `frame_en`, `composition_en`, `angle_en` của shot
7. Dòng CONTINUITY nhắc khung trước cùng cảnh + đính kèm ảnh khung trước nếu đã có

Vì vậy muốn ảnh tốt hơn thì **sửa dữ liệu** (mô tả trong visual bible, `frame_en`), không sửa tay từng prompt.

## Viết `desc_en` trong visual bible từ ảnh thật

Mở ảnh bằng Read rồi mô tả đúng cái thấy: dáng người, kiểu tóc, **màu và chất liệu từng món đồ**, đặc điểm nhận diện; với bối cảnh: vật liệu, màu, hình dạng mái, thứ gì ở trước/sau/hai bên. 40–70 từ. Không tả vẻ đẹp, không đoán tuổi/tính cách từ ảnh. Chưa có ảnh thật thì ghi rõ trong `_ghi_chu` là mô tả theo Bible [GIẢ ĐỊNH].

## Nhận xét ảnh thực tế (Quay phim làm)

So ảnh chủ dự án chụp với kế hoạch của shot, theo thứ tự: (1) đúng chủ thể và hành động chưa, (2) cỡ cảnh/tiêu cự, (3) chiều cao và góc máy, (4) bố cục và khoảng thở, (5) hướng sáng, phơi sáng, (6) vật lạ hiện đại trong khung, (7) liên tục với shot liền trước/sau đã có ảnh.

| `verdict` | Khi nào | `note` phải ghi |
|---|---|---|
| `dat` | Dùng được để quay như ảnh | Một câu điều gì đúng; nếu thực tế hay hơn kế hoạch thì nói rõ và cập nhật kế hoạch theo ảnh |
| `chinh` | Đúng hướng, cần chỉnh nhỏ | Lệnh chỉnh đo được: "hạ máy 30 cm", "lùi 1 m và zoom lên 70mm", "xoay để nắng ở sau lưng" |
| `quay-lai` | Sai chủ thể, sai giờ sáng, hoặc không dựng được | Vì sao, và làm lại thế nào |

**Thực tế thắng kế hoạch.** Khi ảnh thật cho thấy hiện trường khác tưởng tượng (chòi quay hướng khác, không có chỗ lùi máy), sửa kế hoạch của shot đó và các shot liên quan cho khớp hiện trường, không bắt chủ dự án quay cho giống ảnh AI.
