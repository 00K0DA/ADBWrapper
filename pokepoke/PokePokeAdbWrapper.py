from ADBWrapper import ADBWrapper
from abc import ABC, abstractmethod
from datetime import datetime
from DiscordNotificator import DiscordMessage
from image_util import get_color
from pathlib import Path
import numpy as np
from time import sleep
from pokepoke.PokePokeDiscordNotificator import PokePokeDiscordNotificator


class PokePokeADBWrapper(ADBWrapper, ABC):
    base_path = Path(__file__).parent
    app_id = "jp.pokemon.pokemontcgp"
    activity = "com.unity3d.player.UnityPlayerActivity"
    dis = PokePokeDiscordNotificator()

    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)
        self.image_name = target_device_code
        self.image_dir_path = Path(self.base_path, "screenshot")
        self.image_path = Path(self.image_dir_path, self.image_name + ".png")

    def open_pokepoke(self):
        if self.is_pokepoke_running():
            self.stop_pokepoke()
            sleep(5)
        self.launch_app(self.app_id, self.activity)

    def stop_pokepoke(self):
        self.stop_app(app_id=self.app_id)

    def open_home_screen(self):
        sleep(10)
        self.tap(540, 1600)
        sleep(10)

    def is_home_screen_shown(self) -> bool:
        self.get_screen_shot(self.image_dir_path, self.image_name)
        home_color_list = [(242, 236, 224), (241, 236, 226)]
        color = get_color(0, 0, self.image_path)
        result_list = [np.array_equal(color, home_color) for home_color in home_color_list]
        return any(result_list)

    def is_pokepoke_running(self) -> bool:
        package_name, activity_name = self.get_package_and_activity()
        return package_name == self.app_id and activity_name == self.activity

    @abstractmethod
    def open_pack_list_screen(self):
        pass

    @abstractmethod
    def select_pack(self):
        pass

    @abstractmethod
    def open_pack(self):
        pass

    @abstractmethod
    def on_open_pack_result_screen(self):
        pass

    @abstractmethod
    def tap_skip_button(self, end_time=5):
        pass

    @abstractmethod
    def tap_next_button(self, end_time=5):
        pass

    def on_get_new_cards(self):
        self.tap_skip_button()
        self.tap_next_button()
        self.tap_next_button()

    @abstractmethod
    def claim_free_item(self):
        pass

    @abstractmethod
    def claim_daily_mission_reward(self):
        pass

    @abstractmethod
    def open_community_screen(self):
        pass

    @abstractmethod
    def auto_like(self):
        pass

    def is_liked(self, x, y) -> bool:
        self.get_screen_shot(self.image_dir_path, self.image_name)
        liked_color_list = [(249, 246, 239), (249, 246, 240)]
        color = get_color(x, y, self.image_path)
        result_list = [np.array_equal(color, liked_color) for liked_color in liked_color_list]
        return any(result_list)

    def send_result_screen(self):
        self.get_screen_shot(self.image_dir_path, self.image_name)
        message = DiscordMessage(
            title="開封結果",
            message_list=[f"device_code = {self.device_code}"],
            image_path=self.image_path
        )
        self.dis.send_message(message)

    def send_start_message(self):
        message = DiscordMessage(
            title="処理を開始します。",
            message_list=[f"device_code = {self.device_code}"],
        )
        self.dis.send_message(message)

    def send_finish_message(self, next_start_datetime: datetime):
        datetime_string = next_start_datetime.strftime("%Y-%m-%d %H:%M:%S")
        message = DiscordMessage(
            title="処理の終了",
            message_list=[f"device_code = {self.device_code}", f"次の動作予定時刻 = {datetime_string}"]
        )
        self.dis.send_message(message)

    @abstractmethod
    def close_abnormal_dialog(self):
        pass