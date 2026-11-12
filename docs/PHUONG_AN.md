# Phương án hệ thống Agents cho Nà Lạ Valley

Cập nhật 12/11/2026 (bản 2). Đã đọc: Project Bible, repo `vanhungtq/valley-chibi-studio`, repo `0xsline/StoryGen-Atelier`, và mô tả quy trình thực tế của chủ dự án.

## 1. Kết luận

**Repo này là xưởng. Claude Code viết và điều phối. Chủ dự án cung cấp thực tế (ý tưởng, ảnh thật, ảnh từng shot) và tự tạo ảnh AI từ gói prompt. Mọi thứ hội tụ vào một file `bao-cao.html` được dựng lại sau mỗi vòng cho đến bản Final.**

| Việc | Ai làm | Trả bằng gì |
|---|---|---|
| Định hướng, concept, kịch bản, shot list, âm thanh, hướng dẫn quay, rà soát, gói YouTube | Claude Code: 7 agent, 9 lệnh | Gói Claude |
| Xem ảnh bối cảnh/đạo cụ/nhân vật, ảnh cú máy mẫu, ảnh thực tế từng shot và nhận xét | Claude (xem ảnh trực tiếp) | Gói Claude |
| Tạo ảnh storyboard | **Chủ dự án, thủ công**, từ `goi-prompt.html` | Gói ChatGPT Plus / Gemini Pro |
| Xem video YouTube để lấy timeline | Ứng dụng Gemini (dán prompt, dán kết quả) | Gói Gemini Pro |
| Lưu trữ, lịch sử phiên bản | Git/GitHub | Miễn phí |

Không máy chủ, không Cloudflare, không API. Dashboard là một file HTML tĩnh dựng từ trạng thái trong repo.

## 2. Học gì từ StoryGen-Atelier

StoryGen-Atelier là ứng dụng React + Express gọi **API có khóa** của Gemini (văn bản, ảnh) và Vertex Veo (video) để biến một câu thành storyboard rồi thành video AI. Phần hạ tầng không dùng được cho dự án này (cần API tính phí; kênh quay thật nên không cần sinh video). Phần **cách giữ storyboard nhất quán** thì đáng lấy:

| Cơ chế của StoryGen-Atelier | Trong mã của họ | Áp dụng ở đây |
|---|---|---|
| **heroSubject**: mô tả chi tiết nhân vật chính, sinh một lần ở shot 1 rồi gắn vào đầu mọi prompt | `llmService.js`, `imageGenService.js` | `visual-bible.json`: mô tả cố định cho từng nhân vật, **từng bối cảnh, từng đạo cụ**, viết từ ảnh thật. Script gắn vào mọi prompt |
| **Ảnh tham chiếu**: ảnh shot 1 được gửi kèm mọi shot sau | `storyboardController.js` | Gói prompt liệt kê ảnh **thật** cần đính kèm cho từng shot, cộng ảnh khung trước cùng cảnh nếu đã có |
| **previousStyleHint**: prompt nhắc phong cách shot trước | `buildImagePrompt` | Dòng `CONTINUITY` tự sinh: cùng nơi, cùng trang phục, cùng ánh sáng với khung trước |
| **Một khối style chung** cho mọi khung | `BASE_IMAGE_STYLE` | `style` và `negative` trong visual bible |
| **Nhân quả bắt buộc**: mỗi shot phải nói vì sao nó đến sau shot trước ("因此/于是/紧接着") | prompt của `generatePrompts` | Trường `link` bắt buộc cho mọi shot; không viết nổi thì shot thừa |
| **Nhịp 25/50/25** mở–giữa–kết | prompt của `generatePrompts` | Beat map trong kịch bản, hiện thành dòng thời gian trên báo cáo |
| **Cấu trúc prompt** chủ thể / hành động / bối cảnh / máy / phong cách | `VideoGenerationPromptGuide.md` | Khung lắp ghép cố định trong `build_prompt_pack.py` |
| **Phân tích chuyển cảnh A→B** bằng cách xem hai khung | `analyzeShotTransition` | Trường `cut` của Quay phim; Giám sát xem các ảnh thật liền nhau để kiểm liên tục |
| Tạo lại từng shot, nhật ký, thư viện ảnh | regenerate, logs, gallery | Sửa dữ liệu một shot rồi dựng lại; `status.json` + dashboard; lịch sử phiên bản trên báo cáo |

Khác biệt cố ý: ở đó LLM viết tự do từng prompt nên dễ trôi; ở đây **prompt được lắp ghép bằng script từ dữ liệu**, agent chỉ chăm dữ liệu (`desc_en`, `frame_en`). Sửa một chỗ, mọi khung đổi theo.

## 3. Nâng chất lượng kịch bản và storyboard bằng cách nào

1. **Bám ảnh thật.** Biên kịch, Quay phim, Họa sĩ đều phải mở xem ảnh đầu vào trước khi viết và liệt kê ảnh đã xem.
2. **Thang chấm có bằng chứng.** Kịch bản: 10 tiêu chí × 0–2, phải dẫn ID shot (`05-rubric-kich-ban.md`); dưới 15/20 thì quay lại. Storyboard: mỗi shot chủ chốt đủ `link`, `composition`, `light`, `direction`, `cut`, `frame_en` (`06-rubric-storyboard.md`); thiếu là validator báo lỗi.
3. **Chấm độc lập.** `giam-sat` chạy ở ngữ cảnh riêng, chấm lại từ đầu, không tin điểm tự chấm.
4. **Hướng dẫn quay viết cho người cầm máy.** `direction` là lệnh đo được: máy đặt đâu, cao bao nhiêu, cách bao xa, mấy lượt.
5. **Vòng phản hồi bằng ảnh thực tế.** Quay phim xem từng ảnh bạn chụp, chấm đạt / cần chỉnh / quay lại kèm lệnh sửa đo được; hiện trường khác kế hoạch thì kế hoạch đổi theo hiện trường.
6. **Thư viện nuôi agent.** Video mẫu → thẻ kỹ thuật có bằng chứng → sổ tay từng agent. Lỗi chủ dự án sửa cũng thành bài học trong sổ tay.

## 4. Kiến trúc

```
        knowledge/inbox ──/nap-thu-vien──► video-mau/ ──/hoc-tu-thu-vien──► ky-thuat/ ──► so-tay/<agent>
                                                                                              │ (agent đọc trước khi viết)
 input/y-tuong.md + ảnh thật                                                                  ▼
        │  /tap-moi                SHOWRUNNER (phiên chính: định hướng, 3 concept, điều phối, 3 cổng duyệt)
        ▼                            ├ thu-thu ─ bien-kich ─ giam-sat
 shots.json + visual-bible.json ◄────┼ quay-phim ─ am-thanh ─ giam-sat
        │                            └ hoa-si-storyboard ∥ chien-luoc-youtube
        ├─ build_prompt_pack ─► goi-prompt.html ─► bạn tạo ảnh ─► storyboard/<ID>.png ─┐
        ├─ bạn chụp thực tế ─► input/thuc-te/<ID>.jpg ─────────────────────────────────┤
        │  /cap-nhat: sync_inputs → quay-phim nhận xét → (bien-kich chỉnh) → giam-sat  ◄┘
        └─ build_report ─► bao-cao.html  v1 → v2 → … → FINAL
 progress.py ghi status.json ─► dashboard.html
```

**Thư viện kiến thức** (`knowledge/`): bạn thả vào `inbox/` video mẫu (văn bản, timeline, ảnh từng cú máy) hoặc tài liệu. Thủ thư **xem từng ảnh** và lập `reference.json` có nhãn nguồn cho từng cú máy. `/hoc-tu-thu-vien` rút thành thẻ kỹ thuật, bạn duyệt, rồi ghi vào sổ tay agent. Khi sổ tay không đủ, lệnh đó *đề xuất* skill mới hoặc đoạn sửa agent/rubric/validator và chờ bạn đồng ý.

**Dashboard** (`dashboard.html`): 9 bước của mỗi tập, 8 thẻ agent (đang làm / xong / bị chặn + việc đang làm), câu đang chờ bạn quyết, nhật ký, thanh tiến độ ảnh thực tế, số liệu thư viện. Nó hiển thị đúng những gì được ghi bằng `progress.py`; nếu một bước quên ghi thì dashboard thiếu bước đó.

**Báo cáo** (`bao-cao.html`): tiến độ và dòng thời gian dựng · kịch bản · storyboard (hình dự kiến cạnh ảnh thực tế, thông số, hướng dẫn quay, nhận xét, lọc theo trạng thái) · lịch quay theo ánh sáng, đạo cụ · âm thanh · việc tiếp theo · lịch sử phiên bản. `--embed` cho ra một file duy nhất.

## 5. So với Xưởng Chibi

Giữ: thứ tự vai trò, kỷ luật nguồn (đã xem / chủ dự án nói / giả định), thời lượng ±5%, ID ổn định, cổng duyệt. Bỏ: Cloudflare Worker/D1/KV/OAuth, giao diện 3D, giới hạn file 1 MB qua MCP, cơ chế lease 15 phút. Thêm: rà soát độc lập, kiểm tra theo Bible bằng script, âm thanh, YouTube quốc tế, thư viện có bằng chứng, vòng ảnh thực tế.

## 6. Giới hạn cần biết

- **Chưa chạy trọn một tập thật.** Script đã chạy thử với ảnh giả lập; các agent và lệnh chưa. Tập đầu là phép thử; dự kiến phải chỉnh agent sau lần đầu.
- **Claude không xem video.** Thư viện mạnh đến đâu tùy vào ảnh cú máy bạn chụp màn hình; chuyển động máy, âm thanh, nhịp cắt chỉ có khi bạn hoặc Gemini ghi lại.
- **Ảnh AI không giống hệt người thật** dù có ảnh tham chiếu, và một số dịch vụ từ chối dựng người thật từ ảnh. Đủ cho storyboard; ảnh thực tế mới là đích.
- **Repo sẽ nặng dần vì ảnh.** Thu nhỏ ảnh còn cạnh dài ~1600 px trước khi thả vào. Ảnh người thật: chỉ đưa vào khi repo private và người trong ảnh đồng ý.
- **Rà soát của `giam-sat` không thay khảo sát thực địa.**
- Hai file nguyên tắc `01` và `04` là tổng hợp ban đầu của Claude, chưa đối chiếu video thật hay số liệu kênh.

## 7. Lộ trình

| Đợt | Việc | Xong khi |
|---|---|---|
| Đã làm | Thư viện + inbox, 7 agent, 9 lệnh, 5 script, rubric, dashboard, báo cáo, Tập 1 hạt giống | Chuỗi script chạy được với ảnh giả lập |
| 1 | Thả ảnh chòi/đạo cụ/nhân vật vào `episodes/ep01/input/`, trả lời `input/y-tuong.md`, chạy `/tap-moi 01` | Có báo cáo v1 với kịch bản 22 phút đạt ≥ 15/20 |
| 2 | Thả 3–5 video mẫu vào `knowledge/inbox/`, chạy `/nap-thu-vien` rồi `/hoc-tu-thu-vien` | Có thẻ kỹ thuật đã duyệt; sổ tay agent có nội dung |
| 3 | Chụp thực tế, `/cap-nhat 01` nhiều vòng | Bản FINAL Tập 1 |
| 4 | Sau khi quay: ghi bài học thực địa; chỉnh agent theo chỗ lệch | Tập 2 ít [GIẢ ĐỊNH] hơn Tập 1 |

## Nguồn

- https://github.com/vanhungtq/valley-chibi-studio
- https://github.com/0xsline/StoryGen-Atelier (đọc tại commit `033e0c6`: `backend/src/services/llmService.js`, `imageGenService.js`, `controllers/storyboardController.js`, `guide/VideoGenerationPromptGuide.md`)
- Codex `$imagegen` qua đăng nhập ChatGPT (tùy chọn, chưa thử): https://github.com/Sateezg/codex-bridge
- Tiện ích Nano Banana của Gemini CLI cần API key: https://github.com/gemini-cli-extensions/nanobanana
