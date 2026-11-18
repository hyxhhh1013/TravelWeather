# 出行天气助手（TravelWeather）

湖南农业大学 · 移动应用开发（2026 秋季）课程大作业。

## 项目简介

面向出行场景的多城市天气查询应用。首页用随实况变化的天空展示当前城市，并列出小时预报、四日温度范围和其余城市色卡；详情页展示七日温度范围与气温图。天气图标使用 [Meteocons](https://github.com/basmilius/weather-icons) 静态图，按昼夜切换。数据来自公开天气接口 [Open-Meteo](https://open-meteo.com/)，无需 API Key。

## 技术要点对照

| 作业要求 | 本项目实现 |
| --- | --- |
| 网络交互 + loading/error/empty | `WeatherService` + `LoadStatus` 状态机 |
| Row / Column / List / Grid / Scroll | 首页与详情页布局 |
| ≥1 可复用自定义组件 | `WeatherScene`、`WeatherGlyph`、`DayRangeRow`、`CityWeatherRow`、`TempChart`（V2） |
| 状态管理 V2 | `@ComponentV2` + `@Local` / `@Param` / `@Event` |
| Navigation ≥2 页 + 传参 + 返回栈 | 首页点「全部」进入 `DetailPage`（`CityInfo` 传参），「返回」弹栈 |
| 数据可视化加分 | `TempChart` 绑定七日最高温与最低温 |
| Git 分阶段提交 | 见仓库 commit 历史 |

## 环境

- DevEco Studio 26（工程 `compatibleSdkVersion` / `targetSdkVersion` 为 26.0.0）
- 课程机房若仍是 DevEco 5，打开前把上述版本改回 `5.0.0(12)`
- **Previewer 预览调试**（不依赖真机）
- 需联网以请求 Open-Meteo。请求会先尝试本机代理，超时后再直连

## 目录结构

```
TravelWeather/
├── AppScope/                 # 应用级配置与图标
├── entry/src/main/ets/
│   ├── pages/                # Index / HomePage / DetailPage
│   ├── components/           # 天气图标、温度范围、城市色卡、气温图
│   ├── services/             # WeatherService 网络层
│   ├── model/                # 数据模型
│   └── common/               # 城市常量
├── docs/                     # 课程报告
└── README.md
```

## 运行步骤

1. 用 DevEco Studio 打开本工程目录 `TravelWeather`
2. 等待依赖同步完成
3. 打开 `entry/src/main/ets/pages/Index.ets`，再点击 Previewer
4. 首页并行加载 6 个城市；点城市色卡切换天空，点「全部」进入详情

## 作者

- 姓名：黄奕轩
- 学号：202440210217
- 专业：计算机科学与技术 24 级
