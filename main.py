from machine import Pin, SoftI2C
from time import sleep
from esp32_i2c_lcd import I2cLcd


lcdI2C = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(lcdI2C, 39, 2, 16)


button_up = Pin(25, Pin.IN)
button_right = Pin(26, Pin.IN)
button_left = Pin(12, Pin.IN)
button_down = Pin(27, Pin.IN)

led_pin1 = Pin(15, Pin.IN)
led_pin2 = Pin(4, Pin.IN)
led_pin3 = Pin(5, Pin.IN)
led_pin4 = Pin(18, Pin.IN)

button_state = [2, False]  


def read_button() -> list:
    return [button_up.value(), button_down.value(), button_right.value(), button_left.value()]


def handle_button_press(current_state, previous_state) -> None:
    global button_state
    
    if current_state[0] == 1 and previous_state[0] == 0:  # Menu select
        if button_state[0] < 4:
            button_state[0] += 1

        display_menu(button_state[0],button_state[1])

    elif current_state[1] == 1 and previous_state[1] == 0:  # Menu select
        if button_state[0] > 1:
            button_state[0] -= 1

        display_menu(button_state[0],button_state[1])

    elif current_state[2] == 1 and previous_state[2] == 0:  # Toggle On/Off
        button_state[1] = True

        display_menu(button_state[0],button_state[1])

    elif current_state[3] == 1 and previous_state[3] == 0:  # Toggle On/Off
        button_state[1] = False

        display_menu(button_state[0],button_state[1])

    
def display_menu(menu, toggle) -> None:
    lcd.move_to(0,0)
    lcd.putstr(f"Led {menu} Selected")
    lcd.move_to(0,1)
    lcd.putstr(f"Toggle : {toggle}")


def main() -> None:
    previous_state = read_button()
    lcd.clear()
    lcd.move_to(4,0)
    lcd.putstr("Welcome!")
    sleep(2) 

    while True:
        current_state = read_button()
        
        # Handle button press
        if current_state != previous_state:
            handle_button_press(current_state, previous_state)
            previous_state = current_state
        

        sleep(0.2)  # Debounce delay


if __name__ == '__main__':
    main()

