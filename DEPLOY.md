# 部署到 Cloudflare Pages

## 推荐方式：连 GitHub 仓库自动部署

一次配置，以后每次 `git push` 自动发布新版本。

### 1. 在 Cloudflare 创建 Pages 项目

登录 [Cloudflare Dashboard](https://dash.cloudflare.com/) → 左侧 **Workers & Pages** → **Create** → **Pages** → **Connect to Git**

授权 GitHub，选择仓库 `370283761/fushou-site`。

### 2. 构建配置（关键，别填错）

| 配置项 | 填什么 |
|---|---|
| Project name | `fushou-site` |
| Production branch | `main` |
| Framework preset | **None** |
| Build command | **留空** |
| Build output directory | `/`（或留空） |

**这是纯静态站，没有构建步骤。** 如果填了 `npm run build` 之类，构建会失败。

### 3. 部署

点 **Save and Deploy**，等约 30 秒。上线地址：

```
https://fushou-site.pages.dev
```

### 4. 更新域名常量（重要）

部署成功后，把站内的占位域名换成真实地址：

```bash
cd 个人网站
python3 set-domain.py https://fushou-site.pages.dev
git add -A && git commit -m "更新站点域名" && git push
```

推送后 Cloudflare 会自动重新部署。

> 以后绑了自定义域名，再跑一次同样的命令换成新域名即可。

## 绑自定义域名（可选）

Cloudflare Pages 项目 → **Custom domains** → **Set up a domain**，填你的域名，按提示加 CNAME 记录。HTTPS 证书自动签发。

## 必须检查的一件事：AI 爬虫开关

**Cloudflare 默认会拦截 AI 抓取器**，这会直接废掉这个站的核心目标。

Pages 项目 → **Settings** → 找 **AI Crawl Control** 或 **Block AI bots** 项：

- 如果有 **Block AI bots** 开关 → **关闭**
- 如果在 **Security** → **Bots** 里 → 确认没有启用 "Block AI Scrapers and Crawlers"

同时确认 **Under Attack Mode** 处于关闭状态，这个模式会让所有爬虫和部分真人访客看到验证页。

配好之后可以用下面的命令验证：

```bash
# 查看响应头里有没有拦截标记
curl -sI https://fushou-site.pages.dev/ | grep -i -E "cf-mitigated|server"

# 检查 robots.txt 是否原样返回
curl -s https://fushou-site.pages.dev/robots.txt | head -3
```

## 备选方式：本地直传

不想连 Git，或者只想快速传一次：

```bash
npm install -g wrangler
wrangler login
./deploy.sh
```

项目里的 `wrangler.toml` 已经配好，`.assetsignore` 会把 README、脚本等文件排除在线上之外。

## 国内访问说明

`*.pages.dev` 在国内访问不稳定，部分地区需要代理。如果主要读者在国内，建议：

- 绑自定义域名（Cloudflare 全球网络会稍好一些）
- 或者接受这一点——**这个站的首要目标是给 AI 爬虫读，它们走的是境外网络，不受影响**；国内真人读者从公众号点进来时如果慢，可以后续再加一层国内 CDN 或换托管。

## 上线后检查清单

- [ ] 首页、文章列表、两篇文章、关于页都能打开
- [ ] 样式正常（说明 `assets/style.css` 路径没问题）
- [ ] `https://fushou-site.pages.dev/robots.txt` 能直接看到明文
- [ ] `https://fushou-site.pages.dev/llms.txt` 能直接看到明文
- [ ] `https://fushou-site.pages.dev/sitemap.xml` 返回 XML 而非下载
- [ ] 站内所有链接可点，没有 404
- [ ] Cloudflare 的 AI 爬虫拦截已关闭
- [ ] 已跑过 `set-domain.py` 并把占位域名全部替换
