from DiscordNotificator import DiscordNotificator, DiscordMessage


class TklDiscordNotificator(DiscordNotificator):
    __web_hook__url = "https://discord.com/api/webhooks/1348661613917376574/rTd78IeLs4G6rmXNc-VZouAR9uCx41Of8_tEnRLyOAwQwnGKK48U71BlMkrAYR1NimtO"

    def __init__(self) -> None:
        super().__init__(self.__web_hook__url)

    def send_message(self, discord_message: DiscordMessage) -> None:
        super().send_message(discord_message)
