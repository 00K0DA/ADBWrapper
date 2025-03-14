from abc import ABC, abstractmethod

class ADBCommand(ABC):
    @property
    @abstractmethod
    def template(self) -> str:
        """コマンドのテンプレート文字列を返す"""
        pass

    @abstractmethod
    def format_command(self) -> str:
        """テンプレートに値を埋め込んだコマンドを返す"""
        pass 