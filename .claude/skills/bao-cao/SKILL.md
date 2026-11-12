---
name: bao-cao
description: Dựng lại báo cáo HTML của một tập Nà Lạ Valley (kịch bản + storyboard + hướng dẫn quay + tiến độ ảnh thực tế trong một file) và shotlist.csv từ dữ liệu hiện có, không chạy agent nào. Dùng khi chủ dự án nói "xuất báo cáo", "dựng lại báo cáo", "cho tôi file gửi ekip", "in shot list", "/bao-cao 01".
argument-hint: "<số tập> [nhung]"
---

1. `python3 scripts/validate_episode.py episodes/epNN` — nếu CHƯA ĐẠT, liệt kê lỗi và vẫn dựng bản nháp (nói rõ là nháp có lỗi).
2. `python3 scripts/build_report.py episodes/epNN` — thêm `--embed` khi chủ dự án muốn **một file duy nhất** để gửi đi hoặc xem trên điện thoại (ảnh được nhúng và thu nhỏ).
3. `python3 scripts/progress.py build` để dashboard có nút mở báo cáo.
4. Báo đường dẫn `bao-cao.html`, `shotlist.csv`. Bản không nhúng cần giữ nguyên vị trí thư mục `input/` và `storyboard/` cạnh file HTML. In PDF: mở bằng trình duyệt → In → khổ A4.
5. Trong phiên cloud, gửi file bản `--embed` cho chủ dự án bằng công cụ gửi file nếu có.

Báo cáo gồm: tiến độ và dòng thời gian dựng, kịch bản, storyboard (hình dự kiến cạnh ảnh thực tế, hướng dẫn quay, nhận xét, bộ lọc theo trạng thái), lịch quay theo ánh sáng, đạo cụ, âm thanh, việc tiếp theo, lịch sử phiên bản.

Lệnh này không nhận ảnh mới và không nhận xét ảnh; việc đó là `/cap-nhat`.
