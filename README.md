# Nà Lạ Valley · Xưởng tiền kỳ bằng Claude

Bạn đưa **ý tưởng thô và ảnh thật**; hệ thống agent viết **kịch bản, storyboard, hướng dẫn quay** trong một file báo cáo HTML. Bạn chụp ảnh thực tế từng shot, hệ thống nhận xét và cập nhật báo cáo, lặp đến bản Final. Chạy bằng Claude Code với gói thuê bao Claude. **Không dùng API tính phí**; ảnh storyboard do bạn tự tạo từ gói prompt hệ thống chuẩn bị.

Lý do thiết kế: [`docs/PHUONG_AN.md`](docs/PHUONG_AN.md).

## Một tập đi như thế nào

| Bước | Bạn làm | Gõ lệnh | Hệ thống trả |
|---|---|---|---|
| 1 | Viết vài dòng vào `episodes/epNN/input/y-tuong.md`, thả ảnh vào `input/boi-canh/`, `input/dao-cu/`, `input/nhan-vat/` | `/tap-moi NN` | 3 concept để chọn → kịch bản → shot list → **`bao-cao.html` bản v1** + `goi-prompt.html` |
| 2 (tùy chọn) | Mở `goi-prompt.html`, dán từng prompt kèm ảnh tham chiếu vào ChatGPT/Gemini, lưu ảnh vào `storyboard/<ID shot>.png` | `/cap-nhat NN` | Hình dự kiến hiện trên báo cáo |
| 3 | Ra hiện trường, chụp từng shot theo hướng dẫn, lưu `input/thuc-te/<ID shot>.jpg` — có bao nhiêu gửi bấy nhiêu | `/cap-nhat NN` | Nhận xét từng ảnh (đạt / cần chỉnh / quay lại, kèm lệnh sửa đo được), kế hoạch chỉnh theo thực tế, **báo cáo bản mới** |
| 4 | Lặp bước 3 | `/cap-nhat NN final` | Bản FINAL một file, nhúng ảnh |

## Lệnh

| Lệnh | Việc |
|---|---|
| `/tap-moi <số> [ý tưởng]` | Ý tưởng + ảnh → kịch bản, shot list, storyboard, báo cáo v1 (có 3 cổng duyệt) |
| `/cap-nhat <số> [final]` | Nhận ảnh mới, nhận xét, cập nhật báo cáo; chốt Final |
| `/storyboard <số>` | Làm lại visual bible / mô tả khung hình / gói prompt |
| `/bao-cao <số> [nhung]` | Dựng lại báo cáo, không chạy agent |
| `/duyet-tap <số>` | Rà soát độc lập, chấm theo thang điểm |
| `/goi-youtube <số>` | Tiêu đề EN, thumbnail, mô tả, chapters, phụ đề, Micro Cut |
| `/nap-thu-vien` | Nhập video mẫu và tài liệu bạn thả vào `knowledge/inbox/` |
| `/hoc-tu-thu-vien` | Chưng cất thư viện thành thẻ kỹ thuật, nâng cấp sổ tay các agent |
| `/tien-trinh` | Mở dashboard: agent nào đang làm gì |

## Thư viện kiến thức

Thả vào `knowledge/inbox/` (hướng dẫn: [`knowledge/inbox/README.md`](knowledge/inbox/README.md)): video mẫu của kênh khác gồm văn bản nội dung, timeline, **ảnh chụp màn hình từng cú máy**; hoặc tài liệu bất kỳ. `/nap-thu-vien` xem từng ảnh và lập hồ sơ; `/hoc-tu-thu-vien` rút thành thẻ kỹ thuật có bằng chứng, bạn duyệt, rồi ghi vào sổ tay của từng agent để lần viết sau áp dụng.

## Dashboard

```bash
python3 -m http.server 8765
```

Mở `http://localhost:8765/dashboard.html` (tự làm mới 5 giây): các bước của tập, trạng thái từng agent, nhật ký, tiến độ ảnh thực tế, số liệu thư viện.

## Kiểm tra thủ công

```bash
python3 scripts/validate_episode.py episodes/ep01 --draft
```

```bash
python3 scripts/build_report.py episodes/ep01 --embed
```

## Tình trạng

- **Đã chạy thử** với ảnh giả lập: đồng bộ ảnh, kiểm tra, gói prompt, báo cáo (máy tính và điện thoại), dashboard.
- **Chưa chạy thử:** các agent và lệnh `/tap-moi`, `/cap-nhat`, `/nap-thu-vien`, `/hoc-tu-thu-vien` trên dữ liệu thật — chất lượng kịch bản chưa được chứng minh cho đến khi chạy tập đầu. `scripts/codex_imagegen.sh` (tùy chọn) chưa chạy với Codex thật.
- Tập 1 hiện là bản hạt giống 10 shot chép từ Bible, đã viết đủ trường storyboard để làm mẫu; chưa có ảnh thật nào.
- Thư viện chưa có video mẫu nào. Hai file nguyên tắc (`01`, `04`) là tổng hợp ban đầu của Claude, chưa đối chiếu video thật.
