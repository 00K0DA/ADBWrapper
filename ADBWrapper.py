import subprocess
import time
from pathlib import Path
from typing import Union
from MyLogger3 import MyLogger


class ADBWrapper:
    logger = MyLogger("ADBWrapper")
    __DEFAULT_DEVICE_CODE = "__DEFAULT_DEVICE_CODE"
    __COMMAND_TEMPLATE_TAP = "shell input touchscreen tap {x} {y}"
    __COMMAND_TEMPLATE_DOWN = "shell input motionevent DOWN {x} {y}"
    __COMMAND_TEMPLATE_UP = "shell input motionevent UP {x} {y}"
    __COMMAND_TEMPLATE_MOVE = "shell input motionevent MOVE {x} {y}"
    __COMMAND_TEMPLATE_SWIPE = "shell input touchscreen swipe {x1} {y1} {x2} {y2} {swipe_speed}"
    __COMMAND_TEMPLATE_LAUNCH = "shell am start -n {app_id}/{activity_name}"
    __COMMAND_TEMPLATE_TAKE_SCREENSHOT = "shell screencap -p /sdcard/screen_shot_temp.png"
    __COMMAND_TEMPLATE_PULL_SCREENSHOT = "pull /sdcard/screen_shot_temp.png {path}"
    __COMMAND_TEMPLATE_REMOVE_SCREENSHOT = "shell rm /sdcard/screen_shot_temp.png"
    __COMMAND_TEMPLATE_BROADCAST = "shell am broadcast -a {intent_filter}"
    __COMMAND_TEMPLATE_GET_PACKAGE = "shell dumpsys activity activities"

    def __init__(self, target_device_code: str = __DEFAULT_DEVICE_CODE, print_flag: bool = True,
                 file_flag: bool = False):
        self.deviceCode = target_device_code
        self.logger.setPrintFlag(print_flag)
        self.logger.setFileFlag(file_flag)

    def addLogFilePath(self, path: Path) -> None:
        self.logger.addLogFilePath(path)

    def setPrintFlag(self, print_flag: bool) -> None:
        self.logger.setPrintFlag(print_flag)

    def setFileFlag(self, file_flag: bool) -> None:
        self.logger.setFileFlag(file_flag)

    def tap(self, x: int, y: int, sync_flag: bool = True, count: int = 1, span: int = 0, end_time: int = 0) -> None:
        self.logger.info("Tap x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_TAP.format(x=x, y=y)
        )
        for _ in range(count):
            if sync_flag:
                subprocess.run(cmdList, stdout=subprocess.DEVNULL)
            else:
                subprocess.Popen(cmdList, stdout=subprocess.DEVNULL)
            if span != 0:
                time.sleep(span)
        if end_time != 0:
            time.sleep(end_time)

    def longTap(self, x: int, y: int, hold_time: int, sync_flag: bool = True, count: int = 1, span: int = 0,
                end_time: int = 0) -> None:
        self.logger.info("LongTap x={}, y={}, holdTime={}".format(x, y, hold_time))
        downCommandList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_DOWN.format(x=x, y=y)
        )
        upCommandList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_UP.format(x=x, y=y)
        )
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

    def swipe(self, x1: int, y1: int, x2: int, y2: int, end_time: int = 0, swipe_speed: int = 1000) -> None:
        self.logger.info("Swipe x={} to {}, y={} to {}".format(x1, y1, x2, y2))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_SWIPE.format(
                x1=x1, y1=y1, x2=x2, y2=y2, swipe_speed=swipe_speed
            )
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def down(self, x: int, y: int, end_time: int = 0) -> None:
        self.logger.info("DOWN x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_DOWN.format(x=x, y=y)
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def move(self, x: int, y: int, end_time: int = 0, sync_flag: bool = True) -> None:
        self.logger.info("MOVE x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_MOVE.format(x=x, y=y)
        )
        if sync_flag:
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        else:
            subprocess.Popen(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def up(self, x: int, y: int, end_time: int = 0) -> None:
        self.logger.info("(UP x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_UP.format(x=x, y=y)
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def launchApp(self, app_id: str, activity_name: str) -> None:
        self.logger.info("LaunchApp app_id = {}, activity = {}".format(app_id, activity_name))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_LAUNCH.format(
                app_id=app_id,
                activity_name=activity_name
            )
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def getScreenShot(self, path: Path, file_name: str) -> None:
        filePath = Path(path, file_name + ".png")
        self.logger.info("ScreenShot = {}".format(filePath))
        subprocess.run(
            self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_TAKE_SCREENSHOT),
            stdout=subprocess.DEVNULL
        )
        subprocess.run(
            self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_PULL_SCREENSHOT.format(path=filePath)),
            stdout=subprocess.DEVNULL
        )
        subprocess.Popen(
            self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_REMOVE_SCREENSHOT),
            stdout=subprocess.DEVNULL
        )

    def sendBroadcastCommand(self, intent_filter: str, args: dict[str, Union[str, int]]) -> None:
        self.logger.info("SendBroadcast intent_filter={}".format(intent_filter))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_BROADCAST.format(intent_filter=intent_filter)
        )
        for k, v in args.items():
            if type(v) == str:
                self.logger.info("type=String key={}, value={}".format(k, v))
                cmdList.extend(["--es", str(k), str(v)])
            elif type(v) == int:
                self.logger.info("type=Int key={}, value={}".format(k, v))
                cmdList.extend(["--ei", str(k), str(v)])
        self.logger.info(cmdList)
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def getPackageAndActivity(self) -> tuple[str, str]:
        resultStringList = str(subprocess.run(
            self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_GET_PACKAGE), stdout=subprocess.PIPE)
        ).split("\\n")
        for string in resultStringList:
            if "ResumedActivity: ActivityRecord" in string:
                infoTextList = string.lstrip(" ").split(" ")[3].split("/")
                package = infoTextList[0]
                activity = infoTextList[1]
                self.logger.info("package={}".format(package))
                self.logger.info("activity={}".format(activity))
                return package, activity
        return "", ""

    def __createADBCommand(self, command_string: str) -> list[str]:
        commandPrefix = "adb "
        if self.deviceCode is not None:
            commandPrefix += "-s {} ".format(self.deviceCode)
        cmd = commandPrefix + command_string
        return cmd.split(" ")


if __name__ == "__main__":
    pass
