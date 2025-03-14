from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class GetPackage(ADBCommand):
    @property
    def template(self) -> str:
        return "shell dumpsys activity activities"

    def format_command(self) -> str:
        return self.template

@dataclass
class Broadcast(ADBCommand):
    intent_filter: str

    @property
    def template(self) -> str:
        return "shell am broadcast -a {intent_filter}"

    def format_command(self) -> str:
        return self.template.format(intent_filter=self.intent_filter) 