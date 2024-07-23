import dht
import network
from machine import Pin, SoftI2C
from time import sleep as delay
from esp32_i2c_lcd import I2cLcd
from hcsr04 import HCSR04

lcdI2C = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(lcdI2C, 39, 2, 16)
dht_sensor = dht.DHT22(Pin(33))
hcsr04_sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)
    

class Button:
    def __init__(self, button_pin1, button_pin2):
        self.button_pins = [Pin(button_pin1, Pin.IN), Pin(button_pin2, Pin.IN)]
        self.state = 0
        self.previous_val = [0, 0]

    def val(self):
        return [pin.value() for pin in self.button_pins]

    def debounce(self):
        current_val = self.val()
        delay(0.01)  # Debounce delay
        delayed_val = self.val()
        if current_val == delayed_val:
            return current_val
        
        return self.previous_val

    def handle(self):
        current_val = self.debounce()
        if current_val[0] == 1 and self.previous_val[0] == 0: 
            if self.state < 2:
                self.state += 1

        if current_val[1] == 1 and self.previous_val[1] == 0: 
            if self.state > 0: 
                self.state -= 1

        self.previous_val = current_val


class Interaction:
    def __init__(self, select):
        self.select = select
        self.previous_temp = None
        self.previous_distance = None

    @staticmethod
    def initWifi(ssid="Wokwi-GUEST",password=""):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        
        return ssid

        while not wlan.isconnected():
            pass
    
    @staticmethod
    def read_temp():
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        return temp

    @staticmethod
    def read_distance():
        distance = hcsr04_sensor.distance_cm()
        return distance

    def display_temp(self):
        temp = self.read_temp()
        lcd.clear()
        lcd.putstr("Temp : {:.1f} C".format(temp))
        lcd.move_to(0, 1)
        lcd.putstr("     Distance v")
        self.previous_temp = temp

    def display_distance(self):
        distance = self.read_distance()
        lcd.clear()
        lcd.putstr("Distance : {:.1f} Cm".format(distance))
        lcd.move_to(0, 1)
        lcd.putstr("^ Temp    LED v")
        self.previous_distance = distance

    def display_connection(self):
        ssid = self.initWifi()
        lcd.clear()
        lcd.putstr("Connected to: ")
        lcd.move_to(0, 1)
        lcd.putstr(ssid)

    def decide(self):
        if self.select == 2:
            self.display_temp()
        
        elif self.select == 1:
            self.display_distance()

        else:
            self.display_connection()

    def refresh(self):
        if self.select == 2:
            current_temp = self.read_temp()
            if current_temp != self.previous_temp:
                self.display_temp()
                
        elif self.select == 1:
            current_distance = self.read_distance()
            if current_distance != self.previous_distance:
                self.display_distance()


def main():
    buttons = Button(12, 27)
    display = Interaction(0)  
    last_state = -1 

    while True:
        buttons.handle()

        if buttons.state != last_state:
            display.select = buttons.state  
            display.decide()  
            last_state = buttons.state

        display.refresh()
        delay(0.01)  # Main loop delay


if __name__ == '__main__':
    main()
