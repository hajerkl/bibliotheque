from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "librarycontainer"

container_client = blob_service_client.get_container_client(container_name)
try:
    container_client.create_container()
except Exception as e:
    print(f"Container {container_name} already exists or could not be created: {e}")

books = []

@app.route('/')
def home():
    return render_template('home.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['file']
        
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file)

        book = {'title': title, 'author': author, 'file_url': blob_client.url}
        books.append(book)
        
        return redirect(url_for('home'))
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
