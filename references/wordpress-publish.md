# WordPress 发布协议（token2x.com）

## 认证
- 凭据文件 `~/.wp/token2x.env`（600）：`WP_SITE_URL`、`WP_USER`、`WP_APP_PASSWORD`。
- Basic Auth：`base64("Edwardai:" + app_password_without_spaces)`，应用密码**去掉所有空格**再用。
- **必须带浏览器 User-Agent**（如 Chrome UA）。脚本默认 UA（python-urllib 等）会被 Cloudflare 以 error 1010 拦截。
- 先 `GET /wp-json/wp/v2/users/me` 验证登录态。

## 去重
- `GET /wp-json/wp/v2/posts?slug=jianwen-ai-digest-<YYYYMMDD>`。
- 存在 → `POST /wp-json/wp/v2/posts/<id>` 更新（**不要改 slug**，URL 保持稳定）。
- 不存在 → `POST /wp-json/wp/v2/posts` 新建，指定 `slug`。

## 字段
```json
{
  "title": "剑闻 | AI全球速览·10月4日",
  "slug": "jianwen-ai-digest-20261004",
  "content": "<report_to_html.py 生成的 HTML>",
  "excerpt": "剑闻 | AI全球速览·10月4日：……（100-150字）",
  "status": "publish",
  "categories": [10],
  "tags": []
}
```
- `categories`: JianNews 分类 id（`GET /wp/v2/categories?search=JianNews` 查询；没有则 POST 新建）。
- 不传 `featured_media`（用户要求不设特色图片）。

## 验证
发布后回读文章：`status=publish`、标题/excerpt/categories/slug 正确；匿名 GET 文章 URL 确认 200。

## 已知坑
- Cloudflare 1010：请求缺浏览器 UA 时触发，与 Wordfence 无关（Wordfence 已放行应用密码）。
- 应用密码权限不足删 term（`rest_cannot_delete`）：建错的标签/分类删不掉是正常的，留空标签无害。
- 站点主题不输出 `og:image`：微信等平台分享卡片不稳定；根治需在 wp-admin 装 SEO 插件（RankMath/Yoast），需管理员账号密码（应用密码装不了插件）。
- 换 slug 后旧 URL 会 404（无自动跳转），分享出去的旧链接需更新。
