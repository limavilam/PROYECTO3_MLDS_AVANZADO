import { useState } from "react";
import axios from "axios";

export default function ImageUploader() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    processFile(file);
  };

  const handleSelect = (e) => {
    const file = e.target.files[0];
    processFile(file);
  };

  const processFile = (file) => {
    if (!file) return;
    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const upload = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append("file", image);

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(
        "https://alzheimer-app.politebeach-446a1961.eastus.azurecontainerapps.io/predict",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setResult(response.data);
    } catch (err) {
      setResult({ error: "Error procesando la imagen." });
    }

    setLoading(false);
  };

  return (
    <div className="w-full max-w-xl bg-white shadow-lg rounded-xl p-6">
      
      <div
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        className="border-2 border-dashed border-indigo-400 rounded-lg p-8 text-center cursor-pointer bg-indigo-50 hover:bg-indigo-100 transition"
      >
        {preview ? (
          <img src={preview} alt="Preview" className="max-h-64 mx-auto rounded-lg" />
        ) : (
          <p className="text-indigo-600">Arrastra una imagen aquí o haz click para seleccionarla</p>
        )}

        <input
          type="file"
          accept="image/*"
          onChange={handleSelect}
          className="hidden"
          id="fileInput"
        />

        <label
          htmlFor="fileInput"
          className="block mt-4 text-sm text-indigo-700 underline cursor-pointer"
        >
          Seleccionar archivo
        </label>
      </div>

      <button
        onClick={upload}
        disabled={!image || loading}
        className="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-lg transition disabled:bg-gray-400"
      >
        {loading ? "Procesando..." : "Enviar imagen"}
      </button>

      {result && (
        <div className="mt-6 p-4 bg-indigo-100 rounded-lg">
          <h3 className="text-indigo-700 font-semibold">Resultado:</h3>
          <pre className="text-gray-800 mt-2 text-sm">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
