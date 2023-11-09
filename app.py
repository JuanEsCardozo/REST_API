from google.cloud import storage, secretmanager
from flask import Flask
from io import BytesIO
from config import *
import pandas as pd
import io
import json

app = Flask(__name__)

def access_secret_key(project_id, secret_id, version_id):

    try:
        client = secretmanager.SecretManagerServiceClient.from_service_account_file("single-odyssey-404518-d3e05ea7c215.json")

        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("utf-8")
        
        return payload
    
    except Exception as e:
        print("An error occurred:", str(e))

def get_csv_file(blob_name, bucket_name):

    try:
        json_key = json.loads(access_secret_key(PROJECT_ID, SECRET_ID, VERSION))

        storage_client = storage.Client.from_service_account_info(json_key)

        bucket = storage_client.get_bucket(bucket_name)
        csv_data = pd.read_csv(io.BytesIO(bucket.blob(blob_name).download_as_string()), encoding='UTF-8', sep=',', index_col=None)
        df = pd.DataFrame(csv_data)
        print(csv_data)
        return df

    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    app.run(debug=True)