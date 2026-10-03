#!/usr/bin/env python3
"""生成 token2x 文章封面 (900x383, 秋日渐变)。

用法: python3 make_cover.py <out.png> "<主标题>" "<副标题>"
"""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT, MAIN, SUB = sys.argv[1], sys.argv[2], sys.argv[3]

W, H = 900, 383
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)
top = (194, 120, 40)
bottom = (90, 45, 15)
for y in range(H):
    t = y / H
    c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
    draw.line([(0, y), (W, y)], fill=c)
for r in range(120, 0, -1):  # 落日
    draw.ellipse([W - 200 - r, 60 - r, W - 200 + r, 60 + r], outline=(255, 200, 120))

font_path = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
f_title = ImageFont.truetype(font_path, 72, index=1)
f_sub = ImageFont.truetype(font_path, 34, index=1)

draw.text((70, 110), MAIN, fill='#FFF7ED', font=f_title)
draw.text((72, 210), SUB, fill='#FDE68A', font=f_sub)
draw.text((72, 270), '—— token2x', fill='#FCD9A0', font=f_sub)

img.save(OUT)
print(f'wrote {OUT}')
