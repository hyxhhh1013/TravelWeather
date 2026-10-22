# 出行天气助手（TravelWeather）

湖南农业大学 · 移动应用开发（2026 秋季）课程大作业。

## 项目简介

面向出行场景的多城市天气查询应用。首页展示城市网格与实时天气卡片，详情页展示七日预报与温度柱状图。数据来自公开天气接口 [Open-Meteo](https://open-meteo.com/)，无需 API Key。

## 技术要点对照

| 作业要求 | 本项目实现 |
| --- | --- |
| 网络交互 + loading/error/empty | `WeatherService` + `LoadStatus` 状态机 |
| Row / Column / List / Grid / Scroll | 首页与详情页布局 |
| ≥1 可复用自定义组件 | `WeatherCard`、`TempChart`（V2） |
| 状态管理 V2 | `@ComponentV2` + `@Local` / `@Param` / `@Event` |
| Navigation ≥2 页 + 传参 + 返回栈 | `HomePage` → `DetailPage`（`CityInfo` 传参） |
| 数据可视化加分 | `TempChart` 绑定七日最高温 |
| Git 分阶段提交 | 见仓库 commit 历史 |

## 环境

- DevEco Studio（HarmonyOS SDK 5.0.0 / API 12）
- **Previewer 预览调试**（不依赖真机）
- 需联网以请求 Open-Meteo

## 目录结构

```
TravelWeather/
├── AppScope/                 # 应用级配置与图标
├── entry/src/main/ets/
│   ├── pages/                # Index / HomePage / DetailPage
│   ├── components/           # WeatherCard、TempChart
│   ├── services/             # WeatherService 网络层
│   ├── model/                # 数据模型
│   └── common/               # 城市常量
├── docs/                     # 课程报告
└── README.md
```

## 运行步骤

1. 用 DevEco Studio 打开本工程目录 `TravelWeather`
2. 等待依赖同步完成
3. 打开 `entry/src/main/ets/pages/Index.ets`，点击 Previewer
4. 首页自动加载 6 个城市天气；点击「查看七日预报」进入详情

## 作者

- 姓名：黄奕轩
- 学号：202440210217
- 专业：计算机科学与技术 24 级
