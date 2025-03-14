import time

from machigai.domain.AdActivity import AdActivity
from machigai.domain.PlayStoreActivity import PlayStoreActivity
from machigai.MachigaiAdbWrapper import MachigaiAdbWrapper
from time import sleep
import logging
from pathlib import Path
from machigai.calculate_image_position import get_diff_coordinates

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def solve_diff(adb: MachigaiAdbWrapper):
    base_path = Path(__file__).parent
    image_dir_path = base_path / "screenshot"
    image_name = adb.deviceCode
    image_path = Path(image_dir_path, image_name + ".png")
    adb.get_screen_shot(image_dir_path, image_name)
    for x, y in get_diff_coordinates(image_path, adb.get_first_image_coordinate(), adb.get_second_image_coordinate()):
        adb.tap(x, y, end_time=0.5)
    logging.debug("Finish solve_diff")

    time.sleep(7.5)

    # 広告が閉じれるまで待機
    watch_ad(adb)
    logging.debug("Finish on_ad_activity_shown")

    time.sleep(5)
    logging.debug("tap_double_bonus")
    adb.tap_double_bonus()

    # 広告が閉じれるまで待機
    watch_ad(adb)
    logging.debug("Finish tap_double_bonus")

    time.sleep(5)
    logging.debug("tap_close_double_bonus")
    adb.tap_close_double_bonus()

    _, activity_name = adb.getPackageAndActivity()
    if activity_name == ".MainActivity":
        logging.debug("もういっかい")
        time.sleep(5)
        adb.select_recommend_diff()
        time.sleep(5)
        watch_ad(adb)
        solve_diff(adb)
    else:
        logging.debug("終了")


def watch_ad(adb: MachigaiAdbWrapper):
    logging.info("Start Watch Ad")
    time.sleep(2)
    _, activity_name = adb.getPackageAndActivity()
    if ad_activity := AdActivity.resolve(activity_name):
        wait_seconds = ad_activity.get_wait_seconds()
        logging.info(f"AdActivity: {ad_activity}, wait_seconds={wait_seconds}")
        time.sleep(wait_seconds)

    while True:
        _, activity_name = adb.get_package_and_activity()
        if activity_name == ".MainActivity":
            break
        else:
            logging.info(f"Unknown activity: {activity_name}")
            adb.press_back_button()

        time.sleep(1)


def watch_ad_loop(adb: MachigaiAdbWrapper):
    is_ad_played = False
    before_activity_name = ""
    not_main_activity_count = 0
    same_activity_count = 0

    while True:
        package_name, activity_name = adb.getPackageAndActivity()

        is_same_activity = before_activity_name == activity_name
        if is_same_activity:
            same_activity_count += 1
        else:
            same_activity_count = 0

        if activity_name == ".MainActivity":
            not_main_activity_count = 0
        else:
            not_main_activity_count += 1

        logging.debug(f"package={package_name}, activity={activity_name}, same_activity_count={same_activity_count}")

        if ad_activity := AdActivity.resolve(activity_name):
            if not is_ad_played:
                is_ad_played = True
                wait_seconds = ad_activity.get_wait_seconds()
                logging.debug(f"AdActivity: {ad_activity}, wait_seconds={wait_seconds}")
                time.sleep(ad_activity.get_wait_seconds())
            adb.on_ad_activity_shown(ad_activity)
        elif play_store_activity := PlayStoreActivity.resolve(activity_name):
            if play_store_activity:
                adb.on_play_store_activity_shown()

        elif activity_name == ".MainActivity":
            is_ad_played = False
            adb.tap_ad_button()

        else:
            logging.debug(f"Unknown activity: {activity_name}")
            adb.pressBackButton()
            break

        before_activity_name = activity_name

        if same_activity_count >= 10:
            logging.debug("同じActivityが10回続いたため終了します")
            break

        if not_main_activity_count >= 10:
            logging.debug("メインActivity以外が10回続いたため終了します")
            break

        sleep(1)


if __name__ == "__main__":
    pass
