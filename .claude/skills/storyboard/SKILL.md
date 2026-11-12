---
name: storyboard
description: Dựng hoặc bổ sung storyboard cho một tập Nà Lạ Valley - visual bible từ ảnh thật, mô tả khung hình từng shot, và gói prompt (goi-prompt.html) kèm ảnh tham chiếu để chủ dự án tự tạo ảnh thủ công bằng ChatGPT/Gemini. Dùng khi chủ dự án nói "làm storyboard", "xuất prompt tạo ảnh", "làm lại prompt cảnh 3", "/storyboard 01".
argument-hint: "<số tập> [cảnh hoặc shot cụ thể] [tat-ca]"
---

# Storyboard

Mặc định của dự án: **chủ dự án tự tạo ảnh thủ công** từ gói prompt. Hệ thống không gọi dịch vụ tạo ảnh và không dùng API key. Chất lượng đến từ dữ liệu: mô tả cố định viết từ ảnh thật, ảnh tham chiếu đính kèm, và khung hình liền mạch với khung trước (chuẩn: `knowledge/06-rubric-storyboard.md`).

## Các bước

1. `python3 scripts/sync_inputs.py episodes/epNN` — biết ảnh nào mới.
2. Giao `hoa-si-storyboard`:
   - **Việc 1** nếu có ảnh đầu vào chưa nằm trong visual bible, hoặc visual bible còn ghi [GIẢ ĐỊNH].
   - **Việc 2** cho phạm vi được yêu cầu (mặc định: mọi shot chủ chốt chưa có `frame_en`; `tat-ca`: cả shot thường).
   - **Việc 3** dựng gói prompt.
3. Giao `giam-sat` rà bước "storyboard" khi làm cả tập lần đầu.
4. Dựng lại báo cáo: `python3 scripts/build_report.py episodes/epNN`.

## Báo chủ dự án

- `episodes/epNN/goi-prompt.html`: mỗi thẻ có ảnh tham chiếu cần đính kèm, nút sao chép prompt, tên file cần lưu. Bản chữ: `goi-prompt.md`.
- Số khung cần tạo, bao nhiêu chủ chốt. Khuyên làm chủ chốt trước, trong **một** cuộc trò chuyện ChatGPT/Gemini cho cả tập.
- Lưu ảnh vào `episodes/epNN/storyboard/<ID shot>.png` rồi gọi `/cap-nhat NN`.
- Shot nào đã có ảnh thực tế thì không cần tạo ảnh AI.
- Ảnh nên chụp thêm để prompt chính xác hơn (từ kết quả của Họa sĩ).

## Khi ảnh AI trả về sai

Chủ dự án nói ảnh sai thế nào → giao `hoa-si-storyboard` sửa **dữ liệu nguồn** (`desc_en` trong visual bible, `frame_en`/`composition_en` của shot, hoặc `style`/`negative` nếu lỗi lặp lại ở nhiều ảnh), dựng lại gói prompt. Ghi quy tắc rút ra vào `knowledge/so-tay/hoa-si-storyboard.md`.

## Tùy chọn: tạo ảnh tự động bằng Codex CLI

Chỉ khi chủ dự án yêu cầu rõ và máy có Codex CLI đã đăng nhập ChatGPT. Lưu prompt của một shot ra file rồi chạy `scripts/codex_imagegen.sh <file-prompt> episodes/epNN/storyboard/<ID>.png [ảnh tham chiếu…]`. Script này chưa được chạy thử với Codex thật; thử một ảnh trước.
