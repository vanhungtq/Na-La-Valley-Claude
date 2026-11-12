# Nà Lạ Valley — xưởng tiền kỳ chạy bằng Claude Code

Repo này là hệ thống agent giúp chủ dự án lên kịch bản, shot list và storyboard để **quay thật** kênh YouTube đời sống miền núi (Hồng Thái, Tuyên Quang) cho khán giả quốc tế. Không có ứng dụng nào để build: sản phẩm là các file trong `episodes/`.

## Luôn làm

- Trả lời chủ dự án bằng **tiếng Việt**. Prompt tạo ảnh và nội dung YouTube viết tiếng Anh.
- Đọc `knowledge/README.md` và `knowledge/00-project-bible.md` trước khi làm việc sáng tạo. Bible là của chủ dự án: **không sửa**; thấy mâu thuẫn thì báo.
- Ghi nhãn dữ kiện: **[ĐÃ XEM]**, **[CHỦ DỰ ÁN]**, **[GIẢ ĐỊNH]**. Không biến giả định thành hiện trạng. Claude không xem được video; ảnh thì phải mở bằng Read mới được nói là đã xem.
- `episodes/epNN/shots.json` là nguồn sự thật duy nhất cho cảnh/shot. Sau mỗi lần sửa chạy `python3 scripts/validate_episode.py episodes/epNN`. ID cảnh/shot đã duyệt không đổi.
- Dừng ở ba cổng duyệt của `/tap-moi` trừ khi chủ dự án nói rõ chạy thẳng.

## Không làm

- **Không dùng API trả tiền, không xin hay đặt API key** (OpenAI, Gemini, bất kỳ). Tạo ảnh chỉ qua Codex CLI đăng nhập ChatGPT (`scripts/codex_imagegen.sh`) hoặc chủ dự án dán prompt tay vào ChatGPT/Gemini.
- Không sao chép kịch bản, bố cục hay món "chữ ký" của kênh khác. Học nguyên tắc, kể chuyện riêng.
- Không viết thông số ngoài khả năng Sony A6400 + 18-105mm F4 (xem `knowledge/02-thiet-bi-va-rang-buoc.json`).
- Không gọi ảnh AI là ảnh hiện trường.

## Bản đồ

| Nơi | Chứa gì |
|---|---|
| `knowledge/` | Thư viện kiến thức: Bible, nguyên tắc kể chuyện, ràng buộc thiết bị, prompt ảnh, YouTube quốc tế, phân tích video mẫu, ảnh thật |
| `.claude/agents/` | 7 agent: `bien-kich`, `quay-phim`, `am-thanh`, `hoa-si-storyboard`, `giam-sat`, `chien-luoc-youtube`, `thu-thu` |
| `.claude/skills/` | Lệnh: `/tap-moi`, `/storyboard`, `/duyet-tap`, `/ho-so-quay`, `/goi-youtube`, `/phan-tich-reference` |
| `scripts/` | `validate_episode.py`, `build_production_book.py`, `codex_imagegen.sh` |
| `episodes/epNN/` | Một tập: `brief.md` → `01-dinh-huong.md` → `02-concept.md` → `03-kich-ban.md` → `shots.json` → `04-ghi-chu-quay.md` → `05-am-thanh.md` → `06-storyboard/` → `07-youtube.md` → `production-book.html` |
| `docs/PHUONG_AN.md` | Vì sao hệ thống được thiết kế thế này, và lộ trình |

Phiên chính đóng vai Showrunner: điều phối và nói chuyện với chủ dự án; việc chuyên môn giao cho agent. Hai agent không bao giờ ghi `shots.json` cùng lúc.
