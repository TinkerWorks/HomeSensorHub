class Adafruit_BME680_I2C:

    def __init__(self, i2c, address):
        self.address = address

    @property
    def temperature(self):
        return self.address

    @property
    def humidity(self):
        return 30

    @property
    def pressure(self):
        return 30

    @property
    def altitude(self):
        return 30
