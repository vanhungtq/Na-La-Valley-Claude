---
name: cap-nhat
description: Nhận ảnh chụp thực tế từng shot (và ảnh AI, ảnh bối cảnh mới) chủ dự án vừa thả vào một tập Nà Lạ Valley, cho Quay phim nhận xét từng ảnh, chỉnh kịch bản/shot list theo thực tế, rồi dựng lại báo cáo HTML bản mới. Lặp đến khi ra bản Final. Dùng khi chủ dự án nói "đã chụp xong mấy shot", "cập nhật báo cáo", "tôi vừa thêm ảnh", "/cap-nhat 01", "chốt final".
argument-hint: "<số tập> [final]"
---

# Vòng lặp cập nhật theo ảnh thực tế

Mỗi lần chạy tạo ra **một bản báo cáo mới** (v2, v3…). Ảnh không cần đủ: có bao nhiêu xử lý bấy nhiêu.

Ảnh đến từ app Nà Lạ Studio: lệnh này chạy **bên trong vòng của skill `studio`**. Sau khi `app_bridge.py pull` đã tải ảnh về và in danh sách "ẢNH THỰC TẾ CẦN NHẬN XÉT", bỏ qua lệnh `sync_inputs.py` ở mục 1 và dùng danh sách đó; kết thúc bằng việc đẩy kết quả lên app.

## 1. Đồng bộ

```
python3 scripts/progress.py episodes/epNN stage thuc-te working
python3 scripts/sync_inputs.py episodes/epNN
```

Đọc kỹ kết quả:

- **Ảnh thực tế mới/đổi** → danh sách cho Quay phim nhận xét.
- **Hình dự kiến mới** → danh sách cho Họa sĩ storyboard kiểm.
- **CHƯA GẮN ĐƯỢC** (tên file không có ID shot) → mở xem ảnh, đối chiếu với shot list, hỏi chủ dự án xác nhận nó là shot nào (hoặc để Quay phim đề xuất), rồi đổi tên file cho có ID và chạy lại sync. Không đoán rồi im lặng.
- **ID không có trong shots.json** → hỏi chủ dự án: shot mới họ tự thêm, hay gõ nhầm?
- **Ảnh đầu vào chưa đưa vào visual bible** → có ảnh bối cảnh/đạo cụ/nhân vật mới: giao `hoa-si-storyboard` việc 1 cập nhật visual bible.

Không có gì mới thì nói vậy và chỉ dựng lại báo cáo.

## 2. Nhận xét ảnh thực tế

Giao `quay-phim` **việc B** với danh sách ID có ảnh mới. Agent phải mở từng ảnh. Kết quả: mỗi shot có `real.verdict` (`dat` / `chinh` / `quay-lai`) và `real.note` với lệnh sửa đo được; kế hoạch các shot cùng setup được chỉnh theo hiện trường.

Hơn 25 ảnh mới: chia theo cảnh, giao lần lượt (không song song vì cùng ghi `shots.json`).

## 3. Chỉnh kịch bản nếu thực tế khác kế hoạch

Nếu Quay phim báo hiện trường khác kịch bản ở mức hành động (không có chỗ đó, vật khác đi, thứ tự việc thật khác): giao `bien-kich` phần "cập nhật theo ảnh thực tế". Nếu chỉ khác về góc máy/bố cục thì bỏ qua bước này.

## 4. Kiểm ảnh AI và liên tục

- Có hình dự kiến mới: giao `hoa-si-storyboard` việc 4.
- Từ 6 ảnh thực tế trở lên trong cùng một cảnh, hoặc khi chủ dự án muốn chốt Final: giao `giam-sat` rà bước "thuc-te" (liên tục trang phục, mức hoàn thành công trình, hướng sáng giữa các ảnh thật liền nhau).

## 5. Dựng bản mới

```
python3 scripts/validate_episode.py episodes/epNN
python3 scripts/progress.py episodes/epNN rev "<tóm tắt: nhận N ảnh, M đạt, chỉnh gì>"
python3 scripts/build_prompt_pack.py episodes/epNN
python3 scripts/build_report.py episodes/epNN
```

## 6. Báo chủ dự án — ngắn, hành động được

1. Bản vN: bao nhiêu shot đạt / cần chỉnh / quay lại / còn thiếu ảnh.
2. Bảng shot cần chỉnh và quay lại: ID → lệnh sửa (nguyên văn `real.note`).
3. Kế hoạch đã đổi gì vì thực tế (nếu có).
4. Nên chụp gì tiếp theo: ưu tiên shot chủ chốt còn thiếu, gom theo khung giờ ánh sáng.

Trong phiên cloud, gửi `bao-cao.html` dựng với `--embed` cho chủ dự án nếu có công cụ gửi file.

## Chốt bản Final (`/cap-nhat NN final`, hoặc chủ dự án nói "chốt")

Điều kiện: validator ĐẠT; không shot nào ở trạng thái `quay-lai` hay chờ nhận xét; mọi shot chủ chốt có ảnh thực tế `dat`. Shot thường còn thiếu ảnh hoặc còn `chinh` thì liệt kê và hỏi chủ dự án có chấp nhận chốt không — họ là người quyết.

```
python3 scripts/progress.py episodes/epNN final on
python3 scripts/progress.py episodes/epNN rev "Chốt bản FINAL"
python3 scripts/build_report.py episodes/epNN --embed
```

Chưa đủ điều kiện thì không chốt; nói rõ còn thiếu gì.

Sau khi quay xong thật: hỏi chủ dự án điều gì không như kế hoạch, ghi vào `knowledge/so-tay/<agent>.md` mục "Bài học từ thực địa".
