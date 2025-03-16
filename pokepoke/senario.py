from pokepoke.PokePokeAdbWrapper import PokePokeADBWrapper
import logging
from Sound_Player import SoundPlayer
from datetime import datetime, timedelta
import time

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
sound_player = SoundPlayer()


def daily(adb: PokePokeADBWrapper, retry_count: int):
    if retry_count >= 3:
        logging.debug("Retry count is over")
        return
    start_time = datetime.now()
    logging.debug("Start daily")
    adb.send_start_message()
    adb.close_abnormal_dialog()

    adb.stop_pokepoke()
    adb.open_pokepoke()
    adb.open_home_screen()
    if not adb.is_home_screen_shown():
        logging.debug("Can Open Pack!!")
        logging.debug("Open Pack")
        adb.open_pack_list_screen()
        logging.debug("Select pack")
        adb.select_pack()
        logging.debug("Open pack")
        adb.open_pack()
        logging.debug("Open pack result screen")
        adb.on_open_pack_result_screen()
        # # 未入手のカードがあった
        adb.on_get_new_cards()
        daily(adb, retry_count + 1)
    else:
        logging.debug("Can't Open Pack!!")
        logging.debug("Claim daily mission reward")
        adb.claim_daily_mission_reward()
        logging.debug("Claim free item")
        adb.claim_free_item()
        logging.debug("Open Community")
        adb.open_community_screen()
        logging.debug("Auto like")
        adb.auto_like()
        logging.debug("Finish daily")

    next_start_time = start_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=4)
    wait_time = (next_start_time - start_time).total_seconds()

    sound_player.notify()

    logging.debug(f"Waiting for {wait_time} seconds...")
    adb.send_finish_message(next_start_time)
    time.sleep(wait_time)
    daily(adb, 0)


if __name__ == "__main__":
    pass
