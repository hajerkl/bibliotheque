from flask import Flask, render_template, request
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Configuration de la connexion à Azure Blob Storage
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "mycontainer"
container_client = blob_service_client.get_container_client(container_name)
try:
    container_client.create_container()
except Exception as e:
    print("Container already exists.")

@app.route('/')
def home():
    return 'Hello, Azure!'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file)
        return 'File uploaded successfully!'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
