import { TempChart } from '../components/TempChart'
import { WeatherCard } from '../components/WeatherCard'
import {
  CityInfo,
  LoadStatus,
  WeatherBundle,
  weatherCodeToEmoji,
  weatherCodeToText
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
      windSpeed: 0
    },
    daily: {
      dates: [],
      tempMax: [],
      tempMin: [],
      weatherCodes: []
    },
    updatedAt: ''
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

  @Builder
  private DailyList() {
    Column({ space: 10 }) {
      Text('七日预报明细')
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
        .width('100%')

      ForEach(this.weather.daily.dates, (date: string, index: number) => {
        Row() {
          Text(date.substring(5))
            .width(70)
            .fontSize(14)
          Text(weatherCodeToEmoji(this.weather.daily.weatherCodes[index]))
            .fontSize(20)
            .margin({ right: 8 })
          Text(weatherCodeToText(this.weather.daily.weatherCodes[index]))
            .layoutWeight(1)
            .fontSize(14)
          Text(`${this.weather.daily.tempMin[index].toFixed(0)}° / ${this.weather.daily.tempMax[index].toFixed(0)}°`)
            .fontSize(14)
            .fontColor($r('app.color.brand_blue'))
        }
        .width('100%')
        .padding(12)
        .borderRadius(12)
        .backgroundColor($r('app.color.card_background'))
      }, (date: string, index: number) => `${date}-${index}`)
    }
    .width('100%')
    .padding(16)
    .borderRadius(16)
    .backgroundColor('#EEF3FF')
  }

  build() {
    NavDestination() {
      Column() {
        if (this.status === 'loading') {
          Column({ space: 12 }) {
            LoadingProgress().width(48).height(48)
            Text('正在加载城市详情…')
          }
          .width('100%')
          .layoutWeight(1)
          .justifyContent(FlexAlign.Center)
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
            Button('重试').onClick(() => {
              this.loadDetail()
            })
          }
          .width('100%')
          .layoutWeight(1)
          .justifyContent(FlexAlign.Center)
        } else if (this.hasWeather) {
          Scroll() {
            Column({ space: 14 }) {
              WeatherCard({
                city: this.weather.city,
                current: this.weather.current,
                showAction: false
              })

              TempChart({
                title: `${this.weather.city.name} · 七日最高气温`,
                labels: this.weather.daily.dates,
                values: this.weather.daily.tempMax
              })

              this.DailyList()
            }
            .padding(16)
            .width('100%')
          }
          .layoutWeight(1)
          .scrollBar(BarState.Off)
        }
      }
      .width('100%')
      .height('100%')
      .backgroundColor($r('app.color.page_background'))
    }
    .title(this.city.name.length > 0 ? `${this.city.name}详情` : '城市详情')
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
