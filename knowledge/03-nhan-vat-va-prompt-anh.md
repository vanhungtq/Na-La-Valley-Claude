# Nhân vật & khối prompt chuẩn cho ảnh storyboard

Ảnh storyboard là **bản phác dự kiến quay**, không phải ảnh hiện trường. Mục tiêu: người quay nhìn vào hiểu ngay bố cục, cỡ cảnh, hướng sáng. Không cần đẹp như poster.

## Khối cố định — dán nguyên văn vào mọi prompt (tiếng Anh để model ảnh hiểu tốt nhất)

```text
STYLE: cinematic film still, natural light, 35mm film look, muted earth tones
(indigo, moss green, red basalt soil, weathered wood, dry palm thatch), soft
halation, shallow depth of field at f/4. 16:9. No text, no captions, no
watermark, no borders. No plastic, no modern objects, no logos.

SETTING: remote mountain valley in northern Vietnam at 1,200 m, misty,
old plum orchard, terraced fields, bamboo forest, a small rough-sawn timber
hut with a dry palm-leaf thatched roof, clay stove, black cast-iron pan,
woven bamboo baskets, unglazed crackle ceramic.

OLDER SISTER (26): calm, strong build, hair wrapped in a plain cloth scarf,
hand-woven indigo jacket or earth-brown quilted vest, dark raw-silk trousers.

YOUNGER SISTER (23): gentle, slender, single side braid, chunky ecru
knit sweater or brick-red quilted vest, raw linen apron.

CAT: short-haired ash-grey cat, copper-amber eyes.
```

Khi đã có ảnh thật trong `visual-refs/`, đính kèm làm ảnh tham chiếu và thêm dòng: `Match the people, hut and props to the attached reference photos.` Ảnh thật luôn thắng mô tả chữ.

## Khuôn prompt atlas 2×2 (4 shot / 1 ảnh — tiết kiệm hạn mức)

```text
Create ONE image: a 2x2 grid of four 16:9 film stills, edge to edge, no
gutters, no borders, no text. Same characters, costumes, location and time
of day continuity across panels.

[khối cố định ở trên]

TOP-LEFT  (S03-SH01): <cỡ cảnh>, <tiêu cự tương đương>, <góc máy>. <hành động>. <ánh sáng>.
TOP-RIGHT (S03-SH02): ...
BOTTOM-LEFT (S03-SH03): ...
BOTTOM-RIGHT (S03-SH04): ...
```

Quy ước ô (`panel` trong `shots.json`): `0` trên-trái, `1` trên-phải, `2` dưới-trái, `3` dưới-phải. Nhóm lẻ để trống ô cuối.

## Dịch thông số máy sang ngôn ngữ ảnh

| Trong shot list | Viết trong prompt |
|---|---|
| 18–24mm | wide shot, deep space, environment dominant |
| 35mm | medium-wide, natural perspective |
| 50mm | medium shot, waist-up or object with context |
| 70–85mm | telephoto close-up, compressed background, soft bokeh |
| 105mm macro/insert | extreme close-up detail, very shallow focus |
| Top-down 90° | overhead flat-lay view straight down |
| Low angle 35° | low angle looking up |
| 06:30–08:30 | early morning mist, low sun rays through fog |
| 16:30–17:30 | golden hour, warm side light raking across wood |
| 17:30–18:30 | blue hour, cool ambient, warm firelight and filament bulbs |

## Giới hạn cần biết

- Model ảnh hay "làm đẹp" quá mức: thêm `documentary realism, unposed, working hands slightly dirty` khi cần.
- Mặt nhân vật sẽ không giống hệt giữa các lần tạo. Chấp nhận ở mức storyboard; muốn ổn định hơn thì tạo một **model sheet** (xem `visual-refs/README.md`) và luôn đính kèm.
- Không yêu cầu vẽ chữ, số shot lên ảnh. Số shot do production book ghi.
