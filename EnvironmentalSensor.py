import time

import board
import busio
import adafruit_bme280

addresses = [0x77, 0x76]

sensors = []

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)

def probeBME280():
    for addr in addresses:
        try:
            bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, addr)
            print ("Sensor found at 0x%x" % addr)
            return bme280
        except ValueError as ve:
            print(ve)
    return None

sensor = probeBME280()


# OR create library object using our Bus SPI port
#spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
#bme_cs = digitalio.DigitalInOut(board.D10)
#bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
sensor.sea_level_pressure = 1013.25

while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.humidity)
    print("Pressure: %0.1f hPa" % sensor.pressure)
    print("Altitude = %0.2f meters" % sensor.altitude)

    try:
        print("Gas = %0.2f" % sensor.gas)
    except AttributeError as ae:
        print (ae)

    time.sleep(2)
