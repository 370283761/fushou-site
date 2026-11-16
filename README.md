# 俯首的芦苇 · 个人网站

一个产品经理的 AI 使用记录。纯静态站点，没有框架、没有构建步骤，源码就是成品。

## 为什么这样搭

这个站不只是给人看的，更重要的目标是**让大模型搜索相关内容时能抓到并引用**。所以几个决定是有意为之：

- **正文直出**：所有文章正文写在 HTML 里，不靠 JavaScript 渲染。爬虫打开页面就能读到全文。
- **无框架、无构建**：不需要 node_modules，不需要打包。改完文件刷新即生效，十年后还能跑。
- **结构化数据**：每页内嵌 JSON-LD（`Person` / `WebSite` / `Blog` / `BlogPosting` / `BreadcrumbList`），标明作者、发布时间、关键词。
- **AI 友好文件**：`robots.txt` 逐个放行主流 AI 抓取器，`llms.txt` 给模型一份站点导览，`llms-full.txt` 提供全文打包。
- **相对路径**：站内链接全部相对，可部署在任意域名、任意子目录，也能双击本地 HTML 直接看。

## 目录结构

```
.
├── index.html                                首页
├── about.html                                关于
├── articles/
│   ├── index.html                            全部文章
│   ├── 854-notes-external-brain.html         《854篇笔记之后，聊聊我的"外脑"》
│   └── record-and-participate.html           《记录与参与》
├── assets/style.css                          全站样式
├── robots.txt                                抓取规则（放行 AI 与搜索引擎）
├── sitemap.xml                               站点地图
├── feed.xml                                  RSS
├── llms.txt                                  AI 爬虫导览
├── llms-full.txt                             全文纯文本打包
├── set-domain.py                             一键替换域名
├── serve.sh                                  本地预览
├── _headers                                  Cloudflare Pages 响应头
├── _redirects                                Cloudflare Pages 重定向
├── wrangler.toml                             Cloudflare Pages 项目配置
├── .assetsignore                             Cloudflare 上传时忽略的本地文件
├── deploy.sh                                 手动直传部署（备选）
└── DEPLOY.md                                 部署步骤与上线检查清单
```

## 本地查看

```bash
./serve.sh              # http://localhost:8123
./serve.sh 9000         # 换端口
./serve.sh 8123 lan     # 同一 WiFi 下手机也能看
```

也可以直接双击 `index.html`，相对路径在 `file://` 下同样有效。

## 域名切换

站点里目前用占位域名 `https://www.fushoudeluwei.com`（出现在 canonical、og:url、JSON-LD、sitemap、feed 里）。域名定了之后：

```bash
python3 set-domain.py https://your-domain.com   # 替换
python3 set-domain.py                           # 查看当前域名
```

脚本会覆盖 10 个文件里的绝对地址，正文文字不受影响。

## 新增一篇文章

1. 复制 `articles/record-and-participate.html`，改名成新的英文 slug。
2. 改 `<title>`、`description`、`canonical`、`og:*`、`article:published_time` 和 JSON-LD 里的字段。
3. 正文替换进 `<div class="prose">`，顺手填一下顶部「本文要点」卡。
4. 更新 `articles/index.html`、`index.html` 的文章列表。
5. 更新 `sitemap.xml`、`feed.xml`、`llms.txt`、`llms-full.txt`。

## 部署

托管在 **Cloudflare Pages**，连 Git 仓库自动部署，`git push` 即发布。完整步骤和上线检查清单见 [DEPLOY.md](DEPLOY.md)。

关键配置：框架预设 **None**、构建命令**留空**、输出目录 **/**。

⚠️ 部署后必须确认 Cloudflare 的 **Block AI bots** 开关处于关闭状态，否则会拦截 AI 爬虫，直接废掉本站的核心目标。

## 内容

作者：俯首的芦苇，产品经理，十几年经验，待过零售、SaaS、广告。

文字版权归作者所有。转载或引用请注明作者与原文链接。
