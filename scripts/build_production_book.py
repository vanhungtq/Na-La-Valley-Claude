#!/usr/bin/env python3
"""Dựng hồ sơ quay (production-book.html + shotlist.csv) từ shots.json.

Dùng:  python3 scripts/build_production_book.py episodes/ep01
Mở production-book.html bằng trình duyệt, in ra PDF để mang đi hiện trường.
Ảnh storyboard được tham chiếu bằng đường dẫn tương đối; atlas 2x2 được cắt ô bằng CSS.
"""
import csv
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = json.loads((ROOT / "knowledge/02-thiet-bi-va-rang-buoc.json").read_text(encoding="utf-8"))
E = lambda v: html.escape(str(v if v is not None else ""))

CSS = """
body{font:14px/1.45 system-ui,sans-serif;color:#222;margin:24px;max-width:1100px}
h1{margin:0 0 4px}h2{margin:28px 0 8px;border-bottom:2px solid #333;padding-bottom:4px}
h3{margin:18px 0 6px}.meta{color:#555}
table{border-collapse:collapse;width:100%;margin:6px 0}th,td{border:1px solid #bbb;padding:5px 7px;vertical-align:top;text-align:left}
th{background:#eee}.id{font-weight:700;white-space:nowrap}.tech{white-space:nowrap;font-size:12px}
.sb{width:192px;height:108px;border:1px solid #999;background:#f3f3f3 center/cover no-repeat;
display:flex;align-items:center;justify-content:center;color:#888;font-size:11px}
.tag{font-size:10px;color:#a40;display:block}.mc{background:#fff6d6}
.sound{background:#f6f6f6;padding:6px 8px;margin:4px 0;font-size:13px}
ul.check{list-style:none;padding:0;columns:2}ul.check li:before{content:"\\2610  "}
@media print{body{margin:8mm}h2{break-before:page}tr{break-inside:avoid}}
"""


def frame(sh):
    sb = sh.get("storyboard") or {}
    level, img, panel = sb.get("level", "none"), sb.get("image"), sb.get("panel")
    if level == "none" or not img:
        return '<div class="sb">chưa có hình</div>'
    style = f"background-image:url('{E(img)}');"
    if panel in (0, 1, 2, 3):
        style += f"background-size:200% 200%;background-position:{(panel % 2) * 100}% {(panel // 2) * 100}%;"
    label = "Ảnh AI — dự kiến quay" if level == "ai" else "Sơ đồ minh họa"
    return f'<div class="sb" style="{style}"></div><span class="tag">{label}</span>'


def build(ep_dir):
    ep_dir = Path(ep_dir)
    data = json.loads((ep_dir / "shots.json").read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])
    shots = [(sc, sh) for sc in scenes for sh in sc.get("shots", [])]
    total = sum(sh.get("seconds", 0) for _, sh in shots)
    out = [f"<!doctype html><html lang='vi'><meta charset='utf-8'><title>{E(data.get('title'))}</title>"
           f"<style>{CSS}</style><h1>{E(data.get('title'))}</h1>"
           f"<p class='meta'>{E(data.get('episode'))} · {len(scenes)} cảnh · {len(shots)} shot · "
           f"{total / 60:.1f} phút dựng (mục tiêu {data.get('target_seconds', 0) / 60:.1f}) · "
           f"Ảnh storyboard do AI tạo là hình dự kiến, không phải ảnh hiện trường.</p>"]

    out.append("<h2>Lịch quay theo ánh sáng</h2><table><tr><th>Khung giờ</th><th>Ghi chú Bible</th><th>Cảnh</th><th>Số shot</th></tr>")
    for slot, note in RULES["clock_slots"].items():
        scs = [s for s in scenes if s.get("clock_slot") == slot]
        if scs:
            out.append(f"<tr><td class='id'>{E(slot)}</td><td>{E(note)}</td><td>"
                       + ", ".join(f"{E(s['id'])} {E(s.get('title'))}" for s in scs)
                       + f"</td><td>{sum(len(s.get('shots', [])) for s in scs)}</td></tr>")
    out.append("</table>")

    props = sorted({p for _, sh in shots for p in sh.get("props", [])})
    if props:
        out.append("<h2>Đạo cụ cần chuẩn bị</h2><ul class='check'>" + "".join(f"<li>{E(p)}</li>" for p in props) + "</ul>")

    out.append("<h2>Phân cảnh & storyboard</h2>")
    for sc in scenes:
        snd = sc.get("sound") or {}
        out.append(f"<h3>{E(sc.get('id'))} · {E(sc.get('title'))}</h3>"
                   f"<p class='meta'>{E(sc.get('location'))} · {E(sc.get('story_time'))} · quay {E(sc.get('clock_slot'))}"
                   f" · {sum(s.get('seconds', 0) for s in sc.get('shots', []))}s</p>"
                   f"<div class='sound'><b>Âm thanh</b> — Ambience: {E(snd.get('ambience'))} · Foley: {E(snd.get('foley'))}"
                   f" · Accent: {E(snd.get('accent'))} · Nhạc: {E(snd.get('bgm'))}</div>"
                   "<table><tr><th>Shot</th><th>Hình</th><th>Máy</th><th>Hành động</th><th>Âm thanh / ghi chú</th><th>Giây</th></tr>")
        for sh in sc.get("shots", []):
            tech = (f"{E(sh.get('size'))}<br>{E(sh.get('focal_mm'))}mm F{E(sh.get('aperture'))} · {E(sh.get('fps'))}fps"
                    f"<br>{E(sh.get('support'))} · {E(sh.get('movement', 'static'))}<br>{E(sh.get('angle'))}")
            notes = E(sh.get("sound_note"))
            if sh.get("pair"):
                notes += f"<br>Cặp match cut: {E(sh['pair'])}"
            if sh.get("micro_cut"):
                notes += "<br><b>Micro Cut</b> — giữ chủ thể ở 1/3 giữa"
            if sh.get("note"):
                notes += f"<br>{E(sh['note'])}"
            out.append(f"<tr class='{'mc' if sh.get('micro_cut') else ''}'><td class='id'>{E(sh.get('id'))}</td>"
                       f"<td>{frame(sh)}</td><td class='tech'>{tech}</td>"
                       f"<td>{E(sh.get('action'))}<br><i>{E(sh.get('motivation'))}</i></td>"
                       f"<td>{notes}</td><td>{E(sh.get('seconds'))}</td></tr>")
        out.append("</table>")

    out.append("<h2>Danh sách thu Foley tại phòng dựng</h2><ul class='check'>"
               + "".join(f"<li>{E(sc['id'])}: {E((sc.get('sound') or {}).get('foley'))}</li>" for sc in scenes) + "</ul>")
    (ep_dir / "production-book.html").write_text("".join(out) + "</html>", encoding="utf-8")

    cols = ["id", "size", "focal_mm", "aperture", "fps", "support", "movement", "angle", "action", "seconds", "micro_cut"]
    with open(ep_dir / "shotlist.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["scene", "clock_slot"] + cols)
        for sc, sh in shots:
            w.writerow([sc.get("id"), sc.get("clock_slot")] + [sh.get(c, "") for c in cols])
    return len(shots)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    n = build(sys.argv[1])
    print(f"Đã dựng production-book.html và shotlist.csv ({n} shot) trong {sys.argv[1]}")
