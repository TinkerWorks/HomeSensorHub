from communication.sensor_hub import SensorHub

if __name__ == "__main__":
    sensor_hub = SensorHub()
    sensor_hub.start_sniffin(3)
