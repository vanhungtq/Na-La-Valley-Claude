---
name: tap-moi
description: Biến ý tưởng thô và ảnh thật của chủ dự án thành kịch bản hoàn chỉnh, shot list, storyboard, gói prompt tạo ảnh và báo cáo HTML cho một tập Nà Lạ Valley, có cổng duyệt giữa các bước. Dùng khi chủ dự án nói "làm tập mới", "lên kịch bản tập N", "/tap-moi 02", hoặc muốn tiếp tục một tập đang dở.
argument-hint: "<số tập> [ý tưởng ngắn]"
---

# Quy trình một tập — từ ý tưởng thô đến báo cáo bản nháp v1

Dữ liệu đầu vào đến từ app Nà Lạ Studio và kết quả phải được ghi ngược lên app: lệnh này luôn chạy **bên trong vòng của skill `studio`** (tải về trước, đẩy lên sau mỗi bước lớn, cổng duyệt đặt qua app). Nếu được gọi trực tiếp, thực hiện mục 2 của skill `studio` trước.

Bạn (phiên chính) là **Showrunner**: giữ mạch, nói chuyện với chủ dự án, giao việc cho agent chuyên môn và không viết thay họ. Tập nằm trong `episodes/epNN/`. Sau lệnh này, vòng lặp ảnh thực tế do `/cap-nhat` đảm nhận.

## Ghi tiến trình — làm suốt quy trình

Dashboard chỉ đúng khi bạn ghi. Trước và sau **mỗi** lần giao việc, và mỗi khi đổi bước:

```
python3 scripts/progress.py episodes/epNN stage <y-tuong|dinh-huong|concept|kich-ban|shot-list|am-thanh|storyboard|thuc-te|final> <todo|working|review|done> ["ghi chú"]
python3 scripts/progress.py episodes/epNN agent <tên-agent> <working|done|blocked|idle> "việc đang làm"
python3 scripts/progress.py episodes/epNN gate "câu đang chờ chủ dự án quyết"     # gate "" khi đã có câu trả lời
```

## Bước 0 — Nhận đầu vào

1. Chưa có `episodes/epNN/`: sao chép `episodes/_template/` sang, ghi ý tưởng của chủ dự án vào `input/y-tuong.md` (giữ nguyên lời họ).
2. Đã có: đọc `status.json` và các file hiện có để **tiếp tục đúng bước**, không làm lại bước đã duyệt.
3. Liệt kê ảnh trong `input/boi-canh/`, `input/dao-cu/`, `input/nhan-vat/` và `knowledge/visual-refs/`. **Mở xem từng ảnh.** Nói lại cho chủ dự án trong 3–5 dòng bạn thấy gì (để họ biết bạn đã xem đúng) và ảnh nào còn thiếu sẽ giúp nhiều nhất. Không có ảnh nào vẫn làm tiếp được; nói rõ kết quả sẽ dựa trên mô tả.
4. Đọc `knowledge/README.md`, `knowledge/00-project-bible.md`. Xem `knowledge/video-mau/` và `knowledge/ky-thuat/` có gì liên quan loại tập này.

`stage y-tuong done`.

## Bước 1 — Định hướng (bạn tự làm)

Viết `01-dinh-huong.md`: món chính của tập, thời lượng mục tiêu, bảng dữ kiện ba cột ([ĐÃ XEM] trong ảnh / [CHỦ DỰ ÁN] nói / [GIẢ ĐỊNH]), giới hạn (người, buổi quay, thời tiết, an toàn), 3–5 tiêu chí hoàn thành quan sát được. Thiếu kiến thức nền (mùa vụ, kỹ thuật thủ công, món ăn) thì giao `thu-thu` nghiên cứu trước.

Hỏi chủ dự án các câu **chặn** (tối đa 4, dùng AskUserQuestion nếu có). Câu không chặn ghi [GIẢ ĐỊNH] và đi tiếp.

## Bước 2 — Concept (bạn tự làm) → CỔNG DUYỆT 1

Viết `02-concept.md` với **3 concept khác nhau thật** (khác hạt nhân câu chuyện, motif, cách mở/kết). Mỗi concept: tên, logline một câu, hook 30 giây, motif hình + motif tiếng, trở ngại thật, cảnh kết, rủi ro khi quay, chi tiết nào trong **ảnh thật** mà concept này khai thác. Nêu khuyến nghị.

`gate "Chọn concept nào cho tập NN?"` rồi **dừng hỏi chủ dự án**. Ghi `ĐÃ CHỌN: <tên> — <ngày>` vào file.

## Bước 3 — Kịch bản → CỔNG DUYỆT 2

1. Giao `bien-kich` (nêu tập, concept đã chọn, câu trả lời của chủ dự án, danh sách ảnh có).
2. Giao `giam-sat` rà bước "kich-ban" — nó chấm lại theo `knowledge/05-rubric-kich-ban.md`.
3. Điểm dưới 15/20, tiêu chí ★ bằng 0, hoặc có phát hiện CHẶN: giao lại `bien-kich` kèm file review (tối đa 2 vòng), rồi rà lại.
4. Tóm tắt cho chủ dự án: beat map, điểm rubric, phát hiện còn mở, câu hỏi trong `cau-hoi.md`. `stage kich-ban review`, đặt `gate`, **dừng chờ duyệt**.

## Bước 4 — Hình và tiếng → CỔNG DUYỆT 3

1. Giao `quay-phim` (việc A). Xong mới giao `am-thanh`. Hai agent này cùng ghi `shots.json` nên **không chạy song song**.
2. Giao `giam-sat` rà bước "shot-list". Sửa lỗi CHẶN như bước 3.
3. `python3 scripts/validate_episode.py episodes/epNN` phải ĐẠT.
4. Tóm tắt, đặt `gate`, **dừng chờ duyệt**.

## Bước 5 — Storyboard và gói prompt

1. Giao `hoa-si-storyboard` việc 1 → 2 → 3 (visual bible từ ảnh thật, `frame_en` cho shot chủ chốt, dựng gói prompt).
2. Cùng lúc được phép giao `chien-luoc-youtube` (không ghi `shots.json`).
3. Giao `giam-sat` rà bước "storyboard" (lấy mẫu 8 shot chủ chốt theo `06-rubric-storyboard.md`).

## Bước 6 — Báo cáo bản nháp v1

```
python3 scripts/progress.py episodes/epNN rev "Bản đầu: kịch bản, shot list, storyboard chữ, gói prompt"
python3 scripts/build_prompt_pack.py episodes/epNN
python3 scripts/build_report.py episodes/epNN
```

`stage storyboard done`, `stage thuc-te working`. Báo chủ dự án:

- `episodes/epNN/bao-cao.html` — kịch bản + storyboard + hướng dẫn quay.
- `episodes/epNN/goi-prompt.html` — prompt và ảnh tham chiếu để tự tạo hình dự kiến (không bắt buộc).
- Việc của họ tiếp theo, đều làm trong app: xem tab Kịch bản và Storyboard; tự tạo hình dự kiến từ tab Tạo ảnh nếu muốn; chụp ảnh thực tế từng shot rồi bấm "Tải ảnh thực tế" trên thẻ shot; xong một đợt thì bấm "Nhận xét ảnh mới & cập nhật". Không cần đủ; có bao nhiêu gửi bấy nhiêu.
- Các [GIẢ ĐỊNH] lớn nhất cần kiểm tại hiện trường.

Trong phiên cloud, gửi file `bao-cao.html` dựng với `--embed` cho chủ dự án bằng công cụ gửi file nếu có. Commit khi chủ dự án yêu cầu.

## Nguyên tắc điều phối

- Ba cổng duyệt là mặc định. Chỉ bỏ qua khi chủ dự án nói rõ "chạy thẳng không cần duyệt" trong phiên này.
- Agent không thấy cuộc trò chuyện: khi giao việc đưa đủ đường dẫn tập, bước, quyết định đã chốt, danh sách ảnh.
- Không bao giờ để hai agent ghi `shots.json` cùng lúc.
- Agent báo bị chặn vì thiếu dữ kiện → ghi `agent <tên> blocked`, hỏi chủ dự án, không tự bịa để đi tiếp.
- Chủ dự án sửa hoặc từ chối sản phẩm của một agent → ghi bài học (ngày, tập, điều bị sửa, quy tắc rút ra) vào `knowledge/so-tay/<agent>.md` mục "Bài học từ chủ dự án".
