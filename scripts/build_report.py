#!/usr/bin/env python3
"""Dựng báo cáo tập phim: kịch bản + storyboard + hướng dẫn quay trong MỘT file HTML.

Dùng:  python3 scripts/build_report.py episodes/ep01 [--embed]

Tạo bao-cao.html (mở bằng trình duyệt, in ra PDF được) và shotlist.csv.
--embed: nhúng mọi ảnh vào file để gửi đi một file duy nhất (cần Pillow để thu nhỏ ảnh; không có vẫn chạy).
Mỗi shot hiện hình dự kiến và ảnh thực tế cạnh nhau, kèm nhận xét và trạng thái.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nala import RULES, all_shots, coverage, esc, img_src, load_ep, md_to_html, now, read_json, shot_state

BEAT_COLORS = ["#2c3e5d", "#56683f", "#b4532f", "#a8842c", "#6d4a6b", "#3d7273", "#8a5a3a", "#4f5d75"]
CSS = """
:root{--bg:#f6f2ea;--card:#fff;--ink:#23262b;--mute:#6b6f76;--line:#ddd5c6;--soft:#f1ebdf;--indigo:#2c3e5d;--clay:#b4532f;--moss:#56683f;--amber:#b07a14;--red:#a83232}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header.top{background:var(--indigo);color:#fff;padding:28px 24px 22px}
header.top .wrap,main{max-width:1240px;margin:0 auto}
.kicker{font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.75}
header.top h1{margin:6px 0 8px;font-size:28px;line-height:1.2;text-wrap:balance}
.logline{max-width:70ch;opacity:.92;margin:0 0 16px}
.stats{display:flex;flex-wrap:wrap;gap:10px}
.stat{background:rgba(255,255,255,.1);border-radius:10px;padding:9px 14px;min-width:120px}
.stat b{display:block;font-size:21px;font-variant-numeric:tabular-nums}.stat span{font-size:12px;opacity:.8}
.rev{display:inline-block;background:var(--clay);border-radius:99px;padding:2px 12px;font-size:12px;font-weight:600;margin-left:8px;vertical-align:middle}
.rev.final{background:var(--moss)}
nav{position:sticky;top:0;z-index:5;background:#fffdf8;border-bottom:1px solid var(--line);padding:0 16px;overflow-x:auto;white-space:nowrap}
nav a{display:inline-block;padding:11px 12px;color:var(--ink);text-decoration:none;font-size:14px;font-weight:600}
nav a:hover{color:var(--clay)}
main{padding:8px 16px 60px}
section{margin-top:34px}h2{font-size:21px;margin:0 0 12px;padding-bottom:6px;border-bottom:2px solid var(--indigo)}
h3{font-size:17px;margin:22px 0 6px}h4,h5,h6{margin:14px 0 4px}
.prose{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 20px 14px;overflow-x:auto}
.prose p,.prose li{max-width:80ch}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:14px}
th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}th{background:var(--soft)}
pre{white-space:pre-wrap;background:var(--soft);padding:10px;border-radius:8px;font-size:13px}
blockquote{margin:8px 0;padding:6px 14px;border-left:4px solid var(--clay);background:#fffaf0}
.bar{display:flex;height:44px;border-radius:8px;overflow:hidden;border:1px solid var(--line)}
.bar a{display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;font-weight:600;text-decoration:none;min-width:3px;overflow:hidden;border-right:1px solid rgba(255,255,255,.35)}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin:8px 0 0;font-size:13px;color:var(--mute)}
.legend i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;vertical-align:-1px}
.prog{display:flex;height:14px;border-radius:99px;overflow:hidden;background:#e6dfd0;margin:6px 0}
.prog span{display:block}.p-dat{background:var(--moss)}.p-chinh{background:var(--amber)}.p-quay-lai{background:var(--red)}.p-cho{background:#7b8794}.p-ai{background:#b9c3d6}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 6px}
.filters button{border:1px solid var(--line);background:#fff;border-radius:99px;padding:6px 14px;font-size:13px;cursor:pointer;color:var(--ink)}
.filters button.on{background:var(--indigo);color:#fff;border-color:var(--indigo)}
.scene{margin-top:24px}.scene>header{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline}
.scene>header h3{margin:0}.meta{color:var(--mute);font-size:13px}
.sound{background:#fffaf0;border:1px solid var(--line);border-radius:8px;padding:7px 12px;font-size:13px;margin:6px 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px}
.shot{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column;break-inside:avoid}
.shot.key{border-color:var(--clay);box-shadow:0 0 0 1px var(--clay)}
.frames{display:grid;grid-template-columns:1fr;background:#1d2026}.frames.two{grid-template-columns:1fr 1fr;gap:2px}
.frame{position:relative;aspect-ratio:16/9;background:#2a2e36 center/cover no-repeat;display:flex;align-items:center;justify-content:center;color:#8d939e;font-size:12px;text-align:center;padding:8px}
.frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.frame .lab{position:absolute;left:6px;top:6px;background:rgba(0,0,0,.62);color:#fff;font-size:10px;letter-spacing:.06em;padding:2px 7px;border-radius:4px;z-index:1}
.sb{padding:10px 13px 12px;display:flex;flex-direction:column;gap:6px}
.row1{display:flex;align-items:center;gap:7px;flex-wrap:wrap}.sid{font-weight:700;font-size:15px}
.badge{font-size:11px;font-weight:600;border-radius:99px;padding:2px 9px;color:#fff;background:#7b8794}
.b-dat{background:var(--moss)}.b-chinh{background:var(--amber)}.b-quay-lai{background:var(--red)}.b-ai{background:#5f7396}.b-trong{background:#a7a297}
.tag{font-size:11px;border:1px solid var(--line);border-radius:99px;padding:1px 8px;color:var(--mute)}.tag.k{border-color:var(--clay);color:var(--clay);font-weight:600}
.sec{margin-left:auto;font-variant-numeric:tabular-nums;color:var(--mute);font-size:13px}
.spec{font-size:12.5px;color:var(--mute)}
.action{font-size:14.5px}.link{font-size:13px;color:var(--mute);font-style:italic}
dl{margin:2px 0 0;font-size:13px;display:grid;grid-template-columns:auto 1fr;gap:3px 10px}dt{color:var(--mute);white-space:nowrap}dd{margin:0}
.guide{background:#eef2f7;border-radius:7px;padding:7px 10px;font-size:13.5px}.guide b{color:var(--indigo)}
.fb{border-radius:7px;padding:7px 10px;font-size:13.5px;border-left:4px solid #7b8794;background:#f3f4f6}
.fb.dat{border-color:var(--moss);background:#eef3e8}.fb.chinh{border-color:var(--amber);background:#fbf3df}.fb.quay-lai{border-color:var(--red);background:#f9e8e6}
ul.check{list-style:none;padding:0;columns:3 220px;margin:6px 0}ul.check li{break-inside:avoid;padding:2px 0}ul.check li:before{content:"\\2610  "}
.todo li{margin:3px 0}.empty{color:var(--mute)}
footer{max-width:1240px;margin:0 auto;padding:0 16px 40px;color:var(--mute);font-size:12.5px}
@media (max-width:520px){.grid{grid-template-columns:1fr}header.top h1{font-size:22px}}
@media print{nav,.filters{display:none}body{background:#fff;font-size:11pt}.grid{grid-template-columns:1fr 1fr}section{break-before:page}section:first-of-type{break-before:auto}.shot{box-shadow:none}}
"""
JS = """
const bs=document.querySelectorAll('.filters button');
bs.forEach(b=>b.onclick=()=>{bs.forEach(x=>x.classList.remove('on'));b.classList.add('on');const f=b.dataset.f;
 document.querySelectorAll('.shot').forEach(s=>{s.hidden=!(f==='all'||(f==='key'&&s.dataset.key==='1')||(f==='todo'&&['trong','ai','chinh','quay-lai'].includes(s.dataset.st))||s.dataset.st===f)});
 document.querySelectorAll('.scene').forEach(sc=>{sc.hidden=!sc.querySelector('.shot:not([hidden])')})});
"""


def frame(ep_dir, rel, label, embed, panel=None):
    src = img_src(ep_dir, rel, embed)
    if panel in (0, 1, 2, 3) and src:
        return (f"<div class='frame' style=\"background-image:url('{src}');background-size:200% 200%;"
                f"background-position:{(panel % 2) * 100}% {(panel // 2) * 100}%\"><span class='lab'>{label}</span></div>")
    return f"<div class='frame'><span class='lab'>{label}</span><img loading='lazy' src='{src}' alt='{label}'></div>"


def shot_card(ep_dir, sh, embed):
    st, st_label = shot_state(ep_dir, sh)
    sb, real = sh.get("storyboard") or {}, sh.get("real") or {}
    has_plan = sb.get("level", "none") != "none" and sb.get("image")
    has_real = bool(real.get("image"))
    frames = []
    if has_plan:
        frames.append(frame(ep_dir, sb["image"], "DỰ KIẾN · AI" if sb.get("level") == "ai" else "DỰ KIẾN · SƠ ĐỒ", embed, sb.get("panel")))
    if has_real:
        frames.append(frame(ep_dir, real["image"], "THỰC TẾ", embed))
    if not frames:
        frames.append("<div class='frame'>Chưa có hình<br>xem gói prompt hoặc chụp thực tế</div>")
    h = [f"<article class='shot{' key' if sh.get('key') else ''}' id='{esc(sh['id'])}' data-st='{st}' data-key='{1 if sh.get('key') else 0}'>"
         f"<div class='frames{' two' if len(frames) == 2 else ''}'>{''.join(frames)}</div><div class='sb'>"
         f"<div class='row1'><span class='sid'>{esc(sh['id'])}</span><span class='badge b-{st}'>{st_label}</span>"
         + ("<span class='tag k'>Chủ chốt</span>" if sh.get("key") else "")
         + ("<span class='tag'>Micro Cut</span>" if sh.get("micro_cut") else "")
         + f"<span class='sec'>{esc(sh.get('seconds'))}s</span></div>"
         f"<div class='spec'>{esc(sh.get('size'))} · {esc(sh.get('focal_mm'))}mm · F{esc(sh.get('aperture'))} · {esc(sh.get('fps'))}fps · "
         f"{esc(sh.get('support'))}{'' if sh.get('movement', 'static') == 'static' else ' · ' + esc(sh.get('movement'))}</div>"
         f"<div class='action'>{esc(sh.get('action'))}</div>"]
    if sh.get("link"):
        h.append(f"<div class='link'>↳ {esc(sh['link'])}</div>")
    if sh.get("direction"):
        h.append(f"<div class='guide'><b>Hướng dẫn quay:</b> {esc(sh['direction'])}</div>")
    rows = [("Góc máy", sh.get("angle")), ("Bố cục", sh.get("composition")), ("Ánh sáng", sh.get("light")),
            ("Âm thanh", sh.get("sound_note")), ("Cắt sang", sh.get("cut")), ("Cặp match cut", sh.get("pair")),
            ("Kỹ thuật", ", ".join(sh.get("technique", []))), ("Ghi chú", sh.get("note"))]
    rows = [(k, v) for k, v in rows if v]
    if rows:
        h.append("<dl>" + "".join(f"<dt>{k}</dt><dd>{esc(v)}</dd>" for k, v in rows) + "</dl>")
    if has_real and (real.get("note") or real.get("verdict")):
        h.append(f"<div class='fb {esc(real.get('verdict') or '')}'><b>Nhận xét ảnh thực tế — {st_label}:</b> {esc(real.get('note'))}</div>")
    elif has_real:
        h.append("<div class='fb'>Ảnh thực tế đã nhận, chờ nhận xét (chạy /cap-nhat).</div>")
    h.append("</div></article>")
    return "".join(h)


def doc_section(ep_dir, anchor, title, filename):
    p = Path(ep_dir) / filename
    if not p.is_file():
        return ""
    return f"<section id='{anchor}'><h2>{title}</h2><div class='prose'>{md_to_html(p.read_text(encoding='utf-8'))}</div></section>"


def build(ep_dir, embed=False):
    ep_dir = Path(ep_dir)
    data = load_ep(ep_dir)
    status = read_json(ep_dir / "status.json", {}) or {}
    scenes, shots = data.get("scenes", []), all_shots(data)
    total = sum(sh.get("seconds", 0) for _, sh in shots)
    cov = coverage(ep_dir, data)
    rev, final = status.get("revision", 0), status.get("final", False)
    n = max(cov["total"], 1)
    pct = lambda k: f"{cov[k] / n * 100:.2f}%"

    h = [f"<!doctype html><html lang='vi'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<title>{esc(data.get('title'))} — Báo cáo</title><style>{CSS}</style>"
         f"<header class='top'><div class='wrap'><div class='kicker'>Nà Lạ Valley · {esc(data.get('episode'))} · hồ sơ tiền kỳ"
         f"<span class='rev{' final' if final else ''}'>{'BẢN FINAL' if final else f'Bản nháp v{rev}'}</span></div>"
         f"<h1>{esc(data.get('title'))}</h1><p class='logline'>{esc(data.get('logline'))}</p><div class='stats'>"
         f"<div class='stat'><b>{len(scenes)}</b><span>cảnh</span></div><div class='stat'><b>{len(shots)}</b><span>shot</span></div>"
         f"<div class='stat'><b>{total / 60:.1f}′</b><span>/ mục tiêu {data.get('target_seconds', 0) / 60:.0f}′</span></div>"
         f"<div class='stat'><b>{cov['plan']}/{cov['total']}</b><span>hình dự kiến</span></div>"
         f"<div class='stat'><b>{cov['real']}/{cov['total']}</b><span>ảnh thực tế</span></div>"
         f"<div class='stat'><b>{cov['dat']}/{cov['total']}</b><span>shot đạt</span></div></div></div></header>"
         "<nav><a href='#tien-do'>Tiến độ</a><a href='#kich-ban'>Kịch bản</a><a href='#storyboard'>Storyboard</a>"
         "<a href='#huong-dan'>Hướng dẫn quay</a><a href='#am-thanh'>Âm thanh</a><a href='#viec-tiep'>Việc tiếp theo</a>"
         "<a href='#lich-su'>Lịch sử</a></nav><main>"]

    # Tiến độ + dòng thời gian
    beats = []
    for sc in scenes:
        if sc.get("beat") not in beats:
            beats.append(sc.get("beat"))
    color = lambda sc: BEAT_COLORS[beats.index(sc.get("beat")) % len(BEAT_COLORS)]
    h.append("<section id='tien-do'><h2>Tiến độ & dòng thời gian</h2>"
             f"<div class='prog' title='Tiến độ shot'><span class='p-dat' style='width:{pct('dat')}'></span>"
             f"<span class='p-chinh' style='width:{pct('chinh')}'></span><span class='p-quay-lai' style='width:{pct('quay-lai')}'></span>"
             f"<span class='p-cho' style='width:{pct('cho')}'></span><span class='p-ai' style='width:{pct('ai')}'></span></div>"
             f"<div class='legend'><span><i style='background:var(--moss)'></i>Đạt {cov['dat']}</span>"
             f"<span><i style='background:var(--amber)'></i>Cần chỉnh {cov['chinh']}</span>"
             f"<span><i style='background:var(--red)'></i>Quay lại {cov['quay-lai']}</span>"
             f"<span><i style='background:#7b8794'></i>Chờ nhận xét {cov['cho']}</span>"
             f"<span><i style='background:#b9c3d6'></i>Mới có hình dự kiến {cov['ai']}</span>"
             f"<span><i style='background:#e6dfd0'></i>Chưa có hình {cov['trong']}</span></div>"
             "<h3>Dòng thời gian dựng</h3><div class='bar'>")
    for sc in scenes:
        s = sum(x.get("seconds", 0) for x in sc.get("shots", []))
        h.append(f"<a href='#{esc(sc['id'])}' style='flex:{max(s, 1)};background:{color(sc)}' "
                 f"title='{esc(sc['id'])} {esc(sc.get('title'))} · {s}s'>{esc(sc['id'])}</a>")
    h.append("</div><div class='legend'>" + "".join(
        f"<span><i style='background:{BEAT_COLORS[k % len(BEAT_COLORS)]}'></i>{esc(b or 'Chưa gán beat')}</span>"
        for k, b in enumerate(beats)) + "</div></section>")

    # Kịch bản
    script = doc_section(ep_dir, "kich-ban", "Kịch bản", "03-kich-ban.md")
    h.append(script or "<section id='kich-ban'><h2>Kịch bản</h2><p class='empty'>Chưa có 03-kich-ban.md — chạy /tap-moi.</p></section>")

    # Storyboard
    h.append("<section id='storyboard'><h2>Storyboard</h2><div class='filters'>"
             "<button class='on' data-f='all'>Tất cả</button><button data-f='key'>Chủ chốt</button>"
             "<button data-f='todo'>Còn việc</button><button data-f='trong'>Chưa có hình</button>"
             "<button data-f='chinh'>Cần chỉnh</button><button data-f='quay-lai'>Quay lại</button><button data-f='dat'>Đạt</button></div>")
    for sc in scenes:
        snd = sc.get("sound") or {}
        h.append(f"<div class='scene' id='{esc(sc['id'])}'><header><h3><span style='color:{color(sc)}'>■</span> {esc(sc['id'])} · {esc(sc.get('title'))}</h3>"
                 f"<span class='meta'>{esc(sc.get('location'))} · {esc(sc.get('story_time'))} · quay {esc(sc.get('clock_slot'))} · "
                 f"{sum(x.get('seconds', 0) for x in sc.get('shots', []))}s</span></header>"
                 f"<div class='sound'><b>Âm thanh:</b> nền — {esc(snd.get('ambience'))} · thao tác — {esc(snd.get('foley'))}"
                 + (f" · điểm nhấn — {esc(snd['accent'])}" if snd.get("accent") else "")
                 + (f" · nhạc — {esc(snd['bgm'])}" if snd.get("bgm") else " · không nhạc") + "</div><div class='grid'>"
                 + "".join(shot_card(ep_dir, sh, embed) for sh in sc.get("shots", [])) + "</div></div>")
    h.append("</section>")

    # Hướng dẫn quay
    h.append("<section id='huong-dan'><h2>Hướng dẫn quay</h2><h3>Lịch quay theo ánh sáng</h3>"
             "<table><tr><th>Khung giờ</th><th>Điều kiện</th><th>Cảnh</th><th>Shot</th><th>Còn phải quay</th></tr>")
    for slot, note in RULES["clock_slots"].items():
        scs = [s for s in scenes if s.get("clock_slot") == slot]
        if scs:
            left = [sh["id"] for s in scs for sh in s.get("shots", []) if shot_state(ep_dir, sh)[0] != "dat"]
            h.append(f"<tr><td><b>{esc(slot)}</b></td><td>{esc(note)}</td><td>"
                     + ", ".join(f"<a href='#{esc(s['id'])}'>{esc(s['id'])}</a> {esc(s.get('title'))}" for s in scs)
                     + f"</td><td>{sum(len(s.get('shots', [])) for s in scs)}</td><td>{len(left)}</td></tr>")
    h.append("</table>")
    props = sorted({p for _, sh in shots for p in sh.get("props", [])})
    if props:
        h.append("<h3>Đạo cụ cần chuẩn bị</h3><ul class='check'>" + "".join(f"<li>{esc(p)}</li>" for p in props) + "</ul>")
    notes = Path(ep_dir) / "04-ghi-chu-quay.md"
    if notes.is_file():
        h.append(f"<div class='prose'>{md_to_html(notes.read_text(encoding='utf-8'))}</div>")
    h.append("</section>")

    h.append(doc_section(ep_dir, "am-thanh", "Âm thanh", "05-am-thanh.md") or
             "<section id='am-thanh'><h2>Âm thanh</h2><h3>Danh sách thu foley</h3><ul class='check'>"
             + "".join(f"<li>{esc(sc['id'])}: {esc((sc.get('sound') or {}).get('foley'))}</li>" for sc in scenes) + "</ul></section>")

    # Việc tiếp theo
    by = lambda code: [sh for _, sh in shots if shot_state(ep_dir, sh)[0] == code]
    link = lambda sh: f"<a href='#{esc(sh['id'])}'>{esc(sh['id'])}</a>"
    h.append("<section id='viec-tiep'><h2>Việc tiếp theo</h2><ul class='todo'>")
    for code, label in (("quay-lai", "Quay lại"), ("chinh", "Chỉnh rồi chụp lại")):
        for sh in by(code):
            h.append(f"<li><b>{label} {link(sh)}:</b> {esc((sh.get('real') or {}).get('note'))}</li>")
    wait = by("cho")
    if wait:
        h.append(f"<li><b>Chờ AI nhận xét ({len(wait)}):</b> {', '.join(link(s) for s in wait)} — chạy <code>/cap-nhat</code></li>")
    need = [sh for sh in by("trong") + by("ai")]
    if need:
        keys = [s for s in need if s.get("key")]
        h.append(f"<li><b>Chưa có ảnh thực tế ({len(need)} shot, {len(keys)} chủ chốt):</b> "
                 + ", ".join(link(s) for s in (keys or need)[:40]) + ("…" if len(keys or need) > 40 else "")
                 + " — chụp rồi lưu vào <code>input/thuc-te/&lt;ID shot&gt;.jpg</code></li>")
    q = Path(ep_dir) / "cau-hoi.md"
    if q.is_file():
        h.append("</ul><h3>Câu hỏi cần chủ dự án trả lời</h3><div class='prose'>" + md_to_html(q.read_text(encoding="utf-8")) + "</div><ul>")
    if not (by("quay-lai") or by("chinh") or wait or need):
        h.append("<li>Mọi shot đã có ảnh thực tế đạt yêu cầu.</li>")
    h.append("</ul></section>")

    h.append("<section id='lich-su'><h2>Lịch sử phiên bản</h2>")
    revs = status.get("revisions") or []
    h.append("<table><tr><th>Bản</th><th>Thời điểm</th><th>Thay đổi</th></tr>" + "".join(
        f"<tr><td>v{esc(r.get('n'))}</td><td>{esc(r.get('at'))}</td><td>{esc(r.get('note'))}</td></tr>" for r in reversed(revs))
        + "</table>" if revs else "<p class='empty'>Chưa có phiên bản nào được ghi.</p>")
    h.append(f"</section></main><footer>Dựng lúc {now()} từ shots.json. Hình gắn nhãn “DỰ KIẾN” do AI tạo hoặc là sơ đồ, "
             f"không phải ảnh hiện trường.</footer><script>{JS}</script></html>")
    (ep_dir / "bao-cao.html").write_text("".join(h), encoding="utf-8")

    cols = ["id", "key", "size", "focal_mm", "aperture", "fps", "support", "movement", "angle", "action", "direction", "seconds", "micro_cut"]
    with open(ep_dir / "shotlist.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["scene", "clock_slot"] + cols + ["trang_thai"])
        for sc, sh in shots:
            w.writerow([sc.get("id"), sc.get("clock_slot")] + [sh.get(c, "") for c in cols] + [shot_state(ep_dir, sh)[1]])
    return len(shots)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    n = build(args[0], "--embed" in sys.argv)
    print(f"Đã dựng bao-cao.html và shotlist.csv ({n} shot) trong {args[0]}")
