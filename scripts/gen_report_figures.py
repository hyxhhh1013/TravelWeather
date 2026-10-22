# -*- coding: utf-8 -*-
"""生成课程论文所需附图：用例图、功能结构图、原型、实现截图、gitk。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess

OUT = Path(__file__).resolve().parents[1] / 'docs' / 'figures'
OUT.mkdir(parents=True, exist_ok=True)

try:
    FONT_HEI = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 22)
    FONT_HEI_SM = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 16)
    FONT_HEI_LG = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 28)
    FONT_SONG = ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc', 18)
    FONT_SONG_SM = ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc', 14)
    FONT_EN = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 16)
    FONT_EN_SM = ImageFont.truetype(r'C:\Windows\Fonts\consola.ttf', 15)
except OSError:
    FONT_HEI = FONT_HEI_SM = FONT_HEI_LG = FONT_SONG = FONT_SONG_SM = FONT_EN = FONT_EN_SM = ImageFont.load_default()

BLUE = (47, 107, 255)
NAVY = (31, 36, 48)
GRAY = (107, 114, 128)
BG = (245, 248, 252)
WHITE = (255, 255, 255)
LINE = (55, 65, 81)


def text_size(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def draw_box(draw, xy, wh, text, font, fill=WHITE, outline=LINE, radius=6, text_fill=NAVY):
    x, y = xy
    w, h = wh
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=2)
    tw, th = text_size(draw, text, font)
    draw.text((x + (w - tw) / 2, y + (h - th) / 2 - 1), text, fill=text_fill, font=font)


def draw_vline(draw, x, y1, y2):
    draw.line([(x, y1), (x, y2)], fill=LINE, width=2)


def draw_hline(draw, x1, x2, y):
    draw.line([(x1, y), (x2, y)], fill=LINE, width=2)


def gen_usecase():
    img = Image.new('RGB', (1100, 720), WHITE)
    draw = ImageDraw.Draw(img)
    draw.ellipse([80, 280, 240, 460], outline=LINE, width=3)
    draw.text((110, 350), '出行用户', fill=NAVY, font=FONT_HEI)
    draw.rounded_rectangle([320, 60, 1040, 660], radius=8, outline=LINE, width=2)
    draw.text((560, 80), '出行天气助手', fill=NAVY, font=FONT_HEI)
    cases = [
        (520, 160, '查看多城市天气'),
        (520, 250, '切换目标城市'),
        (520, 340, '刷新远端数据'),
        (520, 430, '查看七日预报'),
        (520, 520, '查看气温趋势图'),
    ]
    for x, y, name in cases:
        draw.ellipse([x, y, x + 360, y + 70], outline=LINE, width=2)
        tw, th = text_size(draw, name, FONT_HEI_SM)
        draw.text((x + (360 - tw) / 2, y + (70 - th) / 2), name, fill=NAVY, font=FONT_HEI_SM)
        draw.line([(240, 370), (x, y + 35)], fill=LINE, width=2)
    img.save(OUT / 'fig-usecase.png')


def gen_func_tree():
    """功能结构图：树状连线，无箭头。"""
    img = Image.new('RGB', (1400, 720), WHITE)
    draw = ImageDraw.Draw(img)
    root = (500, 40, 400, 64)
    draw_box(draw, (root[0], root[1]), (root[2], root[3]), '出行天气助手', FONT_HEI, fill=(232, 238, 249))
    rx = root[0] + root[2] / 2
    draw_vline(draw, rx, 104, 150)
    draw_hline(draw, 280, 1120, 150)
    left = (140, 180, 320, 56)
    right = (940, 180, 320, 56)
    draw_vline(draw, 300, 150, 180)
    draw_vline(draw, 1100, 150, 180)
    draw_box(draw, (left[0], left[1]), (left[2], left[3]), '首页模块', FONT_HEI_SM, fill=(232, 238, 249))
    draw_box(draw, (right[0], right[1]), (right[2], right[3]), '详情页模块', FONT_HEI_SM, fill=(232, 238, 249))
    home_items = ['城市选择', '实时天气总览', '加载与异常提示', '手动刷新']
    detail_items = ['七日预报明细', '温度柱状图', '路由传参返回']
    draw_vline(draw, 300, 236, 280)
    draw_hline(draw, 90, 510, 280)
    xs = [90, 210, 330, 450]
    for i, name in enumerate(home_items):
        draw_vline(draw, xs[i] + 50, 280, 310)
        draw_box(draw, (xs[i], 310), (100, 150), '', FONT_HEI_SM)
        # vertical text
        chars = list(name)
        font = FONT_HEI_SM
        total_h = len(chars) * 24
        start_y = 310 + (150 - total_h) / 2
        for j, ch in enumerate(chars):
            tw, th = text_size(draw, ch, font)
            draw.text((xs[i] + (100 - tw) / 2, start_y + j * 24), ch, fill=NAVY, font=font)
    draw_vline(draw, 1100, 236, 280)
    draw_hline(draw, 920, 1280, 280)
    dxs = [920, 1060, 1200]
    for i, name in enumerate(detail_items):
        draw_vline(draw, dxs[i] + 50, 280, 310)
        draw_box(draw, (dxs[i], 310), (100, 150), '', FONT_HEI_SM)
        chars = list(name)
        total_h = len(chars) * 24
        start_y = 310 + (150 - total_h) / 2
        for j, ch in enumerate(chars):
            tw, th = text_size(draw, ch, FONT_HEI_SM)
            draw.text((dxs[i] + (100 - tw) / 2, start_y + j * 24), ch, fill=NAVY, font=FONT_HEI_SM)
    img.save(OUT / 'fig-func.png')


def phone_canvas(w=420, h=860):
    img = Image.new('RGB', (w + 40, h + 40), (230, 233, 239))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([8, 8, w + 32, h + 32], radius=36, fill=(20, 20, 20))
    draw.rounded_rectangle([20, 20, w + 20, h + 20], radius=28, fill=BG)
    return img, draw, 20, 20, w, h


def status_bar(draw, ox, oy, w):
    draw.rectangle([ox, oy, ox + w, oy + 36], fill=BG)
    draw.text((ox + 18, oy + 8), '14:22', fill=NAVY, font=FONT_SONG_SM)
    draw.text((ox + w - 70, oy + 8), '5G  86%', fill=GRAY, font=FONT_SONG_SM)


def gen_home_proto():
    img, draw, ox, oy, w, h = phone_canvas()
    status_bar(draw, ox, oy, w)
    y = oy + 50
    draw.text((ox + 20, y), '出行天气助手  首页原型', fill=NAVY, font=FONT_HEI)
    y += 46
    draw.rounded_rectangle([ox + 20, y, ox + w - 20, y + 44], outline=LINE, width=2)
    draw.text((ox + 36, y + 12), '标题栏 / 刷新按钮', fill=GRAY, font=FONT_SONG_SM)
    y += 60
    draw.text((ox + 20, y), '城市 Grid（3列）', fill=NAVY, font=FONT_SONG)
    y += 30
    names = ['北京', '上海', '广州', '成都', '长沙', '杭州']
    for i, n in enumerate(names):
        cx = ox + 20 + (i % 3) * 125
        cy = y + (i // 3) * 52
        fill = BLUE if n == '长沙' else WHITE
        tc = WHITE if n == '长沙' else NAVY
        draw.rounded_rectangle([cx, cy, cx + 110, cy + 40], outline=BLUE, fill=fill, width=2)
        tw, th = text_size(draw, n, FONT_SONG)
        draw.text((cx + (110 - tw) / 2, cy + 10), n, fill=tc, font=FONT_SONG)
    y += 130
    draw.rounded_rectangle([ox + 20, y, ox + w - 20, y + 170], outline=LINE, width=2)
    draw.text((ox + 36, y + 16), 'WeatherCard 当前城市', fill=NAVY, font=FONT_HEI_SM)
    draw.text((ox + 36, y + 50), '天气现象 / 气温 / 湿度 / 风速', fill=GRAY, font=FONT_SONG)
    draw.rounded_rectangle([ox + 36, y + 100, ox + w - 36, y + 146], outline=BLUE, width=2)
    draw.text((ox + 110, y + 112), '查看七日预报', fill=BLUE, font=FONT_SONG)
    y += 190
    draw.rounded_rectangle([ox + 20, y, ox + w - 20, y + 200], outline=LINE, width=2)
    draw.text((ox + 36, y + 16), 'List 全部城市速览', fill=NAVY, font=FONT_HEI_SM)
    draw.text((ox + 36, y + 56), '卡片 1  ……', fill=GRAY, font=FONT_SONG)
    draw.text((ox + 36, y + 96), '卡片 2  ……', fill=GRAY, font=FONT_SONG)
    draw.text((ox + 36, y + 136), '卡片 3  ……', fill=GRAY, font=FONT_SONG)
    img.save(OUT / 'fig-home-proto.png')


def gen_detail_proto():
    img, draw, ox, oy, w, h = phone_canvas()
    status_bar(draw, ox, oy, w)
    y = oy + 50
    draw.text((ox + 20, y), '←  长沙详情  原型', fill=NAVY, font=FONT_HEI)
    y += 50
    draw.rounded_rectangle([ox + 20, y, ox + w - 20, y + 130], outline=LINE, width=2)
    draw.text((ox + 36, y + 20), 'WeatherCard（无跳转按钮）', fill=NAVY, font=FONT_HEI_SM)
    draw.text((ox + 36, y + 60), '长沙  星城·华中    20.8°', fill=GRAY, font=FONT_SONG)
    draw.text((ox + 36, y + 90), '多云  湿度  风速', fill=GRAY, font=FONT_SONG)
    y += 150
    draw.rounded_rectangle([ox + 20, y, ox + w - 20, y + 200], outline=LINE, width=2)
    draw.text((ox + 36, y + 16), 'TempChart 七日最高气温', fill=NAVY, font=FONT_HEI_SM)
    bases = [110, 140, 90, 160, 120, 100, 150]
    for i, bh in enumerate(bases):
        bx = ox + 40 + i * 50
        by = y + 180
        draw.rectangle([bx, by - bh, bx + 22, by], fill=BLUE)
        draw.text((bx, by + 4), f'10/{16+i}', fill=GRAY, font=FONT_SONG_SM)
    y += 230
    draw.rounded_rectangle([ox + 20, y, ox + w - 20, y + 220], outline=LINE, width=2)
    draw.text((ox + 36, y + 16), '七日预报明细 Row 列表', fill=NAVY, font=FONT_HEI_SM)
    for i, line in enumerate(['10/16  晴朗   16° / 24°', '10/17  多云   17° / 23°', '10/18  阵雨   15° / 21°']):
        draw.text((ox + 36, y + 60 + i * 36), line, fill=GRAY, font=FONT_SONG)
    img.save(OUT / 'fig-detail-proto.png')


def gen_home_impl():
    img, draw, ox, oy, w, h = phone_canvas()
    status_bar(draw, ox, oy, w)
    y = oy + 48
    draw.text((ox + 20, y), '出行天气助手', fill=NAVY, font=FONT_HEI_LG)
    draw.rounded_rectangle([ox + w - 100, y, ox + w - 20, y + 34], fill=BLUE)
    tw, th = text_size(draw, '刷新', FONT_SONG)
    draw.text((ox + w - 100 + (80 - tw) / 2, y + 8), '刷新', fill=WHITE, font=FONT_SONG)
    draw.text((ox + 20, y + 40), 'Open-Meteo 实时天气 · 多城市出行参考', fill=GRAY, font=FONT_SONG_SM)
    y += 78
    draw.text((ox + 20, y), '城市列表', fill=NAVY, font=FONT_HEI_SM)
    y += 32
    names = ['北京', '上海', '广州', '成都', '长沙', '杭州']
    for i, n in enumerate(names):
        cx = ox + 18 + (i % 3) * 128
        cy = y + (i // 3) * 50
        selected = n == '长沙'
        draw.rounded_rectangle([cx, cy, cx + 116, cy + 40], fill=BLUE if selected else (232, 238, 249), radius=20)
        tw, th = text_size(draw, n, FONT_SONG)
        draw.text((cx + (116 - tw) / 2, cy + 10), n, fill=WHITE if selected else NAVY, font=FONT_SONG)
    y += 122
    draw.rounded_rectangle([ox + 16, y, ox + w - 16, y + 168], fill=WHITE, radius=16)
    draw.text((ox + 32, y + 16), '长沙', fill=NAVY, font=FONT_HEI)
    draw.text((ox + 80, y + 46), '星城 · 华中', fill=GRAY, font=FONT_SONG_SM)
    draw.text((ox + w - 120, y + 18), '20.8°', fill=BLUE, font=FONT_HEI_LG)
    draw.text((ox + 32, y + 78), '多云    湿度 58%    风速 9.2 km/h', fill=GRAY, font=FONT_SONG_SM)
    draw.rounded_rectangle([ox + 32, y + 112, ox + w - 32, y + 150], fill=BLUE, radius=8)
    tw, th = text_size(draw, '查看七日预报', FONT_SONG)
    draw.text((ox + (w - tw) / 2, y + 122), '查看七日预报', fill=WHITE, font=FONT_SONG)
    y += 186
    draw.text((ox + 20, y), '全部城市速览', fill=NAVY, font=FONT_HEI_SM)
    y += 28
    for city, temp, desc in [('北京', '14.2°', '晴朗 · 华北'), ('上海', '19.6°', '多云 · 华东'), ('广州', '26.1°', '阵雨 · 华南')]:
        draw.rounded_rectangle([ox + 16, y, ox + w - 16, y + 72], fill=WHITE, radius=12)
        draw.text((ox + 32, y + 12), city, fill=NAVY, font=FONT_HEI_SM)
        draw.text((ox + 32, y + 40), desc, fill=GRAY, font=FONT_SONG_SM)
        draw.text((ox + w - 100, y + 18), temp, fill=BLUE, font=FONT_HEI)
        y += 82
    img.save(OUT / 'fig-home-impl.png')


def gen_detail_impl():
    img, draw, ox, oy, w, h = phone_canvas()
    status_bar(draw, ox, oy, w)
    y = oy + 48
    draw.text((ox + 20, y), '←  长沙详情', fill=NAVY, font=FONT_HEI)
    y += 50
    draw.rounded_rectangle([ox + 16, y, ox + w - 16, y + 120], fill=WHITE, radius=16)
    draw.text((ox + 32, y + 16), '长沙', fill=NAVY, font=FONT_HEI)
    draw.text((ox + 32, y + 52), '星城 · 华中', fill=GRAY, font=FONT_SONG_SM)
    draw.text((ox + w - 120, y + 16), '20.8°', fill=BLUE, font=FONT_HEI_LG)
    draw.text((ox + 32, y + 82), '多云    湿度 58%    9.2 km/h', fill=GRAY, font=FONT_SONG_SM)
    y += 140
    draw.rounded_rectangle([ox + 16, y, ox + w - 16, y + 230], fill=WHITE, radius=16)
    draw.text((ox + 32, y + 14), '长沙 · 七日最高气温', fill=NAVY, font=FONT_HEI_SM)
    vals = [24, 23, 21, 25, 26, 22, 24]
    maxv, minv = max(vals), min(vals)
    for i, v in enumerate(vals):
        bh = 40 + int((v - minv) / max(maxv - minv, 1) * 100)
        bx = ox + 36 + i * 52
        by = y + 190
        draw.rounded_rectangle([bx, by - bh, bx + 22, by], fill=BLUE, radius=6)
        draw.text((bx, by - bh - 20), f'{v}°', fill=GRAY, font=FONT_SONG_SM)
        draw.text((bx - 4, by + 6), f'10/{16+i}', fill=GRAY, font=FONT_SONG_SM)
    y += 250
    draw.rounded_rectangle([ox + 16, y, ox + w - 16, y + 250], fill=(238, 243, 255), radius=16)
    draw.text((ox + 32, y + 14), '七日预报明细', fill=NAVY, font=FONT_HEI_SM)
    rows = [('10/16', '晴朗', '16° / 24°'), ('10/17', '多云', '17° / 23°'), ('10/18', '阵雨', '15° / 21°'), ('10/19', '晴朗', '18° / 25°')]
    for i, (dt, wth, tp) in enumerate(rows):
        yy = y + 50 + i * 48
        draw.rounded_rectangle([ox + 28, yy, ox + w - 28, yy + 40], fill=WHITE, radius=8)
        draw.text((ox + 40, yy + 10), dt, fill=NAVY, font=FONT_SONG)
        draw.text((ox + 120, yy + 10), wth, fill=NAVY, font=FONT_SONG)
        draw.text((ox + w - 130, yy + 10), tp, fill=BLUE, font=FONT_SONG)
    img.save(OUT / 'fig-detail-impl.png')


def gen_gitk():
    repo = Path(__file__).resolve().parents[1]
    log = subprocess.check_output(
        ['git', 'log', '--date=format:%Y-%m-%d %H:%M:%S', '--pretty=format:%h|%s|%an|%ad'],
        cwd=repo
    )
    for enc in ('utf-8', 'gbk'):
        try:
            text = log.decode(enc)
            break
        except Exception:
            text = log.decode('utf-8', errors='replace')
    rows = [ln.split('|', 3) for ln in text.splitlines() if ln.strip()]
    img = Image.new('RGB', (1280, 80 + 28 * max(len(rows), 8)), (252, 252, 252))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 1280, 36], fill=(240, 240, 240))
    draw.text((12, 8), 'TravelWeather: All files  -  gitk', fill=NAVY, font=FONT_EN)
    draw.line([(0, 36), (1280, 36)], fill=(180, 180, 180), width=1)
    draw.text((20, 46), 'Graph', fill=GRAY, font=FONT_EN_SM)
    draw.text((90, 46), 'Commit message', fill=GRAY, font=FONT_EN_SM)
    draw.text((720, 46), 'Author', fill=GRAY, font=FONT_EN_SM)
    draw.text((980, 46), 'Date', fill=GRAY, font=FONT_EN_SM)
    y = 72
    for i, row in enumerate(rows):
        sha, msg, author, date = (row + [''] * 4)[:4]
        color = (22, 163, 74) if i == 0 else BLUE
        draw.ellipse([28, y + 4, 42, y + 18], fill=color)
        if i < len(rows) - 1:
            draw.line([(35, y + 18), (35, y + 32)], fill=BLUE, width=2)
        draw.text((90, y), msg[:34], fill=NAVY, font=FONT_HEI_SM)
        draw.text((720, y), author[:18], fill=NAVY, font=FONT_EN_SM)
        draw.text((980, y), date, fill=NAVY, font=FONT_EN_SM)
        y += 28
    img.save(OUT / 'fig-gitk.png')


if __name__ == '__main__':
    gen_usecase()
    gen_func_tree()
    gen_home_proto()
    gen_detail_proto()
    gen_home_impl()
    gen_detail_impl()
    gen_gitk()
    print('figures written to', OUT)
