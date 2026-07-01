import { useNavigate } from "react-router-dom";
import { CloudUpload } from "lucide-react";
import { Upload } from "lucide-react";

import lockIllustration from "../assets/illustrations/bloqueo_data.png";

export default function NoDatasetPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-6">

      <div className="max-w-4xl w-full flex flex-col lg:flex-row items-center gap-12">

        {/* LEFT - ILLUSTRATION */}
        <div className="flex-1 flex justify-center">
          <img
            src={lockIllustration}
            alt="Dataset bloqueado"
            className="w-[320px] lg:w-[420px] object-contain"
          />
        </div>

        {/* RIGHT - CONTENT */}
        <div className="flex-1 text-center lg:text-left">

          {/* BADGE */}
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-sm font-medium">
            <CloudUpload size={16} />
            Dataset requerido
          </div>

          {/* TITLE */}
          <h1 className="mt-5 text-4xl font-bold text-slate-900">
            No hay dataset cargado
          </h1>

          {/* DESCRIPTION */}
          <p className="mt-4 text-slate-500 text-lg leading-relaxed">
            Para acceder a los dashboards primero debes subir y procesar un archivo CSV.
            Esto permite generar métricas operativas y análisis en tiempo real.
          </p>

          {/* BUTTON */}
          <button
            onClick={() => navigate("/upload")}
            className="
            mt-8
            flex items-center gap-2
            mx-auto lg:mx-0

        bg-blue-50
            border border-blue-200

          text-blue-700
            px-6 py-3
            rounded-xl
            font-medium

            transition-all duration-300

        hover:bg-blue-600
        hover:text-white
        hover:border-blue-600

         hover:shadow-lg
        hover:shadow-blue-500/25
        hover:scale-[1.03]
            "
            >
        <Upload size={18} />
            Ir a cargar dataset
        </button>

        </div>

      </div>
    </div>
  );
}