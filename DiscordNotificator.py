import requests
from pathlib import Path
from dataclasses import dataclass, field
import time
from enum import Enum


@dataclass(frozen=True)
class DiscordMessage:
    title: str = None
    message_list: list[str] = field(default_factory=list)
    image_path: Path = None
    add_timestamp: bool = True

    def get_data(self):
        if self.is_message_empty():
            return {}

        send_message_list = [
            f"**{self.title}**" if self.title else "",
            self.__get_time_string() if self.add_timestamp else "",
            "=" * 32 if self.title else "",
            *self.message_list,
            "=" * 32 if self.message_list else "",
        ]

        send_message_list = [m for m in send_message_list if m]

        data = {
            "content": "\n".join(send_message_list)
        }
        return data

    def get_file(self):
        if self.image_path is None or not self.image_path.exists():
            return {}
        image = open(self.image_path, "rb")
        return {"image": image}

    def is_message_empty(self):
        return not bool(self.title or self.message_list or self.add_timestamp)

    @staticmethod
    def __get_time_string():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class DiscordNotificator:
    def __init__(self, web_hook_url: str):
        self.webhook_url = web_hook_url

    def send_message(self, discord_message: DiscordMessage) -> None:
        requests.post(self.webhook_url, data=discord_message.get_data(), files=discord_message.get_file())


if __name__ == "__main__":
    pass
