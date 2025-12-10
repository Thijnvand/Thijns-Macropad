import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.extensions.RGB import RGB, AnimationModes

# 1. Setup the Keyboard
keyboard = KMKKeyboard()

# 2. Setup the Pins (Based on your Schematic)
# [cite_start]Switches are on A0, A1, A2, A3 [cite: 5]
PINS = [board.A0, board.A1, board.A2, board.A3]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
)

# 3. Setup the LEDs
# [cite_start]LEDs are connected to the TX pin (D0) [cite: 6]
rgb = RGB(
    pixel_pin=board.D0,
    num_pixels=7,
    val_limit=100,       # Brightness (0-255)
    val_default=100,
    hue_default=170,     # 170 is Blue
    sat_default=255,
    animation_mode=AnimationModes.STATIC
)
keyboard.extensions.append(rgb)

# 4. Setup the OLED Screen
# [cite_start]Connected via I2C (SDA/SCL) [cite: 6]
displayio.release_displays()
i2c = busio.I2C(board.SCL, board.SDA)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 32
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Create the text to display
splash = displayio.Group()
display.root_group = splash

text = "MACROPAD\nREADY"
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=8
)
splash.append(text_area)

# 5. Define the Keymap
# Simple Media Keys
keyboard.keymap = [
    [KC.VOLU, KC.VOLD, KC.MUTE, KC.MPLY]
]

if __name__ == '__main__':
    keyboard.go()
