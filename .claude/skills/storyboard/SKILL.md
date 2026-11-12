---
name: storyboard
description: Tạo hoặc bổ sung storyboard cho một tập Nà Lạ Valley - chọn shot chủ chốt, viết prompt atlas 2x2, tạo ảnh bằng Codex CLI (gói ChatGPT, không API) hoặc xuất prompt để dán tay vào ChatGPT/Gemini, hoặc vẽ sơ đồ SVG. Dùng khi chủ dự án nói "làm storyboard", "tạo ảnh phân cảnh", "/storyboard 01".
argument-hint: "<số tập> [svg|codex|thu-cong] [cảnh hoặc shot cụ thể]"
---

# Storyboard

## 1. Chọn đường tạo ảnh

Kiểm tra môi trường trước khi hứa:

```bash
command -v codex && codex login status
```

| Tình huống | Đường đi |
|---|---|
| Có Codex CLI và đã đăng nhập ChatGPT | **codex** — tự động, ảnh lưu thẳng vào repo |
| Phiên Claude trên cloud/điện thoại, hoặc Codex báo hết hạn mức | **thu-cong** — xuất prompt; chủ dự án dán vào ChatGPT hoặc Gemini, lưu ảnh về `06-storyboard/atlas-NN.png`, rồi gọi lại skill để gắn |
| Cần nhanh, hoặc shot phụ | **svg** — Claude tự vẽ sơ đồ |

Mặc định khuyến nghị: **shot chủ chốt bằng ảnh AI, phần còn lại SVG hoặc để trống**. Nói cho chủ dự án biết ước lượng số atlas trước khi chạy (mỗi atlas 1–4 phút và tốn hạn mức ChatGPT đáng kể).

Không dùng API key. Không đề xuất các tiện ích gọi API trả tiền (kể cả tiện ích Nano Banana của Gemini CLI — nó cần API key).

## 2. Giao việc

Giao agent `hoa-si-storyboard` với: thư mục tập, đường tạo ảnh đã chọn, phạm vi (cả tập / cảnh / danh sách shot), số atlas tối đa được phép tạo trong lượt này.

## 3. Đường thủ công — hướng dẫn cho chủ dự án

Sau khi agent viết xong `06-storyboard/atlas-NN.txt`, hiển thị cho chủ dự án:

1. Mở ChatGPT (hoặc Gemini), đính kèm `sheet-*.png` trong `knowledge/visual-refs/` nếu có.
2. Dán nội dung từng file `atlas-NN.txt`, tải ảnh kết quả về.
3. Lưu đúng tên `episodes/epNN/06-storyboard/atlas-NN.png` rồi nhắn "đã lưu ảnh".

Khi ảnh đã có, giao lại `hoa-si-storyboard` bước xem lại + gắn vào `shots.json`.

## 4. Kết thúc

Chạy validator và `build_production_book.py`. Báo: bao nhiêu shot có hình, atlas nào cần làm lại, hạn mức còn dùng được hay đã chạm trần.
