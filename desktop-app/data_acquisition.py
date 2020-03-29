
from datetime import datetime
import argparse
import time

from explorepy import Explore
from explorepy.stream_processor import TOPICS

from patient import Patient
from streaming import publish

PROJECT_ID = 'hospital-at-home-test'
TOPIC_NAME = 'data_stream'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--device_id', help='Device ID (e.g. Explore_1433')
    parser.add_argument('--patient_id', help='User name')
    args = parser.parse_args()

    message_id = 0
    patient_id = args.patient_id
    device_name = args.device_id

    message = {'data': b' ',
               'patient_id': patient_id,
               'timestamp': datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
               'message_id': str(message_id),
               'device_id': device_name,
               'hr': str(70),
               'spo2': str(98),
               'resp': str(10)
               }

    patient = Patient(patient_id=patient_id)
    explore = Explore()
    explore.connect(device_name=device_name)
    explore.stream_processor.subscribe(callback=patient.update_ecg, topic=TOPICS.raw_ExG)
    time.sleep(30)

    while True:
        message = patient.generate_report()
        message['message_id'] = str(message_id)
        message['timestamp'] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        publish(PROJECT_ID, TOPIC_NAME, message)
        message_id += 1
        time.sleep(30)
