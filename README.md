# Nà Lạ Valley · Xưởng tiền kỳ bằng Claude

Hệ thống agent, thư viện kiến thức và skill giúp lên **kịch bản, shot list, storyboard và gói YouTube** cho kênh đời sống miền núi Nà Lạ Valley. Chạy bằng Claude Code với gói thuê bao Claude; ảnh storyboard tạo bằng gói ChatGPT qua Codex CLI. **Không dùng API tính phí.**

Phương án và lý do thiết kế: [`docs/PHUONG_AN.md`](docs/PHUONG_AN.md).

## Bắt đầu trong 5 phút

1. Mở repo này bằng Claude Code (máy tính, web hoặc điện thoại).
2. Gõ `/tap-moi 01` — Claude đọc brief tập 1, hỏi vài câu còn thiếu, đưa 3 concept để bạn chọn, rồi lần lượt giao các agent viết kịch bản, shot list, âm thanh.
3. Gõ `/storyboard 01` để tạo hình, `/ho-so-quay 01` để xuất hồ sơ in mang đi quay.

## Các lệnh

| Lệnh | Việc |
|---|---|
| `/tap-moi <số> [ý tưởng]` | Chạy cả quy trình một tập, có 3 cổng duyệt |
| `/storyboard <số> [svg\|codex\|thu-cong]` | Tạo/bổ sung storyboard |
| `/duyet-tap <số>` | Rà soát độc lập trước khi quay |
| `/ho-so-quay <số>` | Xuất `production-book.html` + `shotlist.csv` |
| `/goi-youtube <số>` | Tiêu đề EN, thumbnail, mô tả, chapters, phụ đề, Micro Cut |
| `/phan-tich-reference <url>` | Đưa video mẫu vào thư viện (qua Gemini) |

## Cài phần tạo ảnh (một lần, trên máy tính)

```bash
npm i -g @openai/codex
```

```bash
codex login
```

Đăng nhập bằng tài khoản ChatGPT Plus. Đừng đặt biến `OPENAI_API_KEY` (script sẽ từ chối chạy để tránh bị tính tiền API). Phiên Claude trên web/điện thoại không có Codex: khi đó `/storyboard` xuất prompt để bạn dán tay vào ChatGPT hoặc Gemini.

## Kiểm tra thủ công

```bash
python3 scripts/validate_episode.py episodes/ep01 --draft
```

```bash
python3 scripts/build_production_book.py episodes/ep01
```

## Tình trạng

- Đã chạy thử: hai script Python (kiểm tra và dựng hồ sơ) với dữ liệu tập 1.
- **Chưa chạy thử:** `scripts/codex_imagegen.sh` với Codex thật, và toàn bộ quy trình `/tap-moi` từ đầu đến cuối. Tập 1 mới là bản hạt giống 10 shot chép từ Bible.
