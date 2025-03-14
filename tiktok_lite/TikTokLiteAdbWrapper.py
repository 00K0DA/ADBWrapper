import time

from ADBWrapper import ADBWrapper
from random import randint
from pathlib import Path
from image_util import is_include_color
import ocr

TEMP_IMAGE_NAME = "temp_image"
TEMP_DIR_PATH = Path(__file__).parent / "img"
TEMP_IMAGE_PATH = Path(TEMP_DIR_PATH, TEMP_IMAGE_NAME + ".png")


class TikTokLiteAdbWrapper(ADBWrapper):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)

    def is_tiktok_lite_running(self) -> bool:
        package_name, activity_name = self.get_package_and_activity()
        return package_name == "com.ss.android.ugc.tiktok.lite"

    def launch_splash_activity(self):
        self.launch_app("com.ss.android.ugc.tiktok.lite", "com.ss.android.ugc.aweme.splash.SplashActivity")

    def is_splash_activity_shown(self) -> bool:
        package_name, activity_name = self.get_package_and_activity()
        return package_name == "com.ss.android.ugc.tiktok.lite" and activity_name == "com.ss.android.ugc.aweme.splash.SplashActivity"

    def is_spark_activity_shown(self) -> bool:
        package_name, activity_name = self.get_package_and_activity()
        return package_name == "com.ss.android.ugc.tiktok.lite" and activity_name == "com.bytedance.hybrid.spark.page.SparkActivity"

    def is_reward_ad_activity_shown(self) -> bool:
        package_name, activity_name = self.get_package_and_activity()
        return package_name == "com.ss.android.ugc.tiktok.lite" and activity_name == "com.ss.android.ugc.aweme.ui.RewardAdActivity"

    def swipe_to_next_video(self):
        start_x = randint(200, 800)
        end_x = start_x + randint(0, 100) - 50
        start_y = randint(1500, 1700)
        end_y = start_y - 1000
        self.swipe(start_x, start_y, end_x, end_y, swipe_speed=200)

    def close_invite_reward_dialog(self):
        self.tap(545, 1700)

    def is_live_video_shown(self) -> bool:
        live_color = (222, 67, 137)
        self.get_screen_shot(TEMP_DIR_PATH, TEMP_IMAGE_NAME)
        return is_include_color(40, 1980, 40, 60, live_color, TEMP_IMAGE_PATH)

    def stop_tiktok(self) -> None:
        self.stop_app("com.ss.android.ugc.tiktok.lite")

    def press_reward_button(self):
        self.tap(875, 900)

    def press_close_reward_button(self):
        self.tap(1000, 200)

    def read_live_watch_reward_button_text(self) -> str:
        self.get_screen_shot(TEMP_DIR_PATH, TEMP_IMAGE_NAME)
        ocr.crop_image(TEMP_IMAGE_PATH, TEMP_IMAGE_PATH, 430, 1790, 220, 50)
        return ocr.read_eng_string(TEMP_IMAGE_PATH)

    def is_live_watch_reward_can_not_claim(self) -> bool:
        return self.read_live_watch_reward_button_text() == "Watch LIVE"

    def press_start_watch_live_button(self):
        self.tap(875, 1880)

    def press_watch_live_reward_button(self):
        self.tap(110, 730)

    def press_claim_watch_live_reward_button(self):
        self.tap(540, 1800)

    def press_close_live_watch_page_button(self):
        self.tap(1050, 200, count=2, span=2)

    def open_spark_page_with_scroll(self):
        self.open_spark_page()
        self.swipe(500, 2300, 500, 250, swipe_speed=100, end_time=2)
        self.swipe(500, 800, 500, 800 + 625, swipe_speed=1000, end_time=2)

    def open_spark_page(self):
        self.tap(330, 2300, end_time=3)

    def press_claim_bonus_button(self):
        self.tap(875, 500, end_time=5)

    def press_back_button(self):
        self.tap(100, 200, end_time=2)


if __name__ == "__main__":
    tiktok_lite_adb_wrapper = TikTokLiteAdbWrapper("25111FDF6001YX")
