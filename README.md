# LED Blink Application

## Overview
A simple Python application for controlling LED using Raspberry Pi 5 GPIO pins. This project serves as hands-on educational material for programming beginners to learn the basics of GPIO control and electronics.

This project includes two simple programs:
- `led_simple.py`: Turns LED on for 3 seconds, then off for 1 second
- `led_blink.py`: Blinks LED continuously at 0.5-second intervals

## Required Hardware
- Raspberry Pi 5
- MicroSD card (with Raspberry Pi OS installed)
- Breadboard
- Jumper wires (male-to-male)
- LED (any color)
- Resistor (approximately 330Ω)
- Power supply (official 5V power adapter)

## Software Requirements
- OS: Raspberry Pi OS (latest version recommended)
- Python 3.9 or higher
- gpiozero library

## Installation
1. Install required libraries:
```bash
pip3 install gpiozero
```

2. Make the scripts executable:
```bash
chmod +x led_simple.py
chmod +x led_blink.py
```

## Circuit Assembly

⚠️ **Important Safety Notes** ⚠️
- Always connect a resistor (approximately 330Ω) in series with the LED
- Connecting an LED without a resistor may damage the LED or Raspberry Pi
- Always perform wiring work with the power off

### Wiring Instructions
1. Turn off the Raspberry Pi power
2. Insert the LED into the breadboard (long leg = anode, short leg = cathode)
3. Connect the LED anode (long leg) to one end of the resistor
4. Connect the other end of the resistor to Raspberry Pi GPIO17 pin using a jumper wire
5. Connect the LED cathode (short leg) to Raspberry Pi GND pin using a jumper wire

### Pin Layout (Raspberry Pi 5)
```
GPIO17 (Pin 11) ----[330Ω Resistor]---- LED(Anode)
                                           |
                                           |
                                       LED(Cathode)
                                           |
GND (Pin 6)    ----------------------------
```

## Usage

### Simple LED Control (led_simple.py)
Turn on LED for 3 seconds, then turn off for 1 second:
```bash
python3 led_simple.py
```

### Continuous LED Blinking (led_blink.py)
Blink LED continuously at 0.5-second intervals:
```bash
python3 led_blink.py
```

### Stopping Execution
- For `led_simple.py`: Runs automatically and exits after completion
- For `led_blink.py`: Press Ctrl+C to safely stop execution
- Both programs automatically clean up GPIO resources

## Troubleshooting

### Common Issues and Solutions

1. **"Permission denied" error**
   ```bash
   sudo python3 led_simple.py
   # or
   sudo python3 led_blink.py
   ```

2. **"GPIO pin is already in use" error**
   - Another process may be using the same GPIO pin
   - Reboot Raspberry Pi to release GPIO resources

3. **LED doesn't light up**
   - Check wiring (especially GND connection)
   - Verify LED polarity (anode/cathode)
   - Ensure resistor is properly connected

4. **"ModuleNotFoundError: No module named 'gpiozero'" error**
   ```bash
   pip3 install gpiozero
   ```

## Learning Points
1. **Basic GPIO Control**: Digital output for LED control
2. **Python Programming**: Function design, exception handling, try-finally structure
3. **Electronic Circuits**: LED circuit basics, resistor functionality
4. **Resource Management**: Proper GPIO cleanup

## Extension Ideas
- Add command-line arguments to control blink interval
- Control multiple LEDs
- Brightness adjustment using PWM
- Add different blink patterns

## License
This project is released under the MIT License. See the LICENSE file for details.

---
Document Number: 06-001
Created: 2025-07-17