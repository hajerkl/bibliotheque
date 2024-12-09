import os
from azure.storage.blob import BlobServiceClient

# Récupérer la chaîne de connexion depuis les variables d'environnement
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
if not connect_str:
    raise ValueError("AZURE_STORAGE_CONNECTION_STRING n'est pas définie")

# Créer le BlobServiceClient
try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    print("Connexion réussie à Azure Blob Storage")
except Exception as e:
    print(f"Erreur lors de la connexion : {e}")
