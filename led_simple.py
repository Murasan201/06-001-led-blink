#!/usr/bin/env python3
"""
LED点灯アプリ（シンプル版）
LEDを点灯・消灯するだけの基本的なプログラム
要件定義書: 06-001_LED点灯アプリ_要件定義書.md
"""

# 標準ライブラリ
from time import sleep

# サードパーティライブラリ
from gpiozero import LED


def main():
    """
    メイン関数：LEDを点灯・消灯する
    """
    # GPIO 17のLEDオブジェクトを作成
    led = LED(17)

    try:
        # LEDを点灯
        print("LEDを点灯します")
        led.on()
        sleep(3)  # 3秒間点灯

        # LEDを消灯
        print("LEDを消灯します")
        led.off()
        sleep(1)  # 1秒間消灯

        print("プログラム終了")

    finally:
        # GPIOリソースをクリーンアップ
        led.close()


if __name__ == "__main__":
    main()
