#!/usr/bin/env python3
"""Quét ảnh chủ dự án vừa thả vào một tập và gắn vào đúng shot.

Dùng:  python3 scripts/sync_inputs.py episodes/ep01

- input/thuc-te/  : ảnh chụp thực tế từng shot. Tên file chứa ID shot, ví dụ S03-SH02.jpg,
                    S03-SH02_lan2.jpg (bản tên xếp sau cùng là bản chính, các bản khác là phương án).
- storyboard/     : ảnh dự kiến do AI tạo, đặt tên theo ID shot, ví dụ S03-SH02.png.
Ảnh thực tế mới hoặc đã thay đổi được đặt verdict=null để Quay phim nhận xét lại.
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nala import IMG_EXT, SHOT_RE, all_shots, load_ep, read_json, write_json


def sha(p):
    return hashlib.sha1(p.read_bytes()).hexdigest()[:12]


def scan(folder):
    found, unmatched = {}, []
    if folder.is_dir():
        for p in sorted(folder.rglob("*")):
            if p.is_file() and p.suffix.lower() in IMG_EXT:
                m = SHOT_RE.search(p.name)
                (found.setdefault(m.group(1).upper(), []).append(p) if m else unmatched.append(p))
    return found, unmatched


def sync(ep_dir):
    ep_dir = Path(ep_dir)
    data = load_ep(ep_dir)
    rel = lambda p: p.relative_to(ep_dir).as_posix()
    real, real_un = scan(ep_dir / "input" / "thuc-te")
    board, board_un = scan(ep_dir / "storyboard")
    ids = {sh["id"] for _, sh in all_shots(data)}
    new_real, new_board, gone = [], [], []

    for _, sh in all_shots(data):
        i = sh["id"]
        cur = sh.get("real") or {}
        if i in real:
            main, alts = real[i][-1], [rel(p) for p in real[i][:-1]]
            h = sha(main)
            if cur.get("sha") != h or cur.get("image") != rel(main):
                sh["real"] = {"image": rel(main), "sha": h, "verdict": None, "note": "", "alts": alts}
                new_real.append(i)
            else:
                cur["alts"] = alts
        elif cur.get("image"):
            sh["real"] = {"image": None, "sha": None, "verdict": None, "note": "", "alts": []}
            gone.append(i)
        sb = sh.setdefault("storyboard", {"level": "none", "image": None, "panel": None})
        if i in board:
            p = rel(board[i][-1])
            if sb.get("image") != p or sb.get("level") == "none":
                sb.update(level="ai" if board[i][-1].suffix.lower() != ".svg" else "svg", image=p, panel=None)
                new_board.append(i)
        elif sb.get("image") and not (ep_dir / sb["image"]).is_file():
            sb.update(level="none", image=None, panel=None)
            gone.append(i + " (hình dự kiến)")

    write_json(ep_dir / "shots.json", data)

    vb = read_json(ep_dir / "visual-bible.json", {}) or {}
    used = {r for k in ("subjects", "locations", "props") for it in (vb.get(k) or {}).values() for r in it.get("refs", [])}
    unused = [rel(p) for sub in ("boi-canh", "dao-cu", "nhan-vat")
              for p in sorted((ep_dir / "input" / sub).glob("*")) if p.suffix.lower() in IMG_EXT and rel(p) not in used]

    print(f"Ảnh thực tế mới/đổi ({len(new_real)}): {', '.join(new_real) or '—'}")
    print(f"Hình dự kiến mới ({len(new_board)}): {', '.join(new_board) or '—'}")
    if gone:
        print(f"File đã bị gỡ: {', '.join(gone)}")
    orphan = sorted(set(list(real) + list(board)) - ids)
    if orphan:
        print(f"ID trong tên file không có trong shots.json: {', '.join(orphan)}")
    for p in real_un + board_un:
        print(f"CHƯA GẮN ĐƯỢC (tên file không có ID shot): {rel(p)}")
    if unused:
        print(f"Ảnh đầu vào chưa đưa vào visual-bible.json ({len(unused)}): {', '.join(unused)}")
    return new_real, new_board


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sync(sys.argv[1])
