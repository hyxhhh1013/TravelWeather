import { DetailPageBuilder } from './DetailPage'
import { HomePageBuilder } from './HomePage'

/**
 * Navigation 根页面：自定义 navDestination，兼容 DevEco Previewer
 * （系统路由表在预览器中不可用，故采用自定义 PageMap）
 */
@Entry
@Component
struct Index {
  pathStack: NavPathStack = new NavPathStack()

  aboutToAppear(): void {
    this.pathStack.pushPathByName('HomePage', null)
  }

  @Builder
  PageMap(name: string) {
    if (name === 'HomePage') {
      HomePageBuilder()
    } else if (name === 'DetailPage') {
      DetailPageBuilder()
    }
  }

  build() {
    Navigation(this.pathStack) {
      // 首页与详情均通过 NavDestination 压栈展示
    }
    .hideNavBar(true)
    .navDestination(this.PageMap)
    .mode(NavigationMode.Stack)
    .title('出行天气助手')
  }
}
