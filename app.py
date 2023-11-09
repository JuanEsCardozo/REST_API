from google.cloud import storage, secretmanager
from flask import Flask

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

if __name__ == '__main__':
    app.run(debug=True)