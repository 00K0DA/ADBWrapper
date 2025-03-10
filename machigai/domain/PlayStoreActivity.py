from enum import Enum
from typing import Optional
import unittest


class PlayStoreActivity(Enum):
    MainActivity = "com.google.android.finsky.activities.MainActivity"
    TransParentActivity = "com.google.android.finsky.transparentmainactivity.TransparentMainActivity"
    AssetBrowserActivity = ".AssetBrowserActivity"

    @staticmethod
    def resolve(activity_name: str) -> Optional["PlayStoreActivity"]:
        for play_store_activity in PlayStoreActivity:
            if play_store_activity.value == activity_name:
                return play_store_activity
        return None


class TestPlayStoreActivity(unittest.TestCase):
    def test_resolve(self):
        self.assertEqual(PlayStoreActivity.resolve("com.google.android.finsky.activities.MainActivity"),
                         PlayStoreActivity.MainActivity)
        self.assertEqual(
            PlayStoreActivity.resolve("com.google.android.finsky.transparentmainactivity.TransparentMainActivity"),
            PlayStoreActivity.TransParentActivity)
        self.assertIsNone(PlayStoreActivity.resolve("dummy.MainActivity"))


if __name__ == "__main__":
    unittest.main()
