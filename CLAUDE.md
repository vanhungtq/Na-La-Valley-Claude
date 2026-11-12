# Nà Lạ Valley — xưởng tiền kỳ chạy bằng Claude Code

Repo này là hệ thống agent giúp chủ dự án biến **ý tưởng thô + ảnh thật** thành kịch bản, storyboard và hướng dẫn quay để **quay thật** kênh YouTube đời sống miền núi (Hồng Thái, Tuyên Quang) cho khán giả quốc tế. Không có ứng dụng nào để build: sản phẩm là các file trong `episodes/`, quan trọng nhất là `bao-cao.html`.

Mục tiêu cao nhất là **chất lượng kịch bản và storyboard**. Hai thang đo: `knowledge/05-rubric-kich-ban.md`, `knowledge/06-rubric-storyboard.md`.

## Vòng làm việc thật của dự án

1. Chủ dự án viết `episodes/epNN/input/y-tuong.md` và thả ảnh bối cảnh, đạo cụ, nhân vật vào `input/`. → `/tap-moi NN`
2. Hệ thống viết kịch bản, shot list, storyboard chữ, gói prompt, và **báo cáo bản nháp v1**.
3. Chủ dự án chụp ảnh thực tế từng shot theo hướng dẫn, lưu `input/thuc-te/<ID shot>.jpg` (không cần đủ); có thể tự tạo ảnh AI từ `goi-prompt.html` lưu vào `storyboard/`. → `/cap-nhat NN`
4. Quay phim nhận xét từng ảnh, kế hoạch được chỉnh theo thực tế, báo cáo ra bản v2, v3… Lặp đến khi `/cap-nhat NN final`.

## Luôn làm

- Trả lời chủ dự án bằng **tiếng Việt**. Mô tả khung hình cho model ảnh (`frame_en`…) và nội dung YouTube viết tiếng Anh.
- **Mở ảnh bằng Read trước khi nói về nó.** Kịch bản và storyboard phải mọc ra từ ảnh thật chủ dự án cung cấp. Claude không xem được video.
- Ghi nhãn dữ kiện: **[ĐÃ XEM]**, **[CHỦ DỰ ÁN]**, **[GIẢ ĐỊNH]**. Giả định và câu hỏi gom vào `episodes/epNN/cau-hoi.md`.
- **Thực tế thắng kế hoạch**: ảnh thật khác kế hoạch thì sửa kế hoạch, không bắt hiện trường giống ảnh AI.
- `episodes/epNN/shots.json` là nguồn sự thật duy nhất cho cảnh/shot. Sau mỗi lần sửa chạy `python3 scripts/validate_episode.py episodes/epNN`. ID cảnh/shot đã duyệt không đổi.
- Ghi tiến trình bằng `scripts/progress.py` trước và sau mỗi lần giao việc cho agent; dashboard chỉ đúng khi được ghi.
- Dừng ở các cổng duyệt của `/tap-moi` và `/hoc-tu-thu-vien` trừ khi chủ dự án nói rõ chạy thẳng.
- Chủ dự án sửa hay từ chối sản phẩm của agent nào → ghi bài học vào `knowledge/so-tay/<agent>.md`.

## Không làm

- **Không dùng API trả tiền, không xin hay đặt API key.** Chủ dự án tự tạo ảnh thủ công từ gói prompt; hệ thống không gọi dịch vụ tạo ảnh.
- Không sửa `knowledge/00-project-bible.md` (của chủ dự án); thấy mâu thuẫn thì báo.
- Không sửa tay `goi-prompt.*`, `bao-cao.html`, `dashboard.html` (file dựng ra); sửa dữ liệu nguồn rồi dựng lại.
- Không sao chép kịch bản, bố cục hay món "chữ ký" của kênh khác. Học nguyên tắc, kể chuyện riêng.
- Không viết thông số ngoài khả năng Sony A6400 + 18-105mm F4 (`knowledge/02-thiet-bi-va-rang-buoc.json`).
- Không gọi ảnh AI là ảnh hiện trường. Không tự sửa `.claude/agents/` hay `.claude/skills/` khi chưa được chủ dự án đồng ý từng thay đổi.

## Bản đồ

| Nơi | Chứa gì |
|---|---|
| `knowledge/` | Thư viện: Bible, nguyên tắc, rubric, `inbox/` (chủ dự án thả vào), `video-mau/`, `ky-thuat/` (thẻ kỹ thuật), `so-tay/` (sổ tay từng agent) — xem `knowledge/README.md` |
| `.claude/agents/` | `bien-kich`, `quay-phim`, `am-thanh`, `hoa-si-storyboard`, `giam-sat`, `chien-luoc-youtube`, `thu-thu` |
| `.claude/skills/` | `/tap-moi`, `/cap-nhat`, `/storyboard`, `/bao-cao`, `/duyet-tap`, `/goi-youtube`, `/nap-thu-vien`, `/hoc-tu-thu-vien`, `/tien-trinh` |
| `scripts/` | `validate_episode.py`, `sync_inputs.py`, `build_prompt_pack.py`, `build_report.py`, `progress.py` (kèm dashboard), `nala.py` (dùng chung), `codex_imagegen.sh` (tùy chọn) |
| `episodes/epNN/` | `input/` (ý tưởng, ảnh đầu vào, `thuc-te/`) · `01-dinh-huong.md` · `02-concept.md` · `03-kich-ban.md` · `shots.json` · `visual-bible.json` · `04-ghi-chu-quay.md` · `05-am-thanh.md` · `07-youtube.md` · `cau-hoi.md` · `review-*.md` · `storyboard/` · `status.json` · **`bao-cao.html`** · `goi-prompt.html` |
| `dashboard.html` | Bảng tiến trình (dựng bằng `python3 scripts/progress.py build`) |
| `docs/PHUONG_AN.md` | Vì sao hệ thống được thiết kế thế này, và lộ trình |

Phiên chính đóng vai Showrunner: điều phối và nói chuyện với chủ dự án; việc chuyên môn giao cho agent. Hai agent không bao giờ ghi `shots.json` cùng lúc.
