import time
import urequests
from machine import Pin, I2C, ADC, WDT
from env import WIFI_SSID, WIFI_PASS, API_HOST, BLYNK_AUTH
from i2c_lcd import I2cLcd


PUMP_PIN = 4
VREF = 3.3
THRESHOLD = 2000
I2C_ADDR = 0x27


wdt = WDT(timeout=60000)  # Enable the Watchdog timer with a timeout of 60 seconds


# Define the GPIO pin where the sensor's AOUT pin is connected
sensor_pin = ADC(Pin(34))  # GPIO34 for analog input
sensor_pin.atten(ADC.ATTN_11DB)  # Set attenuation to measure a wider range of voltages


def read_moisture():
    # Read the analog value (0-4095)
    moisture_value = sensor_pin.read()
    return moisture_value
    
    
# Setup Pump
pump = Pin(PUMP_PIN, Pin.OUT)


# Function to turn on the pump
def pump_on():
    pump.value(1)  # Set GPIO 5 to high to turn on the pump
    print("Pump is ON")


# Function to turn off the pump
def pump_off():
    pump.value(0)  # Set GPIO 5 to low to turn off the pump
    print("Pump is OFF")
    
    
# Setup the LCD
i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)


def log_to_api(val):
    url = f'{API_HOST}/api/sensor'
    data = {'reading': val}
    headers = {'Content-Type': 'application/json'}
    try:
        response = urequests.post(url, json=data, headers=headers)
        print(f'API response: {response.text}')
    except Exception as e:
        print(e)
    finally:
        response.close()


def connect_wifi():
    import network
    import time

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(WIFI_SSID, WIFI_PASS)

    while not station.isconnected():
        print('Connecting to WiFi...')
        time.sleep(1)

    print('Connection successful')
    print(station.ifconfig())
    return station



def main():
    # Connect to WiFi
    wlan = connect_wifi()

    # Infinite loop to keep checking moisture
    while True:
        # Ensure hardware watchdog is fed
        wdt.feed()
        if not wlan.isconnected():
            wlan.connect()
            print('Reconnecting to WiFi...')
            time.sleep(5)
        
        val = read_moisture()

        lcd.clear()
        lcd.putstr(f"moisture: {val:.2f}")

        log_to_api(val)

        # if val > THRESHOLD:
        #     pump_on()
        #     time.sleep(5)
        #     pump_off()
        time.sleep(5)

main()