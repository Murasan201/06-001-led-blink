#!/usr/bin/env python3
"""
LED点滅アプリ
LEDを繰り返し点滅させるプログラム
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
    メイン関数：LEDを無限ループで点滅させる
    Ctrl+Cで安全に終了できる
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
        print("LEDの点滅を開始します（Ctrl+Cで終了）")

        # 無限ループで点滅（0.5秒間隔）
        while True:
            # LED点灯（GPIO17をHIGHに設定）
            led.on()
            print("LED ON")
            sleep(0.5)

            # LED消灯（GPIO17をLOWに設定）
            led.off()
            print("LED OFF")
            sleep(0.5)

    except KeyboardInterrupt:
        # Ctrl+Cで割り込まれた場合（正常な終了方法）
        print("\n点滅を停止します")

    # --- 終了処理 ---
    finally:
        # 終了時にLEDを消灯してGPIOリソースをクリーンアップ
        # gpiozeroではclose()でピンを解放する
        led.off()
        led.close()
        print("GPIOリソースを解放しました")


if __name__ == "__main__":
    main()
