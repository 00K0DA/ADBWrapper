from machigai import MachigaiAdbWrapper
from machigai.domain.AdActivity import AdActivity
from time import sleep

from machigai.domain.Coordinate import Coordinate
from machigai.senario import watch_ad_loop, solve_diff


class Pixel6AdbWrapper(MachigaiAdbWrapper.MachigaiAdbWrapper):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)

    def tap_ad_button(self):
        adb.tap(1000, 2070)

    def on_ad_activity_shown(self, ad_activity: AdActivity):
        if ad_activity == AdActivity.Google:
            self.tap(960, 160)
            self.tap(85, 200)

        elif ad_activity == AdActivity.Moloco_1:
            self.tap(1050, 150, count=2, span=5)

        elif ad_activity == AdActivity.Moloco_2:
            self.tap(1040, 180, count=2, span=5)

        elif ad_activity == AdActivity.AppLovin:
            self.tap(1020, 270)
            self.tap(1020, 200, end_time=5)
            self.tap(950, 160)

        elif ad_activity == AdActivity.ByteDance_1 or ad_activity == AdActivity.ByteDance_3:
            self.tap(1015, 230, count=3, span=5)

        elif ad_activity == AdActivity.ByteDance_2:
            self.tap(1015, 230, count=2, span=5)

        elif ad_activity == AdActivity.MBridge:
            self.tap(1040, 100)

        elif ad_activity == AdActivity.InMobi:
            self.tap(2350, 50)
            self.tap(1030, 200)

        elif ad_activity == AdActivity.Vungle:
            self.tap(1010, 215, count=2, span=10)

        elif ad_activity == AdActivity.FiveCorp:
            self.tap(1025, 225)

    def tap_double_bonus(self):
        self.tap(540, 1300)

    def tap_close_double_bonus(self):
        self.tap(540, 1600)

    def select_recommend_diff(self):
        self.tap(325, 1975)

    def get_first_image_coordinate(self) -> Coordinate:
        return Coordinate(start_x=21, start_y=414, end_x=1059, end_y=1106)

    def get_second_image_coordinate(self) -> Coordinate:
        return Coordinate(start_x=21, start_y=1148, end_x=1059, end_y=1840)


if __name__ == "__main__":
    adb = Pixel6AdbWrapper("25111FDF6001YX")
    # adb.tap(1040, 100)
    # adb.tap(2200, 60)
    solve_diff(adb)
