# if activity_name == "com.google.android.gms.ads.AdActivity":
#     print("GoogleのAdActivity")
#     if is_same_activity:
#         adb.tap(960, 160)
#         # 2回以上連続で表示されるのであれば、動画広告画面と判断
#         sleep(60)
#         adb.tap(85, 200, end_time=3)
#         sleep(3)
#
#     else:
#         # 1回目なら戻るボタンで閉じれないか試す
#         adb.tap(960, 160)
# elif activity_name == "com.moloco.sdk.xenoss.sdkdevkit.android.adrenderer.internal.vast.VastActivity":
#     print("MolocoのVastActivity")
#     sleep(70)
#     adb.tap(980, 140, count=2, span=5)
#
# elif activity_name == "com.applovin.adview.AppLovinFullscreenActivity":
#     print("AppLovinのAppLovinFullscreenActivity")
#     if not is_same_activity:
#         sleep(50)
#     else:
#         sleep(3)
#     adb.tap(980, 140, end_time=5)
#     adb.pressBackButton()
#     sleep(2)
#     adb.tap(950, 160)
#
# elif activity_name == "com.bytedance.sdk.openadsdk.activity.TTRewardExpressVideoActivity" or \
#         activity_name == "com.bytedance.sdk.openadsdk.activity.TTFullScreenExpressVideoActivity":
#     print("TikTokのTTRewardExpressVideoActivity")
#     sleep(60)
#     # adb.tap(950, 180, count=2, span=5)
#     adb.tap(1015, 230, count=3, span=5)
#
# elif activity_name == "com.moloco.sdk.xenoss.sdkdevkit.android.adrenderer.internal.mraid.MraidActivity":
#     print("MolocoのMraidActivity")
#     sleep(60)
#     adb.tap(960, 150, count=2, span=5)
#
# elif activity_name == "com.mbridge.msdk.reward.player.MBRewardVideoActivity":
#     print("mbridgeのMBRewardVideoActivity")
#     if not is_same_activity:
#         sleep(60)
#     else:
#         sleep(3)
#     # adb.tap(960, 60)
#     adb.tap(1015, 215)
#
# elif activity_name == "com.inmobi.ads.rendering.InMobiAdActivity":
#     print("InMobiのInMobiAdActivity")
#     sleep(60)
#     # 横画面の場合
#     adb.tap(2200, 60)
#     # 縦画面の場合
#     adb.tap(940, 190)
#
# elif activity_name == "com.vungle.ads.internal.ui.VungleActivity":
#     print("VungleのVungleActivity")
#     sleep(60)
#     adb.tap(1010, 215, count=2, span=5)


# print("間違い探しページ")
# # adb.tap(920, 1950)
# adb.tap(1000, 2070)