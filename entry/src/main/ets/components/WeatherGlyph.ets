import { weatherIcon } from '../model/WeatherModels'

/**
 * 小时条和七日行上的小天气图标，和大图同一套。
 */
@ComponentV2
export struct WeatherGlyph {
  @Param weatherCode: number = 0
  @Param isDay: boolean = true
  @Param side: number = 28

  build() {
    Image(weatherIcon(this.weatherCode, this.isDay))
      .width(this.side)
      .height(this.side)
      .objectFit(ImageFit.Contain)
  }
}
