# Memory LED Matrix Game - Interactive Pattern Matching Game with LED Matrix Display

The Memory LED Matrix Game is an engaging electronic memory game that challenges players to recreate patterns displayed on a 5x5 LED matrix. Built using MicroPython on embedded hardware, it combines visual memory skills with hand-eye coordination through an intuitive joystick-based interface.

The game features dynamic pattern display, interactive LED control, and real-time scoring. Players must observe a randomly selected pattern, memorize it during a countdown period, and then recreate it using a joystick and color selection system. The game provides immediate feedback through an OLED display showing the player's score and elapsed time, along with audio feedback through a buzzer for successful pattern completion.

## Repository Structure
```
ea801/
└── Memory LED Matrix Game/
    └── main.py           # Main game logic including LED matrix control, input handling, and game flow
```

## Usage Instructions
### Prerequisites
- MicroPython-compatible microcontroller board
- Hardware components:
  * 5x5 WS2812B LED Matrix
  * SSD1306 OLED Display (128x64)
  * Analog joystick
  * 2 push buttons
  * Buzzer
  * Required connections:
    - LED Matrix: Pin 7
    - OLED Display: SCL Pin 15, SDA Pin 14
    - Joystick: VRX Pin 27, VRY Pin 26
    - Button A: Pin 5
    - Button B: Pin 6
    - Buzzer: Pin 21

### Installation
1. Flash MicroPython to your microcontroller
2. Copy `main.py` to the root directory of your microcontroller
3. Install required libraries:
```python
import machine
import ssd1306
import neopixel
```

### Quick Start
1. Power on the device
2. Press Button A to start the game
3. Observe the pattern displayed on the LED matrix during the 5-second countdown
4. Use the joystick to move the cursor around the matrix
5. Press Button B to cycle through available colors
6. Recreate the pattern you memorized
7. The game will show your score and time on the OLED display

### More Detailed Examples
Pattern Creation Example:
```python
# Move cursor with joystick
# Press Button B to cycle through colors:
# - White (255, 255, 255)
# - Red (255, 0, 0)
# - Green (0, 255, 0)
# - Blue (0, 0, 255)
# - Yellow (255, 255, 0)
# - Off (0, 0, 0)
```

### Troubleshooting
Common Issues:
1. LED Matrix not responding
   - Check Pin 7 connection
   - Verify power supply capacity (WS2812B requires 5V)
   - Reset the device

2. Joystick not working
   - Verify ADC connections on pins 26 and 27
   - Check joystick calibration values in code
   - Default thresholds: < 20000 and > 45000

3. OLED Display issues
   - Verify I2C connections (SCL: Pin 15, SDA: Pin 14)
   - Check I2C address configuration
   - Ensure proper power supply

## Data Flow
The game processes user input through the joystick and buttons, updates the LED matrix display, and provides feedback through the OLED display and buzzer.

```ascii
[Joystick/Buttons] -> [Input Processing] -> [Game Logic] -> [LED Matrix/OLED/Buzzer]
     ^                                                             |
     |                                                             |
     +-------------------------------------------------------------
```

Component Interactions:
1. Input Layer: Joystick provides X/Y movement, buttons trigger actions
2. Game Logic: Processes inputs, manages game state, calculates score
3. Display Layer: Updates LED matrix and OLED display
4. Feedback System: Shows score, time, and plays victory melody
5. Memory Management: Stores current pattern and player's recreation
6. Timing System: Manages countdown and gameplay duration
7. State Machine: Controls game flow between display, memorization, and recreation phases
