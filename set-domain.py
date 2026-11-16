#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置站点域名：把全站的占位域名一次性替换成你的真实域名。

用法：
    python3 set-domain.py https://example.com      # 替换
    python3 set-domain.py                          # 只看当前域名和出现次数

替换范围：所有 .html / .xml / .txt 文件里的
canonical、og:url、twitter、JSON-LD、sitemap、feed、llms.txt、robots.txt
稿件正文文字不会被改动。
"""

import os
import re
import sys

PLACEHOLDER = "https://www.fushoudeluwei.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
EXTS = (".html", ".xml", ".txt")


def target_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "node_modules"))]
        for name in filenames:
            if name.endswith(EXTS):
                yield os.path.join(dirpath, name)


def detect_current_domain(files):
    """从 sitemap.xml 的 <loc> 里取站内域名，比统计全文更可靠。"""
    sitemap = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sitemap):
        with open(sitemap, encoding="utf-8") as f:
            locs = re.findall(r"<loc>(https?://[^/<]+)", f.read())
        if locs:
            return sorted(set(locs), key=locs.count, reverse=True)[0]
    return PLACEHOLDER


def main():
    files = list(target_files())

    # 统计各域名出现次数，仅用于展示
    hits = {}
    for path in files:
        with open(path, encoding="utf-8") as f:
            for m in re.findall(r'https?://[a-zA-Z0-9.\-]+', f.read()):
                hits[m] = hits.get(m, 0) + 1
    current = detect_current_domain(files)

    if len(sys.argv) < 2:
        print("当前域名：%s" % current)
        print("出现次数：")
        for url, count in sorted(hits.items(), key=lambda kv: -kv[1]):
            print("  %-40s %d 次" % (url, count))
        print("\n替换为你的域名：  python3 set-domain.py https://your-domain.com")
        return

    new = sys.argv[1].strip().rstrip("/")
    if not new.startswith(("http://", "https://")):
        new = "https://" + new
    if not re.match(r'^https?://[a-zA-Z0-9.\-]+(:\d+)?$', new):
        sys.exit("域名格式不对：%s（示例：https://example.com）" % new)
    if new == current:
        print("域名已经是 %s，无需替换。" % new)
        return

    changed = 0
    total = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        n = text.count(current)
        if n == 0:
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(text.replace(current, new))
        rel = os.path.relpath(path, ROOT)
        print("  %-42s %d 处" % (rel, n))
        changed += 1
        total += n

    print("\n完成：%d 个文件，共替换 %d 处。" % (changed, total))
    print("新域名：%s" % new)
    print("提醒：域名要换成不带末尾斜杠的根域，sitemap/feed 里的路径会自动跟着变。")


if __name__ == "__main__":
    main()
