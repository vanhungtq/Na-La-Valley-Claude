#!/usr/bin/env python3
"""Dựng gói prompt tạo ảnh storyboard để chủ dự án tự tạo thủ công (ChatGPT / Gemini).

Dùng:  python3 scripts/build_prompt_pack.py episodes/ep01 [--all] [--embed]

Mỗi shot một thẻ: ảnh tham chiếu cần đính kèm, prompt đầy đủ (nút sao chép), tên file cần lưu.
Mặc định chỉ gồm shot chưa có ảnh thực tế và chưa có hình dự kiến, shot chủ chốt xếp trước.
--all: gồm cả shot đã có hình.   --embed: nhúng ảnh tham chiếu vào file (gửi đi một file duy nhất).

Prompt được LẮP GHÉP CỐ ĐỊNH từ visual-bible.json + shots.json, không viết tự do từng lần,
để nhân vật / bối cảnh / phong cách giống nhau giữa mọi khung hình.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nala import all_shots, esc, img_src, load_ep, now, read_json, resolve, shot_state

MAX_REFS = 5
LENS = [(24, "wide-angle view, deep space, the environment dominates the frame"),
        (40, "medium-wide view with natural perspective"),
        (60, "medium shot, normal perspective"),
        (90, "telephoto close-up, compressed background, soft out-of-focus backdrop"),
        (999, "long-lens extreme close-up detail, very shallow depth of field")]
SLOT = {"06:30-08:30": "early morning, cool mist, low sun rays breaking through fog",
        "08:30-11:00": "mid-morning clear mountain daylight, crisp directional sun",
        "11:00-13:30": "midday, shaded soft light, avoid harsh top sun",
        "14:00-16:30": "soft afternoon light, gentle warm side light",
        "16:30-17:30": "golden hour, warm low sun raking across textures",
        "17:30-18:30": "blue hour, cool dusk ambient, warm firelight and filament bulbs as key light"}
DEFAULT_STYLE = ("Photorealistic cinematic film still, documentary realism, unposed. Natural light, 35mm film look, "
                 "muted earth tones, gentle film grain, soft highlights. Aspect ratio 16:9.")
DEFAULT_NEG = ("No text, no captions, no watermark, no borders, no split panels. No plastic, no modern objects, "
               "no logos, no glossy studio look. Hands and tools anatomically correct.")


def lens_look(mm):
    return next(t for lim, t in LENS if mm <= lim)


def build_prompt(ep_dir, vb, sc, sh, prev):
    """Trả về (prompt, [(đường_dẫn_ảnh, chú_thích)])."""
    subjects, locs, props = vb.get("subjects") or {}, vb.get("locations") or {}, vb.get("props") or {}
    refs, lines = [], []

    def add_refs(item, label):  # label = (chú thích tiếng Việt cho người đọc, tiếng Anh cho prompt)
        for r in item.get("refs", []):
            if resolve(ep_dir, r) and r not in [x[0] for x in refs]:
                refs.append((r, *label))

    loc = locs.get(sc.get("location_id") or "", {})
    who = [subjects[c] | {"_id": c} for c in sh.get("characters", []) if c in subjects]
    what = [props[p] | {"_id": p} for p in sh.get("prop_ids", []) if p in props]
    for s in who:
        add_refs(s, (s.get("name", s["_id"]), f"the {s.get('name_en', s['_id'])} (person/animal identity and costume)"))
    add_refs(loc, (loc.get("name", "bối cảnh"), "the real location (architecture, materials, surroundings)"))
    for p in what:
        add_refs(p, (p.get("name", p["_id"]), f"the real prop: {p.get('desc_en', p['_id'])}"))
    psb = (prev or {}).get("storyboard") or {}
    if prev and prev.get("_scene") == sc["id"] and resolve(ep_dir, psb.get("image")) and psb.get("panel") is None:
        refs.append((psb["image"], f"khung hình trước ({prev['id']}) — giữ liên tục",
                     "the previous storyboard frame of this scene (keep look, costume and light continuous)"))
    refs = refs[:MAX_REFS]

    if refs:
        lines.append("ATTACHED REFERENCE IMAGES (real photos — match them faithfully, do not redesign):")
        lines += [f"  Image {n}: {en}" for n, (_, _vn, en) in enumerate(refs, 1)]
        lines.append("")
    lines.append("STYLE: " + (vb.get("style") or DEFAULT_STYLE))
    lines.append("")
    lines.append("LOCATION: " + (loc.get("desc_en") or sc.get("location") or "rural mountain valley, northern Vietnam"))
    if who:
        lines.append("")
        lines.append("PEOPLE / ANIMALS IN FRAME (keep identical in every frame of this film):")
        lines += [f"  - {s.get('name_en', s['_id']).upper()}: {s.get('desc_en', '')}" for s in who]
    if what:
        lines.append("KEY PROPS: " + "; ".join(p.get("desc_en", p["_id"]) for p in what))
    lines.append("")
    lines.append(f"CAMERA: {sh.get('size', '')}. {lens_look(sh.get('focal_mm', 35))}. f/{sh.get('aperture', 4)}. "
                 f"Camera position: {sh.get('angle_en') or sh.get('angle', 'eye level')}. Locked-off tripod framing.")
    if sh.get("composition_en") or sh.get("composition"):
        lines.append("COMPOSITION: " + (sh.get("composition_en") or sh["composition"]))
    lines.append("THE MOMENT: " + (sh.get("frame_en") or sh.get("action", "")))
    lines.append("LIGHT: " + SLOT.get(sc.get("clock_slot"), "natural light")
                 + (". " + sh["light_en"] if sh.get("light_en") else ""))
    if prev and prev.get("_scene") == sc["id"]:
        lines.append(f"CONTINUITY: This frame directly follows the previous one ({prev.get('frame_en') or prev.get('action', '')}). "
                     "Same place, same costumes, same props, same weather and time of day. Only the camera framing changes.")
    lines.append("")
    lines.append("CONSTRAINTS: " + (vb.get("negative") or DEFAULT_NEG))
    lines.append("Generate exactly one single image.")
    return "\n".join(lines), refs


def collect(ep_dir, include_all=False):
    ep_dir = Path(ep_dir)
    data = load_ep(ep_dir)
    vb = read_json(ep_dir / "visual-bible.json", {}) or {}
    items, prev = [], None
    for sc, sh in all_shots(data):
        state = shot_state(ep_dir, sh)[0]
        prompt, refs = build_prompt(ep_dir, vb, sc, sh, prev)
        if include_all or state == "trong":
            items.append({"sc": sc, "sh": sh, "prompt": prompt, "refs": refs})
        prev = dict(sh, _scene=sc["id"])
    items.sort(key=lambda x: not x["sh"].get("key"))
    return data, vb, items


CSS = """
:root{--bg:#f6f2ea;--card:#fff;--ink:#23262b;--mute:#6b6f76;--line:#ddd5c6;--indigo:#2c3e5d;--clay:#b4532f;--moss:#56683f}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{background:var(--indigo);color:#fff;padding:22px 20px}header h1{margin:0 0 4px;font-size:22px}header p{margin:0;opacity:.85}
main{max-width:1000px;margin:0 auto;padding:16px}
.how{background:#fffaf0;border:1px solid var(--line);border-left:4px solid var(--clay);border-radius:8px;padding:12px 16px;margin:0 0 18px}
.how ol{margin:6px 0 0;padding-left:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;margin:0 0 16px;overflow:hidden}
.card h2{margin:0;padding:10px 14px;font-size:16px;background:#f1ebdf;border-bottom:1px solid var(--line);display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.key{background:var(--clay);color:#fff;border-radius:99px;padding:1px 9px;font-size:11px;font-weight:600}
.body{padding:12px 14px}.vn{color:var(--mute);margin:0 0 10px}
.refs{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 10px}.refs figure{margin:0;width:150px}
.refs img{width:150px;height:100px;object-fit:cover;border-radius:6px;border:1px solid var(--line);display:block}
.refs figcaption{font-size:11px;color:var(--mute);line-height:1.3;margin-top:3px;word-break:break-all}
pre{white-space:pre-wrap;background:#faf8f3;border:1px solid var(--line);border-radius:8px;padding:10px 12px;font:12.5px/1.5 ui-monospace,Menlo,Consolas,monospace;margin:0 0 10px;max-height:300px;overflow:auto}
button{background:var(--indigo);color:#fff;border:0;border-radius:8px;padding:9px 16px;font-size:14px;cursor:pointer}
button.ok{background:var(--moss)}.save{display:inline-block;margin-left:10px;font-size:13px;color:var(--mute)}.save code{background:#eee6d6;padding:2px 6px;border-radius:4px;color:var(--ink)}
.none{color:var(--mute);font-size:13px;margin:0 0 10px}
"""
JS = """
document.querySelectorAll('button[data-t]').forEach(b=>b.onclick=async()=>{
 const t=document.getElementById(b.dataset.t).textContent;
 try{await navigator.clipboard.writeText(t)}catch(e){const r=document.createRange();r.selectNodeContents(document.getElementById(b.dataset.t));const s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand('copy')}
 b.textContent='Đã sao chép ✓';b.classList.add('ok');setTimeout(()=>{b.textContent='Sao chép prompt';b.classList.remove('ok')},1800)});
"""


def build(ep_dir, include_all=False, embed=False):
    ep_dir = Path(ep_dir)
    data, vb, items = collect(ep_dir, include_all)
    h = [f"<!doctype html><html lang='vi'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<title>Gói prompt · {esc(data.get('episode'))}</title><style>{CSS}</style>"
         f"<header><h1>Gói prompt tạo ảnh storyboard</h1><p>{esc(data.get('title'))} · {len(items)} khung hình cần tạo · "
         f"{sum(1 for x in items if x['sh'].get('key'))} chủ chốt · dựng lúc {now()}</p></header><main>"
         "<div class='how'><b>Cách làm</b><ol><li>Mở ChatGPT hoặc Gemini, tạo một cuộc trò chuyện riêng cho tập này.</li>"
         "<li>Với mỗi thẻ: đính kèm đúng các ảnh tham chiếu theo thứ tự Image 1, 2…, bấm <b>Sao chép prompt</b> rồi dán.</li>"
         "<li>Lưu ảnh kết quả vào thư mục <code>storyboard/</code> của tập với đúng tên file ghi trên thẻ.</li>"
         "<li>Báo Claude <code>/cap-nhat</code> để gắn ảnh vào báo cáo. Shot nào đã có ảnh thực tế thì không cần tạo.</li></ol>"
         "Làm các thẻ <span class='key'>CHỦ CHỐT</span> trước; phần còn lại có thể bỏ qua.</div>"]
    md = [f"# Gói prompt — {data.get('title')}\n\nDựng lúc {now()}. Lưu ảnh vào `storyboard/<ID>.png`.\n"]
    for n, it in enumerate(items):
        sc, sh = it["sc"], it["sh"]
        key = "<span class='key'>CHỦ CHỐT</span>" if sh.get("key") else ""
        h.append(f"<section class='card'><h2>{esc(sh['id'])} {key}<span style='font-weight:400;color:var(--mute)'>"
                 f"{esc(sc.get('title'))} · {esc(sh.get('size'))} · {esc(sh.get('focal_mm'))}mm</span></h2><div class='body'>"
                 f"<p class='vn'>{esc(sh.get('action'))}</p>")
        if it["refs"]:
            h.append("<div class='refs'>" + "".join(
                f"<figure><img src='{img_src(ep_dir, r, embed, 480)}' alt=''><figcaption><b>Image {k}</b> · {esc(lab)}<br>{esc(r)}</figcaption></figure>"
                for k, (r, lab, _en) in enumerate(it["refs"], 1)) + "</div>")
        else:
            h.append("<p class='none'>Chưa có ảnh tham chiếu thật cho khung hình này — prompt chỉ dựa trên mô tả chữ.</p>")
        h.append(f"<pre id='p{n}'>{esc(it['prompt'])}</pre><button data-t='p{n}'>Sao chép prompt</button>"
                 f"<span class='save'>Lưu thành <code>storyboard/{esc(sh['id'])}.png</code></span></div></section>")
        md.append(f"## {sh['id']}{' — CHỦ CHỐT' if sh.get('key') else ''}\n\n{sh.get('action', '')}\n\n"
                  + "".join(f"- Đính kèm Image {k}: `{r}` ({lab})\n" for k, (r, lab, _en) in enumerate(it["refs"], 1))
                  + f"\n```text\n{it['prompt']}\n```\n\nLưu: `storyboard/{sh['id']}.png`\n")
    if not items:
        h.append("<p>Mọi shot đã có hình dự kiến hoặc ảnh thực tế. Dùng <code>--all</code> để xem lại toàn bộ prompt.</p>")
    h.append(f"</main><script>{JS}</script></html>")
    (ep_dir / "goi-prompt.html").write_text("".join(h), encoding="utf-8")
    (ep_dir / "goi-prompt.md").write_text("\n".join(md), encoding="utf-8")
    return len(items)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    n = build(args[0], "--all" in sys.argv, "--embed" in sys.argv)
    print(f"Đã dựng goi-prompt.html và goi-prompt.md ({n} khung hình) trong {args[0]}")
