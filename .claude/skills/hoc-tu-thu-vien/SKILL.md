---
name: hoc-tu-thu-vien
description: Chưng cất thư viện kiến thức của Nà Lạ Valley (video mẫu đã phân tích, tài liệu, bài học thực địa) thành thẻ kỹ thuật có bằng chứng, cập nhật sổ tay của từng agent, và đề xuất skill mới hoặc chỉnh agent khi cần. Dùng khi chủ dự án nói "học từ thư viện", "nâng cấp agents", "rút kỹ thuật từ các video mẫu", "/hoc-tu-thu-vien".
argument-hint: "[chủ đề hoặc tên video cụ thể]"
---

# Học từ thư viện → nâng cấp agents

Mục tiêu: lần viết kịch bản và storyboard sau **khác đi một cách kiểm chứng được** vì thư viện đã lớn hơn. Bạn (phiên chính) tự làm lệnh này; cần đọc rộng nên đừng chia nhỏ cho agent.

## 1. Đọc

- Mọi `knowledge/video-mau/*/reference.json` và `phan-tich.md` (bỏ thư mục `_mau`). **Mở xem ảnh** của những cú máy định dùng làm bằng chứng.
- `knowledge/kien-thuc/`, `knowledge/chu-de/`.
- Các thẻ đã có trong `knowledge/ky-thuat/` và sáu sổ tay trong `knowledge/so-tay/`.
- `review-*.md` và `real.note` của các tập đã làm: lỗi nào lặp lại?

Thư viện chưa có video mẫu nào: nói rõ, chỉ xử lý được bài học từ chủ dự án/thực địa, và dừng ở đó.

## 2. Tìm mẫu lặp lại

Một kỹ thuật đáng thành thẻ khi: xuất hiện ở từ 2 video trở lên, **hoặc** 1 video nhưng chủ dự án nói rõ muốn học, **hoặc** là lời giải cho một lỗi đã lặp lại trong review/ảnh thực tế. Ưu tiên kỹ thuật làm được với A6400 + 18-105 F4, một người quay.

## 3. Viết thẻ đề xuất

Theo mẫu trong `knowledge/ky-thuat/README.md`, trạng thái `đề xuất`. Mỗi thẻ có bằng chứng trỏ tới `video-mau/<thư-mục>#<số shot>`. Tối đa 8 thẻ mỗi lần; ít mà chắc.

Không viết thẻ từ hiểu biết chung không có bằng chứng trong thư viện. Điều đó thuộc về `01-nguyen-tac-ke-chuyen.md` và phải giữ nhãn "khởi điểm".

## 4. CỔNG DUYỆT — chủ dự án chọn

Trình bảng: mã, tên, một dòng mô tả, bằng chứng, agent nào sẽ dùng. Hỏi chủ dự án giữ thẻ nào, sửa thẻ nào, bỏ thẻ nào. Thẻ được giữ đổi trạng thái thành `đã duyệt <ngày>`; thẻ bị bỏ thì xóa file.

## 5. Nâng cấp agents qua sổ tay

Với mỗi thẻ đã duyệt, thêm vào `knowledge/so-tay/<agent>.md` mục "Thẻ kỹ thuật cần áp dụng" một dòng: mã, tên, **khi nào dùng** và **dùng thế nào trong sản phẩm của agent đó** (Biên kịch: đặt ở beat nào; Quay phim: thông số; Họa sĩ: cách viết `frame_en`; Giám sát: kiểm điều gì). Ghi ngày.

Gộp các bài học trùng nhau trong sổ tay; sổ tay dài quá 80 dòng thì cô lại, giữ điều còn đúng.

## 6. Khi sổ tay không đủ — đề xuất, không tự làm

- **Quy trình lặp lại nhiều bước** xuất hiện (ví dụ "cảnh nấu ăn luôn cần cùng bộ 7 shot"): đề xuất một skill mới trong `.claude/skills/<tên>/SKILL.md`, đưa bản nháp cho chủ dự án xem.
- **Một agent sai có hệ thống** mà sổ tay không sửa được (thiếu bước, sai thứ tự đọc): đề xuất đoạn sửa cụ thể trong `.claude/agents/<agent>.md`.
- **Rubric thiếu tiêu chí** bắt được lỗi đã lặp: đề xuất thêm vào `05-rubric-kich-ban.md` hoặc `06-rubric-storyboard.md`.
- **Ràng buộc máy móc** kiểm được bằng script: đề xuất thêm vào `02-thiet-bi-va-rang-buoc.json` / `validate_episode.py`.

Chỉ sửa các file này sau khi chủ dự án đồng ý từng thay đổi.

## 7. Ghi nhật ký và báo lại

Thêm một mục vào `knowledge/NHAT-KY-HOC.md` (tạo nếu chưa có): ngày, đã đọc những video nào, thẻ nào được duyệt, sổ tay nào đổi, đề xuất nào đang chờ. Chạy `python3 scripts/progress.py build`.

Báo chủ dự án: số thẻ mới, agent nào được nâng cấp và khác đi thế nào ở lần viết tới, và thư viện đang thiếu loại video mẫu nào.
