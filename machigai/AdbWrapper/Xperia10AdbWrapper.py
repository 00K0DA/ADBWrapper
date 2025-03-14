from machigai import MachigaiAdbWrapper
from machigai.domain.AdActivity import AdActivity
from time import sleep

from machigai.senario import watch_ad_loop


class Xperia10AdbWrapper(MachigaiAdbWrapper.MachigaiAdbWrapper):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)

    def tap_ad_button(self):
        adb.tap(1000, 2140)

    def on_ad_activity_shown(self, ad_activity: AdActivity):
        if ad_activity == AdActivity.Google:
            self.tap(80, 80)
            self.tap(1015, 50)

        elif ad_activity == AdActivity.Moloco_1:
            adb.tap(1050, 50, count=2, span=5)

        elif ad_activity == AdActivity.Moloco_2:
            self.tap(960, 150, count=2, span=5)

        elif ad_activity == AdActivity.AppLovin:
            self.tap(1020, 80, count=2, span=5)

        elif ad_activity == AdActivity.ByteDance_1 or ad_activity == AdActivity.ByteDance_2 or ad_activity == AdActivity.ByteDance_3:
            self.tap(1015, 230, count=3, span=5)

        elif ad_activity == AdActivity.MBridge:
            self.tap(1040, 100)

        elif ad_activity == AdActivity.InMobi:
            self.tap(2200, 60)
            self.tap(940, 190)

        elif ad_activity == AdActivity.Vungle:
            adb.tap(1040, 75, count=2, span=8)

if __name__ == "__main__":
    adb = Xperia10AdbWrapper("HQ631V0CEF")
    # adb.long_tap(1020, 80, 2)
    # adb.tap(1060, 80)

    watch_ad_loop(adb)
