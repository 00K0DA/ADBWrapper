from machigai import MachigaiAdbWrapper
from machigai.domain.AdActivity import AdActivity
from time import sleep

from machigai.senario import watch_ad_loop

class Pixel8ProAdbWrapper(MachigaiAdbWrapper.MachigaiAdbWrapper):
    def __init__(self, target_device_code: str, should_output_log: bool = False):
        super().__init__(target_device_code, should_output_log)


if __name__ == "__main__":
    adb = Pixel8ProAdbWrapper("emulator-5554", should_output_log=True)
