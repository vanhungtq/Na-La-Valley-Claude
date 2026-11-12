#!/usr/bin/env python3
"""Ghi tiến trình của agents và dựng lại dashboard.html ở gốc repo.

Dùng:
  python3 scripts/progress.py episodes/ep01 agent <agent> <working|done|blocked|idle> "việc đang làm"
  python3 scripts/progress.py episodes/ep01 stage <stage> <todo|working|review|done> ["ghi chú"]
  python3 scripts/progress.py episodes/ep01 gate "câu hỏi đang chờ chủ dự án"      (gate "" để xóa)
  python3 scripts/progress.py episodes/ep01 rev "tóm tắt thay đổi của bản mới"     (tăng số phiên bản)
  python3 scripts/progress.py episodes/ep01 final <on|off>
  python3 scripts/progress.py build                                                (chỉ dựng lại dashboard)

Xem trực tiếp:  python3 -m http.server 8765   rồi mở http://localhost:8765/dashboard.html (tự làm mới mỗi 5 giây).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nala import AGENTS, ROOT, STAGES, coverage, esc, load_ep, now, read_json, write_json

A_STATES = {"working": "Đang làm", "done": "Xong", "blocked": "Bị chặn", "idle": "Chờ việc"}
S_STATES = {"todo": "Chưa làm", "working": "Đang làm", "review": "Chờ duyệt", "done": "Xong"}


def load_status(ep_dir):
    st = read_json(Path(ep_dir) / "status.json", {}) or {}
    st.setdefault("revision", 0)
    st.setdefault("final", False)
    st.setdefault("stages", {})
    st.setdefault("agents", {})
    st.setdefault("gate", "")
    st.setdefault("log", [])
    st.setdefault("revisions", [])
    return st


def log(st, who, state, msg):
    st["log"].append({"at": now(), "who": who, "state": state, "msg": msg})
    st["log"] = st["log"][-200:]


def update(ep_dir, cmd, args):
    st = load_status(ep_dir)
    if cmd == "agent":
        name, state, msg = args[0], args[1], (args[2] if len(args) > 2 else "")
        if name not in AGENTS or state not in A_STATES:
            sys.exit(f"agent phải thuộc {list(AGENTS)}, trạng thái thuộc {list(A_STATES)}")
        st["agents"][name] = {"state": state, "msg": msg, "at": now()}
        log(st, name, state, msg)
    elif cmd == "stage":
        name, state, msg = args[0], args[1], (args[2] if len(args) > 2 else "")
        if name not in dict(STAGES) or state not in S_STATES:
            sys.exit(f"stage phải thuộc {[s for s, _ in STAGES]}, trạng thái thuộc {list(S_STATES)}")
        st["stages"][name] = state
        log(st, "showrunner", "stage", f"{dict(STAGES)[name]} → {S_STATES[state]}" + (f": {msg}" if msg else ""))
    elif cmd == "gate":
        st["gate"] = args[0] if args else ""
        if st["gate"]:
            log(st, "showrunner", "gate", st["gate"])
    elif cmd == "rev":
        st["revision"] += 1
        st["revisions"].append({"n": st["revision"], "at": now(), "note": args[0] if args else ""})
        log(st, "showrunner", "rev", f"Bản v{st['revision']}: {args[0] if args else ''}")
    elif cmd == "final":
        st["final"] = args[0] == "on"
        st["stages"]["final"] = "done" if st["final"] else "todo"
        log(st, "showrunner", "final", "Chốt bản FINAL" if st["final"] else "Mở lại bản nháp")
    else:
        sys.exit(__doc__)
    write_json(Path(ep_dir) / "status.json", st)


CSS = """
:root{--bg:#f6f2ea;--card:#fff;--ink:#23262b;--mute:#6b6f76;--line:#ddd5c6;--soft:#f1ebdf;--indigo:#2c3e5d;--clay:#b4532f;--moss:#56683f;--amber:#b07a14;--red:#a83232}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{background:var(--indigo);color:#fff;padding:20px 22px}header h1{margin:0;font-size:22px}header p{margin:3px 0 0;opacity:.8;font-size:13px}
main{max-width:1240px;margin:0 auto;padding:18px 16px 50px}
.ep{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:22px}
.ep h2{margin:0;font-size:18px}.ep .sub{color:var(--mute);font-size:13px;margin:2px 0 12px}
.pill{display:inline-block;border-radius:99px;padding:2px 11px;font-size:12px;font-weight:600;color:#fff;background:var(--clay);margin-left:8px}.pill.final{background:var(--moss)}
.gate{background:#fbf3df;border:1px solid #e3c98a;border-left:5px solid var(--amber);border-radius:8px;padding:10px 14px;margin:0 0 14px}
.pipe{display:flex;gap:4px;overflow-x:auto;padding-bottom:4px}
.st{flex:1 0 108px;border-radius:8px;padding:8px 10px;background:#ebe5d8;color:#7a766c;font-size:12.5px;line-height:1.3;position:relative}
.st b{display:block;font-size:11px;opacity:.75;font-weight:600}
.st.working{background:var(--indigo);color:#fff}.st.review{background:var(--amber);color:#fff}.st.done{background:var(--moss);color:#fff}
.st.working:after{content:"";position:absolute;right:8px;top:9px;width:8px;height:8px;border-radius:50%;background:#fff;animation:p 1.2s infinite}
@keyframes p{50%{opacity:.2}}
h3{font-size:14px;margin:18px 0 8px;color:var(--mute);text-transform:uppercase;letter-spacing:.08em}
.agents{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.ag{border:1px solid var(--line);border-radius:10px;padding:10px 12px;border-left:5px solid #c9c2b3;background:#fdfbf7}
.ag.working{border-left-color:var(--indigo);background:#eef2f7}.ag.done{border-left-color:var(--moss)}.ag.blocked{border-left-color:var(--red);background:#f9e8e6}
.ag .n{font-weight:700}.ag .s{font-size:12px;color:var(--mute)}.ag .m{font-size:13px;margin-top:4px;min-height:1.4em}
.prog{display:flex;height:16px;border-radius:99px;overflow:hidden;background:#e6dfd0}
.prog span{display:block}.p-dat{background:var(--moss)}.p-chinh{background:var(--amber)}.p-quay-lai{background:var(--red)}.p-cho{background:#7b8794}.p-ai{background:#b9c3d6}
.nums{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:var(--mute);margin-top:6px}
.links a{display:inline-block;margin:10px 10px 0 0;background:var(--indigo);color:#fff;text-decoration:none;border-radius:8px;padding:7px 14px;font-size:13.5px}
.links a.alt{background:#fff;color:var(--indigo);border:1px solid var(--indigo)}
table{border-collapse:collapse;width:100%;font-size:13px}td{border-top:1px solid var(--line);padding:5px 8px;vertical-align:top}
td.t{white-space:nowrap;color:var(--mute);font-variant-numeric:tabular-nums}td.w{white-space:nowrap;font-weight:600}
.lib{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}
.lib div{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}.lib b{font-size:24px;display:block}
.empty{color:var(--mute)}
"""


def library_stats():
    k = ROOT / "knowledge"
    vids = [d for d in (k / "video-mau").glob("*") if d.is_dir() and not d.name.startswith("_")]
    shots = sum(len((read_json(d / "reference.json", {}) or {}).get("shots", [])) for d in vids)
    count = lambda sub, pat: len([p for p in (k / sub).glob(pat) if p.name not in ("README.md", "_TEMPLATE.md")]) if (k / sub).is_dir() else 0
    inbox = len([p for p in (k / "inbox").rglob("*") if p.is_file() and p.name != "README.md"]) if (k / "inbox").is_dir() else 0
    return [("Video mẫu đã phân tích", len(vids)), ("Cú máy mẫu có ảnh", shots), ("Thẻ kỹ thuật", count("ky-thuat", "KT-*.md")),
            ("Tài liệu kiến thức", count("kien-thuc", "*.md") + count("chu-de", "*.md")),
            ("Sổ tay agent", count("so-tay", "*.md")), ("Đang chờ trong inbox", inbox)]


def build_dashboard():
    h = [f"<!doctype html><html lang='vi'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<meta http-equiv='refresh' content='5'><title>Nà Lạ Valley · Tiến trình</title><style>{CSS}</style>"
         f"<header><h1>Nà Lạ Valley · Bảng tiến trình</h1><p>Cập nhật {now()} · trang tự làm mới mỗi 5 giây khi mở qua máy chủ cục bộ</p></header><main>"]
    eps = sorted(p.parent for p in (ROOT / "episodes").glob("*/shots.json") if not p.parent.name.startswith("_"))
    if not eps:
        h.append("<p class='empty'>Chưa có tập nào. Chạy /tap-moi.</p>")
    for ep in eps:
        data, st = load_ep(ep), load_status(ep)
        cov = coverage(ep, data)
        n = max(cov["total"], 1)
        pct = lambda k: f"{cov[k] / n * 100:.2f}%"
        h.append(f"<section class='ep'><h2>{esc(data.get('title') or ep.name)}"
                 f"<span class='pill{' final' if st['final'] else ''}'>{'FINAL' if st['final'] else 'Bản nháp v' + str(st['revision'])}</span></h2>"
                 f"<div class='sub'>{esc(ep.name)} · {len(data.get('scenes', []))} cảnh · {cov['total']} shot</div>")
        if st["gate"]:
            h.append(f"<div class='gate'><b>Đang chờ bạn quyết định:</b> {esc(st['gate'])}</div>")
        h.append("<div class='pipe'>" + "".join(
            f"<div class='st {esc(st['stages'].get(sid, 'todo'))}'><b>{k}. {S_STATES[st['stages'].get(sid, 'todo')]}</b>{esc(label)}</div>"
            for k, (sid, label) in enumerate(STAGES, 1)) + "</div>")
        h.append("<h3>Agents</h3><div class='agents'>")
        for aid, name in AGENTS.items():
            a = st["agents"].get(aid, {"state": "idle", "msg": "", "at": ""})
            h.append(f"<div class='ag {esc(a['state'])}'><div class='n'>{esc(name)}</div>"
                     f"<div class='s'>{A_STATES.get(a['state'], a['state'])}{' · ' + esc(a['at']) if a.get('at') else ''}</div>"
                     f"<div class='m'>{esc(a.get('msg'))}</div></div>")
        h.append("</div><h3>Storyboard & ảnh thực tế</h3>"
                 f"<div class='prog'><span class='p-dat' style='width:{pct('dat')}'></span><span class='p-chinh' style='width:{pct('chinh')}'></span>"
                 f"<span class='p-quay-lai' style='width:{pct('quay-lai')}'></span><span class='p-cho' style='width:{pct('cho')}'></span>"
                 f"<span class='p-ai' style='width:{pct('ai')}'></span></div>"
                 f"<div class='nums'><span>Đạt {cov['dat']}</span><span>Cần chỉnh {cov['chinh']}</span><span>Quay lại {cov['quay-lai']}</span>"
                 f"<span>Chờ nhận xét {cov['cho']}</span><span>Mới có hình dự kiến {cov['ai']}</span><span>Chưa có hình {cov['trong']}</span></div>"
                 "<div class='links'>"
                 + (f"<a href='episodes/{ep.name}/bao-cao.html'>Mở báo cáo</a>" if (ep / "bao-cao.html").is_file() else "")
                 + (f"<a class='alt' href='episodes/{ep.name}/goi-prompt.html'>Gói prompt tạo ảnh</a>" if (ep / "goi-prompt.html").is_file() else "")
                 + "</div><h3>Nhật ký</h3>")
        logs = st["log"][-14:][::-1]
        h.append("<table>" + "".join(
            f"<tr><td class='t'>{esc(l['at'])}</td><td class='w'>{esc(AGENTS.get(l['who'], l['who']))}</td><td>{esc(l['msg'])}</td></tr>"
            for l in logs) + "</table>" if logs else "<p class='empty'>Chưa có hoạt động.</p>")
        h.append("</section>")
    h.append("<h3>Thư viện kiến thức</h3><div class='lib'>" + "".join(
        f"<div><b>{v}</b>{esc(k)}</div>" for k, v in library_stats()) + "</div></main></html>")
    (ROOT / "dashboard.html").write_text("".join(h), encoding="utf-8")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["build"]:
        pass
    elif len(a) >= 2:
        update(a[0], a[1], a[2:])
    else:
        sys.exit(__doc__)
    build_dashboard()
    print("Đã cập nhật dashboard.html")
