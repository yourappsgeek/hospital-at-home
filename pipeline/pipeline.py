import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


SUBSCRIPTION = 'projects/hospital-at-home-test/subscriptions/data-sub'
TOPIC = 'projects/hospital-at-home-test/topics/data_stream'
DATA_TABLE_SPEC = 'hospital-at-home-test:Recordings.VitalSigns'
INFO_TABLE_SPEC = 'hospital-at-home-test:Recordings.PatientInfo'


class PrintElement(beam.DoFn):
    def __init__(self):
        pass

    def process(self, element):
        logging.info('Message: {}'.format(element))
        return [element]


class BigqueryTransform(beam.DoFn):
    def process(self, element, *args, **kwargs):
        import numpy as np
        out = {'PatientID': element.attributes['patient_id'],
               'Timestamp': element.attributes['timestamp'],
               'SpO2': int(element.attributes['spo2']),
               'HeartRate': int(element.attributes['hr']),
               'RespRate': float(element.attributes['resp']),
               'ECG': np.frombuffer(element.data).tolist()
               }
        return [out]


root = logging.getLogger()
root.setLevel(logging.INFO)

signal_pl = beam.Pipeline(options=PipelineOptions())

message = (signal_pl | 'Read from Pub/Sub topic'
                >> beam.io.ReadFromPubSub(topic=TOPIC, with_attributes=True)
                )


bq_data = (message | 'Transform to BigQuery'
           >> beam.ParDo(BigqueryTransform())
           )


bq_save = (bq_data | beam.io.WriteToBigQuery(
    DATA_TABLE_SPEC,
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
    create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER)
           )

result = signal_pl.run()
result.wait_until_finish()