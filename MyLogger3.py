import datetime
import inspect
from pathlib import Path


class MyLogger:
    # Constructor
    def __init__(self, logger_name="MyLogger", print_flag=True, file_flag=False):
        self.loggerName = logger_name
        self.printFlag = print_flag
        self.fileFlag = file_flag
        self.filePathList = []

    # API for modify configs.
    def addLogFilePath(self, path):
        tempPath = Path(path)
        if tempPath in self.filePathList:
            return
        self.__makeFileIfNotExists(tempPath)
        self.filePathList.append(tempPath)

    def setFileFlag(self, boolean):
        self.fileFlag = boolean

    def setPrintFlag(self, boolean):
        self.printFlag = boolean

    # APIs for adding logs.
    def info(self, log):
        self.__addLog("INFO", log)

    def debug(self, log):
        self.__addLog("DEBUG", log)

    def warn(self, log):
        self.__addLog("WARN", log)

    def error(self, log):
        self.__addLog("ERROR", log)

    def notice(self, log):
        self.__addLog("NOTICE", log)

    def startFuncLog(self):
        funcName = inspect.stack()[1].function
        self.info("Start {}".format(funcName))

    def finishFuncLog(self):
        funcName = inspect.stack()[1].function
        self.info("Finish {}".format(funcName))

    def createLog(self, target_name=None):
        if target_name is None:
            target_name = self.loggerName
        self.info("Created {}".format(target_name))

    # Private Functions
    def __addLog(self, tag, log):
        tag = self.__makeFormatTag(tag)
        dataString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logText = "{} {} {} {}".format(dataString, self.loggerName, tag, log)
        if self.printFlag:
            print(logText)

        if len(self.filePathList) == 0 or not self.fileFlag:
            return
        self.__addLogToFile(logText)

    def __addLogToFile(self, log_text):
        for filePath in self.filePathList:
            self.__makeFileIfNotExists(filePath)
            with open(filePath, "a", encoding="utf-8") as f:
                f.write(log_text + "\n")

    @staticmethod
    def __makeFormatTag(tag):
        return "[{}]".format(tag).ljust(8)

    @staticmethod
    def __makeFileIfNotExists(path):
        if not path.exists():
            path.parent.mkdir(parents=True)
            path.touch()


if __name__ == "__main__":
    pass
