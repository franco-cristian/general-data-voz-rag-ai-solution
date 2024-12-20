# Document AI RAG (Retrieve-Augment-Generate)

Este proyecto implementa un sistema de preguntas y respuestas basado en documentos utilizando la metodología RAG (Retrieve, Augment, Generate). Combina Azure Ai Search, OpenAI, y Azure Functions para proporcionar respuestas basadas en información contenida en documentos cargados en Azure Blob Storage.

---

## **Arquitectura**

- **Backend**: Desarrollado con Azure Functions.
  - Recupera documentos de Azure Blob Storage.
  - Realiza búsquedas en Azure Cognitive Search.
  - Genera respuestas con OpenAI GPT.
  
- **Frontend**: Desarrollado con React.
  - Permite cargar documentos.
  - Proporciona una interfaz para realizar preguntas y obtener respuestas.

---



