# Ảnh tham chiếu thật

Thả ảnh vào đây để storyboard bám hiện trường thay vì tưởng tượng. Ảnh nên ≤ 2 MB (resize cạnh dài 2000 px) để repo nhẹ.

## Quy ước tên file

```
loc-<nơi>-<mô tả>.jpg      loc-choi-mat-truoc.jpg, loc-suoi-da-reu.jpg
char-<ai>-<trang phục>.jpg  char-chi-ao-cham.jpg, char-em-ao-len.jpg, char-meo.jpg
prop-<vật>.jpg              prop-chao-gang.jpg, prop-gui-tre.jpg
sheet-<ai>.png              model sheet do AI tạo từ ảnh thật (xem dưới)
```

## Model sheet (làm một lần, dùng mãi)

Để mặt và trang phục nhân vật ổn định giữa các ảnh storyboard, tạo cho mỗi nhân vật một tấm model sheet rồi luôn đính kèm khi tạo ảnh:

1. Mở ứng dụng Gemini (gói Pro) hoặc ChatGPT, tải 2–3 ảnh thật của nhân vật.
2. Prompt: `Character reference sheet of this person: front, three-quarter, side and back view, full body, neutral grey background, same outfit, even soft light, photographic. No text.`
3. Lưu thành `sheet-chi.png`, `sheet-em.png`, `sheet-meo.png`.

Ảnh người thật là dữ liệu cá nhân: chỉ đưa vào repo khi repo ở chế độ **private** và người trong ảnh đồng ý.
