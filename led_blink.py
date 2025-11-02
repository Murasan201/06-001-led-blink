#!/usr/bin/env python3
"""
LED点灯アプリ
Raspberry Pi GPIOを使用してLEDを点滅させるPythonアプリケーション
要件定義書: 06-001_LED点灯アプリ_要件定義書.md
"""

import argparse
import time
import signal
import sys
from datetime import datetime
from gpiozero import LED, GPIOPinInUse

class LEDBlinker:
    """
    GPIO を操作して LED を点滅させるクラス

    初心者向けに機能を整理し、シンプルな実装にしています。
    """
    
    def __init__(self, pin=17, interval=1.0, count=None):
        """
        LEDを制御するためのクラスを初期化する

        Args:
            pin (int): 使用するGPIOピン番号（デフォルト: 17）
            interval (float): 点滅間隔（秒、デフォルト: 1.0秒）
            count (int): 点滅回数（None で無限ループ）
        """
        self.pin = pin              # 使用するGPIOピン番号
        self.interval = interval    # 点滅間隔（秒）
        self.count = count          # 点滅回数（None=無限）
        self.led = None             # LEDオブジェクト
        self.blink_counter = 0      # 点滅回数カウンタ
        self.running = True         # 実行状態フラグ
        
    def setup_gpio(self):
        """
        GPIOピンをLED制御用に初期化する

        gpiozero ライブラリを使用して LED オブジェクトを作成し、
        エラーが発生した場合はプログラムを終了します。
        """
        try:
            # gpiozeroライブラリを使用してLEDオブジェクトを作成
            self.led = LED(self.pin)
            print(f"GPIO ピン {self.pin} が LED 制御用に初期化されました")
        except GPIOPinInUse:
            # 指定したピンが既に使用中の場合のエラー処理
            print(f"エラー: GPIO ピン {self.pin} は既に使用中です")
            sys.exit(1)
        except Exception as e:
            # その他のGPIO初期化エラーの処理
            print(f"エラー: GPIO ピン {self.pin} の初期化に失敗しました: {e}")
            sys.exit(1)
    
    def cleanup(self):
        """
        GPIO リソースをクリーンアップして終了する

        LED オブジェクトを閉じて GPIO リソースを適切に解放します。
        """
        if self.led:
            # LEDオブジェクトを閉じてGPIOリソースを解放
            self.led.close()
            print("\nGPIO クリーンアップが完了しました")
    
    def signal_handler(self, signum, frame):
        """
        割り込み信号（Ctrl+C）を処理する

        実行フラグを False に設定して安全にループを終了します。
        """
        print("\n割り込み信号を受け取りました。LED 点滅を停止しています...")
        # 実行フラグをFalseにして安全にループを終了
        self.running = False
    
    def log_blink_status(self, status):
        """
        LED の状態をタイムスタンプ付きでログ出力する

        Args:
            status (str): LED の状態（'ON' または 'OFF'）
        """
        # 現在時刻を取得してフォーマット
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # LED状態とカウンタをログ出力
        print(f"[{timestamp}] 点滅 #{self.blink_counter}: LED {status}")
    
    def blink_led(self):
        """
        LED を点滅させるメイン処理を実行する

        設定された間隔と回数に基づいて LED を点灯・消灯します。
        """
        # 実行設定の表示
        print(f"GPIO ピン {self.pin} の LED 点滅を開始します")
        print(f"点滅間隔: {self.interval} 秒")
        if self.count:
            print(f"点滅回数: {self.count} 回")
        else:
            print("点滅回数: 無限ループ（Ctrl+C で停止）")
        print("-" * 50)
        
        # Ctrl+C割り込み処理の設定
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            # メインの点滅ループ
            while self.running:
                # 指定回数に達した場合は終了
                if self.count and self.blink_counter >= self.count:
                    break
                
                # 点滅回数をカウントアップ
                self.blink_counter += 1
                
                # LED点灯フェーズ
                self.led.on()
                self.log_blink_status("ON")
                time.sleep(self.interval)
                
                # 割り込みチェック
                if not self.running:
                    break
                
                # LED消灯フェーズ
                self.led.off()
                self.log_blink_status("OFF")
                time.sleep(self.interval)
                
        except Exception as e:
            # 予期しないエラーの処理
            print(f"エラー: LED 点滅中にエラーが発生しました: {e}")
        finally:
            # 必ずGPIOクリーンアップを実行
            self.cleanup()
            print(f"LED 点滅が完了しました。合計点滅数: {self.blink_counter} 回")

def parse_arguments():
    """
    コマンドライン引数を解析して返す

    Returns:
        argparse.Namespace: 解析されたコマンドライン引数
    """
    parser = argparse.ArgumentParser(
        description="LED点灯アプリ - Raspberry Pi GPIO LED Blink Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python3 led_blink.py                    # デフォルト設定（GPIO17, 1秒間隔, 無限ループ）
  python3 led_blink.py --pin 18           # GPIO18を使用
  python3 led_blink.py --interval 0.5     # 0.5秒間隔で点滅
  python3 led_blink.py --count 10         # 10回点滅後に終了
  python3 led_blink.py --pin 18 --interval 0.5 --count 20
        """
    )
    
    parser.add_argument(
        "--pin",
        type=int,
        default=17,
        help="使用するGPIOピン番号 (デフォルト: 17)"
    )
    
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="点滅間隔（秒） (デフォルト: 1.0)"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="点滅回数（省略時は無限ループ）"
    )
    
    return parser.parse_args()

def validate_arguments(args):
    """
    コマンドライン引数の値をチェックする

    Args:
        args (argparse.Namespace): 検証するコマンドライン引数
    """
    # GPIOピン番号の範囲チェック（Raspberry Pi の有効範囲）
    if args.pin < 1 or args.pin > 40:
        print("エラー: GPIO ピン番号は 1 から 40 の間である必要があります")
        sys.exit(1)

    # 点滅間隔の正数チェック
    if args.interval <= 0:
        print("エラー: 点滅間隔は 0 より大きい値である必要があります")
        sys.exit(1)

    # 点滅回数の正数チェック（指定時のみ）
    if args.count is not None and args.count <= 0:
        print("エラー: 点滅回数は 0 より大きい値である必要があります")
        sys.exit(1)

def main():
    """
    アプリケーションのメイン処理を実行する

    コマンドライン引数を処理して LED 点滅を実行します。
    """
    # コマンドライン引数の解析と検証
    args = parse_arguments()
    validate_arguments(args)
    
    # アプリケーション開始メッセージ
    print("=" * 50)
    print("LED 点灯アプリ - Raspberry Pi LED Blink Application")
    print("=" * 50)
    
    # LEDBlinkerインスタンスを作成して実行
    blinker = LEDBlinker(args.pin, args.interval, args.count)
    blinker.setup_gpio()  # GPIO初期化
    blinker.blink_led()   # LED点滅実行

if __name__ == "__main__":
    main()