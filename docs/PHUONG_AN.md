# Phương án hệ thống Agents cho Nà Lạ Valley

Ngày nghiên cứu: 12/11/2026. Đã đọc: Project Bible của chủ dự án và toàn bộ repo `vanhungtq/valley-chibi-studio` (README, AGENTS.md, quy trình 5 vai trò, skill, hợp đồng dữ liệu, báo cáo OpenMontage).

## 1. Kết luận

**Lấy chính repo này làm xưởng, Claude Code làm bộ não, Codex CLI làm tay vẽ, Gemini làm mắt xem video.** Không dựng máy chủ, không dùng API.

| Việc | Ai làm | Trả bằng gì |
|---|---|---|
| Định hướng, concept, kịch bản, shot list, âm thanh, rà soát, gói YouTube, điều phối | Claude Code (7 agent + 6 skill trong repo) | Gói Claude đang có |
| Ảnh storyboard | Codex CLI, skill `$imagegen` có sẵn, đăng nhập ChatGPT | Gói ChatGPT Plus |
| Xem và phân tích video mẫu trên YouTube | Ứng dụng Gemini (dán prompt, dán kết quả về) | Gói Gemini Pro |
| Model sheet nhân vật, ảnh "hero" cần đẹp | Ứng dụng Gemini hoặc ChatGPT, làm tay | Hai gói trên |
| Lưu trữ, lịch sử, đồng bộ giữa máy tính và điện thoại | Git/GitHub | Miễn phí |

## 2. Xưởng Chibi đã làm được gì, và vì sao không dựng tiếp trên đó

Xưởng Chibi là một phòng điều khiển trên Cloudflare (giao diện 3D, D1/KV, OAuth GitHub, MCP) để **Codex** làm nội dung. Những gì nên giữ và đã mang sang đây:

- Năm trách nhiệm chuyên môn và thứ tự định hướng → concept → kịch bản → shot list → hồ sơ.
- Kỷ luật nguồn: tách điều đã xem, lời chủ dự án, giả định; ảnh AI không phải ảnh hiện trường.
- Ràng buộc thời lượng ±5%, giữ ID cảnh/shot, atlas storyboard 2×2 để tiết kiệm lượt tạo ảnh.
- Cổng duyệt của chủ dự án giữa các bước.

Những giới hạn của nó khi chuyển sang Claude:

| Giới hạn ở Xưởng Chibi | Ở repo này |
|---|---|
| Rà soát là **tự rà soát** của cùng một phiên Codex | Agent `giam-sat` chạy ở ngữ cảnh riêng, chỉ thấy file, không thấy lập luận của người viết |
| Năm vai trò chạy nối tiếp trong một phiên | Agent chạy ngữ cảnh riêng; storyboard và gói YouTube chạy song song |
| File nộp qua MCP ≤ 1 MB, đọc ≤ 5 MB, lease 15 phút, phải báo tiến độ để giữ việc | File nằm thẳng trong git, không giới hạn kiểu đó |
| Chọn tài liệu bằng từ khóa, tối đa 16 file | Agent tự đọc/grep cả thư viện; skill chỉ nạp khi cần |
| Kiểm tra máy móc chỉ có cấu trúc và thời lượng | Thêm kiểm tra theo Bible: dải 18–105 mm, F4, fps, 85% khóa máy, cặp hai tiêu cự, lịch ánh sáng, ba tầng âm thanh |
| Cần duy trì Worker, D1, KV, OAuth App | Không có hạ tầng nào để duy trì |
| Chưa có vai trò YouTube/quốc tế hóa, âm thanh, quản lý tri thức (báo cáo OpenMontage đề xuất) | Có `chien-luoc-youtube`, `am-thanh`, `thu-thu` |

Thứ mất đi: giao diện chibi 3D và trang web xem tiến độ. Thay bằng `production-book.html` và việc đọc file trên GitHub. Nếu sau này muốn giữ giao diện đó, MCP của Xưởng là MCP từ xa chuẩn (OAuth 2.1) nên về nguyên tắc Claude Code kết nối được và nhận việc thay Codex; tôi **chưa thử** và không khuyến nghị làm trước khi quay xong vài tập.

## 3. Kiến trúc

```
Chủ dự án
   │  /tap-moi 02 "mận ngâm đầu mùa"
   ▼
Phiên chính = SHOWRUNNER (định hướng, 3 concept, điều phối, hỏi chủ dự án)
   │
   ├─ thu-thu ............ nghiên cứu mùa vụ/kỹ thuật, nhập phân tích video mẫu
   ├─ bien-kich .......... beat map + kịch bản + khung shots.json
   ├─ giam-sat ........... rà soát độc lập sau mỗi bước (chỉ viết review)
   ├─ quay-phim .......... thông số máy, cặp match cut, thứ tự quay, continuity
   ├─ am-thanh ........... 3 tầng âm, danh sách foley, bản đồ nhạc
   ├─ hoa-si-storyboard .. prompt atlas 2×2 → Codex $imagegen / SVG / dán tay
   └─ chien-luoc-youtube . tiêu đề EN, thumbnail, chapters, phụ đề, Micro Cut
   │
   ▼
episodes/epNN/  (shots.json là nguồn sự thật) ──► validate ──► production-book.html
```

Ba cổng duyệt: chọn concept → duyệt kịch bản → duyệt shot list. Sau cổng 3 mới tốn hạn mức tạo ảnh.

**Thư viện kiến thức** (`knowledge/`): Bible nguyên văn; nguyên tắc kể chuyện không lời; ràng buộc thiết bị dạng JSON cho script đọc; khối prompt nhân vật cố định; đóng gói YouTube quốc tế; `references/` cho phân tích video mẫu; `visual-refs/` cho ảnh thật; `chu-de/` cho nghiên cứu có nguồn. Hai file nguyên tắc (01, 04) là tổng hợp ban đầu của Claude, **chưa đối chiếu video thật hay số liệu kênh** — chúng có mục "bài học" để sửa dần.

## 4. Tạo ảnh không dùng API — điều đã kiểm chứng và chưa

| Đường | Tình trạng | Ghi chú |
|---|---|---|
| **Codex CLI `$imagegen`** gọi từ Claude Code qua `codex exec` | Nhiều dự án cộng đồng xác nhận chạy bằng đăng nhập ChatGPT Plus, không cần API key. **Tôi chưa chạy thử được** (phiên cloud không có Codex) và không mở được tài liệu chính thức của OpenAI (trang bị chặn trong phiên này) | Mỗi ảnh 1–4 phút; tốn hạn mức gấp khoảng 3–5 lần lượt thường (số của một dự án cộng đồng). Có báo cáo lỗi hết hạn mức ảnh trên Plus dù hạn mức chung còn. Đặt `OPENAI_API_KEY` sẽ chuyển sang tính tiền API → script chặn sẵn |
| **Dán tay vào ChatGPT / Gemini** | Chắc chắn dùng được | Hệ thống xuất sẵn file prompt từng atlas; chậm hơn nhưng không phụ thuộc CLI |
| **SVG do Claude vẽ** | Chắc chắn dùng được | Sơ đồ bố cục, không phải ảnh; không tốn gì |
| Gemini CLI + tiện ích Nano Banana | **Loại** | Tiện ích yêu cầu `NANOBANANA_API_KEY` (API tính phí). Không tìm thấy đường nào dùng gói Gemini Pro để tạo ảnh từ dòng lệnh |
| Codex làm MCP server cho Claude | Không cần | Gọi `codex exec` bằng một script 50 dòng đơn giản hơn và dễ sửa hơn cài MCP |

Vì hạn mức Plus có hạn, hệ thống mặc định chỉ tạo ảnh cho **shot chủ chốt** (mỗi setup máy một hình + shot Micro Cut + ứng viên thumbnail): tập 20 phút khoảng 40–60 hình = 10–15 atlas, thay vì 150+ shot.

**Vai trò thật của Gemini** không phải vẽ storyboard tự động mà là thứ Claude không làm được: **xem video YouTube**. `/phan-tich-reference` tạo prompt để Gemini xem một tập của Lý Tử Thất/Điền Tây Tiểu Ca và trả bảng timecode; `thu-thu` chuẩn hóa vào thư viện. Đây là cách biến "style Lý Tử Thất" từ cảm nhận thành dữ liệu.

## 5. Chạy ở đâu

| Nơi | Viết kịch bản, shot list, rà soát | Tạo ảnh tự động |
|---|---|---|
| Claude Code trên máy tính (CLI/desktop) đã cài Codex | Có | Có |
| Claude Code trên web/điện thoại | Có | Không — dùng đường dán tay hoặc SVG |

## 6. Lộ trình

| Đợt | Việc | Tiêu chí xong |
|---|---|---|
| **0 — đã làm** | Thư viện, 7 agent, 6 skill, 3 script, tập 1 hạt giống | Validator và production book chạy được trên dữ liệu tập 1 |
| **1 — tuần này** | Trả lời câu hỏi trong `episodes/ep01/brief.md`; chạy `/tap-moi 01`; thử `scripts/codex_imagegen.sh` với một atlas | Có kịch bản 22 phút qua validator; biết chắc đường Codex chạy hay phải dán tay |
| **2** | 5–8 phân tích video mẫu qua `/phan-tich-reference`; ảnh khảo sát chòi và model sheet vào `visual-refs/` | Agent viết có dẫn reference; storyboard giống hiện trường |
| **3 — sau khi quay tập 1** | Ghi "bài học thực địa" vào thư viện; chỉnh agent theo chỗ kịch bản lệch thực tế | Tập 2 ít [GIẢ ĐỊNH] hơn tập 1 |
| **4 — khi cần** | Lịch nội dung theo mùa (12 tập), animatic từ storyboard, nối lại giao diện Xưởng Chibi qua MCP | Chỉ làm khi 3 tập đầu đã lên sóng |

## 7. Rủi ro

- **Chất lượng chưa được chứng minh.** Các agent mới được viết, chưa chạy trọn một tập. Tập 1 là phép thử; dự kiến phải chỉnh prompt agent sau lần chạy đầu.
- **Đường Codex có thể đổi.** Không có cam kết ổn định cho `$imagegen` qua CLI; đường dán tay là phương án dự phòng luôn sẵn.
- **Rà soát của `giam-sat` không thay khảo sát thực địa.** Nó bắt lỗi logic trên giấy; mái chòi thật chịu được ai đứng lên thì chỉ người ở đó biết.
- **Ảnh người thật trong repo.** Chỉ đưa vào khi repo để private và người trong ảnh đồng ý.

## Nguồn

- Repo đối chiếu: https://github.com/vanhungtq/valley-chibi-studio
- Codex `$imagegen` qua đăng nhập ChatGPT (dự án cộng đồng): https://github.com/Sateezg/codex-bridge · https://github.com/jdmnk/codex-imagegen-cli · https://github.com/leeguooooo/image-use/
- Báo cáo lỗi hạn mức ảnh trên Plus: https://github.com/openai/codex/issues/49214
- Tiện ích Nano Banana của Gemini CLI cần API key: https://github.com/gemini-cli-extensions/nanobanana
