import re
import subprocess
import time
import logging
from pathlib import Path
from typing import Union
from threading import Timer
from adb_commands import (
    # Input Commands
    Tap, Swipe, Down, Up, Move, Text, KeyEvent,
    # App Commands
    Launch, Stop, GetPackage, Broadcast,
    # System Commands
    Reboot, WaitForDevice, WaitForBootComplete, ConnectWireless,
    # Device Commands
    Take as ScreenshotTake, Sync as ScreenshotSync,
    Pull as ScreenshotPull, Remove as ScreenshotRemove,
    SetDaltonizerEnabled, SetDaltonizerGrayScale
)


class ADBWrapper:
    __DEFAULT_DEVICE_CODE = "__DEFAULT_DEVICE_CODE"

    def __init__(self, target_device_code: str = __DEFAULT_DEVICE_CODE, print_flag: bool = True):
        self.deviceCode = target_device_code
        self.logger = logging.getLogger(__name__)
        self.stream_handler = None
        self.set_print_flag(print_flag)

    def add_log_file_path(self, path: Path) -> None:
        handler = logging.FileHandler(path)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def set_print_flag(self, print_flag: bool) -> None:
        if print_flag:
            if self.stream_handler is None:
                self.stream_handler = logging.StreamHandler()
                self.stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                self.logger.addHandler(self.stream_handler)
            self.logger.setLevel(logging.INFO)
        else:
            if self.stream_handler is not None:
                self.logger.removeHandler(self.stream_handler)
                self.stream_handler = None
            self.logger.setLevel(logging.WARNING)

    def set_file_flag(self, file_flag: bool) -> None:
        if file_flag:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)

    def tap(self, x: int, y: int, sync_flag: bool = True, count: int = 1, span: int = 0,
            end_time: int or float = 0) -> None:
        self.logger.info("Tap x=%d, y=%d", x, y)
        cmd = Tap(x=x, y=y)
        cmdList = self.__createADBCommand(cmd.format_command())
        for _ in range(count):
            if sync_flag:
                subprocess.run(cmdList, stdout=subprocess.DEVNULL)
            else:
                subprocess.Popen(cmdList, stdout=subprocess.DEVNULL)
            if span != 0:
                time.sleep(span)
        if end_time != 0:
            time.sleep(end_time)

    def long_tap(self, x: int, y: int, hold_time: int, sync_flag: bool = True, count: int = 1, span: int = 0,
                end_time: int = 0) -> None:
        self.logger.info("LongTap x=%d, y=%d, holdTime=%d", x, y, hold_time)
        down_cmd = Down(x=x, y=y)
        up_cmd = Up(x=x, y=y)
        downCommandList = self.__createADBCommand(down_cmd.format_command())
        upCommandList = self.__createADBCommand(up_cmd.format_command())
        for _ in range(count):
            if sync_flag:
                subprocess.run(downCommandList, stdout=subprocess.DEVNULL)
                time.sleep(hold_time)
                subprocess.run(upCommandList, stdout=subprocess.DEVNULL)
            else:
                subprocess.Popen(downCommandList, stdout=subprocess.DEVNULL)
                time.sleep(hold_time)
                subprocess.Popen(upCommandList, stdout=subprocess.DEVNULL)
            if span != 0:
                time.sleep(span)
        if end_time != 0:
            time.sleep(end_time)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, end_time: int or float = 0, swipe_speed: int = 1000) -> None:
        self.logger.info("Swipe x=%d to %d, y=%d to %d", x1, x2, y1, y2)
        cmd = Swipe(x1=x1, y1=y1, x2=x2, y2=y2, swipe_speed=swipe_speed)
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def down(self, x: int, y: int, end_time: int = 0) -> None:
        self.logger.info("DOWN x=%d, y=%d", x, y)
        cmd = Down(x=x, y=y)
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def move(self, x: int, y: int, end_time: int = 0, sync_flag: bool = True) -> None:
        self.logger.info("MOVE x=%d, y=%d", x, y)
        cmd = Move(x=x, y=y)
        cmdList = self.__createADBCommand(cmd.format_command())
        if sync_flag:
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        else:
            subprocess.Popen(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def up(self, x: int, y: int, end_time: int = 0) -> None:
        self.logger.info("UP x=%d, y=%d", x, y)
        cmd = Up(x=x, y=y)
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def launchApp(self, app_id: str, activity_name: str) -> None:
        self.logger.info("LaunchApp app_id = %s, activity = %s", app_id, activity_name)
        cmd = Launch(app_id=app_id, activity_name=activity_name)
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.PIPE)

    def getScreenShot(self, path: Path, file_name: str) -> None:
        filePath = Path(path, file_name + ".png")
        self.logger.info("ScreenShot = %s", filePath)
        while True:
            result = subprocess.run(
                self.__createADBCommand(ScreenshotTake().format_command()),
                stdout=subprocess.PIPE
            )
            if result.returncode == 0:
                break
            else:
                time.sleep(1)
        subprocess.run(
            self.__createADBCommand(ScreenshotSync().format_command()),
            stdout=subprocess.DEVNULL
        )
        subprocess.run(
            self.__createADBCommand(ScreenshotPull(path=filePath).format_command()),
            stdout=subprocess.DEVNULL
        )
        subprocess.run(
            self.__createADBCommand(ScreenshotRemove().format_command()),
            stdout=subprocess.DEVNULL
        )

    def sendBroadcastCommand(self, intent_filter: str, args: dict[str, Union[str, int]]) -> None:
        self.logger.info("SendBroadcast intent_filter=%s", intent_filter)
        cmd = Broadcast(intent_filter=intent_filter)
        cmdList = self.__createADBCommand(cmd.format_command())
        for k, v in args.items():
            if type(v) == str:
                self.logger.info("type=String key=%s, value=%s", k, v)
            elif type(v) == int:
                self.logger.info("type=Int key=%s, value=%d", k, v)
            cmdList.extend(["--{}".format("es" if type(v) == str else "ei"), str(k), str(v)])
        self.logger.info("command=%s", cmdList)
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def getPackageAndActivity(self) -> tuple[str, str]:
        while True:
            result = subprocess.run(
                self.__createADBCommand(GetPackage().format_command()),
                stdout=subprocess.PIPE
            )
            if result.returncode == 0:
                break
            else:
                time.sleep(1)

        for string in result.stdout.decode("utf-8").split("\n"):
            if "ResumedActivity: ActivityRecord" in string:
                infoTextList = string.lstrip(" ").split(" ")[3].split("/")
                package = infoTextList[0]
                activity = infoTextList[1]
                self.logger.info("package=%s", package)
                self.logger.info("activity=%s", activity)
                return package, activity
        return "", ""

    def wirelessConnect(self, ip_address: str, port: str) -> None:
        self.logger.info("Connect to %s:%s", ip_address, port)
        cmd = ConnectWireless(ip_address=ip_address, port=port)
        cmdList = self.__createADBCommand(cmd.format_command())
        self.deviceCode = "{}:{}".format(ip_address, port)
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def pressPowerButton(self) -> None:
        self.logger.info("Press Power Button")
        self.__keyEvent("KEYCODE_POWER")

    def reboot(self) -> None:
        self.logger.info("Reboot")
        cmd = Reboot()
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def waitForDevice(self) -> None:
        self.logger.info("WaitForDevice")
        cmd = WaitForDevice()
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def waitForBootComplete(self) -> None:
        self.logger.info("WaitForBootComplete")
        cmd = WaitForBootComplete()
        cmdList = self.__createADBCommand(cmd.format_command())
        while True:
            result = subprocess.run(cmdList, stdout=subprocess.PIPE)
            self.logger.info("result=%s", result)
            self.logger.info("stdout=%s", result.stdout)
            if "1" in str(result.stdout):
                break
            else:
                time.sleep(3)

    def stopApp(self, app_id: str) -> None:
        self.logger.info("StopApp app_id=%s", app_id)
        cmd = Stop(app_id=app_id)
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def setScreenGrayScale(self, enabled: bool) -> None:
        if enabled:
            cmd = SetDaltonizerEnabled(enabled=1)
            cmdList = self.__createADBCommand(cmd.format_command())
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)
            cmd = SetDaltonizerGrayScale()
            cmdList = self.__createADBCommand(cmd.format_command())
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        else:
            cmd = SetDaltonizerEnabled(enabled=0)
            cmdList = self.__createADBCommand(cmd.format_command())
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def pressBackButton(self) -> None:
        self.__keyEvent("KEYCODE_BACK")

    def pressEnterButton(self) -> None:
        self.__keyEvent("KEYCODE_ENTER")

    def pressSearchButton(self) -> None:
        self.__keyEvent("KEYCODE_SEARCH")

    def inputText(self, text: str) -> None:
        text = text.replace(" ", "%s")
        cmd = Text(text=text)
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def __keyEvent(self, key_code: str) -> None:
        cmd = KeyEvent(key_code=key_code)
        cmdList = self.__createADBCommand(cmd.format_command())
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def __createADBCommand(self, command_string: str) -> list[str]:
        commandPrefix = "adb "
        if self.deviceCode is not None:
            commandPrefix += "-s {} ".format(self.deviceCode)
        cmd = commandPrefix + command_string
        self.logger.info("cmd = %s", cmd)
        return cmd.split(" ")


if __name__ == "__main__":
    adb = ADBWrapper("37311FDJG009F5")
    adb.getPackageAndActivity()
    pass
