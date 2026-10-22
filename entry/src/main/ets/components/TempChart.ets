/**
 * 简易温度柱状图（加分项：数据可视化）
 * 使用网络返回的每日最高温动态绘制
 */
@ComponentV2
export struct TempChart {
  @Param title: string = '未来气温趋势'
  @Param labels: string[] = []
  @Param values: number[] = []

  private maxValue(): number {
    if (this.values.length === 0) {
      return 1
    }
    let max = this.values[0]
    for (let i = 1; i < this.values.length; i++) {
      if (this.values[i] > max) {
        max = this.values[i]
      }
    }
    return max <= 0 ? 1 : max
  }

  private minValue(): number {
    if (this.values.length === 0) {
      return 0
    }
    let min = this.values[0]
    for (let i = 1; i < this.values.length; i++) {
      if (this.values[i] < min) {
        min = this.values[i]
      }
    }
    return min
  }

  private barHeight(value: number): number {
    const min = this.minValue()
    const max = this.maxValue()
    const span = Math.max(max - min, 1)
    return 40 + ((value - min) / span) * 100
  }

  private shortLabel(date: string): string {
    if (date.length >= 10) {
      return date.substring(5)
    }
    return date
  }

  build() {
    Column({ space: 12 }) {
      Text(this.title)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
        .fontColor($r('app.color.text_primary'))
        .width('100%')

      if (this.values.length === 0) {
        Text('暂无图表数据')
          .fontSize(14)
          .fontColor($r('app.color.text_secondary'))
          .width('100%')
          .textAlign(TextAlign.Center)
          .padding(24)
      } else {
        Row({ space: 8 }) {
          ForEach(this.values, (value: number, index: number) => {
            Column({ space: 6 }) {
              Text(`${value.toFixed(0)}°`)
                .fontSize(11)
                .fontColor($r('app.color.text_secondary'))
              Column()
                .width(18)
                .height(this.barHeight(value))
                .borderRadius(8)
                .linearGradient({
                  angle: 180,
                  colors: [['#6EA8FF', 0], ['#2F6BFF', 1]]
                })
              Text(this.shortLabel(this.labels[index] ?? ''))
                .fontSize(10)
                .fontColor($r('app.color.text_secondary'))
            }
            .layoutWeight(1)
            .alignItems(HorizontalAlign.Center)
            .justifyContent(FlexAlign.End)
            .height(170)
          }, (value: number, index: number) => `${index}-${value}`)
        }
        .width('100%')
        .alignItems(VerticalAlign.Bottom)
      }
    }
    .width('100%')
    .padding(16)
    .borderRadius(16)
    .backgroundColor($r('app.color.card_background'))
  }
}
