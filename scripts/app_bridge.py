#!/usr/bin/env python3
"""Cầu nối giữa app Nà Lạ Studio (dữ liệu trên Claude) và thư mục làm việc cục bộ của agents.

Script này KHÔNG gọi mạng. Claude đọc/ghi dữ liệu app bằng công cụ ArtifactData và Artifact;
script chỉ chuyển đổi giữa các file JSON đã tải về và cấu trúc file mà agents làm việc.

  pull <dump> <ep>            dựng episodes/<ep>/ từ dữ liệu đã tải (ArtifactData ... out_dir=<dump>)
  push <ep> <out> [k=v ...]   xuất tài liệu để ghi ngược lên app, in mảng `writes` cho ArtifactData batch
  pull-lib <dump>             dựng knowledge/video-mau/ và knowledge/kien-thuc/ từ thư viện trong app
  push-lib <out> [k=v ...]    xuất phân tích, thẻ kỹ thuật, sổ tay để ghi lên app

<dump>/assets/ chứa các tệp ảnh/clip Claude đã tải bằng Artifact read (tên = id + đuôi tệp).
k=v là phiên bản hiện tại của tài liệu đã có trên app, ví dụ:  episodes/ep01=4  episodes/ep01/scenes/S01=2
"""
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nala import ROOT, VERDICTS, all_shots, now, read_json, write_json

DOCS = {"dinh-huong": "01-dinh-huong.md", "concept": "02-concept.md", "kich-ban": "03-kich-ban.md",
        "ghi-chu-quay": "04-ghi-chu-quay.md", "am-thanh": "05-am-thanh.md", "youtube": "07-youtube.md",
        "cau-hoi": "cau-hoi.md", "review": "review-truoc.md"}
LOCAL_ONLY = ("real", "storyboard")


def slug(s, n=40):
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", str(s)).strip("-")
    return s[:n] or "tep"


def dump_docs(dump, coll):
    d = Path(dump) / coll
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json"))} if d.is_dir() else {}


def place(dump, asset, target_stem, missing):
    """Chép tệp asset đã tải vào đúng chỗ; trả về đường dẫn (hoặc None nếu chưa tải)."""
    if not asset:
        return None
    hit = sorted((Path(dump) / "assets").glob(asset + ".*"))
    if not hit:
        missing.append(asset)
        return None
    dst = Path(str(target_stem) + hit[0].suffix.lower())
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.is_file() or dst.stat().st_size != hit[0].stat().st_size:
        shutil.copyfile(hit[0], dst)
    return dst


def sha(p):
    return hashlib.sha1(p.read_bytes()).hexdigest()[:12]


def pull(dump, ep):
    ep_dir = ROOT / "episodes" / ep
    if not ep_dir.is_dir():
        shutil.copytree(ROOT / "episodes" / "_template", ep_dir)
    brief = dump_docs(dump, "briefs").get(ep)
    if not brief:
        sys.exit(f"Không thấy briefs/{ep} trong {dump}. Hãy tải collection 'briefs' trước.")
    status = dump_docs(dump, "episodes").get(ep, {})
    b = f"episodes/{ep}/"
    scenes, docs = dump_docs(dump, b + "scenes"), dump_docs(dump, b + "docs")
    media, inputs = dump_docs(dump, b + "media"), dump_docs(dump, b + "inputs")
    jobs = [j for j in dump_docs(dump, "jobs").values() if j.get("ep") in (ep, "") and j.get("state") in ("queued", "running")]
    missing, manifest = [], {}
    rel = lambda p: p.relative_to(ep_dir).as_posix()

    idea = [f"# Ý tưởng thô — {brief.get('title', ep)}", "", "> Nguồn: chủ dự án viết trong app Nà Lạ Studio [CHỦ DỰ ÁN].", "",
            f"- **Thời lượng mục tiêu:** {brief.get('minutes', 20)} phút", "", brief.get("idea", "").strip() or "*(chưa viết)*", ""]
    notes = [j for j in sorted(jobs, key=lambda j: str(j.get("at"))) if j.get("note")]
    if notes:
        idea += ["## Yêu cầu và câu trả lời mới của chủ dự án", ""] + [f"- ({j.get('at')}, {j.get('type')}) {j['note']}" for j in notes] + [""]
    (ep_dir / "input").mkdir(exist_ok=True)
    (ep_dir / "input" / "y-tuong.md").write_text("\n".join(idea), encoding="utf-8")

    for kind in ("boi-canh", "dao-cu", "nhan-vat"):
        d = ep_dir / "input" / kind
        d.mkdir(parents=True, exist_ok=True)
        keep = set()
        for it in (x for x in inputs.values() if x.get("kind") == kind):
            p = place(dump, it.get("asset"), d / f"{slug(Path(it.get('name', 'anh')).stem)}__{it['asset'][:8]}", missing)
            if p:
                manifest[rel(p)] = it["asset"]
                keep.add(p.name)
        for old in d.iterdir():  # ảnh chủ dự án đã xóa trong app
            if old.name not in keep and old.name != ".gitkeep":
                old.unlink()

    if scenes:
        data = read_json(ep_dir / "shots.json", {}) or {}
        data.update(episode=ep, title=status.get("title") or brief.get("title", ep), logline=status.get("logline", ""),
                    target_seconds=status.get("target_seconds") or int(brief.get("minutes", 20)) * 60)
        data["scenes"] = [scenes[k] for k in sorted(scenes, key=lambda k: (scenes[k].get("order", 0), k))]
    else:
        data = read_json(ep_dir / "shots.json")
        data.update(episode=ep, title=brief.get("title", ep), target_seconds=int(brief.get("minutes", 20)) * 60)
        if (ep_dir / "shots.json").read_text(encoding="utf-8") == (ROOT / "episodes/_template/shots.json").read_text(encoding="utf-8"):
            data["scenes"] = []  # tập mới: bỏ cảnh mẫu của template
    review = []
    for sc, sh in all_shots(data):
        m = media.get(sh["id"], {})
        for junk in ("prompt", "prompt_refs", "order"):
            sh.pop(junk, None)
        rp = place(dump, m.get("real"), ep_dir / "input" / "thuc-te" / sh["id"], missing)
        pp = place(dump, m.get("plan"), ep_dir / "storyboard" / sh["id"], missing)
        if rp:
            manifest[rel(rp)] = m["real"]
            same = sh.get("real_asset") == m["real"] and sh.get("verdict") in VERDICTS
            sh["real"] = {"image": rel(rp), "sha": sha(rp), "verdict": sh.get("verdict") if same else None,
                          "note": sh.get("real_note", "") if same else "", "alts": []}
            if not same:
                review.append(sh["id"])
        else:
            sh["real"] = {"image": None, "sha": None, "verdict": None, "note": "", "alts": []}
        if pp:
            manifest[rel(pp)] = m["plan"]
        sh["storyboard"] = {"level": "ai" if pp else "none", "image": rel(pp) if pp else None, "panel": None}
        for k in ("real_asset", "verdict", "real_note"):
            sh.pop(k, None)
    for sc in data.get("scenes", []):
        sc.pop("order", None)
    for sub in ("input/thuc-te", "storyboard"):  # ảnh chủ dự án đã gỡ hoặc thay trong app
        for old in (ep_dir / sub).glob("*"):
            if old.name != ".gitkeep" and rel(old) not in manifest:
                old.unlink()
    write_json(ep_dir / "shots.json", data)

    for key, fn in DOCS.items():
        if key in docs and docs[key].get("md"):
            (ep_dir / fn).write_text(docs[key]["md"], encoding="utf-8")
    if "visual-bible" in docs and docs["visual-bible"].get("data"):
        write_json(ep_dir / "visual-bible.json", docs["visual-bible"]["data"])
    st = {k: status.get(k, d) for k, d in (("revision", 0), ("final", False), ("stages", {}), ("agents", {}),
                                           ("gate", ""), ("log", []), ("revisions", []))}
    write_json(ep_dir / "status.json", st)
    write_json(ep_dir / ".assets.json", manifest)

    print(f"Đã dựng {ep_dir.relative_to(ROOT)}: {len(data.get('scenes', []))} cảnh, {len(inputs)} ảnh đầu vào, "
          f"{sum(1 for m in media.values() if m.get('real'))} ảnh thực tế, {sum(1 for m in media.values() if m.get('plan'))} hình dự kiến.")
    if notes:
        print(f"Có {len(notes)} ghi chú/câu trả lời mới của chủ dự án trong input/y-tuong.md.")
    if review:
        print(f"ẢNH THỰC TẾ CẦN NHẬN XÉT ({len(review)}): {', '.join(review)}")
    if missing:
        print(f"CHƯA TẢI {len(set(missing))} tệp — dùng Artifact read (path=<id>, out_dir={dump}/assets) rồi chạy lại pull:")
        print(" ".join(sorted(set(missing))))


def emit(out, coll, doc_id, data, versions, writes):
    p = Path(out) / coll / f"{doc_id}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    write_json(p, data)
    w = {"op": "set", "collection": coll, "doc_id": doc_id, "file_path": str(p)}
    if f"{coll}/{doc_id}" in versions:
        w["if_version"] = versions[f"{coll}/{doc_id}"]
    writes.append(w)


def finish(writes, versions, known_prefixes):
    for key, v in versions.items():  # tài liệu có trên app nhưng không còn ở cục bộ → xóa
        coll, _, doc = key.rpartition("/")
        if any(coll == p for p in known_prefixes) and not any(w["collection"] == coll and w["doc_id"] == doc for w in writes):
            writes.append({"op": "delete", "collection": coll, "doc_id": doc, "if_version": v})
    for i in range(0, len(writes), 50):
        print(f"--- ArtifactData action=batch, writes (lô {i // 50 + 1}) ---")
        print(json.dumps(writes[i:i + 50], ensure_ascii=False))
    new = [w for w in writes if "if_version" not in w]
    print(f"\n{len(writes)} thao tác; {len(new)} không có if_version (chỉ đúng nếu tài liệu đó CHƯA có trên app).")


def parse_versions(args):
    out = {}
    for a in args:
        k, _, v = a.partition("=")
        if not v.isdigit():
            sys.exit(f"Phiên bản phải dạng đường-dẫn=số, nhận được: {a}")
        out[k] = int(v)
    return out


def push(ep, out, versions):
    from build_prompt_pack import collect
    ep_dir = ROOT / "episodes" / ep
    manifest = read_json(ep_dir / ".assets.json", {}) or {}
    data, _vb, items = collect(ep_dir, include_all=True)
    prompts = {it["sh"]["id"]: it for it in items}
    status = read_json(ep_dir / "status.json", {}) or {}
    writes, b = [], f"episodes/{ep}/"
    for n, sc in enumerate(data.get("scenes", [])):
        doc = {k: v for k, v in sc.items() if k != "shots"}
        doc["order"] = n
        doc["shots"] = []
        for sh in sc.get("shots", []):
            s = {k: v for k, v in sh.items() if k not in LOCAL_ONLY}
            real = sh.get("real") or {}
            if real.get("image") and real.get("verdict") in VERDICTS:
                s.update(real_asset=manifest.get(real["image"]), verdict=real["verdict"], real_note=real.get("note", ""))
            it = prompts.get(sh["id"])
            if it and (sh.get("frame_en") or sh.get("action")):
                s["prompt"] = it["prompt"]
                s["prompt_refs"] = [{"asset": manifest[r], "label": vn} for r, vn, _en in it["refs"] if r in manifest]
            doc["shots"].append(s)
        emit(out, b + "scenes", sc["id"], doc, versions, writes)
    for key, fn in DOCS.items():
        p = ep_dir / fn
        if key == "review":  # gộp mọi review-*.md, bản mới nhất lên đầu
            parts = sorted(ep_dir.glob("review-*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
            text = "\n\n---\n\n".join(x.read_text(encoding="utf-8") for x in parts)
        else:
            text = p.read_text(encoding="utf-8") if p.is_file() else ""
        if text.strip():
            emit(out, b + "docs", key, {"md": text, "at": now()}, versions, writes)
    vb = read_json(ep_dir / "visual-bible.json")
    if vb:
        emit(out, b + "docs", "visual-bible", {"data": vb, "at": now()}, versions, writes)
    epdoc = {"title": data.get("title", ep), "logline": data.get("logline", ""), "target_seconds": data.get("target_seconds"),
             **{k: status.get(k) for k in ("revision", "final", "stages", "agents", "gate", "revisions")},
             "log": (status.get("log") or [])[-60:], "updatedAt": now()}
    emit(out, "episodes", ep, epdoc, versions, writes)
    finish(writes, versions, {b + "scenes", b + "docs"})


def pull_lib(dump):
    lib, decisions = dump_docs(dump, "library"), dump_docs(dump, "decisions")
    done = set(dump_docs(dump, "analysis"))
    missing, todo = [], []
    for lid, it in lib.items():
        base = ROOT / "knowledge" / ("video-mau" if it.get("kind") == "video-mau" else "kien-thuc") / f"{slug(it.get('title', lid))}__{lid[:8]}"
        base.mkdir(parents=True, exist_ok=True)
        frames = []
        for n, f in enumerate(it.get("frames", []), 1):
            p = place(dump, f.get("asset"), base / "frames" / f"{n:03d}", missing)
            frames.append({"n": n, "image": p.relative_to(base).as_posix() if p else None, "asset": f.get("asset"),
                           "clip": f.get("clip"), "giay_trong_clip": f.get("t"), "ghi_chu_chu_du_an": f.get("note", "")})
        for c in it.get("clips", []):
            place(dump, c.get("asset"), base / "clips" / slug(Path(c.get("name", "clip")).stem), missing)
        (base / "noi-dung.md").write_text(
            f"# {it.get('title', '')}\n\n- Kênh: {it.get('channel', '')}\n- Link gốc: {it.get('url', '')}\n- Thêm lúc: {it.get('at', '')}\n"
            f"- Mã trong app: {lid}\n\n## Nội dung / điều chủ dự án muốn học\n\n{it.get('text', '')}\n\n## Timeline chủ dự án ghi\n\n{it.get('timeline', '')}\n",
            encoding="utf-8")
        write_json(base / "nguon.json", {"app_id": lid, "frames": frames, "clips": [c.get("name") for c in it.get("clips", [])]})
        if lid not in done:
            todo.append(base.relative_to(ROOT).as_posix())
    write_json(ROOT / "knowledge" / ".decisions.json", decisions)
    print(f"Thư viện: {len(lib)} mục, {len(todo)} mục chưa phân tích:")
    for t in todo:
        print("  " + t)
    if decisions:
        print("Quyết định thẻ kỹ thuật của chủ dự án: " + ", ".join(f"{k}={v.get('status')}" for k, v in decisions.items()))
    if missing:
        print(f"CHƯA TẢI {len(set(missing))} tệp — Artifact read (path=<id>, out_dir={dump}/assets) rồi chạy lại pull-lib:")
        print(" ".join(sorted(set(missing))))


def push_lib(out, versions):
    writes, k = [], ROOT / "knowledge"
    for sub in ("video-mau", "kien-thuc"):
        for base in sorted((k / sub).glob("*__*")):
            src, an = read_json(base / "nguon.json"), base / "phan-tich.md"
            if src and an.is_file():
                emit(out, "analysis", src["app_id"], {"md": an.read_text(encoding="utf-8"), "at": now()}, versions, writes)
    for card in sorted((k / "ky-thuat").glob("KT-*.md")):
        text = card.read_text(encoding="utf-8")
        head = re.search(r"^# (KT-\d+)\s*[·:-]\s*(.+)$", text, re.M)
        if not head:
            print(f"BỎ QUA {card.name}: dòng đầu phải dạng '# KT-001 · Tên'")
            continue
        field = lambda name: (re.search(rf"\*\*{name}:\*\*\s*(.+)", text) or [None, ""])[1].strip()
        body = text[head.end():].strip()
        emit(out, "cards", head[1], {"title": head[2].strip(), "kind": field("Loại"),
                                     "for": [a.strip() for a in re.split(r"[,;]", field("Dành cho")) if a.strip()],
                                     "md": body, "at": now()}, versions, writes)
    for pb in sorted((k / "so-tay").glob("*.md")):
        emit(out, "playbooks", pb.stem, {"md": pb.read_text(encoding="utf-8"), "at": now()}, versions, writes)
    finish(writes, versions, {"cards"})


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "pull":
        pull(a[1], a[2])
    elif len(a) >= 3 and a[0] == "push":
        push(a[1], a[2], parse_versions(a[3:]))
    elif len(a) == 2 and a[0] == "pull-lib":
        pull_lib(a[1])
    elif len(a) >= 2 and a[0] == "push-lib":
        push_lib(a[1], parse_versions(a[2:]))
    else:
        sys.exit(__doc__)
