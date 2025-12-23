# LED点灯アプリ セットアップガイド

このドキュメントでは、LED点灯アプリを実行するための環境構築手順を説明します。

## 目次

1. [必要なハードウェア](#1-必要なハードウェア)
2. [回路の組み立て](#2-回路の組み立て)
3. [ソフトウェア環境の確認](#3-ソフトウェア環境の確認)
4. [依存パッケージのインストール](#4-依存パッケージのインストール)
5. [動作確認テスト](#5-動作確認テスト)
6. [プログラムの実行](#6-プログラムの実行)
7. [トラブルシューティング](#7-トラブルシューティング)

---

## 1. 必要なハードウェア

以下のハードウェアを用意してください。

| 部品 | 数量 | 備考 |
|------|------|------|
| Raspberry Pi 5 | 1台 | Raspberry Pi OS インストール済み |
| microSDカード | 1枚 | 32GB以上推奨 |
| ブレッドボード | 1個 | - |
| LED | 1個 | 任意の色（赤、緑、黄など） |
| 抵抗 | 1個 | 330Ω（オレンジ-オレンジ-茶-金） |
| ジャンパーワイヤ（オス-オス） | 2本 | - |
| 電源アダプタ | 1個 | 公式5V/3A以上推奨 |

---

## 2. 回路の組み立て

### 安全上の注意

> **警告**: 以下の注意事項を必ず守ってください。
> - **必ず330Ω抵抗を使用してください**（抵抗なしでLEDを接続すると、LEDやRaspberry Piが破損します）
> - **配線作業は必ず電源OFFの状態で行ってください**
> - LEDの極性（プラス/マイナス）を確認してください

### LEDの極性について

LEDには極性があります：
- **アノード（+側）**: 足が長い方
- **カソード（-側）**: 足が短い方、内部の大きな金属板側

### 配線図

```
Raspberry Pi 5                  ブレッドボード

GPIO17 (ピン11) ────────────── [330Ω抵抗] ──── LED(アノード/長い足)
                                                    │
                                               LED(カソード/短い足)
                                                    │
GND (ピン6)     ────────────────────────────────────┘
```

### ピン配置（Raspberry Pi 5 40ピンヘッダー）

```
                    ┌─────────────────────────────────┐
                    │  Raspberry Pi 5 GPIO Header     │
                    │         (上から見た図)           │
                    ├─────────────────────────────────┤
        3.3V (1)   ●│○ (2)  5V                        │
      GPIO2 (3)   ○│○ (4)  5V                        │
      GPIO3 (5)   ○│○ (6)  GND    ← GND接続         │
      GPIO4 (7)   ○│○ (8)  GPIO14                    │
         GND (9)  ○│○ (10) GPIO15                    │
     GPIO17 (11)  ●│○ (12) GPIO18  ← GPIO17接続     │
     GPIO27 (13)  ○│○ (14) GND                       │
                    └─────────────────────────────────┘
                    ● = 使用するピン
```

### 配線手順

1. **Raspberry Piの電源をOFFにする**
2. **LEDをブレッドボードに挿す**
   - 長い足（アノード）と短い足（カソード）を別の列に挿す
3. **抵抗を接続する**
   - 抵抗の片方をLEDのアノード（長い足）と同じ列に挿す
   - 抵抗のもう片方を別の列に挿す
4. **ジャンパーワイヤを接続する**
   - 抵抗のもう片方の列 → Raspberry Pi GPIO17（ピン11）
   - LEDのカソード（短い足）の列 → Raspberry Pi GND（ピン6）

---

## 3. ソフトウェア環境の確認

### 3.1 Pythonバージョンの確認

```bash
python3 --version
```

**期待される出力**:
```
Python 3.9.x 以上
```

> 本環境での確認結果: `Python 3.13.5`

### 3.2 pipの確認

```bash
pip3 --version
```

**期待される出力**:
```
pip XX.X.X from /usr/lib/python3/dist-packages/pip (python 3.x)
```

> 本環境での確認結果: `pip 25.1.1`

### 3.3 ユーザーグループの確認

GPIOにアクセスするには、ユーザーが`gpio`グループに所属している必要があります。

```bash
groups
```

**期待される出力**（gpioが含まれていること）:
```
pi adm dialout cdrom sudo audio video plugdev games users input render netdev spi i2c gpio lpadmin
```

`gpio`グループに所属していない場合:
```bash
sudo usermod -aG gpio $USER
```
その後、再ログインしてください。

### 3.4 GPIOデバイスの確認

```bash
ls -la /dev/gpiochip*
```

**期待される出力**:
```
crw-rw----+ 1 root gpio 254,  0 ... /dev/gpiochip0
...
```

---

## 4. 依存パッケージのインストール

### 4.1 gpiozeroのインストール確認

```bash
pip3 show gpiozero
```

**インストール済みの場合の出力**:
```
Name: gpiozero
Version: 2.0.1
Summary: A simple interface to GPIO devices with Raspberry Pi
...
```

> 本環境での確認結果: `gpiozero 2.0.1` インストール済み

### 4.2 gpiozeroがインストールされていない場合

#### 方法1: pipでインストール（推奨）

```bash
pip3 install gpiozero
```

#### 方法2: requirements.txtを使用

```bash
cd /home/pi/work/project/06-003-led-blink
pip3 install -r requirements.txt
```

### 4.3 インストールの確認

```bash
python3 -c "from gpiozero import LED; print('gpiozero OK')"
```

**期待される出力**:
```
gpiozero OK
```

---

## 5. 動作確認テスト

### 5.1 GPIOピンの状態確認

```bash
pinctrl get 17
```

**期待される出力**:
```
17: no    pd | -- // GPIO17 = none
```

これはGPIO17が未使用（利用可能）であることを示します。

### 5.2 簡易テスト（ハードウェアなし）

LEDを接続していなくてもプログラムの動作確認ができます。

```bash
cd /home/pi/work/project/06-003-led-blink
python3 -c "
from gpiozero import LED
from time import sleep

print('GPIO17テスト開始')
led = LED(17)
led.on()
print('LED ON 状態')
sleep(1)
led.off()
print('LED OFF 状態')
led.close()
print('テスト完了')
"
```

**期待される出力**:
```
GPIO17テスト開始
LED ON 状態
LED OFF 状態
テスト完了
```

### 5.3 LED点滅テスト

LEDを接続した状態で、以下のコマンドを実行してください。

```bash
python3 -c "
from gpiozero import LED
from time import sleep

led = LED(17)
print('LED点滅テスト開始（3回点滅）')
for i in range(3):
    led.on()
    print(f'LED ON ({i+1})')
    sleep(0.3)
    led.off()
    print(f'LED OFF ({i+1})')
    sleep(0.3)
led.close()
print('テスト完了')
"
```

LEDが3回点滅すれば成功です。

---

## 6. プログラムの実行

### 6.1 led_simple.py（基本プログラム）

LEDを3秒間点灯し、1秒間消灯してから終了します。

```bash
cd /home/pi/work/project/06-003-led-blink
python3 led_simple.py
```

**期待される出力**:
```
LEDを点灯します
LEDを消灯します
プログラム終了
```

### 6.2 led_blink.py（点滅プログラム）

LEDを0.5秒間隔で連続的に点滅させます。`Ctrl+C`で終了します。

```bash
cd /home/pi/work/project/06-003-led-blink
python3 led_blink.py
```

**期待される出力**:
```
LEDの点滅を開始します（Ctrl+Cで終了）
LED ON
LED OFF
LED ON
LED OFF
...
（Ctrl+Cを押す）
点滅を停止します
```

### 6.3 スクリプトを直接実行する方法

```bash
chmod +x led_simple.py led_blink.py
./led_simple.py
./led_blink.py
```

---

## 7. トラブルシューティング

### 問題1: "Permission denied" エラー

**症状**:
```
PermissionError: [Errno 13] Permission denied
```

**原因**: GPIOへのアクセス権限がない

**解決方法**:
```bash
# gpioグループに追加
sudo usermod -aG gpio $USER

# 再ログイン（またはリブート）
logout
# または
sudo reboot
```

### 問題2: "ModuleNotFoundError: No module named 'gpiozero'"

**症状**:
```
ModuleNotFoundError: No module named 'gpiozero'
```

**解決方法**:
```bash
pip3 install gpiozero
```

### 問題3: LEDが点灯しない

**確認事項**:
1. **配線の確認**
   - GPIO17とLEDが正しく接続されているか
   - GNDが接続されているか
   - 抵抗が回路に含まれているか

2. **LEDの極性確認**
   - アノード（長い足）が抵抗側
   - カソード（短い足）がGND側

3. **LEDの故障確認**
   - 別のLEDで試してみる

### 問題4: "GPIO pin is already in use" エラー

**症状**:
```
GPIOPinInUse: GPIO pin 17 is already in use
```

**解決方法**:
```bash
# 他のプロセスがGPIOを使用していないか確認
ps aux | grep python

# 必要に応じてプロセスを終了
kill <プロセスID>

# または、Raspberry Piを再起動
sudo reboot
```

### 問題5: プログラムが応答しない

**解決方法**:
- `Ctrl+C`を押して強制終了
- それでも終了しない場合は`Ctrl+Z`で一時停止後、`kill %1`で終了

---

## 環境情報サマリー

本環境で確認した構成:

| 項目 | バージョン/状態 |
|------|----------------|
| OS | Raspberry Pi OS (Linux 6.12.47+rpt-rpi-2712) |
| Python | 3.13.5 |
| pip | 25.1.1 |
| gpiozero | 2.0.1 |
| GPIOグループ | 所属確認済み |
| GPIO17 | 利用可能 |

---

## 関連ドキュメント

- [README.md](README.md) - プロジェクト概要（英語）
- [06-001_LED点灯アプリ_要件定義書.md](06-001_LED点灯アプリ_要件定義書.md) - 詳細な要件
- [CLAUDE.md](CLAUDE.md) - プロジェクトルール

---

文書番号: 06-001-SETUP
最終更新: 2025-12-23
