from machine import Pin, SoftI2C
from time import sleep
from esp32_i2c_lcd import I2cLcd

# Initialize I2C and LCD
lcdI2C = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(lcdI2C, 39, 2, 16)

# Initialize buttons
button_up = Pin(25, Pin.IN)
button_right = Pin(26, Pin.IN)
button_left = Pin(12, Pin.IN)
button_down = Pin(27, Pin.IN)

# Initialize button state values
button_state = [2, False]  # [vertical_value, horizontal_value]

def read_button():
    return [button_up.value(), button_down.value(), button_right.value(), button_left.value()]

def handle_button_press(current_state, previous_state):
    global button_state
    if current_state[0] == 1 and previous_state[0] == 0:  # Up button pressed
        if button_state[0] < 4:
            button_state[0] += 1
        lcd.clear()
        lcd.putstr(f"Vert: {button_state[0]}")
    elif current_state[1] == 1 and previous_state[1] == 0:  # Down button pressed
        if button_state[0] > 1:
            button_state[0] -= 1
        lcd.clear()
        lcd.putstr(f"Vert: {button_state[0]}")
    elif current_state[2] == 1 and previous_state[2] == 0:  # Right button pressed
        button_state[1] = True
        lcd.clear()
        lcd.putstr(f"Horiz: {button_state[1]}")
    elif current_state[3] == 1 and previous_state[3] == 0:  # Left button pressed
        button_state[1] = False
        lcd.clear()
        lcd.putstr(f"Horiz: {button_state[1]}")

def main():
    previous_state = read_button()
    lcd.clear()
    lcd.putstr("Ready")

    while True:
        current_state = read_button()
        
        # Handle button press
        if current_state != previous_state:
            handle_button_press(current_state, previous_state)
            previous_state = current_state
        
        print(f"Vertical: {button_state[0]}, Horizontal: {button_state[1]}")
        sleep(0.1)  # Debounce delay

if __name__ == '__main__':
    main()
