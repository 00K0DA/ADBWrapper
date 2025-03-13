from time import sleep

import DiscordNotificator
from TikTokLiteAdbWrapper import TikTokLiteAdbWrapper
import time
from random import randint
from datetime import datetime, timedelta
from pathlib import Path

from tiktok_lite.TklDiscordNotificator import TklDiscordNotificator  # type: ignore

base_path = Path(__file__).parent
screen_shot_image_name = "screenshot"
screen_shot_path = base_path / f"{screen_shot_image_name}.png"

adb = TikTokLiteAdbWrapper("25111FDF6001YX")
dis = TklDiscordNotificator()


def main() -> None:
    max_tap_count = 5130
    close_app()
    open_app_and_page()
    while True:
        start_time = datetime.now()
        adb.tap(1000, 410)
        send_start_message()
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
                    sleep(5)
            if tap_count % 1000 == 0:
                send_progress_message(tap_count, max_tap_count)
        send_end_message()
        close_app()
        wait_until_next_hour(start_time)
        open_app_and_page()


def tap() -> None:
    # x=540±300, y=1500±300の範囲をタップ
    tap_range = 250
    x = 540 + randint(0, 2 * tap_range) - tap_range
    y = 1500 + randint(0, 2 * tap_range) - tap_range
    adb.tap(x, y)


def close_and_open_page() -> None:
    adb.press_back_button()
    time.sleep(2)
    adb.tap(540, 1975, end_time=2)


def wait_until_next_hour(start_time: datetime) -> None:
    # 次の15分になる時刻を計算
    next_hour = start_time.replace(minute=18, second=0, microsecond=0) + timedelta(hours=1)

    # 次の15分までの待機時間を計算
    wait_time = (next_hour - datetime.now()).total_seconds()

    if wait_time < 0:
        print("Error: wait_time is negative")
        return

    # その時間だけスリープ
    print(f"Waiting for {wait_time} seconds until {next_hour.strftime('%H:%M:%S')}...")
    time.sleep(wait_time)


def open_app_and_page() -> None:
    adb.launch_splash_activity()
    time.sleep(2)
    adb.open_spark_page()
    adb.swipe(540, 200, 540, 1200)
    adb.swipe(540, 200, 540, 1200, end_time=2)
    adb.tap(540, 1975, count=3, span=1, end_time=2)
    adb.tap(540, 1560, count=5, span=1)
    adb.tap(1120, 440, count=5, span=1)


def close_app() -> None:
    adb.stop_tiktok()


def wait_start_time(start_hour: int, start_minute: int = 0, start_second: int = 0) -> None:
    start_time = datetime.now().replace(hour=start_hour, minute=start_minute, second=start_second)
    wait_time = (start_time - datetime.now()).total_seconds()

    if wait_time < 0:
        print("Error: wait_time is negative")
        return

    # その時間だけスリープ
    print(f"Waiting for {wait_time} seconds until {start_time.strftime('%H:%M:%S')}...")
    time.sleep(wait_time)


def send_start_message() -> None:
    adb.getScreenShot(base_path, screen_shot_image_name)
    message = DiscordNotificator.DiscordMessage(
        title="タップ処理の開始",
        message_list=[f"device_code = {adb.deviceCode}"],
        image_path=screen_shot_path
    )
    dis.send_message(message)


def send_progress_message(tap_count: int, max_tap_count: int) -> None:
    adb.getScreenShot(base_path, screen_shot_image_name)
    percent = tap_count / max_tap_count * 100
    message = DiscordNotificator.DiscordMessage(
        title="進捗",
        message_list=[
            f"device_code = {adb.deviceCode}",
            f"{tap_count} taps completed. {percent:.2f}%"],
        image_path=screen_shot_path
    )
    dis.send_message(message)


def send_end_message() -> None:
    adb.getScreenShot(base_path, screen_shot_image_name)
    message = DiscordNotificator.DiscordMessage(
        title="タップ処理の終了",
        message_list=[f"device_code = {adb.deviceCode}"],
        image_path=screen_shot_path
    )

    dis.send_message(message)


if __name__ == "__main__":
    # wait_start_time(0, 20)
    main()
