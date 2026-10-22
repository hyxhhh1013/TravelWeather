import {
  CityInfo,
  CurrentWeather,
  weatherCodeToEmoji,
  weatherCodeToText
} from '../model/WeatherModels'

/**
 * 可复用城市天气卡片（状态管理 V2）
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
    windSpeed: 0
  }
  @Param showAction: boolean = true
  @Event onOpenDetail: () => void = () => {}

  build() {
    Column({ space: 12 }) {
      Row() {
        Text(weatherCodeToEmoji(this.current.weatherCode))
          .fontSize(36)
        Column({ space: 4 }) {
          Text(this.city.name)
            .fontSize(20)
            .fontWeight(FontWeight.Medium)
            .fontColor($r('app.color.text_primary'))
          Text(this.city.desc)
            .fontSize(13)
            .fontColor($r('app.color.text_secondary'))
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)
        .margin({ left: 12 })

        Text(`${this.current.temperature.toFixed(1)}°`)
          .fontSize(32)
          .fontWeight(FontWeight.Bold)
          .fontColor($r('app.color.brand_blue'))
      }
      .width('100%')

      Row({ space: 16 }) {
        Text(weatherCodeToText(this.current.weatherCode))
        Text(`湿度 ${this.current.humidity}%`)
        Text(`风速 ${this.current.windSpeed.toFixed(1)} km/h`)
      }
      .width('100%')
      .fontSize(13)
      .fontColor($r('app.color.text_secondary'))

      if (this.showAction) {
        Button('查看七日预报')
          .width('100%')
          .height(40)
          .backgroundColor($r('app.color.brand_blue'))
          .onClick(() => {
            this.onOpenDetail()
          })
      }
    }
    .width('100%')
    .padding(16)
    .borderRadius(16)
    .backgroundColor($r('app.color.card_background'))
    .shadow({
      radius: 12,
      color: '#1A2F6BFF',
      offsetX: 0,
      offsetY: 4
    })
  }
}
