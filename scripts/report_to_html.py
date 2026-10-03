#!/usr/bin/env python3
"""把 daily-intelligence 日报 md 转成 token2x 用的秋日风响应式 HTML。

用法: python3 report_to_html.py <report.md> <out.html> "<标题>" "<副标题>"
标题如: 今日AI速览 · 10月3日 · 完整版
副标题如: AI · 科技 · 比特币宏观 · X 原帖直拉 · 每日完整情报

设计: md2wechat-lite autumn-warm 配色,内联样式;
外层 max-width:700px 居中容器,手机全宽、桌面居中阅读栏;
图片请加 style="max-width:100%;height:auto;display:block;"。
"""
import re
import sys

SEC_EMOJI = {'加密行情': '💹', 'AI': '🤖', '科技': '🔬', '融资': '💰',
             '比特币': '₿', 'X 动态': '🐦', 'Reddit': '🗨️'}


def main():
    report, out, title, subtitle = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    lines = open(report, encoding='utf-8').read().split('\n')

    html = ['<div style="max-width:700px;margin:0 auto;padding:0 18px;box-sizing:border-box;'
            'font-size:16px;color:#4a413d;line-height:1.8;word-break:break-word;'
            'font-family:Optima-Regular,Optima,PingFangSC-light,PingFangTC-light,'
            '\'PingFang SC\',Cambria,Cochin,Georgia,Times,serif;">']
    html.append(f'''
<div style="text-align:center;padding:28px 20px 20px 20px;background:#FFF7ED;border-radius:12px;margin-bottom:24px;">
<div style="font-size:13px;color:#B45309;letter-spacing:4px;margin-bottom:10px;">🍂 每 日 情 报 🍂</div>
<div style="font-size:26px;font-weight:bold;color:#7C2D12;line-height:1.4;">{title}</div>
<div style="font-size:13px;color:#A16207;margin-top:8px;">{subtitle}</div>
</div>''')

    in_status = False
    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()
        if line.startswith('## '):
            t = line[3:].strip()
            in_status = '数据源状态' in t
            if not in_status and '数据口径' not in t:
                emoji = next((e for k, e in SEC_EMOJI.items() if k in t), '📌')
                clean = re.sub(r'（[^）]*）', '', t).strip()
                html.append(f'<div style="font-size:20px;font-weight:bold;color:#7C2D12;'
                            f'margin:26px 0 12px 0;border-bottom:2px solid #E8A04C;'
                            f'padding-bottom:6px;">{emoji} {clean}</div>')
            i += 1
            continue
        if in_status or not line.strip() or line.strip().startswith('>') \
                or line.strip() == '---' or line.startswith('# '):
            i += 1
            continue
        if line.startswith('**') and line.endswith('**') and len(line) > 4:
            item_title = re.sub(r'\*\*(.+?)\*\*',
                                r'<strong style="color:#9A3412;">\1</strong>',
                                line.strip('*').strip())
            i += 1
            parts, link = [], ''
            while i < n and not lines[i].startswith('**') and not lines[i].startswith('## ') \
                    and not lines[i].startswith('- ') and lines[i].strip() not in ('', '---'):
                l = lines[i].strip()
                m = re.match(r'🔗 \[(.+?)\]\((.+?)\)', l)
                if m:
                    link = f'<a href="{m.group(2)}" style="color:#B45309;">{m.group(1)}</a>'
                elif l:
                    parts.append(l)
                i += 1
            summary = re.sub(r'\*\*(.+?)\*\*',
                             r'<strong style="color:#9A3412;">\1</strong>', ' '.join(parts))
            html.append('<div style="margin-bottom:20px;">')
            html.append(f'<div style="font-size:17px;font-weight:bold;color:#7C2D12;'
                        f'margin-bottom:6px;">🍁 {item_title}</div>')
            if summary:
                html.append(f'<p style="color:#4a413d;margin:0 0 4px 0;">{summary}</p>')
            if link:
                html.append(f'<p style="color:#4a413d;margin:0;font-size:14px;">🔗 {link}</p>')
            html.append('</div>')
            continue
        if line.startswith('- '):
            content = re.sub(r'\*\*(.+?)\*\*',
                             r'<strong style="color:#9A3412;">\1</strong>',
                             line[2:].strip())
            j = i + 1
            extra = []
            while j < n and lines[j].strip().startswith('🔗'):
                lm = re.match(r'🔗 \[(.+?)\]\((.+?)\)', lines[j].strip())
                if lm:
                    extra.append(f'<a href="{lm.group(2)}" style="color:#B45309;">{lm.group(1)}</a>')
                j += 1
            html.append(f'<p style="color:#4a413d;margin:0 0 10px 0;">• {content}</p>')
            if extra:
                html.append(f'<p style="color:#4a413d;margin:-6px 0 12px 14px;'
                            f'font-size:14px;">🔗 {" ".join(extra)}</p>')
            i = j
            continue
        i += 1

    html.append('''
<div style="text-align:center;padding:20px;background:#FFF7ED;border-radius:12px;margin-top:8px;">
<p style="color:#92400E;font-size:14px;margin:0;">🍂 以上就是今天的完整情报 🍂</p>
<p style="color:#A16207;font-size:13px;margin:8px 0 0 0;">假期继续，模型不停，妞妞帮你盯着</p>
</div>
</div>''')
    open(out, 'w', encoding='utf-8').write('\n'.join(html))
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
