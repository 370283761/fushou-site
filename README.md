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
│   ├── record-and-participate.html           《记录与参与》
│   └── ai-and-teams.html                     《带AI之后，我重新理解了带团队》
├── assets/
│   ├── style.css                             全站样式
│   ├── wechat-qr.png                         公众号二维码
│   └── img/                                  文章配图（封面 + 正文图）
├── robots.txt                                抓取规则（放行 AI 与搜索引擎）
├── sitemap.xml                               站点地图
├── feed.xml                                  RSS
├── llms.txt                                  AI 爬虫导览
├── llms-full.txt                             全文纯文本打包
├── set-domain.py                             一键替换域名
└── serve.sh                                  本地预览
```

正文图默认按 65% 宽居中（`@media` 手机端改通栏），不要直接通栏铺满。

## 本地查看

```bash
./serve.sh              # http://localhost:8123
./serve.sh 9000         # 换端口
./serve.sh 8123 lan     # 同一 WiFi 下手机也能看
```

也可以直接双击 `index.html`，相对路径在 `file://` 下同样有效。

## 域名

线上地址：**https://370283761.github.io/fushou-site/**

站点里的绝对地址（canonical、og:url、JSON-LD、sitemap、feed）已经指向这个地址。以后换自定义域名：

```bash
python3 set-domain.py https://你的域名      # 替换
python3 set-domain.py                     # 查看当前域名
```

脚本覆盖 10 个文件里的绝对地址，正文文字不受影响。

## 新增一篇文章

1. 复制 `articles/record-and-participate.html`，改名成新的英文 slug。
2. 改 `<title>`、`description`、`canonical`、`og:*`、`article:published_time` 和 JSON-LD 里的字段。
3. 正文替换进 `<div class="prose">`，顺手填一下顶部「本文要点」卡。
4. 更新 `articles/index.html`、`index.html` 的文章列表。
5. 更新 `sitemap.xml`、`feed.xml`、`llms.txt`、`llms-full.txt`。

## 部署

托管在 **GitHub Pages**，源为 `main` 分支根目录。改完文件 `git push` 即可，约 1 分钟自动发布。

访问：https://370283761.github.io/fushou-site/

换自定义域名：仓库 Settings → Pages → Custom domain，填好后把上面域名替换命令再跑一次。

## 内容

作者：俯首的芦苇，产品经理，十几年经验，待过零售、SaaS、广告。

联系邮箱：370283761@qq.com

文字版权归作者所有。转载或引用请注明作者与原文链接。

## 公众号二维码

`assets/wechat-qr.png` 是公众号「俯首的芦苇」的真实二维码（500×500，白底，四周留约 6 个模块的静区），从公众号后台的「扫码/搜索联合传播样式」长图中裁出。

换二维码时保持正方形、边长 ≥ 300px 的 PNG 即可：

```bash
cp ~/Downloads/你的二维码.png assets/wechat-qr.png
git add assets/wechat-qr.png && git commit -m "更新公众号二维码" && git push
```

页面里图片按 150px（手机 130px）显示，不用追求大尺寸，也不要做圆角裁切或加滤镜——会降低识别率。
