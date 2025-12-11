import ImageUploader from "./components/ImageUploader";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col items-center p-6 bg-gradient-to-br from-indigo-50 to-blue-100">
      
      <h1 className="text-3xl font-bold text-indigo-700 mt-6 mb-2">
        Alzheimer Detection
      </h1>

      <p className="text-gray-600 mb-10 text-center max-w-xl">
        Sube una imagen de resonancia magnética (MRI) para detectar el nivel de deterioro cognitivo utilizando nuestro modelo de IA.
      </p>

      <ImageUploader />
    </div>
  );
}
