# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / 'docs' / 'figures' / 'fig1-architecture.png'
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1400, 820
img = Image.new('RGB', (W, H), (255, 255, 255))
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 22)
    font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf', 18)
    font_small = ImageFont.truetype(r'C:\Windows\Fonts\simsun.ttc', 16)
except OSError:
    font_title = font = font_small = ImageFont.load_default()


def box(xy, text, fill, outline='#2F6BFF', w=220, h=72):
    x, y = xy
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=fill, outline=outline, width=2)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x + (w - tw) / 2, y + (h - th) / 2 - 2), text, fill='#1F2430', font=font)


def arrow(p1, p2):
    draw.line([p1, p2], fill='#4B5563', width=3)
    x2, y2 = p2
    draw.polygon([(x2, y2), (x2 - 8, y2 - 12), (x2 + 8, y2 - 12)], fill='#4B5563')


# layers
layers = [
    (40, 70, 1320, 170, '#F3F7FF', '表现层  pages / components'),
    (40, 280, 1320, 170, '#F6FFF4', '业务层  model / common / 状态机'),
    (40, 490, 1320, 170, '#FFF8F0', '数据层  WeatherService + Open-Meteo'),
]
for x, y, w, h, fill, title in layers:
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=fill, outline='#D1D5DB', width=1)
    draw.text((x + 18, y + 12), title, fill='#374151', font=font_title)

box((80, 120), 'Index\nNavigation 宿主', '#FFFFFF', w=230, h=80)
box((360, 120), 'HomePage\n城市 Grid / List', '#FFFFFF', w=250, h=80)
box((660, 120), 'DetailPage\n七日预报', '#FFFFFF', w=230, h=80)
box((980, 120), 'WeatherCard\nTempChart', '#FFFFFF', w=230, h=80)

box((120, 340), 'CityInfo / WeatherBundle', '#FFFFFF', w=320, h=72)
box((520, 340), 'LoadStatus 状态机', '#FFFFFF', w=280, h=72)
box((900, 340), 'CITY_LIST 城市常量', '#FFFFFF', w=280, h=72)

box((180, 550), 'WeatherService.fetchWeather', '#FFFFFF', w=360, h=72)
box((740, 550), 'Open-Meteo HTTPS JSON', '#FFFFFF', w=360, h=72)

arrow((195, 200), (195, 340))
arrow((485, 200), (650, 340))
arrow((775, 200), (650, 340))
arrow((1095, 200), (1040, 340))
arrow((280, 412), (360, 550))
arrow((360, 622), (740, 586))

draw.text((40, 690), '图 1  出行天气助手分层结构', fill='#111827', font=font_title)
draw.text((40, 730), '首页通过 WeatherService 拉取多城市天气，详情页接收 CityInfo 路由参数后再次请求七日数据，', fill='#4B5563', font=font_small)
draw.text((40, 756), 'WeatherCard 与 TempChart 作为可复用组件同时服务于首页与详情页。', fill='#4B5563', font=font_small)

img.save(OUT, 'PNG')
print('wrote', OUT)
