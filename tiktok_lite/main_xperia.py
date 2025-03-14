from TikTokLiteAdbWrapper import TikTokLiteAdbWrapper
import time
from random import randint
from random import shuffle

adb = TikTokLiteAdbWrapper("HQ631V0CEF")


def watch_video():
    adb.setScreenGrayScale(True)
    if adb.is_tiktok_lite_running():
        adb.stop_tiktok()
    adb.launch_splash_activity()
    start_time = time.time()
    last_restart_app_time = start_time
    video_count = 0
    while True:
        video_count += 1

        # 読み込みも含めて3秒待つ
        time.sleep(3)

        # 3時間経過したら終了
        if time.time() - start_time > 3600 * 6:
            break

        wait_seconds = randint(100, 120) / 10
        time.sleep(wait_seconds)

        # まれにギフトページに遷移するので、動画画面に戻す
        if not adb.is_splash_activity_shown():
            adb.launch_splash_activity()
            # 読み込みも含めて3秒待つ
            time.sleep(2)

        # 動画をスワイプする
        adb.swipe_to_next_video()

        if not video_count == 0 and video_count % 5 == 0:
            elapsed_time = time.time() - start_time
            print(f"{video_count} videos watched. Elapsed time: {elapsed_time // 60:.0f}m {elapsed_time % 60:.0f}s")

        if time.time() - last_restart_app_time > 60 * 6:
            print("Restart app")
            adb.stop_tiktok()
            adb.launch_splash_activity()
            last_restart_app_time = time.time()

    adb.setScreenGrayScale(False)
    adb.pressPowerButton()


def watch_video_v2():
    adb.launch_splash_activity()
    start_time = time.time()
    last_restart_app_time = start_time
    video_count = 0
    adb.long_tap(540, 410, 2)
    pass


def watch_reward_video(count=30):
    for _ in range(count):
        print("広告を再生します")
        adb.press_reward_button()
        time.sleep(25)
        print("広告を閉じます")
        adb.pressBackButton()
        time.sleep(2)


def claim_watch_live():
    adb.press_start_watch_live_button()
    time.sleep(5)
    adb.press_watch_live_reward_button()
    time.sleep(5)
    claim_count = 0
    while True:
        if adb.is_live_watch_reward_can_not_claim():
            print("Watch LIVE")
            time.sleep(20)
        else:
            print("Claim")
            adb.press_claim_watch_live_reward_button()
            claim_count += 1
            if claim_count >= 10:
                break
    print("閉じる")
    adb.press_close_live_watch_page_button()


def search_video(count=20):
    search_word_list = [
        "Twice", "Nayeon", "Jeongyeon", "Momo", "Sana", "Jihyo", "Mina", "Dahyun", "Chaeyoung", "Tzuyu",
        "shiba inu", "shiba", "misamo", "myakkomyako", "ramuzuqun", "misachunchun", "enako_cos", "mumei",
        "menmenman_39",
        "pokemon", "pikachu", "eevee", "mew", "mewtwo", "charizard", "bulbasaur", "squirtle", "psyduck", "snorlax",
    ]
    shuffle(search_word_list)
    print("検索ボタンを押します。")
    adb.tap(875, 1750)
    time.sleep(2)
    for i in range(count):
        word = search_word_list[i % len(search_word_list)]
        print(f"{i + 1}回目の検索: {word}")
        adb.inputText(word)
        time.sleep(1)
        adb.tap(1000, 185)
        print("待機")
        time.sleep(20)

        print("単語入力画面に戻ります")
        adb.pressBackButton()
        time.sleep(1)

    for _ in range(2):
        adb.pressBackButton()
        time.sleep(1)


if __name__ == "__main__":
    # adb.setScreenGrayScale(True)

    # y=900の部分にボタンを持ってきて
    # watch_reward_video(30)

    # watch_video()

    # y=1750の部分にボタンを持ってきて
    search_video(12)

    # claim_watch_live()
    # print(adb.getPackageAndActivity())
