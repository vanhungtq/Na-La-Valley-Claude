# Nà Lạ Valley · Xưởng tiền kỳ

Hai phần:

- **App Nà Lạ Studio** — giao diện bạn dùng hằng ngày, chạy trên claude.ai: https://claude.ai/artifact/7WeknhdrjPium3HMoESGTM (riêng tư, chỉ tài khoản của bạn mở được). Dữ liệu, ảnh và clip nằm trong app.
- **Repo này** — code: mã nguồn app, 7 agent, các lệnh, script, kiến thức nền. Agents chạy trong Claude Code mở trên repo này.

Không dùng API tính phí. Ảnh storyboard do bạn tự tạo từ prompt app chuẩn bị.

## Cách dùng

| Bạn làm trong app | Rồi | Agents trả về trong app |
|---|---|---|
| Tab **Đầu vào**: viết ý tưởng thô, tải ảnh bối cảnh / đạo cụ / nhân vật, bấm *Viết kịch bản & storyboard* | Gõ `/studio` trong Claude Code | 3 concept để chọn → kịch bản → storyboard từng shot kèm hướng dẫn quay → prompt tạo ảnh |
| Trả lời câu hỏi agents đặt ra (ô màu vàng đầu trang) | `/studio` | Bước tiếp theo |
| Tab **Tạo ảnh** (tùy chọn): sao chép prompt + ảnh tham chiếu sang ChatGPT/Gemini, gắn ảnh kết quả vào shot | — | Hình dự kiến hiện cạnh ảnh thực tế |
| Tab **Storyboard**: tải ảnh thực tế từng shot (không cần đủ), bấm *Nhận xét ảnh mới & cập nhật* | `/studio` | Mỗi ảnh: đạt / cần chỉnh / quay lại kèm lệnh sửa; kế hoạch chỉnh theo thực tế; bản mới |
| Bấm *Chốt bản Final* | `/studio` | Bản Final |
| **Thư viện**: thêm clip ngắn của video mẫu (app tự trích khung hình) kèm ghi chú; bấm *Phân tích mục mới*, sau đó *Rút kỹ thuật & nâng cấp agents*; duyệt từng thẻ kỹ thuật | `/studio` | Phân tích từng cú máy; thẻ kỹ thuật; sổ tay agents được cập nhật |
| **Agents**: xem hàng việc, bước của từng tập, agent nào đang làm gì, nhật ký | — | Cập nhật trực tiếp khi agents chạy |

Việc trong hàng chỉ chạy khi có một phiên Claude Code đang mở và bạn gõ `/studio`. App không tự khởi động agents.

## Giới hạn

- Agents xem ảnh và chuỗi khung hình của clip; không xem video chạy, không nghe âm thanh.
- Mỗi tệp tải lên tối đa 20 MB; ảnh được tự thu nhỏ còn cạnh dài 1920 px.
- Ảnh AI không giống hệt người thật; một số dịch vụ từ chối dựng người thật từ ảnh tham chiếu.

## Tình trạng

- **Đã kiểm tra:** app chạy với dữ liệu giả lập trên máy tính và điện thoại, sáng và tối; ghi và đọc cơ sở dữ liệu thật của app; đường đồng bộ app → thư mục làm việc → app (Tập 1 mẫu đi một vòng không sai lệch).
- **Chưa kiểm tra:** tải ảnh/clip và trích khung hình trong app thật (chỉ bạn đăng nhập mới thử được); tải tệp từ kho của app về phiên; toàn bộ quy trình agents trên một tập thật. Tập đầu là phép thử.
- Tập 1 trong app là bản hạt giống 10 shot chép từ Bible.

## Cho người sửa code

```bash
python3 scripts/validate_episode.py episodes/_template --draft
```

Sửa giao diện: `studio/app.html`, đăng lại qua công cụ Artifact của Claude với `url` trong `studio/app.json`. Lý do thiết kế: [`docs/PHUONG_AN.md`](docs/PHUONG_AN.md).
