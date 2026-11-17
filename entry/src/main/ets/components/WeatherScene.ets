import { weatherIcon } from '../model/WeatherModels'

/**
 * 天空右侧的天气图标，使用 Meteocons 静态图。
 */
@ComponentV2
export struct WeatherScene {
  @Param weatherCode: number = 0
  @Param isDay: boolean = true

  build() {
    Image(weatherIcon(this.weatherCode, this.isDay))
      .width(148)
      .height(148)
      .objectFit(ImageFit.Contain)
  }
}
