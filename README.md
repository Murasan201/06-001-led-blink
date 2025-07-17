# LED Blink Application

## Overview
A Python application for controlling LED blinking using Raspberry Pi 5 GPIO pins. This project serves as hands-on educational material for programming beginners to learn the basics of GPIO control and electronics.

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

2. Make the script executable:
```bash
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

### Basic Usage Examples
```bash
# Run with default settings (GPIO17, 1-second interval, infinite loop)
python3 led_blink.py

# Use GPIO18
python3 led_blink.py --pin 18

# 0.5-second interval blinking
python3 led_blink.py --interval 0.5

# Blink 10 times then exit
python3 led_blink.py --count 10

# Combine multiple options
python3 led_blink.py --pin 18 --interval 0.5 --count 20
```

### Command Line Arguments
- `--pin`: GPIO pin number to use (default: 17)
- `--interval`: Blink interval in seconds (default: 1.0)
- `--count`: Number of blinks (omit for infinite loop)

### Stopping Execution
- Press Ctrl+C to safely stop execution
- The program automatically cleans up GPIO resources

## Troubleshooting

### Common Issues and Solutions

1. **"Permission denied" error**
   ```bash
   sudo python3 led_blink.py
   ```

2. **"GPIO pin is already in use" error**
   - Another process may be using the same GPIO pin
   - Try specifying a different pin number

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
2. **Python Programming**: Class design, exception handling, signal processing
3. **Electronic Circuits**: LED circuit basics, resistor functionality
4. **Command Line**: Argument processing with argparse

## Extension Ideas
- Control multiple LEDs
- Brightness adjustment using PWM
- Temperature sensor integration
- Web interface addition

## License
This project is released under the MIT License. See the LICENSE file for details.

---
Document Number: 06-001
Created: 2025-07-17