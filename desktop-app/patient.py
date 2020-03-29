from datetime import datetime
import numpy as np
from explorepy.tools import HeartRateEstimator


class Patient:
    def __init__(self, patient_id, age=None, location=None, diagnose_date=None, symptoms_onset_date=None):
        """

        Args:
            patient_id:
            age:
            location:
            diagnose_date:
            symptoms_onset_date:
        """
        self.id = patient_id
        self.age = age
        self.location = location
        self.symptoms_onset = symptoms_onset_date
        self.diagnosis_date = diagnose_date
        self.ecg = np.zeros((0,))
        self.resp = np.zeros((0,))
        self.time_vector = np.zeros((0,))
        self.hr_estimator = HeartRateEstimator()

    def update_ecg(self, packet):
        time_vector, signal = packet.get_data(250)
        self.ecg = np.concatenate((self.ecg, signal[1, :]), axis=0)
        self.resp = np.concatenate((self.resp, signal[0, :]), axis=0)
        self.time_vector = np.concatenate((self.time_vector, time_vector), axis=0)

    def get_spo2(self):
        dummy_data = np.random.randint(70, 100, size=30)
        return int(dummy_data.mean())

    def get_hr(self):
        # r_times, _ = self.hr_estimator.estimate(ecg_sig=self.ecg, time_vector=self.time_vector)
        # return (r_times[-1], r_times[0])/len(r_times)
        return np.random.randint(40, 100, size=1)

    def get_resp(self):
        return np.random.randint(7, 30, size=1)

    def generate_report(self):
        report = {
            'data': self.ecg[::2].tobytes(),
            'patient_id': self.id,
            'timestamp': datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            'hr': str(self.get_hr()[0]),
            'spo2': str(self.get_spo2()),
            'resp': str(self.get_resp()[0])
        }
        self.reset_data()
        return report

    def reset_data(self):
        self.ecg = np.zeros((0,))
        self.resp = np.zeros((0,))
        self.time_vector = np.zeros((0,))


