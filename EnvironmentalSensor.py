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

sensors.append(probeBME280())


# OR create library object using our Bus SPI port
#spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
#bme_cs = digitalio.DigitalInOut(board.D10)
#bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

while True:
    print("\nTemperature: %0.1f C" % bme280.temperature)
    print("Humidity: %0.1f %%" % bme280.humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)

    try:
        print("Gas = %0.2f" % bme280.gas)
    except AttributeError as ae:
        print (ae)

    time.sleep(2)
