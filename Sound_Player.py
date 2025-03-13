from playsound import playsound
from pathlib import Path


class SoundPlayer:
    base_path = Path(__file__).parent
    sound_dir_path = Path(base_path, "resource")
    notify_sound_path = Path(sound_dir_path, "notifi_1.m4a")

    def notify(self):
        playsound(self.notify_sound_path)

if __name__ == "__main__":
    SoundPlayer().notify()
