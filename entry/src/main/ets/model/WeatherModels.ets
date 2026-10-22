/**
 * 天气数据模型
 */
export interface CityInfo {
  id: string
  name: string
  latitude: number
  longitude: number
  desc: string
}

export interface CurrentWeather {
  temperature: number
  humidity: number
  weatherCode: number
  windSpeed: number
}

export interface DailyForecast {
  dates: string[]
  tempMax: number[]
  tempMin: number[]
  weatherCodes: number[]
}

export interface WeatherBundle {
  city: CityInfo
  current: CurrentWeather
  daily: DailyForecast
  updatedAt: string
}

export type LoadStatus = 'idle' | 'loading' | 'success' | 'empty' | 'error'

export function weatherCodeToText(code: number): string {
  if (code === 0) {
    return '晴朗'
  }
  if (code === 1 || code === 2) {
    return '多云'
  }
  if (code === 3) {
    return '阴天'
  }
  if (code === 45 || code === 48) {
    return '有雾'
  }
  if (code >= 51 && code <= 67) {
    return '降雨'
  }
  if (code >= 71 && code <= 77) {
    return '降雪'
  }
  if (code >= 80 && code <= 82) {
    return '阵雨'
  }
  if (code >= 95) {
    return '雷暴'
  }
  return '未知'
}

export function weatherCodeToEmoji(code: number): string {
  if (code === 0) {
    return '☀️'
  }
  if (code <= 3) {
    return '⛅'
  }
  if (code <= 48) {
    return '🌫️'
  }
  if (code <= 67 || (code >= 80 && code <= 82)) {
    return '🌧️'
  }
  if (code <= 77) {
    return '❄️'
  }
  return '⛈️'
}
