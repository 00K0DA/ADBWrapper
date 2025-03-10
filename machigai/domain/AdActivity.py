import unittest
from enum import Enum
from typing import Optional


class AdActivity(Enum):
    Google = "com.google.android.gms.ads.AdActivity"
    Moloco_1 = "com.moloco.sdk.xenoss.sdkdevkit.android.adrenderer.internal.vast.VastActivity"
    Moloco_2 = "com.moloco.sdk.xenoss.sdkdevkit.android.adrenderer.internal.mraid.MraidActivity"
    AppLovin = "com.applovin.adview.AppLovinFullscreenActivity"
    ByteDance_1 = "com.bytedance.sdk.openadsdk.activity.TTRewardExpressVideoActivity"
    ByteDance_2 = "com.bytedance.sdk.openadsdk.activity.TTFullScreenExpressVideoActivity"
    ByteDance_3 = "com.bytedance.sdk.openadsdk.activity.TTRewardVideoActivity"
    MBridge = "com.mbridge.msdk.reward.player.MBRewardVideoActivity"
    InMobi = "com.inmobi.ads.rendering.InMobiAdActivity"
    Vungle = "com.vungle.ads.internal.ui.VungleActivity"
    FiveCorp = "com.five_corp.ad.AdActivity"

    @staticmethod
    def resolve(activity_name: str) -> Optional["AdActivity"]:
        for ad_activity in AdActivity:
            if ad_activity.value == activity_name:
                return ad_activity
        return None

    def get_wait_seconds(self) -> int:
        if self == AdActivity.Moloco_1 or self == AdActivity.Moloco_2 or self == AdActivity.ByteDance_2:
            return 70
        elif self == AdActivity.Vungle:
            return 80
        elif self == AdActivity.ByteDance_1:
            return 65
        else:
            return 60


class TestAdActivity(unittest.TestCase):
    def test_resolve_valid(self):
        """有効なアクティビティ名を渡した場合、正しく `AdActivity` を返すか"""
        self.assertEqual(AdActivity.resolve("com.google.android.gms.ads.AdActivity"), AdActivity.Google)

    def test_resolve_invalid(self):
        """無効なアクティビティ名を渡した場合、None を返すか"""
        self.assertIsNone(AdActivity.resolve("dummy.MainActivity"))
        self.assertIsNone(AdActivity.resolve("com.unknown.sdk.SomeActivity"))


if __name__ == "__main__":
    unittest.main()
