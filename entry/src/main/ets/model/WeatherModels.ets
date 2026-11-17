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
  isDay: boolean
}

export interface DailyForecast {
  dates: string[]
  tempMax: number[]
  tempMin: number[]
  weatherCodes: number[]
}

export interface HourlyPoint {
  label: string
  temperature: number
  weatherCode: number
  isDay: boolean
}

export interface WeatherBundle {
  city: CityInfo
  current: CurrentWeather
  daily: DailyForecast
  hourly: HourlyPoint[]
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

export type WeatherTone = 'clear' | 'cloud' | 'rain' | 'snow' | 'fog' | 'storm'

export function isWetWeather(code: number): boolean {
  if (code >= 51 && code <= 67) {
    return true
  }
  if (code >= 71 && code <= 77) {
    return true
  }
  if (code >= 80 && code <= 82) {
    return true
  }
  if (code >= 95) {
    return true
  }
  return false
}

export function weatherTone(code: number): WeatherTone {
  if (code === 0) {
    return 'clear'
  }
  if (code === 45 || code === 48) {
    return 'fog'
  }
  if (code >= 71 && code <= 77) {
    return 'snow'
  }
  if (code >= 95) {
    return 'storm'
  }
  if (isWetWeather(code)) {
    return 'rain'
  }
  if (code <= 3) {
    return 'cloud'
  }
  return 'cloud'
}

export function travelAdvice(temperature: number, weatherCode: number): string {
  if (weatherCode >= 95) {
    return '有雷雨，尽量改到室内'
  }
  if (weatherCode >= 71 && weatherCode <= 77) {
    return '有雪，路面湿滑，穿防滑鞋'
  }
  if (isWetWeather(weatherCode)) {
    return '可能下雨，出门带伞'
  }
  if (weatherCode === 45 || weatherCode === 48) {
    return '有雾，能见度不高，提前出门'
  }
  if (temperature <= 5) {
    return '气温偏低，注意保暖'
  }
  if (temperature >= 30) {
    return '天气炎热，注意防晒补水'
  }
  if (temperature <= 12) {
    return '早晚偏凉，带一件薄外套'
  }
  return '天气合适，适合出门'
}

export interface WeekBrief {
  lowest: number
  highest: number
  wetDays: number
  tip: string
}

export function buildWeekBrief(daily: DailyForecast): WeekBrief {
  let lowest = 0
  let highest = 0
  let wetDays = 0
  if (daily.tempMin.length > 0) {
    lowest = daily.tempMin[0]
  }
  if (daily.tempMax.length > 0) {
    highest = daily.tempMax[0]
  }
  const count = daily.dates.length
  for (let i = 0; i < count; i++) {
    const dayMin = daily.tempMin[i] ?? lowest
    const dayMax = daily.tempMax[i] ?? highest
    if (dayMin < lowest) {
      lowest = dayMin
    }
    if (dayMax > highest) {
      highest = dayMax
    }
    const code = daily.weatherCodes[i] ?? 0
    if (isWetWeather(code)) {
      wetDays = wetDays + 1
    }
  }
  let tip = '这一周气温平稳，轻装即可'
  if (wetDays >= 4) {
    tip = `这周有 ${wetDays} 天可能下雨或降雪，记得带伞`
  } else if (wetDays > 0 && lowest <= 8) {
    tip = `最低 ${lowest.toFixed(0)}°，还有 ${wetDays} 天降水，外套和伞都带上`
  } else if (lowest <= 5) {
    tip = `最低 ${lowest.toFixed(0)}°，加一件厚外套`
  } else if (lowest <= 12) {
    tip = `早晚会降到 ${lowest.toFixed(0)}°，带一件外套`
  } else if (wetDays > 0) {
    tip = `有 ${wetDays} 天可能降水，包里放一把伞`
  } else if (highest >= 30) {
    tip = `最高 ${highest.toFixed(0)}°，注意防晒和补水`
  }
  return { lowest, highest, wetDays, tip }
}

/**
 * Meteocons 静态图标（MIT，Bas Milius）。文件在 resources/base/media，许可见 third_party/meteocons-LICENSE。
 */
export function weatherIcon(code: number, isDay: boolean): Resource {
  if (code === 0) {
    return isDay ? $r('app.media.wx_clear_day') : $r('app.media.wx_clear_night')
  }
  if (code === 1 || code === 2) {
    return isDay ? $r('app.media.wx_partly_day') : $r('app.media.wx_partly_night')
  }
  if (code === 3) {
    return isDay ? $r('app.media.wx_overcast_day') : $r('app.media.wx_overcast_night')
  }
  if (code === 45 || code === 48) {
    return isDay ? $r('app.media.wx_fog_day') : $r('app.media.wx_fog_night')
  }
  if ((code >= 71 && code <= 77) || code === 85 || code === 86) {
    return isDay ? $r('app.media.wx_snow_day') : $r('app.media.wx_snow_night')
  }
  if (code >= 95) {
    return isDay ? $r('app.media.wx_storm_day') : $r('app.media.wx_storm_night')
  }
  if (code >= 80 && code <= 82) {
    return isDay ? $r('app.media.wx_shower_day') : $r('app.media.wx_shower_night')
  }
  if ((code >= 51 && code <= 67)) {
    return isDay ? $r('app.media.wx_rain_day') : $r('app.media.wx_rain_night')
  }
  return isDay ? $r('app.media.wx_partly_day') : $r('app.media.wx_partly_night')
}

export function skyStops(code: number, isDay: boolean): Array<[string, number]> {
  const tone = weatherTone(code)
  if (!isDay) {
    if (tone === 'clear') {
      return [['#071428', 0], ['#16356E', 0.55], ['#2A558F', 1]]
    }
    if (tone === 'rain') {
      return [['#101820', 0], ['#243246', 0.6], ['#3A4C62', 1]]
    }
    if (tone === 'snow') {
      return [['#1C2838', 0], ['#3A4C62', 1]]
    }
    if (tone === 'fog') {
      return [['#242A32', 0], ['#4A545E', 1]]
    }
    if (tone === 'storm') {
      return [['#120E24', 0], ['#3A2860', 1]]
    }
    return [['#161E2C', 0], ['#3A4A62', 1]]
  }
  if (tone === 'clear') {
    return [['#1A6FE0', 0], ['#3AA4F2', 0.48], ['#8EDBFF', 1]]
  }
  if (tone === 'rain') {
    return [['#1A335F', 0], ['#3E6294', 0.55], ['#6E8EBE', 1]]
  }
  if (tone === 'snow') {
    return [['#3A6794', 0], ['#8EB3D4', 1]]
  }
  if (tone === 'fog') {
    return [['#56616F', 0], ['#8E99A8', 1]]
  }
  if (tone === 'storm') {
    return [['#261E52', 0], ['#624892', 1]]
  }
  return [['#46586F', 0], ['#6E849C', 0.5], ['#B7C6D6', 1]]
}

export function dayTitle(date: string): string {
  const now = new Date()
  const month = `${now.getMonth() + 1}`.padStart(2, '0')
  const day = `${now.getDate()}`.padStart(2, '0')
  const today = `${now.getFullYear()}-${month}-${day}`
  if (date === today) {
    return '今天'
  }
  return weekdayLabel(date)
}

export function weekdayLabel(date: string): string {
  const parts = date.split('-')
  if (parts.length < 3) {
    return ''
  }
  const parsed = new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]))
  const names: string[] = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const index = parsed.getDay()
  if (index < 0 || index >= names.length) {
    return ''
  }
  return names[index]
}

export function formatTemp(value: number): string {
  const rounded = Math.round(value)
  if (rounded === 0) {
    return '0°'
  }
  return `${rounded}°`
}

export function shortDate(date: string): string {
  if (date.length >= 10) {
    return date.substring(5)
  }
  return date
}
