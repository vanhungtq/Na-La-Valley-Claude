---
name: duyet-tap
description: Rà soát độc lập một tập Nà Lạ Valley ở trạng thái hiện tại - chạy validator và giao Giám sát kiểm nhân quả, continuity, khả thi, tuân thủ Bible. Dùng khi chủ dự án nói "kiểm tra tập N", "review kịch bản", "/duyet-tap 01", hoặc trước khi mang hồ sơ đi quay.
argument-hint: "<số tập>"
---

1. Chạy `python3 scripts/validate_episode.py episodes/epNN` và ghi lại kết quả.
2. Xác định bước hiện tại của tập (kịch bản / shot list / storyboard / thuc-te) từ `status.json` và các file đang có. Ghi `python3 scripts/progress.py episodes/epNN agent giam-sat working "rà soát theo yêu cầu"`.
3. Giao agent `giam-sat` rà soát bước đó; nó chấm theo `knowledge/05-rubric-kich-ban.md` hoặc `06-rubric-storyboard.md` và mở xem ảnh. Không tóm tắt hộ nội dung cho agent — để nó tự đọc file.
4. Trình cho chủ dự án: kết luận, điểm rubric, bảng phát hiện mức CHẶN và NÊN SỬA, câu hỏi cần trả lời.
5. Hỏi chủ dự án muốn sửa những mục nào; giao agent phụ trách tương ứng (`bien-kich`, `quay-phim`, `am-thanh`) kèm đường dẫn file review. Sau khi sửa, chạy lại validator.

Giám sát là rà soát độc lập trong hệ thống, không thay khảo sát thực địa. Nhắc chủ dự án các mục [GIẢ ĐỊNH] cần kiểm tại hiện trường.
