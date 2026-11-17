import http from '@ohos.net.http'
import { CityInfo, CurrentWeather, DailyForecast, HourlyPoint, WeatherBundle } from '../model/WeatherModels'

/**
 * 使用公开接口 Open-Meteo 获取天气（无需 API Key）
 * 文档：https://open-meteo.com/
 */
export class WeatherService {
  static async fetchWeather(city: CityInfo): Promise<WeatherBundle> {
    const url =
      `https://api.open-meteo.com/v1/forecast?latitude=${city.latitude}` +
      `&longitude=${city.longitude}` +
      `&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,is_day` +
      `&hourly=temperature_2m,weather_code,is_day` +
      `&daily=weather_code,temperature_2m_max,temperature_2m_min` +
      `&timezone=Asia%2FShanghai&forecast_days=7`

    const raw = await WeatherService.requestText(url)
    const data = JSON.parse(raw) as Record<string, Object>
    const currentObj = data['current'] as Record<string, number>
    const dailyObj = data['daily'] as Record<string, Object>
    const hourlyObj = data['hourly'] as Record<string, Object>

    if (!currentObj || !dailyObj) {
      throw new Error('接口返回数据为空')
    }

    const current: CurrentWeather = {
      temperature: Number(currentObj['temperature_2m'] ?? 0),
      humidity: Number(currentObj['relative_humidity_2m'] ?? 0),
      weatherCode: Number(currentObj['weather_code'] ?? 0),
      windSpeed: Number(currentObj['wind_speed_10m'] ?? 0),
      isDay: Number(currentObj['is_day'] ?? 1) === 1
    }

    const daily: DailyForecast = {
      dates: (dailyObj['time'] as string[]) ?? [],
      tempMax: (dailyObj['temperature_2m_max'] as number[]) ?? [],
      tempMin: (dailyObj['temperature_2m_min'] as number[]) ?? [],
      weatherCodes: (dailyObj['weather_code'] as number[]) ?? []
    }

    if (daily.dates.length === 0) {
      throw new Error('暂无预报数据')
    }

    const hourly = hourlyObj ? WeatherService.readHourly(hourlyObj) : []

    const now = new Date()
    const updatedAt =
      `${now.getHours().toString().padStart(2, '0')}:` +
      `${now.getMinutes().toString().padStart(2, '0')}:` +
      `${now.getSeconds().toString().padStart(2, '0')}`

    return {
      city,
      current,
      daily,
      hourly,
      updatedAt
    }
  }

  private static readHourly(hourlyObj: Record<string, Object>): HourlyPoint[] {
    const times = (hourlyObj['time'] as string[]) ?? []
    const temps = (hourlyObj['temperature_2m'] as number[]) ?? []
    const codes = (hourlyObj['weather_code'] as number[]) ?? []
    const days = (hourlyObj['is_day'] as number[]) ?? []
    const now = new Date()
    const month = `${now.getMonth() + 1}`.padStart(2, '0')
    const day = `${now.getDate()}`.padStart(2, '0')
    const hour = `${now.getHours()}`.padStart(2, '0')
    const key = `${now.getFullYear()}-${month}-${day}T${hour}`
    let start = 0
    for (let i = 0; i < times.length; i++) {
      if (times[i].indexOf(key) === 0 || times[i] >= key) {
        start = i
        break
      }
    }
    const points: HourlyPoint[] = []
    const end = Math.min(times.length, start + 24)
    for (let i = start; i < end; i++) {
      const time = times[i] ?? ''
      let label = time.length >= 16 ? time.substring(11, 16) : ''
      if (i === start) {
        label = '现在'
      }
      points.push({
        label,
        temperature: Number(temps[i] ?? 0),
        weatherCode: Number(codes[i] ?? 0),
        isDay: Number(days[i] ?? 1) === 1
      })
    }
    return points
  }

  /**
   * 预览器不会继承 Windows 系统代理。这台电脑直连 Open-Meteo 会超时，
   * 本机代理 127.0.0.1:7892 可以访问。先走代理，失败再直连，方便没有代理的环境。
   */
  private static async requestText(url: string): Promise<string> {
    const localProxy: http.HttpProxy = {
      host: '127.0.0.1',
      port: 7892,
      exclusionList: []
    }
    try {
      return await WeatherService.requestOnce(url, localProxy, 8000)
    } catch (proxyErr) {
      return await WeatherService.requestOnce(url, false, 12000)
    }
  }

  private static async requestOnce(url: string, proxy: boolean | http.HttpProxy,
    timeoutMs: number): Promise<string> {
    const httpRequest = http.createHttp()
    try {
      const response = await httpRequest.request(url, {
        method: http.RequestMethod.GET,
        expectDataType: http.HttpDataType.STRING,
        usingProtocol: http.HttpProtocol.HTTP1_1,
        usingProxy: proxy,
        connectTimeout: timeoutMs,
        readTimeout: timeoutMs
      })
      if (response.responseCode !== 200) {
        throw new Error(`HTTP ${response.responseCode}`)
      }
      if (typeof response.result === 'string') {
        return response.result
      }
      return JSON.stringify(response.result)
    } finally {
      httpRequest.destroy()
    }
  }
}
