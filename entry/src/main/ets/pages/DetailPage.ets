import { DayRangeRow } from '../components/DayRangeRow'
import { TempChart } from '../components/TempChart'
import {
  buildWeekBrief,
  CityInfo,
  dayTitle,
  LoadStatus,
  skyStops,
  WeatherBundle
} from '../model/WeatherModels'
import { WeatherService } from '../services/WeatherService'

@ComponentV2
struct DetailPage {
  pathStack: NavPathStack = new NavPathStack()
  @Local city: CityInfo = {
    id: '',
    name: '',
    latitude: 0,
    longitude: 0,
    desc: ''
  }
  @Local status: LoadStatus = 'idle'
  @Local errorMessage: string = ''
  @Local hasWeather: boolean = false
  @Local weather: WeatherBundle = {
    city: {
      id: '',
      name: '',
      latitude: 0,
      longitude: 0,
      desc: ''
    },
    current: {
      temperature: 0,
      humidity: 0,
      weatherCode: 0,
      windSpeed: 0,
      isDay: true
    },
    daily: {
      dates: [],
      tempMax: [],
      tempMin: [],
      weatherCodes: []
    },
    hourly: [],
    updatedAt: ''
  }

  private goBack(): void {
    if (this.pathStack.size() > 0) {
      this.pathStack.pop()
    }
  }

  private async loadDetail(): Promise<void> {
    if (!this.city.id) {
      this.status = 'empty'
      this.errorMessage = '未收到城市参数'
      return
    }
    this.status = 'loading'
    this.hasWeather = false
    try {
      this.weather = await WeatherService.fetchWeather(this.city)
      this.hasWeather = true
      this.status = 'success'
    } catch (err) {
      this.status = 'error'
      this.errorMessage = `详情加载失败：${JSON.stringify(err)}`
    }
  }

  private scaleMin(): number {
    const daily = this.weather.daily
    let min = daily.tempMin.length > 0 ? daily.tempMin[0] : 0
    for (let i = 1; i < daily.tempMin.length; i++) {
      if (daily.tempMin[i] < min) {
        min = daily.tempMin[i]
      }
    }
    return min
  }

  private scaleMax(): number {
    const daily = this.weather.daily
    let max = daily.tempMax.length > 0 ? daily.tempMax[0] : 1
    for (let i = 1; i < daily.tempMax.length; i++) {
      if (daily.tempMax[i] > max) {
        max = daily.tempMax[i]
      }
    }
    return max
  }

  private dayIndexes(): number[] {
    const indexes: number[] = []
    for (let i = 0; i < this.weather.daily.dates.length; i++) {
      indexes.push(i)
    }
    return indexes
  }

  build() {
    NavDestination() {
      Column() {
        Row() {
          Text('返回')
            .fontSize(16)
            .fontColor(Color.White)
            .width(48)
            .onClick(() => {
              this.goBack()
            })
          Column({ space: 2 }) {
            Text(this.city.name.length > 0 ? this.city.name : '城市详情')
              .fontSize(18)
              .fontWeight(FontWeight.Medium)
              .fontColor(Color.White)
            if (this.hasWeather) {
              Text(`${this.weather.current.temperature.toFixed(0)}°`)
                .fontSize(13)
                .fontColor('#E7F2FF')
            }
          }
          .alignItems(HorizontalAlign.Start)
          .layoutWeight(1)
        }
        .width('100%')
        .padding({ left: 16, right: 20, top: 12, bottom: 16 })
        .alignItems(VerticalAlign.Center)
        .linearGradient({
          angle: 135,
          colors: skyStops(
            this.hasWeather ? this.weather.current.weatherCode : 0,
            this.hasWeather ? this.weather.current.isDay : true
          )
        })

        if (this.status === 'loading') {
          Column({ space: 12 }) {
            LoadingProgress().width(48).height(48)
            Text('正在加载城市详情')
              .fontSize(14)
              .fontColor($r('app.color.text_secondary'))
          }
          .width('100%')
          .layoutWeight(1)
          .justifyContent(FlexAlign.Center)
          .backgroundColor('#F6F8FB')
        } else if (this.status === 'error' || this.status === 'empty') {
          Column({ space: 12 }) {
            Text(this.status === 'empty' ? '空数据' : '请求异常')
              .fontSize(18)
              .fontColor($r('app.color.danger'))
            Text(this.errorMessage)
              .fontSize(13)
              .fontColor($r('app.color.text_secondary'))
              .padding({ left: 24, right: 24 })
              .textAlign(TextAlign.Center)
            Button('重试')
              .height(40)
              .backgroundColor($r('app.color.brand_blue'))
              .onClick(() => {
                this.loadDetail()
              })
          }
          .width('100%')
          .layoutWeight(1)
          .justifyContent(FlexAlign.Center)
          .backgroundColor('#F6F8FB')
        } else if (this.hasWeather) {
          Scroll() {
            Column({ space: 16 }) {
              Column({ space: 2 }) {
                ForEach(this.dayIndexes(), (index: number) => {
                  DayRangeRow({
                    title: dayTitle(this.weather.daily.dates[index]),
                    weatherCode: this.weather.daily.weatherCodes[index],
                    low: this.weather.daily.tempMin[index],
                    high: this.weather.daily.tempMax[index],
                    scaleMin: this.scaleMin(),
                    scaleMax: this.scaleMax()
                  })
                }, (index: number) => `detail-day-${index}`)
              }
              .width('100%')
              .padding({ left: 16, right: 16, top: 8, bottom: 8 })
              .borderRadius(20)
              .backgroundColor(Color.White)

              TempChart({
                title: '七日气温',
                labels: this.weather.daily.dates,
                highs: this.weather.daily.tempMax,
                lows: this.weather.daily.tempMin
              })

              Text(buildWeekBrief(this.weather.daily).tip)
                .fontSize(15)
                .fontColor($r('app.color.text_primary'))
                .lineHeight(22)
                .width('100%')
                .padding({ left: 4, right: 4, bottom: 8 })
            }
            .width('100%')
            .padding({ left: 16, right: 16, top: 16, bottom: 28 })
          }
          .layoutWeight(1)
          .scrollBar(BarState.Off)
          .backgroundColor('#F6F8FB')
        }
      }
      .width('100%')
      .height('100%')
      .backgroundColor('#F6F8FB')
    }
    .hideTitleBar(true)
    .onReady((context: NavDestinationContext) => {
      this.pathStack = context.pathStack
      const param = context.pathInfo.param as CityInfo
      if (param && param.id) {
        this.city = param
        this.loadDetail()
      } else {
        this.status = 'empty'
        this.errorMessage = '路由未传入城市信息'
      }
    })
  }
}

@Builder
export function DetailPageBuilder() {
  DetailPage()
}
