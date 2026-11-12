#!/usr/bin/env python3
"""Kiểm tra shots.json của một tập theo ràng buộc trong Project Bible.

Dùng:  python3 scripts/validate_episode.py episodes/ep01 [--draft]
--draft: lệch thời lượng chỉ là cảnh báo (dùng khi kịch bản chưa viết xong).
Thoát mã 1 nếu có LỖI. Chỉ dùng thư viện chuẩn.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = json.loads((ROOT / "knowledge/02-thiet-bi-va-rang-buoc.json").read_text(encoding="utf-8"))
SHOT_ID = re.compile(r"^(S\d{2})-SH\d{2}$")
SCENE_ID = re.compile(r"^S\d{2}$")


def load(ep_dir):
    return json.loads((Path(ep_dir) / "shots.json").read_text(encoding="utf-8"))


def all_shots(data):
    return [(sc, sh) for sc in data.get("scenes", []) for sh in sc.get("shots", [])]


def validate(ep_dir, draft=False):
    ep_dir = Path(ep_dir)
    data = load(ep_dir)
    cam, gram, dur = RULES["camera"], RULES["grammar"], RULES["duration"]
    errors, warns = [], []
    seen = set()

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
        if sh.get("pair") and sh["pair"] not in ids:
            warns.append(f"{i}: pair '{sh['pair']}' không tồn tại")

        sb = sh.get("storyboard") or {}
        level = sb.get("level", "none")
        if level not in RULES["storyboard_levels"]:
            errors.append(f"{i}: storyboard.level='{level}' không hợp lệ")
        elif level != "none":
            img = sb.get("image")
            if not img or not (ep_dir / img).is_file():
                errors.append(f"{i}: storyboard ghi '{level}' nhưng không thấy file '{img}'")
            if sb.get("panel") not in (None, 0, 1, 2, 3):
                errors.append(f"{i}: storyboard.panel phải là 0–3 hoặc null")

        total += sec
        if sh.get("micro_cut"):
            micro += sec
        if sh.get("support") in RULES["supports_locked"] and sh.get("movement", "static") == "static":
            locked += 1

    if target and shots:
        dev = (total - target) / target
        msg = f"Tổng {total:.0f}s so với mục tiêu {target:.0f}s (lệch {dev:+.1%}, cho phép ±{dur['tolerance']:.0%})"
        if abs(dev) > dur["tolerance"]:
            (warns if draft else errors).append(msg)
    if shots:
        ratio = locked / len(shots)
        if ratio < gram["locked_off_ratio_min"]:
            warns.append(f"Máy khóa tĩnh {ratio:.0%} < {gram['locked_off_ratio_min']:.0%} theo Bible")
    if micro and not dur["micro_cut_seconds_min"] <= micro <= dur["micro_cut_seconds_max"]:
        warns.append(f"Micro Cut {micro:.0f}s ngoài khoảng "
                     f"{dur['micro_cut_seconds_min']}–{dur['micro_cut_seconds_max']}s")

    done = sum(1 for _, s in shots if (s.get("storyboard") or {}).get("level", "none") != "none")
    stats = {"scenes": len(data.get("scenes", [])), "shots": len(shots), "seconds": total,
             "target": target, "micro_cut": micro,
             "locked_ratio": locked / len(shots) if shots else 0, "storyboard": done}
    return errors, warns, stats


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    errors, warns, st = validate(args[0], draft="--draft" in sys.argv)
    print(f"{st['scenes']} cảnh · {st['shots']} shot · {st['seconds']:.0f}/{st['target']:.0f}s · "
          f"máy tĩnh {st['locked_ratio']:.0%} · micro cut {st['micro_cut']:.0f}s · "
          f"storyboard {st['storyboard']}/{st['shots']}")
    for w in warns:
        print("CẢNH BÁO  " + w)
    for e in errors:
        print("LỖI       " + e)
    print("ĐẠT" if not errors else f"CHƯA ĐẠT — {len(errors)} lỗi")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
