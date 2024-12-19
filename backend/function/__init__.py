import logging
import os
import json
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import openai
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Obtener configuración desde variables de entorno
    storage_connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    search_service_endpoint = os.getenv("SEARCH_ENDPOINT")
    search_api_key = os.getenv("SEARCH_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Conectar a Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_name = "data"
    container_client = blob_service_client.get_container_client(container_name)

    # Obtener lista de blobs
    blobs = [blob.name for blob in container_client.list_blobs()]
    
    # Conectar a Azure Cognitive Search
    search_client = SearchClient(
        endpoint=search_service_endpoint,
        index_name="documents",
        credential=AzureKeyCredential(search_api_key)
    )
    
    # Recuperar los documentos relevantes
    query = req.params.get('query', 'example query')
    results = search_client.search(search_text=query, top=5)
    page_chunks = [result['page_text'] for result in results]
    
    # Generar respuesta con OpenAI
    openai.api_key = openai_api_key
    prompt = f"Given the documents: {page_chunks}, answer the query: {query}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    # Devolver respuesta
    return func.HttpResponse(
        json.dumps({"answer": response.choices[0].text.strip(), "blobs": blobs}),
        mimetype="application/json"
    )
