from machine import Pin, SoftI2C
from time import sleep as delay
from esp32_i2c_lcd import I2cLcd

# Setup LCD
lcdI2C = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(lcdI2C, 39, 2, 16)

class Button:
    def __init__(self, button_pin1, button_pin2):
        self.button_pins = [Pin(button_pin1, Pin.IN), Pin(button_pin2, Pin.IN)]
        self.state = 0
        self.previous_val = [0, 0]
    
    def val(self):
        return [pin.value() for pin in self.button_pins]

    def debounce(self):
        current_val = self.val()
        delay(0.05)  # Debounce delay
        delayed_val = self.val()

        if current_val == delayed_val:
            return current_val
        
        return self.previous_val

    def handle(self):
        current_val = self.debounce()

        if current_val[0] == 1 and self.previous_val[0] == 0: 
            if self.state < 4:
                self.state += 1

        if current_val[1] == 1 and self.previous_val[1] == 0: 
            if self.state > 0:  
                self.state -= 1

        self.previous_val = current_val

def main():
    buttons = Button(12, 27)
    last_state = -1 

    while True:
        buttons.handle()

        if buttons.state != last_state:
            lcd.clear()
            lcd.putstr(f"State: {buttons.state}")
            last_state = buttons.state

        delay(0.01)  # Main loop delay

if __name__ == '__main__':
    main()
