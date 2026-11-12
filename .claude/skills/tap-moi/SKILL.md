---
name: tap-moi
description: Chạy quy trình tiền kỳ cho một tập Nà Lạ Valley từ brief đến hồ sơ quay - định hướng, concept, kịch bản, shot list, âm thanh, storyboard, gói YouTube - có cổng duyệt của chủ dự án giữa các bước. Dùng khi chủ dự án nói "làm tập mới", "lên kịch bản tập N", "/tap-moi 02", hoặc muốn tiếp tục một tập đang dở.
argument-hint: "<số tập> [ý tưởng ngắn]"
---

# Quy trình một tập

Bạn (phiên chính) là **Showrunner**: giữ mạch, nói chuyện với chủ dự án, giao việc cho các agent chuyên môn và không tự viết thay họ. Tập làm việc trong `episodes/epNN/`.

## Bước 0 — Xác định trạng thái

1. Nếu `episodes/epNN/` chưa có: sao chép `episodes/_template/` sang, điền `brief.md` từ lời chủ dự án.
2. Nếu đã có: đọc các file hiện có để biết đang ở bước nào (bảng dưới) và **tiếp tục từ đó**, không làm lại bước đã duyệt.
3. Đọc `knowledge/README.md` và `knowledge/00-project-bible.md`.

| File đã có | Nghĩa là |
|---|---|
| `01-dinh-huong.md` | Xong bước 1 |
| `02-concept.md` có dòng `ĐÃ CHỌN:` | Xong cổng duyệt 1 |
| `03-kich-ban.md` + `review-kich-ban.md` | Xong bước 3 |
| `04-ghi-chu-quay.md`, `05-am-thanh.md` | Xong bước 4 |
| `06-storyboard/`, `07-youtube.md`, `production-book.html` | Xong bước 5–6 |

## Bước 1 — Định hướng (bạn tự làm)

Viết `01-dinh-huong.md`: món chính của tập, thời lượng mục tiêu, bảng dữ kiện ba cột ([ĐÃ XEM] / [CHỦ DỰ ÁN] / [GIẢ ĐỊNH]), giới hạn (người, buổi quay, thời tiết, an toàn), 3–5 tiêu chí hoàn thành quan sát được, và **câu hỏi cần chủ dự án trả lời**. Nếu thiếu kiến thức nền (mùa vụ, kỹ thuật thủ công, món ăn), giao agent `thu-thu` nghiên cứu trước.

Hỏi chủ dự án các câu hỏi chặn (tối đa 4 câu, dùng AskUserQuestion nếu có). Câu không chặn thì ghi [GIẢ ĐỊNH] và đi tiếp.

## Bước 2 — Concept (bạn tự làm) → CỔNG DUYỆT 1

Viết `02-concept.md` với **3 concept khác nhau thật** (khác hạt nhân câu chuyện, motif, cách mở/kết — không chỉ đổi tên). Mỗi concept: tên, logline một câu, hook 30 giây, motif hình + motif tiếng, mạch cảm xúc, cảnh kết, rủi ro khi quay. Nêu khuyến nghị của bạn.

**Dừng lại và hỏi chủ dự án chọn concept nào.** Ghi `ĐÃ CHỌN: <tên> — <ngày>` vào file.

## Bước 3 — Kịch bản → CỔNG DUYỆT 2

1. Giao agent `bien-kich` (nói rõ tập, concept đã chọn, câu trả lời của chủ dự án).
2. Giao agent `giam-sat` rà soát bước "kich-ban".
3. Nếu có phát hiện mức CHẶN: giao lại `bien-kich` sửa kèm file review (tối đa 2 vòng), rồi `giam-sat` rà lại.
4. Tóm tắt cho chủ dự án: beat map, thống kê, phát hiện còn mở, câu hỏi. **Dừng chờ duyệt.**

## Bước 4 — Hình và tiếng → CỔNG DUYỆT 3

1. Giao `quay-phim`. Xong mới giao `am-thanh` (cả hai cùng ghi `shots.json` nên **không chạy song song**).
2. Giao `giam-sat` rà soát bước "shot-list". Sửa lỗi CHẶN như bước 3.
3. Chạy `python3 scripts/validate_episode.py episodes/epNN` — phải ĐẠT.
4. Tóm tắt, **dừng chờ duyệt**.

## Bước 5 — Storyboard và gói YouTube (song song được)

- Hỏi chủ dự án mức storyboard nếu chưa rõ (xem skill `storyboard`). Giao `hoa-si-storyboard`.
- Cùng lúc giao `chien-luoc-youtube` (agent này không ghi `shots.json`).

## Bước 6 — Hồ sơ quay

Chạy `python3 scripts/build_production_book.py episodes/epNN`. Báo cáo cuối: đường dẫn `production-book.html`, `shotlist.csv`, thống kê, phần còn thiếu, các [GIẢ ĐỊNH] cần kiểm tại hiện trường. Commit theo yêu cầu của chủ dự án.

## Nguyên tắc điều phối

- Ba cổng duyệt là mặc định. Chỉ bỏ qua khi chủ dự án nói rõ "chạy thẳng không cần duyệt" trong phiên này.
- Khi giao việc cho agent: đưa đủ đường dẫn tập, bước, quyết định đã chốt. Agent không thấy cuộc trò chuyện này.
- Không bao giờ để hai agent ghi `shots.json` cùng lúc.
- Agent báo bị chặn vì thiếu dữ kiện → hỏi chủ dự án, không tự bịa để đi tiếp.
