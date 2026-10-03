---
name: "jianwen-ai-digest"
description: "剑闻「全球AI速览」发布 skill：把 daily-intelligence 日报转成秋日风响应式 HTML，按固定品牌规范（标题/摘要/slug/分类目录）发布到 token2x.com WordPress。触发语：「发全球AI速览」「发布剑闻」"
---

# 剑闻 · 全球AI速览发布

## Purpose
把 `daily-intelligence-skill` 产出的日报 md，按 2026-10-03 定版的品牌规范转成 HTML 并发布到 token2x.com（WordPress）。品牌规范一旦变更，同步更新本文件与 `references/publish-spec.md`。

## 品牌规范（2026-10-03 定版）

| 项目 | 规范 |
|---|---|
| 标题 | `剑闻 \| AI全球速览·<M>月<D>日`（如"剑闻 \| AI全球速览·10月4日"） |
| URL slug | `jianwen-ai-digest-<YYYYMMDD>`（英文，带年份防重名） |
| 分类目录 | JianNews（id 10；没有就新建） |
| 标签 | 空，不加任何 tag |
| 特色图片 | 不设（用户明确要求） |
| 摘要 excerpt | 纯文本 100–150 字，以"剑闻 \| AI全球速览·<M>月<D>日："开头，浓缩 3–5 个最重要头条 + 一句话数据来源 |
| 排版 | 秋日风（autumn-warm）+ 响应式：外层 `max-width:700px` 居中，手机全宽、桌面居中阅读栏；图片一律 `max-width:100%;height:auto` |

## Workflow

1. 输入：`~/workspace/daily-intelligence/YYYY-MM-DD-report.md`（daily-intelligence-skill 产出）。
2. 生成 HTML：
   ```bash
   cd ~/workspace/daily-intelligence
   python3 <skill>/scripts/report_to_html.py <report.md> token2x-<YYYY-MM-DD>-full.html \
     "剑闻 | AI全球速览·<M>月<D>日" "AI · 科技 · 比特币宏观 · X 原帖直拉 · 每日完整情报"
   ```
   （封面脚本 `scripts/make_cover.py` 保留备用；token2x 当前不设特色图片。）
3. 写摘要文本（100–150 字，见上表），存 `token2x-<YYYY-MM-DD>-excerpt.txt`。
4. 按 `references/wordpress-publish.md` 发布到 WordPress（查 slug 去重：有则更新、无则新建；更新时**不改 slug**）。
5. 回读确认：status=publish、标题/excerpt/categories/slug 正确、页面匿名访问 200。

## Tooling
- `scripts/report_to_html.py`：日报 md → 秋日风响应式 HTML（内联样式，WordPress/公众号通用）。
- `scripts/make_cover.py`：生成 900×383 秋日封面（备用）。
- 凭据：`~/.wp/token2x.env`（600 权限，WP_SITE_URL / WP_USER / WP_APP_PASSWORD）。**凭据只存本机，不进 skill、不进 Git、不进记忆；绝不在日志/回复中打印。**

## Operating Rules
1. 每次发布前用 `/wp/v2/posts?slug=<slug>` 查当天是否已发，避免重复创建。
2. 所有 WP REST 请求必须带浏览器 User-Agent，否则 Cloudflare 返回 1010 拦截；应用密码使用前去掉空格。
3. 不设 featured_media、不加 tag；分类目录固定 JianNews。
4. 事实口径：标题/摘要中的数字、人名、机构名必须来自日报原文，不编造。
5. 每日自动跑的 cron 为 `daily-intelligence-token2x`（约 7:38 用户本地时区），改规范时同步更新该 cron。
