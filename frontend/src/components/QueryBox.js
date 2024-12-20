import React, { useState } from 'react';

function QueryBox() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSearch = async () => {
    const res = await fetch(`http://localhost:7071/api/function_app?query=${query}`);
    const data = await res.json();
    setResponse(data.answer);
  };

  return (
    <div>
      <h2>Ask a Question</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query"
      />
      <button onClick={handleSearch}>Search</button>
      <p>Response: {response}</p>
    </div>
  );
}

export default QueryBox;
