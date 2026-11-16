#!/usr/bin/env bash
# 手动部署到 Cloudflare Pages（直传方式，不经过 Git）
#
# 首次使用需要：
#   npm install -g wrangler
#   wrangler login
#
# 用法：
#   ./deploy.sh                         部署到生产环境
#   ./deploy.sh preview                 部署到预览环境
#
# 注意：如果已经在 Cloudflare 后台连了 GitHub 仓库（推荐方式），
#       git push 就会自动部署，不需要跑这个脚本。

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT="fushou-site"
BRANCH="${1:-main}"

if ! command -v wrangler >/dev/null 2>&1; then
  echo "未找到 wrangler。先安装并登录："
  echo "  npm install -g wrangler"
  echo "  wrangler login"
  exit 1
fi

echo "部署 $PROJECT（分支：$BRANCH）"
wrangler pages deploy "$DIR" --project-name "$PROJECT" --branch "$BRANCH" --commit-dirty=true
