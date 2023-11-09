from sqlalchemy import create_engine, insert, text
from google.cloud.sql.connector import Connector
from google.cloud import storage, secretmanager
from flask import Flask, request, jsonify
from datetime import datetime
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

def write_to_cloud_sql(df, table):
    try:
        connector = Connector()
        db_passwd = access_secret_key(PROJECT_ID, DB_PASSWORD, VERSION)
        engine = create_engine(
            "mysql+pymysql://",
            creator=lambda: get_db_conn(connector, db_passwd),
        )
        
        with engine.connect() as db_conn:
            data_to_insert = df.to_dict(orient='records')
            print(data_to_insert)
            query = insert(table).values(data_to_insert)
            db_conn.execute(query)
            db_conn.commit()
        
        return "Data Successfully Uploaded"
            
    except Exception as e:
        print("An error occurred:", str(e))

def get_data(query):
    try:
        connector = Connector()
        db_passwd = access_secret_key(PROJECT_ID, DB_PASSWORD, VERSION)
        engine = create_engine(
            "mysql+pymysql://",
            creator=lambda: get_db_conn(connector, db_passwd),
        )
        
        with engine.connect() as db_conn:
            result = db_conn.execute(text(query)).fetchall()
        
        return result
            
    except Exception as e:
        print("An error occurred:", str(e))

def get_db_conn(connector, db_passwd):
    
    try:
        conn = connector.connect(
            "single-odyssey-404518:us-central1:challenge-db",
            "pymysql",
            user = "root",
            password = db_passwd,
            db = "challenge"
        )
        return conn
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