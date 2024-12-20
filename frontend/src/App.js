import React, { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleSearch = async () => {
    const res = await fetch(
      `https://<AZURE_FUNCTION_URL>/api/function_name?query=${encodeURIComponent(
        query
      )}`
    );
    const data = await res.json();
    setResponse(data.answer);
  };

  return (
    <div>
      <h1>Document AI RAG</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Escribe tu pregunta"
      />
      <button onClick={handleSearch}>Buscar</button>
      <p>{response}</p>
    </div>
  );
}

export default App;
