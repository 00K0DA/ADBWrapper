from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class SetDaltonizerEnabled(ADBCommand):
    enabled: int

    @property
    def template(self) -> str:
        return "shell settings put secure accessibility_display_daltonizer_enabled {enabled}"

    def format_command(self) -> str:
        return self.template.format(enabled=self.enabled)

@dataclass
class SetDaltonizerGrayScale(ADBCommand):
    @property
    def template(self) -> str:
        return "shell settings put secure accessibility_display_daltonizer 0"

    def format_command(self) -> str:
        return self.template 