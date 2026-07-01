import { useState } from "react";
import { useNavigate } from "react-router-dom";

import UploadBox from "../../components/upload/UploadBox";
import LoadingSpinner from "../../components/common/LoadingSpinner";

import { uploadCsv } from "../../api/upload/upload.service";
import { useDataset } from "../../context/DatasetContext";

export default function UploadPage() {

  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const { refreshDatasetStatus, setDatasetLoaded } = useDataset();


  const handleUpload = async () => {

  if (!file) {
    setError("Seleccione un archivo CSV");
    return;
  }

  try {

    setLoading(true);
    setError("");

    const response = await uploadCsv(file);

    setSuccess(response.message);

    // 🔥 ACTUALIZAR DATASET GLOBAL (CLAVE DEL SISTEMA)
    await refreshDatasetStatus();

    // fallback por seguridad
    setDatasetLoaded(true);

    // navegación controlada
    setTimeout(() => {
      navigate("/dashboard/operational");
    }, 1200);

  } catch (err) {

    setError(
      err.response?.data?.detail ||
      "Error procesando archivo"
    );

  } finally {
    setLoading(false);
  }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">

      {/* HEADER */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold text-slate-900">
          Carga tu Dataset
        </h1>

        <p className="mt-2 text-slate-500">
          Sube tu archivo CSV para generar información operativa y de gestión.
        </p>
      </div>

      {/* MAIN CARD */}
      <div className="bg-white border border-slate-200 rounded-3xl p-8 shadow-sm">

        <UploadBox file={file} setFile={setFile} />

        {/* ACTION */}
        <div className="mt-8 flex justify-center">
          <button
            onClick={handleUpload}
            disabled={loading}
            className="
              bg-blue-600
              hover:bg-blue-700
              text-white
              font-semibold
              px-8
              py-3
              rounded-xl
              transition
              disabled:opacity-50
            "
          >
            Procesar Dataset
          </button>
        </div>

        {/* STATES */}
        <div className="mt-6 space-y-3">

          {loading && <LoadingSpinner />}

          {success && (
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700">
              {success}
            </div>
          )}

          {error && (
            <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-600">
              {error}
            </div>
          )}

        </div>

      </div>

    </div>
  );
}