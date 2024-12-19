import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState([]);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const fetchData = async () => {
    try {
      const response = await axios.get("https://<tu-function-app-url>/api/process_data", {
        params: { query: query }
      });
      setData(response.data.blobs);
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div>
      <h1>Document AI RAG</h1>
      <input
        type="text"
        value={query}
        onChange={handleQueryChange}
        placeholder="Escribe tu pregunta"
      />
      <button onClick={fetchData}>Consultar</button>
      <div>
        <h2>Respuesta:</h2>
        <p>{answer}</p>
      </div>
      <h2>Blobs en Azure Storage:</h2>
      <ul>
        {data.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;