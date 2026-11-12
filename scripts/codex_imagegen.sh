#!/usr/bin/env bash
# Tạo một ảnh bằng skill $imagegen có sẵn của Codex CLI, dùng đăng nhập ChatGPT (Plus/Pro).
# KHÔNG dùng API key. Chạy trên máy đã `codex login` (không chạy được trong phiên Claude trên cloud).
#
# Dùng:  scripts/codex_imagegen.sh <file-prompt.txt> <ảnh-ra.png> [ảnh-tham-chiếu ...]
#
# LƯU Ý: script này CHƯA được chạy thử với Codex thật khi viết (môi trường viết không có Codex).
# Cờ lệnh của `codex exec` có thể đổi theo phiên bản; nếu lỗi, chạy `codex exec --help` rồi sửa dòng EXEC.
set -euo pipefail

[ $# -ge 2 ] || { sed -n '2,8p' "$0"; exit 64; }

if [ -n "${OPENAI_API_KEY:-}" ]; then
  echo "DỪNG: biến OPENAI_API_KEY đang được đặt — Codex sẽ chuyển sang tính tiền API." >&2
  echo "Chạy 'unset OPENAI_API_KEY' rồi thử lại." >&2
  exit 2
fi
command -v codex >/dev/null || { echo "Chưa có Codex CLI: npm i -g @openai/codex && codex login" >&2; exit 3; }
codex login status >/dev/null 2>&1 || { echo "Codex chưa đăng nhập ChatGPT: chạy 'codex login'" >&2; exit 3; }

prompt_file=$1; out=$2; shift 2
[ -f "$prompt_file" ] || { echo "Không thấy file prompt: $prompt_file" >&2; exit 66; }
mkdir -p "$(dirname "$out")"
out_dir=$(cd "$(dirname "$out")" && pwd); out_name=$(basename "$out")
[ -e "$out_dir/$out_name" ] && { echo "Đã có $out — xóa hoặc đổi tên trước (tránh tạo trùng tốn hạn mức)." >&2; exit 5; }

refs=()
for r in "$@"; do
  [ -f "$r" ] || { echo "Không thấy ảnh tham chiếu: $r" >&2; exit 66; }
  refs+=(-i "$(cd "$(dirname "$r")" && pwd)/$(basename "$r")")
done

task="\$imagegen Generate exactly one image and save it in the current directory as '$out_name'. Do not create any other files. Image brief:

$(cat "$prompt_file")"

marker=$(mktemp)
# EXEC
codex exec --sandbox workspace-write --skip-git-repo-check -C "$out_dir" "$task" "${refs[@]}"

if [ ! -s "$out_dir/$out_name" ]; then
  # Codex đôi khi lưu vào thư mục riêng của nó thay vì thư mục làm việc.
  found=$(find "${CODEX_HOME:-$HOME/.codex}/generated_images" -type f -newer "$marker" \
          \( -name '*.png' -o -name '*.jpg' -o -name '*.webp' \) 2>/dev/null | tail -1 || true)
  [ -n "$found" ] && cp "$found" "$out_dir/$out_name"
fi
rm -f "$marker"

[ -s "$out_dir/$out_name" ] || { echo "Codex chạy xong nhưng không thấy ảnh. Xem log phía trên (có thể hết hạn mức)." >&2; exit 4; }
echo "OK $out_dir/$out_name"
