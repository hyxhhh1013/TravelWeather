import { WeatherGlyph } from './WeatherGlyph'
import { formatTemp } from '../model/WeatherModels'

/**
 * 一日温度范围：最低、对齐到全周刻度的色条、最高
 */
@ComponentV2
export struct DayRangeRow {
  @Param title: string = ''
  @Param weatherCode: number = 0
  @Param low: number = 0
  @Param high: number = 0
  @Param scaleMin: number = 0
  @Param scaleMax: number = 1

  private span(): number {
    return Math.max(this.scaleMax - this.scaleMin, 1)
  }

  private leftWeight(): number {
    return Math.max((this.low - this.scaleMin) / this.span(), 0.02)
  }

  private midWeight(): number {
    return Math.max((this.high - this.low) / this.span(), 0.08)
  }

  private rightWeight(): number {
    return Math.max(1 - this.leftWeight() - this.midWeight(), 0.02)
  }

  build() {
    Row() {
      Text(this.title)
        .width(48)
        .fontSize(15)
        .fontWeight(FontWeight.Medium)
        .fontColor($r('app.color.text_primary'))

      Column() {
        WeatherGlyph({ weatherCode: this.weatherCode, isDay: true, side: 28 })
      }
      .width(32)
      .alignItems(HorizontalAlign.Center)

      Text(formatTemp(this.low))
        .width(36)
        .fontSize(14)
        .fontColor($r('app.color.text_secondary'))
        .textAlign(TextAlign.End)

      Row() {
        Column()
          .layoutWeight(this.leftWeight())
          .height(6)
        Column()
          .layoutWeight(this.midWeight())
          .height(6)
          .borderRadius(3)
          .backgroundColor($r('app.color.brand_blue'))
        Column()
          .layoutWeight(this.rightWeight())
          .height(6)
      }
      .layoutWeight(1)
      .height(6)
      .margin({ left: 10, right: 10 })
      .borderRadius(3)
      .backgroundColor('#E4EAF2')
      .clip(true)

      Text(formatTemp(this.high))
        .width(36)
        .fontSize(14)
        .fontWeight(FontWeight.Medium)
        .fontColor($r('app.color.text_primary'))
    }
    .width('100%')
    .height(40)
    .alignItems(VerticalAlign.Center)
  }
}
