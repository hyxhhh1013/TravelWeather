import { CityInfo } from '../model/WeatherModels'

/** 预设城市列表（国内主要出行城市） */
export const CITY_LIST: CityInfo[] = [
  {
    id: 'beijing',
    name: '北京',
    latitude: 39.9042,
    longitude: 116.4074,
    desc: '首都 · 华北'
  },
  {
    id: 'shanghai',
    name: '上海',
    latitude: 31.2304,
    longitude: 121.4737,
    desc: '魔都 · 华东'
  },
  {
    id: 'guangzhou',
    name: '广州',
    latitude: 23.1291,
    longitude: 113.2644,
    desc: '花城 · 华南'
  },
  {
    id: 'chengdu',
    name: '成都',
    latitude: 30.5728,
    longitude: 104.0668,
    desc: '天府 · 西南'
  },
  {
    id: 'changsha',
    name: '长沙',
    latitude: 28.2282,
    longitude: 112.9388,
    desc: '星城 · 华中'
  },
  {
    id: 'hangzhou',
    name: '杭州',
    latitude: 30.2741,
    longitude: 120.1551,
    desc: '天堂 · 华东'
  }
]
