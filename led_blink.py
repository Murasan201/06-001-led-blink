#!/usr/bin/env python3
"""
LED点滅アプリ
LEDを繰り返し点滅させるプログラム
要件定義書: 06-001_LED点灯アプリ_要件定義書.md
"""

# 標準ライブラリ
from time import sleep

# サードパーティライブラリ
from gpiozero import LED


def main():
    """
    メイン関数：LEDを無限ループで点滅させる
    """
    # GPIO 17のLEDオブジェクトを作成
    led = LED(17)

    try:
        print("LEDの点滅を開始します（Ctrl+Cで終了）")

        # 無限ループで点滅
        while True:
            # LED点灯
            led.on()
            print("LED ON")
            sleep(0.5)  # 0.5秒待機

            # LED消灯
            led.off()
            print("LED OFF")
            sleep(0.5)  # 0.5秒待機

    except KeyboardInterrupt:
        # Ctrl+Cで割り込まれた場合の処理
        print("\n点滅を停止します")

    finally:
        # 終了時にLEDを消灯してGPIOリソースをクリーンアップ
        led.off()
        led.close()


if __name__ == "__main__":
    main()
