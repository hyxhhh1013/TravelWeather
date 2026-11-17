import { CITY_LIST } from '../common/CityData'
import { CityWeatherRow } from '../components/CityWeatherRow'
import { DayRangeRow } from '../components/DayRangeRow'
import { WeatherGlyph } from '../components/WeatherGlyph'
import { WeatherScene } from '../components/WeatherScene'
import {
  dayTitle,
  formatTemp,
  HourlyPoint,
  LoadStatus,
  skyStops,
  WeatherBundle,
  weatherCodeToText
} from '../model/WeatherModels'
import { WeatherService } from '../services/WeatherService'

@ComponentV2
struct HomePage {
  pathStack: NavPathStack = new NavPathStack()
  @Local status: LoadStatus = 'idle'
  @Local errorMessage: string = ''
  @Local weatherList: WeatherBundle[] = []
  @Local selectedCityId: string = CITY_LIST[0].id

  aboutToAppear(): void {
    this.loadAllCities()
  }

  private async loadAllCities(): Promise<void> {
    this.status = 'loading'
    this.errorMessage = ''
    const result: WeatherBundle[] = []
    const jobs: Promise<void>[] = []
    let failed = 0

    for (let i = 0; i < CITY_LIST.length; i++) {
      const city = CITY_LIST[i]
      const job = WeatherService.fetchWeather(city).then((bundle: WeatherBundle): void => {
        result.push(bundle)
      }, (): void => {
        failed = failed + 1
      })
      jobs.push(job)
    }
    await Promise.all(jobs)

    const ordered: WeatherBundle[] = []
    for (let i = 0; i < CITY_LIST.length; i++) {
      const cityId = CITY_LIST[i].id
      for (let j = 0; j < result.length; j++) {
        if (result[j].city.id === cityId) {
          ordered.push(result[j])
        }
      }
    }
    this.weatherList = ordered
    if (ordered.length === 0) {
      this.status = failed > 0 ? 'error' : 'empty'
      this.errorMessage = '网络请求失败：六个城市都没有返回数据'
      return
    }
    if (!this.hasSelected()) {
      this.selectedCityId = ordered[0].city.id
    }
    this.status = 'success'
  }

  private findBundle(cityId: string): WeatherBundle | null {
    for (let i = 0; i < this.weatherList.length; i++) {
      if (this.weatherList[i].city.id === cityId) {
        return this.weatherList[i]
      }
    }
    return null
  }

  private hasSelected(): boolean {
    return this.findBundle(this.selectedCityId) !== null
  }

  private selectedBundle(): WeatherBundle {
    const found = this.findBundle(this.selectedCityId)
    if (found) {
      return found
    }
    return this.weatherList[0]
  }

  private scaleMin(): number {
    const daily = this.selectedBundle().daily
    let min = daily.tempMin.length > 0 ? daily.tempMin[0] : 0
    for (let i = 1; i < daily.tempMin.length; i++) {
      if (daily.tempMin[i] < min) {
        min = daily.tempMin[i]
      }
    }
    return min
  }

  private scaleMax(): number {
    const daily = this.selectedBundle().daily
    let max = daily.tempMax.length > 0 ? daily.tempMax[0] : 1
    for (let i = 1; i < daily.tempMax.length; i++) {
      if (daily.tempMax[i] > max) {
        max = daily.tempMax[i]
      }
    }
    return max
  }

  private previewIndexes(): number[] {
    const total = this.selectedBundle().daily.dates.length
    const count = total > 4 ? 4 : total
    const indexes: number[] = []
    for (let i = 0; i < count; i++) {
      indexes.push(i)
    }
    return indexes
  }

  private clockText(): string {
    const raw = this.selectedBundle().updatedAt
    if (raw.length >= 5) {
      return raw.substring(0, 5)
    }
    return raw
  }

  private openDetail(): void {
    this.pathStack.pushPathByName('DetailPage', this.selectedBundle().city)
  }

  @Builder
  private Sky() {
    Stack({ alignContent: Alignment.TopEnd }) {
      WeatherScene({
        weatherCode: this.selectedBundle().current.weatherCode,
        isDay: this.selectedBundle().current.isDay
      })
        .margin({ top: 12, right: 8 })

      Column({ space: 6 }) {
        Row() {
          Text(this.selectedBundle().city.name)
            .fontSize(20)
            .fontWeight(FontWeight.Medium)
            .fontColor(Color.White)
            .layoutWeight(1)
          Text(this.clockText())
            .fontSize(13)
            .fontColor('#E7F2FF')
            .onClick(() => {
              this.loadAllCities()
            })
        }
        .width('68%')

        Text(`${this.selectedBundle().current.temperature.toFixed(0)}°`)
          .fontSize(72)
          .fontWeight(FontWeight.Bold)
          .fontColor(Color.White)

        Text(`${weatherCodeToText(this.selectedBundle().current.weatherCode)} · 最高 ${formatTemp(this.selectedBundle().daily.tempMax[0])}  最低 ${formatTemp(this.selectedBundle().daily.tempMin[0])}`)
          .fontSize(15)
          .fontColor(Color.White)
          .width('70%')
      }
      .alignItems(HorizontalAlign.Start)
      .padding({ left: 24, top: 16, right: 20 })
      .width('100%')
    }
    .width('100%')
    .height(268)
    .clip(true)
  }

  @Builder
  private HourlyStrip() {
    Scroll() {
      Row({ space: 4 }) {
        ForEach(this.selectedBundle().hourly, (point: HourlyPoint, index: number) => {
          Column({ space: 6 }) {
            Text(point.label)
              .fontSize(12)
              .fontColor(index === 0 ? $r('app.color.text_primary') : $r('app.color.text_secondary'))
            WeatherGlyph({
              weatherCode: point.weatherCode,
              isDay: point.isDay,
              side: 30
            })
            Text(formatTemp(point.temperature))
              .fontSize(15)
              .fontWeight(FontWeight.Medium)
              .fontColor($r('app.color.text_primary'))
          }
          .width(58)
          .padding({ top: 10, bottom: 10 })
          .borderRadius(16)
          .backgroundColor(index === 0 ? '#EEF4FF' : Color.Transparent)
          .alignItems(HorizontalAlign.Center)
        }, (point: HourlyPoint, index: number) => `${this.selectedCityId}-${index}-${point.temperature}`)
      }
      .padding({ right: 8 })
    }
    .scrollable(ScrollDirection.Horizontal)
    .scrollBar(BarState.Off)
    .width('100%')
    .nestedScroll({
      scrollForward: NestedScrollMode.SELF_FIRST,
      scrollBackward: NestedScrollMode.SELF_FIRST
    })
  }

  @Builder
  private Metrics() {
    Grid() {
      GridItem() {
        Column({ space: 4 }) {
          Text('湿度')
            .fontSize(12)
            .fontColor($r('app.color.text_secondary'))
          Text(`${this.selectedBundle().current.humidity}%`)
            .fontSize(22)
            .fontWeight(FontWeight.Medium)
            .fontColor($r('app.color.text_primary'))
        }
        .width('100%')
        .height(72)
        .padding({ left: 16 })
        .alignItems(HorizontalAlign.Start)
        .justifyContent(FlexAlign.Center)
        .borderRadius(16)
        .backgroundColor('#F3F6FA')
      }
      GridItem() {
        Column({ space: 4 }) {
          Text('风速')
            .fontSize(12)
            .fontColor($r('app.color.text_secondary'))
          Text(`${this.selectedBundle().current.windSpeed.toFixed(0)} km/h`)
            .fontSize(22)
            .fontWeight(FontWeight.Medium)
            .fontColor($r('app.color.text_primary'))
        }
        .width('100%')
        .height(72)
        .padding({ left: 16 })
        .alignItems(HorizontalAlign.Start)
        .justifyContent(FlexAlign.Center)
        .borderRadius(16)
        .backgroundColor('#F3F6FA')
      }
    }
    .columnsTemplate('1fr 1fr')
    .columnsGap(10)
    .rowsTemplate('1fr')
    .width('100%')
    .height(72)
  }

  @Builder
  private DailyPreview() {
    Column({ space: 4 }) {
      Row() {
        Text('未来七日')
          .fontSize(13)
          .fontColor($r('app.color.text_secondary'))
          .layoutWeight(1)
        Text('全部')
          .fontSize(14)
          .fontColor($r('app.color.brand_blue'))
          .onClick(() => {
            this.openDetail()
          })
      }
      .width('100%')
      .margin({ bottom: 4 })

      ForEach(this.previewIndexes(), (index: number) => {
        DayRangeRow({
          title: dayTitle(this.selectedBundle().daily.dates[index]),
          weatherCode: this.selectedBundle().daily.weatherCodes[index],
          low: this.selectedBundle().daily.tempMin[index],
          high: this.selectedBundle().daily.tempMax[index],
          scaleMin: this.scaleMin(),
          scaleMax: this.scaleMax()
        })
      }, (index: number) => `${this.selectedCityId}-day-${index}`)
    }
    .width('100%')
  }

  @Builder
  private CityCards() {
    List({ space: 10 }) {
      ForEach(this.weatherList, (item: WeatherBundle) => {
        ListItem() {
          CityWeatherRow({
            city: item.city,
            current: item.current,
            selected: item.city.id === this.selectedCityId,
            onOpen: (): void => {
              this.selectedCityId = item.city.id
            }
          })
        }
      }, (item: WeatherBundle) => item.city.id)
    }
    .width('100%')
    .height(this.weatherList.length * 78)
    .scrollBar(BarState.Off)
    .nestedScroll({
      scrollForward: NestedScrollMode.PARENT_FIRST,
      scrollBackward: NestedScrollMode.SELF_FIRST
    })
  }

  @Builder
  private StatusView() {
    Column({ space: 12 }) {
      if (this.status === 'loading') {
        LoadingProgress().width(48).height(48).color(Color.White)
        Text('正在获取天气')
          .fontSize(14)
          .fontColor(Color.White)
      } else if (this.status === 'error') {
        Text('加载失败')
          .fontSize(18)
          .fontColor(Color.White)
        Text(this.errorMessage)
          .fontSize(13)
          .fontColor('#E7F2FF')
          .textAlign(TextAlign.Center)
        Text('重新加载')
          .fontSize(15)
          .fontColor(Color.White)
          .padding({ left: 16, right: 16, top: 8, bottom: 8 })
          .borderRadius(16)
          .backgroundColor('#33FFFFFF')
          .onClick(() => {
            this.loadAllCities()
          })
      } else {
        Text('暂无天气数据')
          .fontSize(16)
          .fontColor(Color.White)
      }
    }
    .width('100%')
    .layoutWeight(1)
    .justifyContent(FlexAlign.Center)
    .padding(24)
  }

  build() {
    NavDestination() {
      Column() {
        if (this.status !== 'success') {
          this.StatusView()
        } else {
          this.Sky()
          Scroll() {
            Column({ space: 22 }) {
              if (this.selectedBundle().hourly.length > 0) {
                this.HourlyStrip()
              }
              this.Metrics()
              this.DailyPreview()
              this.CityCards()
            }
            .width('100%')
            .padding({ left: 20, right: 20, top: 22, bottom: 32 })
          }
          .layoutWeight(1)
          .margin({ top: -28 })
          .scrollBar(BarState.Off)
          .align(Alignment.Top)
          .backgroundColor(Color.White)
          .borderRadius({ topLeft: 28, topRight: 28 })
          .clip(true)
        }
      }
      .width('100%')
      .height('100%')
      .linearGradient({
        angle: 180,
        colors: this.status === 'success' ?
          skyStops(this.selectedBundle().current.weatherCode, this.selectedBundle().current.isDay) :
          [['#1A6FE0', 0], ['#49C8FF', 1]]
      })
    }
    .hideTitleBar(true)
    .onReady((context: NavDestinationContext) => {
      this.pathStack = context.pathStack
    })
  }
}

@Builder
export function HomePageBuilder() {
  HomePage()
}
