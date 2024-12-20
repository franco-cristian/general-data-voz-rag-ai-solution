import React from 'react';

function FileUploader() {
  const handleUpload = (event) => {
    const file = event.target.files[0];
    console.log("Uploading file:", file.name);
    // Aquí iría la lógica para subir al Blob Storage
  };

  return (
    <div>
      <h2>Upload a File</h2>
      <input type="file" onChange={handleUpload} />
    </div>
  );
}

export default FileUploader;
