import { formatTemp, shortDate, weekdayLabel } from '../model/WeatherModels'

/**
 * 七日最高 / 最低气温区间图（加分项：数据可视化）
 */
@ComponentV2
export struct TempChart {
  @Param title: string = '七日气温'
  @Param labels: string[] = []
  @Param highs: number[] = []
  @Param lows: number[] = []

  private count(): number {
    let total = this.highs.length
    if (this.lows.length < total) {
      total = this.lows.length
    }
    if (this.labels.length < total) {
      total = this.labels.length
    }
    return total
  }

  private lowBound(): number {
    const total = this.count()
    if (total === 0) {
      return 0
    }
    let min = this.lows[0]
    for (let i = 1; i < total; i++) {
      if (this.lows[i] < min) {
        min = this.lows[i]
      }
    }
    return min
  }

  private highBound(): number {
    const total = this.count()
    if (total === 0) {
      return 1
    }
    let max = this.highs[0]
    for (let i = 1; i < total; i++) {
      if (this.highs[i] > max) {
        max = this.highs[i]
      }
    }
    return max
  }

  private rangeHeight(high: number, low: number): number {
    const span = Math.max(this.highBound() - this.lowBound(), 1)
    const height = ((high - low) / span) * 108
    if (height < 18) {
      return 18
    }
    return height
  }

  private rangeTop(high: number, low: number): number {
    const span = Math.max(this.highBound() - this.lowBound(), 1)
    const top = ((this.highBound() - high) / span) * 108
    const height = this.rangeHeight(high, low)
    const maxTop = 108 - height
    if (top > maxTop) {
      return maxTop
    }
    if (top < 0) {
      return 0
    }
    return top
  }

  build() {
    Column({ space: 14 }) {
      Text(this.title)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
        .fontColor($r('app.color.text_primary'))
        .width('100%')

      if (this.count() === 0) {
        Text('暂无图表数据')
          .fontSize(14)
          .fontColor($r('app.color.text_secondary'))
          .width('100%')
          .textAlign(TextAlign.Center)
          .padding(24)
      } else {
        Row() {
          ForEach(this.highs, (high: number, index: number) => {
            if (index < this.count()) {
              Column({ space: 4 }) {
                Text(formatTemp(high))
                  .fontSize(11)
                  .fontColor($r('app.color.text_primary'))
                Stack({ alignContent: Alignment.Top }) {
                  Column()
                    .width(8)
                    .height(108)
                    .borderRadius(8)
                    .backgroundColor('#E4EAF3')
                  Column()
                    .width(8)
                    .height(this.rangeHeight(high, this.lows[index]))
                    .margin({ top: this.rangeTop(high, this.lows[index]) })
                    .borderRadius(8)
                    .linearGradient({
                      angle: 180,
                      colors: [['#8ECAFF', 0], ['#1F6FE5', 1]]
                    })
                }
                .width(28)
                .height(108)
                Text(formatTemp(this.lows[index]))
                  .fontSize(11)
                  .fontColor($r('app.color.text_secondary'))
                Text(weekdayLabel(this.labels[index] ?? ''))
                  .fontSize(11)
                  .fontColor($r('app.color.text_primary'))
                Text(shortDate(this.labels[index] ?? ''))
                  .fontSize(10)
                  .fontColor($r('app.color.text_secondary'))
              }
              .layoutWeight(1)
              .alignItems(HorizontalAlign.Center)
            }
          }, (high: number, index: number) => `${index}-${high}`)
        }
        .width('100%')
        .alignItems(VerticalAlign.Top)
      }
    }
    .width('100%')
    .padding(16)
    .borderRadius(20)
    .backgroundColor(Color.White)
  }
}
