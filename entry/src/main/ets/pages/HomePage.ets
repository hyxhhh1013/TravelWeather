import { CITY_LIST } from '../common/CityData'
import { WeatherCard } from '../components/WeatherCard'
import { CityInfo, LoadStatus, WeatherBundle } from '../model/WeatherModels'
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

    try {
      for (let i = 0; i < CITY_LIST.length; i++) {
        const city = CITY_LIST[i]
        const bundle = await WeatherService.fetchWeather(city)
        result.push(bundle)
      }
      this.weatherList = result
      this.status = result.length === 0 ? 'empty' : 'success'
    } catch (err) {
      this.weatherList = []
      this.status = 'error'
      this.errorMessage = `网络请求失败：${JSON.stringify(err)}`
    }
  }

  private openDetail(city: CityInfo): void {
    this.pathStack.pushPathByName('DetailPage', city)
  }

  @Builder
  private StatusView() {
    Column({ space: 12 }) {
      if (this.status === 'loading') {
        LoadingProgress().width(48).height(48)
        Text('正在拉取远端天气数据…')
          .fontSize(14)
          .fontColor($r('app.color.text_secondary'))
      } else if (this.status === 'error') {
        Text('加载失败')
          .fontSize(18)
          .fontWeight(FontWeight.Medium)
          .fontColor($r('app.color.danger'))
        Text(this.errorMessage)
          .fontSize(13)
          .fontColor($r('app.color.text_secondary'))
          .textAlign(TextAlign.Center)
        Button('重新加载')
          .onClick(() => {
            this.loadAllCities()
          })
      } else if (this.status === 'empty') {
        Text('暂无天气数据')
          .fontSize(16)
          .fontColor($r('app.color.text_secondary'))
        Button('刷新')
          .onClick(() => {
            this.loadAllCities()
          })
      }
    }
    .width('100%')
    .padding(24)
    .justifyContent(FlexAlign.Center)
  }

  build() {
    NavDestination() {
      Column() {
        Row() {
          Column({ space: 4 }) {
            Text('出行天气助手')
              .fontSize(24)
              .fontWeight(FontWeight.Bold)
              .fontColor($r('app.color.text_primary'))
            Text('Open-Meteo 实时天气 · 多城市出行参考')
              .fontSize(12)
              .fontColor($r('app.color.text_secondary'))
          }
          .alignItems(HorizontalAlign.Start)
          .layoutWeight(1)

          Button('刷新')
            .height(36)
            .backgroundColor($r('app.color.brand_blue'))
            .onClick(() => {
              this.loadAllCities()
            })
        }
        .width('100%')
        .padding({
          left: 16,
          right: 16,
          top: 12,
          bottom: 8
        })

        if (this.status !== 'success') {
          this.StatusView()
        } else {
          Scroll() {
            Column({ space: 14 }) {
              Text('城市列表')
                .fontSize(16)
                .fontWeight(FontWeight.Medium)
                .width('100%')

              Grid() {
                ForEach(CITY_LIST, (city: CityInfo) => {
                  GridItem() {
                    Text(city.name)
                      .fontSize(14)
                      .fontColor(this.selectedCityId === city.id ? Color.White : $r('app.color.text_primary'))
                      .textAlign(TextAlign.Center)
                      .width('100%')
                      .height(40)
                      .borderRadius(20)
                      .backgroundColor(this.selectedCityId === city.id ?
                        $r('app.color.brand_blue') : '#E8EEF9')
                      .onClick(() => {
                        this.selectedCityId = city.id
                      })
                  }
                }, (city: CityInfo) => city.id)
              }
              .columnsTemplate('1fr 1fr 1fr')
              .columnsGap(10)
              .rowsGap(10)
              .width('100%')

              ForEach(this.weatherList, (item: WeatherBundle) => {
                if (item.city.id === this.selectedCityId) {
                  Column({ space: 8 }) {
                    WeatherCard({
                      city: item.city,
                      current: item.current,
                      showAction: true,
                      onOpenDetail: () => {
                        this.openDetail(item.city)
                      }
                    })
                    Text(`更新时间 ${item.updatedAt}`)
                      .fontSize(12)
                      .fontColor($r('app.color.text_secondary'))
                      .width('100%')
                  }
                  .width('100%')
                }
              }, (item: WeatherBundle) => `selected-${item.city.id}`)

              Text('全部城市速览')
                .fontSize(16)
                .fontWeight(FontWeight.Medium)
                .width('100%')
                .margin({ top: 8 })

              List({ space: 12 }) {
                ForEach(this.weatherList, (item: WeatherBundle) => {
                  ListItem() {
                    WeatherCard({
                      city: item.city,
                      current: item.current,
                      showAction: true,
                      onOpenDetail: () => {
                        this.openDetail(item.city)
                      }
                    })
                  }
                }, (item: WeatherBundle) => item.city.id)
              }
              .width('100%')
              .nestedScroll({
                scrollForward: NestedScrollMode.PARENT_FIRST,
                scrollBackward: NestedScrollMode.SELF_FIRST
              })
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
    .title('首页')
    .onReady((context: NavDestinationContext) => {
      this.pathStack = context.pathStack
    })
  }
}

@Builder
export function HomePageBuilder() {
  HomePage()
}
