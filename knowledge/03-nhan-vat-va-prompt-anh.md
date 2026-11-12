# Ảnh tham chiếu & cách prompt ảnh được lắp ghép

Ảnh storyboard là **hình dự kiến quay**, không phải ảnh hiện trường. Chủ dự án tự tạo ảnh thủ công bằng ChatGPT hoặc Gemini từ **gói prompt** (`goi-prompt.html`) do hệ thống dựng. Chuẩn chi tiết: `06-rubric-storyboard.md`.

## Ảnh thật đi vào đâu

| Ảnh | Thả vào | Dùng cho |
|---|---|---|
| Bối cảnh, đạo cụ, nhân vật của **một tập** | `episodes/epNN/input/boi-canh/`, `dao-cu/`, `nhan-vat/` | Visual bible của tập đó |
| Thứ dùng cho **mọi tập** (hai chị em, mèo, căn chòi) | `knowledge/visual-refs/` | Mọi tập tham chiếu lại |
| Ảnh chụp thực tế từng shot | `episodes/epNN/input/thuc-te/<ID shot>.jpg` | Thay hình dự kiến trên báo cáo |
| Ảnh AI bạn đã tạo | `episodes/epNN/storyboard/<ID shot>.png` | Hình dự kiến trên báo cáo |

## Thứ tự ưu tiên của một khung hình

1. Ảnh thực tế của chính shot đó (không cần tạo ảnh AI nữa).
2. Ảnh AI tạo từ prompt có đính kèm ảnh thật của người/nơi/vật.
3. Ảnh AI chỉ từ mô tả chữ (khi chưa có ảnh thật nào) — báo cáo vẫn dùng được nhưng độ giống thấp.
4. Chưa có hình: báo cáo vẫn đủ hướng dẫn quay bằng chữ.

## Giới hạn của model ảnh

- Mặt người không giống hệt giữa các lần tạo dù có ảnh tham chiếu; đủ cho storyboard. Làm trong **cùng một cuộc trò chuyện** cho mỗi tập thì ổn định hơn.
- Model hay làm đẹp quá mức; `style` trong visual bible đã có "documentary realism, unposed". Vẫn quá bóng bẩy thì thêm vào `style`, đừng sửa từng prompt.
- Không yêu cầu vẽ chữ hay số shot lên ảnh.
- Một số dịch vụ từ chối tạo ảnh giống người thật từ ảnh tham chiếu. Khi đó bỏ ảnh nhân vật, giữ ảnh bối cảnh và đạo cụ; mô tả chữ trong prompt vẫn giữ trang phục đúng.

## Model sheet (tùy chọn, làm một lần)

Để ổn định hơn, tạo cho mỗi nhân vật một tấm nhiều góc rồi lưu vào `knowledge/visual-refs/sheet-<ai>.png` và thêm vào `refs` của nhân vật trong visual bible. Prompt: `Character reference sheet of this person: front, three-quarter, side and back view, full body, neutral grey background, same outfit, even soft light, photographic. No text.`
