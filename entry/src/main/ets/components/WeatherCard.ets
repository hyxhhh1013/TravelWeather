import { WeatherScene } from './WeatherScene'
import {
  CityInfo,
  CurrentWeather,
  formatTemp,
  travelAdvice,
  weatherCodeToText,
  WeatherTone,
  weatherTone
} from '../model/WeatherModels'

/**
 * 可复用城市天气主卡片（状态管理 V2）
 * 背景随天气变化，展示当前气温、湿度和出行建议
 */
@ComponentV2
export struct WeatherCard {
  @Param city: CityInfo = {
    id: '',
    name: '',
    latitude: 0,
    longitude: 0,
    desc: ''
  }
  @Param current: CurrentWeather = {
    temperature: 0,
    humidity: 0,
    weatherCode: 0,
    windSpeed: 0,
    isDay: true
  }
  @Param high: number = 0
  @Param low: number = 0
  @Param showRange: boolean = false
  @Param showAction: boolean = true
  @Event onOpenDetail: () => void = () => {}

  private tone(): WeatherTone {
    return weatherTone(this.current.weatherCode)
  }

  private gradientStops(): Array<[string, number]> {
    const tone = this.tone()
    if (tone === 'clear') {
      return [['#1565E0', 0], ['#3EC6FF', 1]]
    }
    if (tone === 'rain') {
      return [['#1E3A6E', 0], ['#4E7BB5', 1]]
    }
    if (tone === 'snow') {
      return [['#3E6C99', 0], ['#8FB4D4', 1]]
    }
    if (tone === 'fog') {
      return [['#5A6573', 0], ['#8E99A8', 1]]
    }
    if (tone === 'storm') {
      return [['#2C2158', 0], ['#6A4E9A', 1]]
    }
    return [['#4A5D78', 0], ['#8AA0B8', 1]]
  }

  @Builder
  private Metric(label: string, value: string) {
    Column({ space: 2 }) {
      Text(label)
        .fontSize(12)
        .fontColor('#E7F2FF')
      Text(value)
        .fontSize(18)
        .fontWeight(FontWeight.Medium)
        .fontColor(Color.White)
    }
    .width('100%')
    .height(62)
    .padding({ left: 14, right: 14 })
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Start)
    .borderRadius(14)
    .backgroundColor('#2EFFFFFF')
  }

  build() {
    Column({ space: 12 }) {
      Row() {
        Column({ space: 4 }) {
          Text(this.city.name)
            .fontSize(22)
            .fontWeight(FontWeight.Bold)
            .fontColor(Color.White)
          Text(this.city.desc)
            .fontSize(13)
            .fontColor('#E7F2FF')
          Text(`${this.current.temperature.toFixed(1)}°`)
            .fontSize(48)
            .fontWeight(FontWeight.Bold)
            .fontColor(Color.White)
            .margin({ top: 4 })
          Text(weatherCodeToText(this.current.weatherCode))
            .fontSize(15)
            .fontColor(Color.White)
          if (this.showRange) {
            Text(`最低 ${formatTemp(this.low)}  最高 ${formatTemp(this.high)}`)
              .fontSize(13)
              .fontColor('#E7F2FF')
          }
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)

        WeatherScene({ weatherCode: this.current.weatherCode, isDay: this.current.isDay })
      }
      .width('100%')
      .alignItems(VerticalAlign.Center)

      Grid() {
        GridItem() {
          this.Metric('湿度', `${this.current.humidity}%`)
        }
        GridItem() {
          this.Metric('风速', `${this.current.windSpeed.toFixed(1)} km/h`)
        }
      }
      .columnsTemplate('1fr 1fr')
      .columnsGap(10)
      .rowsTemplate('1fr')
      .width('100%')
      .height(62)

      Text(travelAdvice(this.current.temperature, this.current.weatherCode))
        .fontSize(14)
        .fontColor(Color.White)
        .width('100%')

      if (this.showAction) {
        Text('查看七日预报  ›')
          .fontSize(13)
          .fontColor(Color.White)
          .width('100%')
          .margin({ top: 2 })
      }
    }
    .width('100%')
    .padding(20)
    .borderRadius(24)
    .clip(true)
    .linearGradient({
      angle: 145,
      colors: this.gradientStops()
    })
    .onClick(() => {
      if (this.showAction) {
        this.onOpenDetail()
      }
    })
  }
}
