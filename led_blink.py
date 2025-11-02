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
    """LED制御クラス
    GPIO操作とLED点滅制御を一括管理する初心者向けのシンプルな実装
    """
    
    def __init__(self, pin=17, interval=1.0, count=None):
        """LEDBlinkerクラスの初期化
        
        Args:
            pin (int): 使用するGPIOピン番号（デフォルト: 17）
            interval (float): 点滅間隔（秒）（デフォルト: 1.0）
            count (int): 点滅回数（None=無限ループ）
        """
        self.pin = pin              # 使用するGPIOピン番号
        self.interval = interval    # 点滅間隔（秒）
        self.count = count          # 点滅回数（None=無限）
        self.led = None             # LEDオブジェクト
        self.blink_counter = 0      # 点滅回数カウンタ
        self.running = True         # 実行状態フラグ
        
    def setup_gpio(self):
        """GPIO初期化

        指定されたピンをLED制御用に設定し、LEDオブジェクトを作成します。
        エラーが発生した場合はプログラムを終了します。
        """
        try:
            # gpiozeroライブラリを使用してLEDオブジェクトを作成
            self.led = LED(self.pin)
            print(f"GPIO pin {self.pin} initialized for LED control")
        except GPIOPinInUse:
            # 指定したピンが既に使用中の場合のエラー処理
            print(f"Error: GPIO pin {self.pin} is already in use")
            sys.exit(1)
        except Exception as e:
            # その他のGPIO初期化エラーの処理
            print(f"Error initializing GPIO pin {self.pin}: {e}")
            sys.exit(1)
    
    def cleanup(self):
        """GPIO終了処理

        LEDオブジェクトを閉じてGPIOリソースを適切にクリーンアップします。
        """
        if self.led:
            # LEDオブジェクトを閉じてGPIOリソースを解放
            self.led.close()
            print("\nGPIO cleanup completed")
    
    def signal_handler(self, signum, frame):
        """シグナルハンドラ

        Ctrl+C等の割り込み信号を受け取り、実行フラグを False に設定して
        安全にループを終了します。
        """
        print("\nInterrupt received, stopping LED blink...")
        # 実行フラグをFalseにして安全にループを終了
        self.running = False
    
    def log_blink_status(self, status):
        """点滅状況をログ出力

        タイムスタンプ付きで LED の状態（ON/OFF）とカウンタを記録します。

        Args:
            status (str): LED の状態（'ON' または 'OFF'）
        """
        # 現在時刻を取得してフォーマット
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # LED状態とカウンタをログ出力
        print(f"[{timestamp}] Blink #{self.blink_counter}: LED {status}")
    
    def blink_led(self):
        """LED点滅実行

        メインの点滅ロジックを実行します。
        設定された間隔と回数に基づいて LED を点灯・消灯します。
        """
        # 実行設定の表示
        print(f"Starting LED blink on GPIO pin {self.pin}")
        print(f"Interval: {self.interval}s")
        if self.count:
            print(f"Count: {self.count} times")
        else:
            print("Count: Infinite (press Ctrl+C to stop)")
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
            print(f"Error during LED blinking: {e}")
        finally:
            # 必ずGPIOクリーンアップを実行
            self.cleanup()
            print(f"LED blink completed. Total blinks: {self.blink_counter}")

def parse_arguments():
    """コマンドライン引数の解析

    ユーザーが指定した各種パラメータ（ピン番号、間隔、回数）を解析して返します。

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
    """引数の妥当性検証

    コマンドライン引数の入力値の範囲と形式をチェックします。
    不正な値の場合はエラーメッセージを表示してプログラムを終了します。

    Args:
        args (argparse.Namespace): 検証するコマンドライン引数
    """
    # GPIOピン番号の範囲チェック（Raspberry Pi の有効範囲）
    if args.pin < 1 or args.pin > 40:
        print("Error: GPIO pin number must be between 1 and 40")
        sys.exit(1)
    
    # 点滅間隔の正数チェック
    if args.interval <= 0:
        print("Error: Interval must be greater than 0")
        sys.exit(1)
    
    # 点滅回数の正数チェック（指定時のみ）
    if args.count is not None and args.count <= 0:
        print("Error: Count must be greater than 0")
        sys.exit(1)

def main():
    """メイン関数

    コマンドライン引数を処理してアプリケーションを実行します。
    LED点滅のセットアップと実行を統括します。
    """
    # コマンドライン引数の解析と検証
    args = parse_arguments()
    validate_arguments(args)
    
    # アプリケーション開始メッセージ
    print("=" * 50)
    print("LED点灯アプリ - LED Blink Application")
    print("=" * 50)
    
    # LEDBlinkerインスタンスを作成して実行
    blinker = LEDBlinker(args.pin, args.interval, args.count)
    blinker.setup_gpio()  # GPIO初期化
    blinker.blink_led()   # LED点滅実行

if __name__ == "__main__":
    main()