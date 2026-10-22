import { AbilityConstant, ConfigurationConstant, UIAbility, Want } from '@kit.AbilityKit'
import { hilog } from '@kit.PerformanceAnalysisKit'
import { window } from '@kit.ArkUI'

const DOMAIN = 0x0000

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    try {
      this.context.getApplicationContext().setColorMode(ConfigurationConstant.ColorMode.COLOR_MODE_NOT_SET)
    } catch (err) {
      hilog.error(DOMAIN, 'TravelWeather', 'Failed to set colorMode. Cause: %{public}s', JSON.stringify(err))
    }
    hilog.info(DOMAIN, 'TravelWeather', 'Ability onCreate')
  }

  onDestroy(): void {
    hilog.info(DOMAIN, 'TravelWeather', 'Ability onDestroy')
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(DOMAIN, 'TravelWeather', 'Ability onWindowStageCreate')
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(DOMAIN, 'TravelWeather', 'Failed to load content. Cause: %{public}s', JSON.stringify(err))
        return
      }
      hilog.info(DOMAIN, 'TravelWeather', 'Succeeded in loading content.')
    })
  }

  onWindowStageDestroy(): void {
    hilog.info(DOMAIN, 'TravelWeather', 'Ability onWindowStageDestroy')
  }

  onForeground(): void {
    hilog.info(DOMAIN, 'TravelWeather', 'Ability onForeground')
  }

  onBackground(): void {
    hilog.info(DOMAIN, 'TravelWeather', 'Ability onBackground')
  }
}
