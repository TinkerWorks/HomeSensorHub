import time

from communication.data_sender import DataSender
from communication.sensor_hub import SensorHub

if __name__ == "__main__":
    sh = SensorHub()
    ds = DataSender()

    while True:
        sh.collect_all_data()
        data = sh.get_data()

        for topic, value in data.items():
            ds.send_current(value, topic)
        time.sleep(2)
