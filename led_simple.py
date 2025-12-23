#!/usr/bin/env python3
"""
LED点灯アプリ（シンプル版）
LEDを点灯・消灯するだけの基本的なプログラム
要件定義書: 06-001_LED点灯アプリ_要件定義書.md
"""

# 標準ライブラリ
import sys
from time import sleep

# サードパーティライブラリ
# gpiozero: Raspberry Pi GPIO制御用ライブラリ（ピン設定を自動で行う）
from gpiozero import LED


def main():
    """
    メイン関数：LEDを点灯・消灯する
    3秒点灯 → 1秒消灯 → 終了
    """
    # --- LED初期化 ---
    # GPIO17（物理ピン11）を使用してLEDを制御
    # gpiozeroライブラリが自動的にピンを出力モードに設定する
    try:
        led = LED(17)
    except Exception as e:
        print(f"[GPIO初期化]エラー: {e}")
        print("対処方法: 配線とGPIOピンを確認してください")
        print("ヒント: 他のプログラムがGPIO17を使用していないか確認")
        sys.exit(1)

    # --- メイン処理 ---
    try:
        # LED点灯（GPIO17をHIGHに設定）
        print("LEDを点灯します")
        led.on()
        sleep(3)  # 3秒間点灯

        # LED消灯（GPIO17をLOWに設定）
        print("LEDを消灯します")
        led.off()
        sleep(1)  # 1秒間消灯

        print("プログラム終了")

    # --- 終了処理 ---
    finally:
        # GPIOリソースをクリーンアップ
        # gpiozeroではclose()でピンを解放する
        led.close()
        print("GPIOリソースを解放しました")


if __name__ == "__main__":
    main()
