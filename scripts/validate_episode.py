#!/usr/bin/env python3
"""Kiểm tra shots.json của một tập theo ràng buộc trong Project Bible và chuẩn storyboard.

Dùng:  python3 scripts/validate_episode.py episodes/ep01 [--draft]
--draft: lệch thời lượng và thiếu trường storyboard chỉ là cảnh báo.
Thoát mã 1 nếu có LỖI.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nala import RULES, VERDICTS, all_shots, coverage, load_ep, read_json, resolve

SHOT_ID = re.compile(r"^(S\d{2})-SH\d{2}$")
SCENE_ID = re.compile(r"^S\d{2}$")
# Trường làm nên chất lượng storyboard: thiếu ở shot chủ chốt là LỖI, ở shot thường là cảnh báo gộp.
BOARD_FIELDS = {"link": "lý do tiếp nối shot trước", "composition": "bố cục", "light": "ánh sáng",
                "direction": "hướng dẫn quay", "frame_en": "mô tả khung hình cho prompt ảnh"}


def validate(ep_dir, draft=False):
    ep_dir = Path(ep_dir)
    data = load_ep(ep_dir)
    vb = read_json(ep_dir / "visual-bible.json", {}) or {}
    cam, gram, dur = RULES["camera"], RULES["grammar"], RULES["duration"]
    errors, warns, seen = [], [], set()

    target = data.get("target_seconds")
    if not isinstance(target, (int, float)) or target <= 0:
        errors.append("target_seconds: thiếu hoặc không hợp lệ")
        target = 0
    if not data.get("scenes"):
        errors.append("scenes: chưa có cảnh nào")

    for sc in data.get("scenes", []):
        sid = sc.get("id", "?")
        if not SCENE_ID.match(str(sid)):
            errors.append(f"{sid}: ID cảnh phải dạng S01")
        if sid in seen:
            errors.append(f"{sid}: trùng ID cảnh")
        seen.add(sid)
        if sc.get("clock_slot") not in RULES["clock_slots"]:
            errors.append(f"{sid}: clock_slot '{sc.get('clock_slot')}' không thuộc lịch ánh sáng của Bible")
        if sc.get("location_id") and sc["location_id"] not in (vb.get("locations") or {}):
            errors.append(f"{sid}: location_id '{sc['location_id']}' chưa có trong visual-bible.json")
        sound = sc.get("sound") or {}
        for layer in ("ambience", "foley"):
            if not str(sound.get(layer, "")).strip():
                errors.append(f"{sid}: thiếu sound.{layer} (Bible: 3 tầng âm thanh)")
        shots = sc.get("shots", [])
        if not shots:
            errors.append(f"{sid}: cảnh không có shot")
        focals = [s.get("focal_mm") for s in shots if isinstance(s.get("focal_mm"), (int, float))]
        if len(shots) >= gram["matching_cut_min_shots_per_scene"] and focals:
            if min(focals) > gram["wide_focal_max"] or max(focals) < gram["tele_focal_min"]:
                warns.append(f"{sid}: chưa đủ cặp 'một hành động — hai tiêu cự' "
                             f"(cần ≤{gram['wide_focal_max']}mm và ≥{gram['tele_focal_min']}mm)")

    shots = all_shots(data)
    ids = {sh.get("id") for _, sh in shots}
    total = micro = locked = 0
    missing = {f: [] for f in BOARD_FIELDS}
    for sc, sh in shots:
        i = sh.get("id", "?")
        m = SHOT_ID.match(str(i))
        if not m:
            errors.append(f"{i}: ID shot phải dạng S01-SH01")
        elif m.group(1) != sc.get("id"):
            errors.append(f"{i}: tiền tố không khớp cảnh {sc.get('id')}")
        if i in seen:
            errors.append(f"{i}: trùng ID shot")
        seen.add(i)

        f = sh.get("focal_mm")
        if not isinstance(f, (int, float)) or not cam["focal_mm_min"] <= f <= cam["focal_mm_max"]:
            errors.append(f"{i}: focal_mm={f} ngoài dải {cam['focal_mm_min']}–{cam['focal_mm_max']}mm của ống kính")
        a = sh.get("aperture")
        if not isinstance(a, (int, float)) or a < cam["aperture_min"]:
            errors.append(f"{i}: aperture={a} — ống kính không mở hơn F{cam['aperture_min']}")
        if sh.get("fps") not in cam["fps_allowed"]:
            errors.append(f"{i}: fps={sh.get('fps')} không thuộc {cam['fps_allowed']}")
        if sh.get("support") not in RULES["supports_allowed"]:
            errors.append(f"{i}: support='{sh.get('support')}' không thuộc {RULES['supports_allowed']}")
        sec = sh.get("seconds")
        if not isinstance(sec, (int, float)) or sec <= 0:
            errors.append(f"{i}: seconds phải > 0")
            sec = 0
        elif sec > gram["shot_seconds_warn_max"]:
            warns.append(f"{i}: {sec}s — shot dài, kiểm tra có đủ nội dung không")
        for field in ("size", "action"):
            if not str(sh.get(field, "")).strip():
                errors.append(f"{i}: thiếu {field}")
        for c in sh.get("characters", []):
            if c not in RULES["characters"]:
                errors.append(f"{i}: nhân vật '{c}' không có trong Bible ({', '.join(RULES['characters'])})")
        for p in sh.get("prop_ids", []):
            if p not in (vb.get("props") or {}):
                errors.append(f"{i}: prop_ids '{p}' chưa có trong visual-bible.json")
        if sh.get("pair") and sh["pair"] not in ids:
            warns.append(f"{i}: pair '{sh['pair']}' không tồn tại")

        for field in BOARD_FIELDS:
            if not str(sh.get(field, "")).strip():
                missing[field].append((i, bool(sh.get("key"))))

        sb = sh.get("storyboard") or {}
        level = sb.get("level", "none")
        if level not in RULES["storyboard_levels"]:
            errors.append(f"{i}: storyboard.level='{level}' không hợp lệ")
        elif level != "none":
            if not resolve(ep_dir, sb.get("image")):
                errors.append(f"{i}: storyboard ghi '{level}' nhưng không thấy file '{sb.get('image')}'")
            if sb.get("panel") not in (None, 0, 1, 2, 3):
                errors.append(f"{i}: storyboard.panel phải là 0–3 hoặc null")
        real = sh.get("real") or {}
        if real.get("image") and not resolve(ep_dir, real["image"]):
            errors.append(f"{i}: real.image '{real['image']}' không tồn tại")
        if real.get("verdict") not in (None, *VERDICTS):
            errors.append(f"{i}: real.verdict phải là một trong {list(VERDICTS)} hoặc null")
        if real.get("verdict") in ("chinh", "quay-lai") and not str(real.get("note", "")).strip():
            errors.append(f"{i}: real.verdict='{real['verdict']}' phải kèm real.note nói rõ cần sửa gì")

        total += sec
        if sh.get("micro_cut"):
            micro += sec
        if sh.get("support") in RULES["supports_locked"] and sh.get("movement", "static") == "static":
            locked += 1

    for field, label in BOARD_FIELDS.items():
        keys = [i for i, k in missing[field] if k]
        rest = [i for i, k in missing[field] if not k]
        if keys:
            (warns if draft else errors).append(
                f"{len(keys)} shot chủ chốt thiếu {field} ({label}): {', '.join(keys[:6])}{'…' if len(keys) > 6 else ''}")
        if rest:
            warns.append(f"{len(rest)} shot thường thiếu {field}: {', '.join(rest[:6])}{'…' if len(rest) > 6 else ''}")

    for kind in ("subjects", "locations", "props"):
        for key, item in (vb.get(kind) or {}).items():
            for r in item.get("refs", []):
                if not resolve(ep_dir, r):
                    errors.append(f"visual-bible {kind}.{key}: không thấy ảnh tham chiếu '{r}'")

    if target and shots:
        dev = (total - target) / target
        if abs(dev) > dur["tolerance"]:
            (warns if draft else errors).append(
                f"Tổng {total:.0f}s so với mục tiêu {target:.0f}s (lệch {dev:+.1%}, cho phép ±{dur['tolerance']:.0%})")
    if shots and locked / len(shots) < gram["locked_off_ratio_min"]:
        warns.append(f"Máy khóa tĩnh {locked / len(shots):.0%} < {gram['locked_off_ratio_min']:.0%} theo Bible")
    if micro and not dur["micro_cut_seconds_min"] <= micro <= dur["micro_cut_seconds_max"]:
        warns.append(f"Micro Cut {micro:.0f}s ngoài khoảng {dur['micro_cut_seconds_min']}–{dur['micro_cut_seconds_max']}s")
    if shots and not any(sh.get("key") for _, sh in shots):
        warns.append("Chưa shot nào được đánh dấu key (shot chủ chốt cần hình trước)")

    cov = coverage(ep_dir, data)
    stats = {"scenes": len(data.get("scenes", [])), "shots": len(shots), "seconds": total, "target": target,
             "micro_cut": micro, "locked_ratio": locked / len(shots) if shots else 0, "cov": cov,
             "keys": sum(1 for _, s in shots if s.get("key"))}
    return errors, warns, stats


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    errors, warns, st = validate(args[0], draft="--draft" in sys.argv)
    c = st["cov"]
    print(f"{st['scenes']} cảnh · {st['shots']} shot ({st['keys']} chủ chốt) · {st['seconds']:.0f}/{st['target']:.0f}s · "
          f"máy tĩnh {st['locked_ratio']:.0%} · micro cut {st['micro_cut']:.0f}s")
    print(f"Hình dự kiến {c['plan']}/{c['total']} · ảnh thực tế {c['real']}/{c['total']} "
          f"(đạt {c['dat']}, cần chỉnh {c['chinh']}, quay lại {c['quay-lai']}, chờ nhận xét {c['cho']})")
    for w in warns:
        print("CẢNH BÁO  " + w)
    for e in errors:
        print("LỖI       " + e)
    print("ĐẠT" if not errors else f"CHƯA ĐẠT — {len(errors)} lỗi")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
