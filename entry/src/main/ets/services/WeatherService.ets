import http from '@ohos.net.http'
import { CityInfo, CurrentWeather, DailyForecast, WeatherBundle } from '../model/WeatherModels'

/**
 * 使用公开接口 Open-Meteo 获取天气（无需 API Key）
 * 文档：https://open-meteo.com/
 */
export class WeatherService {
  static async fetchWeather(city: CityInfo): Promise<WeatherBundle> {
    const url =
      `https://api.open-meteo.com/v1/forecast?latitude=${city.latitude}` +
      `&longitude=${city.longitude}` +
      `&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m` +
      `&daily=weather_code,temperature_2m_max,temperature_2m_min` +
      `&timezone=Asia%2FShanghai&forecast_days=7`

    const httpRequest = http.createHttp()
    try {
      const response = await httpRequest.request(url, {
        method: http.RequestMethod.GET,
        header: {
          'Content-Type': 'application/json'
        },
        expectDataType: http.HttpDataType.STRING,
        connectTimeout: 15000,
        readTimeout: 15000
      })

      if (response.responseCode !== 200) {
        throw new Error(`HTTP ${response.responseCode}`)
      }

      const raw = typeof response.result === 'string'
        ? response.result
        : JSON.stringify(response.result)
      const data = JSON.parse(raw) as Record<string, Object>

      const currentObj = data['current'] as Record<string, number>
      const dailyObj = data['daily'] as Record<string, Object>

      if (!currentObj || !dailyObj) {
        throw new Error('接口返回数据为空')
      }

      const current: CurrentWeather = {
        temperature: Number(currentObj['temperature_2m'] ?? 0),
        humidity: Number(currentObj['relative_humidity_2m'] ?? 0),
        weatherCode: Number(currentObj['weather_code'] ?? 0),
        windSpeed: Number(currentObj['wind_speed_10m'] ?? 0)
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

      const now = new Date()
      const updatedAt =
        `${now.getHours().toString().padStart(2, '0')}:` +
        `${now.getMinutes().toString().padStart(2, '0')}:` +
        `${now.getSeconds().toString().padStart(2, '0')}`

      return {
        city,
        current,
        daily,
        updatedAt
      }
    } finally {
      httpRequest.destroy()
    }
  }
}
