import time
from abc import ABC, abstractmethod
from ADBWrapper import ADBWrapper
from machigai.domain.AdActivity import AdActivity
from machigai.domain.Coordinate import Coordinate


class MachigaiAdbWrapper(ADBWrapper, ABC):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)

    @abstractmethod
    def on_ad_activity_shown(self, ad_activity: AdActivity):
        pass

    @abstractmethod
    def tap_ad_button(self):
        pass

    @abstractmethod
    def tap_double_bonus(self):
        pass

    @abstractmethod
    def tap_close_double_bonus(self):
        pass

    @abstractmethod
    def select_recommend_diff(self):
        pass

    @abstractmethod
    def get_first_image_coordinate(self) -> Coordinate:
        pass

    @abstractmethod
    def get_second_image_coordinate(self) -> Coordinate:
        pass

    def on_play_store_activity_shown(self):
        self.pressBackButton()


if __name__ == "__main__":
    pass
