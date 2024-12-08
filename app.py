from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Configuration de la connexion à Azure Blob Storage
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "librarycontainer"

# Vérifie si le conteneur existe, sinon crée-le
container_client = blob_service_client.get_container_client(container_name)
try:
    container_client.create_container()
except Exception as e:
    print(f"Container {container_name} already exists or could not be created.")

# Liste pour stocker les détails des livres (peut être remplacée par une base de données plus tard)
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
        
        # Télécharger le fichier dans Azure Blob Storage
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file)

        # Ajouter les détails du livre à la liste
        book = {'title': title, 'author': author, 'file_url': blob_client.url}
        books.append(book)
        
        return redirect(url_for('home'))
    return render_template('add_book.html')

if __name__ == '__main__':
    app.run(debug=True)
