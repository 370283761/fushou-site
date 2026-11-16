#!/usr/bin/env bash
# 本地启动个人网站
#
#   ./serve.sh            默认 127.0.0.1:8123
#   ./serve.sh 9000       指定端口
#   ./serve.sh 8123 lan   允许同一 WiFi 下的手机访问
#
# 停止：Ctrl+C，或 kill $(lsof -ti:8123)

set -euo pipefail

PORT="${1:-8123}"
MODE="${2:-local}"
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$MODE" = "lan" ]; then
  HOST="0.0.0.0"
else
  HOST="127.0.0.1"
fi

if lsof -ti:"$PORT" >/dev/null 2>&1; then
  echo "端口 $PORT 已被占用（PID $(lsof -ti:"$PORT")）。"
  echo "换一个端口：./serve.sh $((PORT + 1))"
  exit 1
fi

echo "个人网站已启动"
echo "  本地地址  http://localhost:$PORT/"
if [ "$MODE" = "lan" ]; then
  for ip in $(ipconfig getifaddr en0 2>/dev/null; ipconfig getifaddr en1 2>/dev/null); do
    echo "  局域网    http://$ip:$PORT/"
  done
fi
echo "  按 Ctrl+C 停止"
echo

exec python3 -m http.server "$PORT" --bind "$HOST" --directory "$DIR"
