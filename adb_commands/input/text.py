from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class Text(ADBCommand):
    text: str

    @property
    def template(self) -> str:
        return "shell input text {text}"

    def format_command(self) -> str:
        return self.template.format(text=self.text)

@dataclass
class KeyEvent(ADBCommand):
    key_code: str

    @property
    def template(self) -> str:
        return "shell input keyevent {key_code}"

    def format_command(self) -> str:
        return self.template.format(key_code=self.key_code) 