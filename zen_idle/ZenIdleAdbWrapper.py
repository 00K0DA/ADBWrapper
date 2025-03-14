from ADBWrapper import ADBWrapper
from constants import Constants
import time
from ocr import crop_image, read_string_decimal
from config import Config


class ZenIdleAdbWrapper(ADBWrapper):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)

    def open_ball_update(self):
        self.logger.startFuncLog()
        self.tap(150, 2450, end_time=1)

    def open_stage_update(self):
        self.logger.startFuncLog()
        self.tap(345, 2450, end_time=1)

    def open_card_update(self):
        self.logger.startFuncLog()
        self.tap(540, 2450, end_time=1)

    def close_tab(self):
        self.logger.startFuncLog()
        self.open_ball_update()
        self.open_stage_update()
        self.open_stage_update()

    def show_last_stage(self):
        self.logger.startFuncLog()
        self.tap(1030, 2350, end_time=1)

    def show_1st_stage(self):
        self.logger.startFuncLog()
        self.tap(1030, 2230, end_time=1)

    def close_vip_ball_dialog(self):
        self.logger.startFuncLog()
        self.tap(540, 1600, count=2, end_time=0.5)

    def tap_ball_for_stage_1(
            self,
            only_up_side=False):
        x_pattern_1 = [70, 380, 720, 1010]
        x_pattern_2 = [70, 210, 380, 540, 720, 870, 1010]
        x_pattern_3 = [210, 540, 870]
        # オファーウォールボタンを誤タップしないために1010を除外
        x_pattern_4 = [70, 210, 380, 540, 720, 870]

        if not only_up_side:
            self.swipe(540, 1000, 540, 1000 - 100, swipe_speed=1000, end_time=1)
            tap_point_y_dict = {
                2065: x_pattern_1,
                1920: x_pattern_2,
                1235: x_pattern_1,
                1140: x_pattern_2,
                900: x_pattern_3,
                800: x_pattern_2,
            }
            for _ in range(2):
                for y, x_list in tap_point_y_dict.items():
                    for x in x_list:
                        self.tap(x, y, end_time=0.1)

        self.swipe(540, 1000, 540, 1000 + 300, swipe_speed=500, end_time=0.5)
        tap_point_y_dict = {
            780: x_pattern_1,
            700: x_pattern_4,
        }
        for _ in range(2):
            for y, x_list in tap_point_y_dict.items():
                for x in x_list:
                    self.tap(x, y, end_time=0.1)
        # VIPボールのダイアログが開かれていると、画面と処理に影響が出るため、閉じる
        self.close_vip_ball_dialog()

    def tap_ball_for_stage_3(self, tap_count=5):
        # 詰まる部分のボールをタップ
        point_list = [
            (60, 1615),
            (1020, 1615),
            (100, 1550),
            (980, 1550),
            (270, 1400),
            (810, 1400),
            (540, 1380),
        ]
        for _ in range(tap_count):
            for point in point_list:
                self.tap(point[0], point[1], end_time=0.1)
        # VIPボールのダイアログが開かれていると、画面と処理に影響が出るため、閉じる
        self.close_vip_ball_dialog()

    def scroll_up_stage(self):
        self.logger.startFuncLog()
        self.swipe(540, 1000, 540, 1000 + 595, swipe_speed=1000, end_time=1)

    def scroll_down_stage(self):
        self.logger.startFuncLog()
        self.swipe(540, 1000 + 595, 540, 1000, swipe_speed=1000, end_time=1)

    def receive_reward(self):
        self.logger.startFuncLog()
        self.tap(980, 150, end_time=1)
        self.tap(540, 810, count=3, end_time=1)
        self.tap(925, 555, end_time=1)

    def remove_all_ball(self):
        self.logger.startFuncLog()
        self.tap(1015, 85, end_time=1)
        self.tap(300, 1325, end_time=1)
        self.tap(540, 1830, end_time=1)

    def do_pre_stage(self):
        self.logger.startFuncLog()

        self.show_1st_stage()

        self.tap(980, 2485, end_time=1)
        self.try_to_get_screen_shot_until_success()

        self.tap(360, 2295, end_time=1)
        self.tap(730, 1585, end_time=1)
        # タブを閉じる
        self.tap(980, 2485, end_time=1)

    def try_to_get_screen_shot_until_success(self):
        self.logger.startFuncLog()
        if Constants.TEMP_IMAGE_PATH.exists():
            Constants.TEMP_IMAGE_PATH.unlink()
        self.get_screen_shot(Constants.TEMP_DIR_PATH, Constants.TEMP_IMAGE_NAME)

    def buy_card(self):
        self.logger.startFuncLog()
        self.open_card_update()
        # カードを購入
        self.tap(425, 200, end_time=1)
        self.try_to_get_screen_shot_until_success()
        # 閉じる
        self.tap(955, 1130, count=2, end_time=0.5)
        self.open_card_update()

    def update_ball(
            self,
            update_ball_1_to_3=True,
            update_ball_4_to_6=True,
            update_ball_7_to_9=True,
            update_ball_10_to_12=True,
    ):
        self.logger.startFuncLog()

        def swipe_to_target_internal(current_swipe_count, target_swipe_count):
            needed_swipe_count = target_swipe_count - current_swipe_count
            is_needed_swipe_down = needed_swipe_count > 0
            if is_needed_swipe_down:
                for _ in range(needed_swipe_count):
                    self.swipe(315, 2285, 315, 2285 - 425, swipe_speed=1000, end_time=3)
                    current_swipe_count += 1
            else:
                for _ in range(abs(needed_swipe_count)):
                    self.swipe(315, 2285 - 425, 315, 2285, swipe_speed=1000, end_time=3)
                    current_swipe_count -= 1
            return current_swipe_count

        def tap_ball_internal():
            # 3つ目の価値
            self.tap(700, 2300, count=2)
            # 3つ目のタイム
            self.tap(945, 2300)

            # 2つ目の価値
            self.tap(700, 2080, count=2)
            # 2つ目のタイム
            self.tap(945, 2080)

            # 1つ目の価値
            self.tap(700, 1875, count=2)
            # 1つ目のタイム
            self.tap(945, 1875, end_time=0.5)

        self.open_ball_update()
        swiped_count = 0
        tasks = [
            (update_ball_10_to_12, 3),
            (update_ball_7_to_9, 2),
            (update_ball_4_to_6, 1),
            (update_ball_1_to_3, 0),
        ]
        for should_update, target_swipe in tasks:
            if should_update:
                swiped_count = swipe_to_target_internal(swiped_count, target_swipe)
                tap_ball_internal()

        self.swipe(315, 1800, 315, 2400, swipe_speed=100, end_time=1)
        self.open_ball_update()

    def update_stage(
            self,
            max_stage=2,
    ):
        self.logger.startFuncLog()
        self.open_stage_update()
        if max_stage <= 3:
            if max_stage == 3:
                # 3つ目の障害物 & 3つ目のゲートボーナス
                self.tap(945, 2330, count=2)
                self.tap(700, 2330)
            # 1つ目の障害物 & 1つ目のゲートボーナス
            self.tap(945, 1875, count=2)
            self.tap(700, 1875)

            if max_stage >= 2:
                # 2つ目の障害物 & 2つ目のゲートボーナス
                self.tap(945, 2130, count=2)
                self.tap(690, 2130)
        elif max_stage <= 10:
            scroll_amount_dict = {
                4: 250,
                5: 420,
                6: 570,
                7: 720,
                8: 880,
                9: 1070,
                10: 1230,
            }
            scroll_up_count_dict = {
                4: 1,
                5: 1,
                6: 2,
                7: 2,
                8: 3,
                9: 3,
                10: 4,
            }
            self.swipe(315, 2285, 315, 2285 - scroll_amount_dict.get(max_stage), swipe_speed=1000, end_time=2)
            for i in range(scroll_up_count_dict.get(max_stage)):
                self.tap(945, 2330, count=2)
                self.tap(700, 2330)
                self.tap(945, 2040, count=2)
                self.tap(690, 2040, end_time=0.5)
                is_last = i == scroll_up_count_dict.get(max_stage) - 1
                swipe_speed = 100 if is_last else 1000
                self.swipe(315, 1800, 315, 1800 + 375, swipe_speed=swipe_speed, end_time=2)

            # 3つ目の障害物 & 3つ目のゲートボーナス
            self.tap(945, 2330, count=2)
            self.tap(700, 2330)
            # 2つ目の障害物 & 2つ目のゲートボーナス
            self.tap(945, 2130, count=2)
            self.tap(690, 2130)
            # 1つ目の障害物 & 1つ目のゲートボーナス
            self.tap(945, 1875, count=2)
            self.tap(700, 1875)

        self.open_stage_update()

    def is_target_app_running(self):
        self.logger.startFuncLog()
        app_id, activity_name = self.get_package_and_activity()
        return app_id == Constants.TARGET_APP_ID and activity_name == Constants.TARGET_ACTIVITY_NAME

    def get_video_reward(self):
        self.logger.startFuncLog()
        self.tap(1030, 285, end_time=0.25)
        self.tap(540, 1490, end_time=0.25)

    def read_gem_count(self, capture_new_image=True):
        self.logger.startFuncLog()
        if capture_new_image:
            self.try_to_get_screen_shot_until_success()
        crop_image(Constants.TEMP_IMAGE_PATH, Constants.CROP_IMAGE_PATH, 660, 35, 150, 70)
        gem_count = read_string_decimal(Constants.CROP_IMAGE_PATH, is_include_plus=False, is_include_dot=False)
        self.logger.info("OCRの結果(ジェムの数): {}".format(gem_count))
        try:
            gem_count = int(gem_count)
        except ValueError:
            return None

        return gem_count

    def read_pre_stage_bonus(self, capture_new_image=True):
        self.logger.startFuncLog()
        if capture_new_image:
            self.try_to_get_screen_shot_until_success()
        crop_image(Constants.TEMP_IMAGE_PATH, Constants.CROP_IMAGE_PATH, 660, 2000, 200, 70)
        pre_stage_bonus = read_string_decimal(Constants.CROP_IMAGE_PATH, is_include_plus=True, is_include_dot=True)
        self.logger.info("OCRの結果(プレステージボーナス): {}".format(pre_stage_bonus))
        try:
            pre_stage_bonus = str(pre_stage_bonus).replace("+", "")
            pre_stage_bonus = float(pre_stage_bonus)
        except ValueError:
            return None

        return pre_stage_bonus

    def reboot_and_launch_app(self):
        self.logger.startFuncLog()
        # 再起動
        self.logger.info("端末を再起動します")
        self.reboot()
        # 再起動完了まで待機
        self.logger.info("再起動完了まで待機します")
        self.wait_for_device()
        # 起動完了まで待機
        self.logger.info("起動完了まで待機します")
        self.wait_for_boot_complete()
        time.sleep(5)

        while True:
            # ロック画面を解除
            self.logger.info("ロック画面を解除します")
            self.swipe(540, 2000, 540, 1000, swipe_speed=500, end_time=10)

            # アプリを起動
            self.logger.info("アプリを起動します")
            self.launch_app(Constants.TARGET_APP_ID, Constants.TARGET_ACTIVITY_NAME)
            time.sleep(10)
            app_id, activity_name = self.get_package_and_activity()
            if app_id == Constants.TARGET_APP_ID and activity_name == Constants.TARGET_ACTIVITY_NAME:
                break
            else:
                self.logger.info("アプリが起動していません app_id: {}, activity_name: {}".format(app_id, activity_name))
                time.sleep(5)

        # アプリが完全に起動するまで待機
        time.sleep(15)
        # 放置ボーナスの受け取り
        self.tap(540, 1600, count=3, end_time=1, span=1)

    def get_tournament_status(self):
        self.logger.startFuncLog()
        self.tap(65, 300, end_time=1)
        self.try_to_get_screen_shot_until_success()
        self.tap(965, 500, end_time=1)

    def get_challenge_status(self):
        self.logger.startFuncLog()
        self.tap(1030, 420, end_time=1)
        self.try_to_get_screen_shot_until_success()
        self.tap(925, 615, end_time=1)

    def tap_ball_for_stage_7(self):
        def tap_internal(tap_count):
            y_tap_list = list(range(2000, 1400, -100))
            for _ in range(tap_count):
                for y in y_tap_list:
                    self.tap(1000, y)
                    self.tap(80, y)

        self.open_stage_update()
        # ステージ7を表示
        self.swipe(540, 2350, 540, 2350 - 950, swipe_speed=3000, end_time=1)
        # ステージ7をタップ & 移動する
        self.tap(210, 2300, end_time=1)
        # 一番上までスクロール
        self.swipe(540, 1800, 540, 2350, swipe_speed=100, end_time=1)
        self.open_stage_update()

        tap_internal(6 * 2)

        self.swipe(540, 1000, 540, 1000 - 550, swipe_speed=1000, end_time=1)
        tap_internal(5)

        self.swipe(540, 1000, 540, 1000 - 600, swipe_speed=1000, end_time=1)
        tap_internal(4)

        self.swipe(540, 1000, 540, 1000 - 750, swipe_speed=1000, end_time=1)
        tap_internal(3)

        self.swipe(540, 1000, 540, 1000 - 750, swipe_speed=1000, end_time=1)
        tap_internal(2)

        self.swipe(540, 1000, 540, 1000 - 775, swipe_speed=1000, end_time=1)
        tap_internal(1)

        # self.swipe(540, 1000, 540, 1000 + 800, swipe_speed=1000, end_time=1)

        # VIPボールのダイアログが開かれていると、画面と処理に影響が出るため、閉じる
        self.close_vip_ball_dialog()


if __name__ == "__main__":
    adbw = ZenIdleAdbWrapper(Config.DEVICE_CODE, should_output_log=True)
    adbw.show_1st_stage()
    pass
