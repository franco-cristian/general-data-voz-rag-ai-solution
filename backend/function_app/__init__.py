import logging
import os
import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import openai
import azure.functions as func

# Generar embeddings usando text-embedding-ada-002
def generate_embedding(text, api_key):
    openai.api_key = api_key
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']

# Azure Function principal
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Configuración
        search_endpoint = os.getenv("AZURE_COGNITIVE_SEARCH_ENDPOINT")
        search_api_key = os.getenv("AZURE_COGNITIVE_SEARCH_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")

        # Inicializar cliente de Azure Cognitive Search
        search_client = SearchClient(
            endpoint=search_endpoint,
            index_name="documents",  # Cambia al nombre de tu índice
            credential=AzureKeyCredential(search_api_key)
        )

        # Obtener la consulta del usuario
        query = req.params.get('query')
        if not query:
            return func.HttpResponse("Por favor, proporciona una consulta.", status_code=400)

        # Generar embedding de la consulta
        query_embedding = generate_embedding(query, openai_api_key)

        # Buscar documentos relevantes usando búsqueda vectorial
        results = search_client.search(
            search_text="",  # No se usa texto completo, solo vector
            vectors={"value": query_embedding, "fields": "content_vector", "k": 5}
        )
        documents = [doc["content"] for doc in results]

        if not documents:
            return func.HttpResponse(
                json.dumps({"error": "No se encontraron documentos relevantes."}),
                mimetype="application/json",
                status_code=404
            )

        # Crear el prompt para GPT-4
        prompt = f"""
        A continuación se presentan fragmentos relevantes basados en tu consulta: "{query}".
        Utiliza estos documentos para responder con precisión:

        {documents}

        Respuesta:
        """
        # Generar respuesta con GPT-4
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=300
        )

        # Devolver la respuesta generada
        return func.HttpResponse(
            json.dumps({"query": query, "answer": response.choices[0].text.strip()}),
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error interno: {str(e)}", status_code=500)
