import time

from pokepoke.PokePokeAdbWrapper import PokePokeADBWrapper
from pokepoke.senario import daily


class Pixel8ProAdbWrapper(PokePokeADBWrapper):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)

    def open_pack_list_screen(self):
        self.tap(840, 2025, end_time=2)

    def select_pack(self):
        # リストからパックを選択
        self.tap(820, 1025, end_time=10)
        # パックを前面に表示
        self.tap(540, 1400, end_time=5)

    def open_pack(self):
        # 「開封する」をタップ
        self.tap(540, 1800, end_time=5)
        # スキップボタンをタップ
        self.tap_skip_button()
        # パックを開く
        self.swipe(100, 1245, 900, 1245, swipe_speed=500, end_time=5)
        # カードを一枚づつ見る
        self.tap(540, 1120, count=5, span=1, end_time=5)

    def on_open_pack_result_screen(self):
        # 写真を送る
        self.send_result_screen()
        # 「次へ」をタップ
        self.tap(540, 2150, end_time=5)

    def tap_skip_button(self, end_time=5):
        self.tap(925, 2150, end_time=end_time)

    def tap_next_button(self, end_time=5):
        self.tap(540, 2050, end_time=5)

    def claim_free_item(self):
        # ショップ/交換所を開く
        self.tap(735, 1570, end_time=5)
        # 毎日プレゼントを受け取る
        self.tap(540, 800, end_time=5)
        # OKをタップ
        self.tap(540, 1475, end_time=5)
        # 閉じる
        self.tap(540, 2150, end_time=5)

    def claim_daily_mission_reward(self):
        # ミッションを開く
        self.tap(925, 2000, end_time=5)

        # デイリーミッションのタブを選択
        self.swipe(100, 2000, 800, 2000, swipe_speed=250, end_time=1)
        self.tap(250, 2000, end_time=1)

        # 「まとめて受け取る」をタップ
        self.tap(800, 1850, end_time=5)
        # 受け取る
        self.tap(945, 445, end_time=5)
        # 「OK」をタップ
        self.tap(540, 1425, end_time=5)
        # 閉じるをタップ
        self.tap(540, 2100, end_time=5, count=3, span=1)
        pass

    def open_community_screen(self):
        self.tap(500, 2185, end_time=5)

    def auto_like(self):
        # 誰かのコレクション
        self.tap(265, 1800, end_time=5)
        # 先頭のフレンドを選択
        self.tap(330, 1625, end_time=5)
        while self.is_liked(625, 670):
            self.tap(625, 670, end_time=1)
            self.swipe(900, 900, 100, 900, swipe_speed=250, end_time=5)
        # 閉じる
        self.tap(500, 2150, end_time=5)
        # ホームに戻る
        self.tap(140, 2185, end_time=5)

    def close_abnormal_dialog(self):
        self.stop_pokepoke()
        time.sleep(5)
        self.open_pokepoke()
        adb.open_home_screen()
        #カードの取得が正常に行われていない場合に出るダイアログを閉じる
        adb.tap(540, 1475, end_time=2)
        self.stop_pokepoke()


if __name__ == "__main__":
    # Wired
    adb = Pixel8ProAdbWrapper("37311FDJG009F5")

    # Wireless
    # adb = Pixel8ProAdbWrapper("adb-37311FDJG009F5-5QIqGs._adb-tls-connect._tcp")
    daily(adb, retry_count=0)
    # adb.send_result_screen()
