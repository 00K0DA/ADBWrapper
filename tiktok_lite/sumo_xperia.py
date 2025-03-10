from TikTokLiteAdbWrapper import TikTokLiteAdbWrapper
import time
from random import randint
from datetime import datetime, timedelta
from sumo import wait_until_next_hour, wait_start_time

adb = TikTokLiteAdbWrapper("HQ631V0CEF")


def main():
    max_tap_count = 5130
    close_app()
    open_app_and_page()
    while True:
        start_time = datetime.now()
        adb.tap(1000, 410)
        for i in range(max_tap_count):
            tap()
            # 0.005~0.30秒待つ
            time.sleep(randint(5, 30) / 100)
            tap_count = i + 1
            if tap_count % 10 == 0:
                adb.tap(1000, 410)
            if tap_count % 25 == 0:
                percent = tap_count / max_tap_count * 100
                print(f"{tap_count} taps completed. {percent:.2f}%")
                if not adb.is_tiktok_lite_running() or not adb.is_spark_activity_shown():
                    print("TikTok Lite is not running. Restarting...")
                    close_app()
                    open_app_and_page()
                    time.sleep(5)

        close_app()
        wait_until_next_hour(start_time)
        open_app_and_page()


def tap():
    # x=540±175, y=1500±175の範囲をタップ
    tap_range = 175
    x = 540 + randint(0, 2 * tap_range) - tap_range
    y = 1500 + randint(0, 2 * tap_range) - tap_range
    adb.tap(x, y)


def close_and_open_page():
    adb.press_back_button()
    time.sleep(2)
    adb.tap(540, 1975, end_time=2)


def open_app_and_page():
    adb.launch_splash_activity()
    time.sleep(5)
    adb.open_spark_page()
    adb.swipe(540, 200, 540, 1200)
    adb.swipe(540, 200, 540, 1200)
    adb.tap(540, 1975, end_time=2)
    adb.tap(540, 1560, count=5, span=1)
    adb.tap(1120, 440, count=5, span=1)


def close_app():
    adb.stop_tiktok()


if __name__ == "__main__":
    wait_start_time(21, 20)
    main()
