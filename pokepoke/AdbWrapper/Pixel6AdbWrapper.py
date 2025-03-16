from pokepoke.PokePokeAdbWrapper import PokePokeADBWrapper
from pokepoke.senario import daily


class Pixel6AdbWrapper(PokePokeADBWrapper):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)

    def open_pack_list_screen(self):
        self.tap(840, 2150, end_time=2)

    def select_pack(self):
        # リストからパックを選択
        self.tap(885, 1115, end_time=10)
        # パックを前面に表示
        self.tap(540, 1400, end_time=5)

    def open_pack(self):
        # 「開封する」をタップ
        self.tap(540, 1900, end_time=5)
        # スキップボタンをタップ
        self.tap_skip_button()
        # パックを開く
        self.swipe(65, 1325, 900, 1325, swipe_speed=500, end_time=5)
        # カードを一枚づつ見る(早送りする)
        self.down(1000, 2300, end_time=10)
        self.up(1000, 2300, end_time=5)

    def on_open_pack_result_screen(self):
        # 写真を送る
        self.send_result_screen()
        # 「次へ」をタップ
        self.tap(540, 2280, end_time=5)

    def tap_skip_button(self, end_time=5):
        self.tap(1000, 2300, end_time=end_time)

    def tap_next_button(self, end_time=5):
        self.tap(540, 2200, end_time=5)

    def claim_free_item(self):
        # ショップ/交換所を開く
        self.tap(735, 1700, end_time=5)
        # 毎日プレゼントを受け取る
        self.tap(540, 800, end_time=5)
        # OKをタップ
        self.tap(540, 1575, end_time=5)
        # 閉じる
        self.tap(540, 2240, end_time=5, count=3, span=1)

    def claim_daily_mission_reward(self):
        # ミッションを開く
        self.tap(1000, 2100, end_time=5)

        # デイリーミッションのタブを選択
        self.swipe(100, 2120, 800, 2120, swipe_speed=250, end_time=1)
        self.tap(250, 2120, end_time=1)

        # 「まとめて受け取る」をタップ
        self.tap(800, 1980, end_time=5)
        # 受け取る
        self.tap(1000, 450, end_time=5)
        # 「OK」をタップ
        self.tap(540, 1515, end_time=5)
        # 閉じるをタップ
        self.tap(540, 2240, end_time=5, count=3, span=1)

    def open_community_screen(self):
        self.tap(500, 2320, end_time=5)

    def auto_like(self):
        # 誰かのコレクション
        self.tap(265, 1900, end_time=5)
        # 先頭のフレンドを選択
        self.tap(345, 1750, end_time=5)
        while self.is_liked(675, 740):
            self.tap(675, 740, end_time=1)
            self.swipe(900, 900, 100, 900, swipe_speed=250, end_time=5)
        # 閉じる
        self.tap(540, 2290, end_time=5)
        # ホームに戻る
        self.tap(140, 2320, end_time=5)


if __name__ == "__main__":
    # Wired
    adb = Pixel6AdbWrapper("25111FDF6001YX")

    # Wireless
    # adb = Pixel8ProAdbWrapper("adb-37311FDJG009F5-5QIqGs._adb-tls-connect._tcp")
    from datetime import datetime, timedelta
    import time

    while True:
        now = datetime.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=4)
        wait_time = (next_hour - now).total_seconds()
        if wait_time < 0:
            break
        else:
            print(f"Waiting for {wait_time} seconds...")
            time.sleep(wait_time)

        daily(adb)
