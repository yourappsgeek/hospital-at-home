from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud import bigquery_storage_v1beta1


credentials = service_account.Credentials.from_service_account_file(
    'hospital-at-home-test-e03adb4c441e.json')
project_id = 'hospital-at-home-test'
client = bigquery.Client(credentials= credentials,project=project_id)
bqstorageclient = bigquery_storage_v1beta1.BigQueryStorageClient(credentials=credentials)


query_job = client.query("""
  SELECT *
  FROM 
  `hospital-at-home-test.Recordings.VitalSigns`
  LIMIT 1000""")
patient_info_df = query_job.result().to_dataframe(bqstorage_client=bqstorageclient)

 

print(patient_info_df.head())
