import {
  CityInfo,
  CurrentWeather,
  skyStops,
  weatherCodeToText
} from '../model/WeatherModels'

/**
 * 其他城市的色卡。点击后首页天空切换到这座城市。
 */
@ComponentV2
export struct CityWeatherRow {
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
  @Param selected: boolean = false
  @Event onOpen: () => void = () => {}

  build() {
    Row() {
      Column({ space: 2 }) {
        Text(this.city.name)
          .fontSize(17)
          .fontWeight(FontWeight.Medium)
          .fontColor(Color.White)
        Text(weatherCodeToText(this.current.weatherCode))
          .fontSize(12)
          .fontColor('#E7F2FF')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Text(`${this.current.temperature.toFixed(0)}°`)
        .fontSize(28)
        .fontWeight(FontWeight.Bold)
        .fontColor(Color.White)
    }
    .width('100%')
    .height(68)
    .padding({ left: 16, right: 16 })
    .borderRadius(18)
    .linearGradient({
      angle: 135,
      colors: skyStops(this.current.weatherCode, this.current.isDay)
    })
    .border({
      width: this.selected ? 2 : 0,
      color: Color.White
    })
    .onClick(() => {
      this.onOpen()
    })
  }
}
