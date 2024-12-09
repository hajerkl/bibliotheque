from flask import Flask, render_template, request, redirect, url_for
from azure.storage.blob import BlobServiceClient
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://books:Jesaispas0@books.database.windows.net/books?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    file_url = db.Column(db.String(120), nullable=False)

# Connexion au stockage Azure Blob
connect_str = "DefaultEndpointsProtocol=https;AccountName=stockage109;AccountKey=MGloPgqLLRNfUb4Yr/L8a83dhpnqdatUrbkk9xMzu0Sk6YzG317xYEkmYF629tgn7ByyhGCm0l/N+AStuKgl1w==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "librarycontainer"

container_client = blob_service_client.get_container_client(container_name)
try:
    if not container_client.exists():
        container_client.create_container()
        print(f"Container {container_name} created.")
    else:
        print(f"Container {container_name} already exists.")
except Exception as e:
    print(f"Error creating or accessing the container: {e}")

@app.route('/')
def home():
    books = Book.query.all()  # Récupère les livres de la base de données
    return render_template('home.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['file']

        # Upload du fichier vers Azure Blob Storage
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file)

        # Créer un nouvel enregistrement de livre et l'ajouter à la base de données
        new_book = Book(title=title, author=author, file_url=blob_client.url)
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('add_book.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Créer toutes les tables
    app.run(host='0.0.0.0', port=8000, debug=True)
