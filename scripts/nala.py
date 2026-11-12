"""Phần dùng chung cho các script của xưởng Nà Lạ. Chỉ dùng thư viện chuẩn (Pillow là tùy chọn)."""
import base64
import html
import io
import json
import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = json.loads((ROOT / "knowledge/02-thiet-bi-va-rang-buoc.json").read_text(encoding="utf-8"))
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
SHOT_RE = re.compile(r"(S\d{2}-SH\d{2})", re.I)
VERDICTS = {"dat": "Đạt", "chinh": "Cần chỉnh", "quay-lai": "Quay lại"}
AGENTS = {
    "showrunner": "Showrunner", "thu-thu": "Thủ thư", "bien-kich": "Biên kịch",
    "quay-phim": "Quay phim", "am-thanh": "Âm thanh", "hoa-si-storyboard": "Họa sĩ storyboard",
    "giam-sat": "Giám sát", "chien-luoc-youtube": "Chiến lược YouTube",
}
STAGES = [
    ("y-tuong", "Ý tưởng & ảnh đầu vào"), ("dinh-huong", "Định hướng"), ("concept", "Concept"),
    ("kich-ban", "Kịch bản"), ("shot-list", "Shot list"), ("am-thanh", "Âm thanh"),
    ("storyboard", "Storyboard & gói prompt"), ("thuc-te", "Ảnh thực tế"), ("final", "Bản Final"),
]


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def esc(v):
    return html.escape(str(v if v is not None else ""))


def read_json(path, default=None):
    path = Path(path)
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def load_ep(ep_dir):
    return json.loads((Path(ep_dir) / "shots.json").read_text(encoding="utf-8"))


def all_shots(data):
    return [(sc, sh) for sc in data.get("scenes", []) for sh in sc.get("shots", [])]


def resolve(ep_dir, rel):
    """Đường dẫn ảnh có thể tính từ thư mục tập hoặc từ gốc repo."""
    if not rel:
        return None
    for base in (Path(ep_dir), ROOT):
        p = base / rel
        if p.is_file():
            return p
    return None


def shot_state(ep_dir, sh):
    """Trạng thái hiển thị của một shot: (mã, nhãn)."""
    real = sh.get("real") or {}
    if real.get("image") and resolve(ep_dir, real["image"]):
        v = real.get("verdict")
        if v in VERDICTS:
            return v, VERDICTS[v]
        return "cho", "Chờ nhận xét"
    sb = sh.get("storyboard") or {}
    if sb.get("level", "none") != "none" and sb.get("image") and resolve(ep_dir, sb["image"]):
        return "ai", "Có hình dự kiến"
    return "trong", "Chưa có hình"


def coverage(ep_dir, data):
    c = {"total": 0, "trong": 0, "ai": 0, "cho": 0, "dat": 0, "chinh": 0, "quay-lai": 0, "plan": 0}
    for _, sh in all_shots(data):
        c["total"] += 1
        c[shot_state(ep_dir, sh)[0]] += 1
        sb = sh.get("storyboard") or {}
        if sb.get("level", "none") != "none" and resolve(ep_dir, sb.get("image")):
            c["plan"] += 1
    c["real"] = c["cho"] + c["dat"] + c["chinh"] + c["quay-lai"]
    return c


def img_src(ep_dir, rel, embed=False, max_px=1280, out_dir=None):
    """src cho thẻ <img>: đường dẫn tương đối, hoặc data URI khi embed=True."""
    p = resolve(ep_dir, rel)
    if not p:
        return ""
    if not embed:
        return esc(os.path.relpath(p, out_dir or ep_dir).replace(os.sep, "/"))
    raw, mime = p.read_bytes(), "image/" + p.suffix.lower().lstrip(".").replace("jpg", "jpeg")
    try:  # thu nhỏ nếu có Pillow, để file báo cáo không quá nặng
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
        im.thumbnail((max_px, max_px))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=82)
        raw, mime = buf.getvalue(), "image/jpeg"
    except Exception:
        pass
    return f"data:{mime};base64,{base64.b64encode(raw).decode()}"


def _inline(t):
    t = esc(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<i>\1</i>", t)
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', t)


def md_to_html(text):
    """Chuyển Markdown cơ bản (tiêu đề, bảng, danh sách, trích dẫn, đoạn) sang HTML."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
        elif ln.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre>" + esc("\n".join(lines[i + 1:j])) + "</pre>")
            i = j + 1
        elif re.match(r"#{1,5} ", ln):
            n = len(ln) - len(ln.lstrip("#"))
            out.append(f"<h{min(n + 2, 6)}>{_inline(ln[n:].strip())}</h{min(n + 2, 6)}>")
            i += 1
        elif ln.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            body = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
            if body:
                out.append("<table><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in body[0]) + "</tr>"
                           + "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in body[1:])
                           + "</table>")
        elif re.match(r"\s*([-*]|\d+\.) ", ln):
            tag = "ol" if re.match(r"\s*\d+\.", ln) else "ul"
            items = []
            while i < len(lines) and re.match(r"\s*([-*]|\d+\.) ", lines[i]):
                items.append(_inline(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i])))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>")
        elif ln.startswith(">"):
            out.append(f"<blockquote>{_inline(ln.lstrip('> '))}</blockquote>")
            i += 1
        elif re.fullmatch(r"-{3,}", ln.strip()):
            out.append("<hr>")
            i += 1
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,5} |\s*([-*]|\d+\.) |>|```|\s*\|)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
    return "\n".join(out)
