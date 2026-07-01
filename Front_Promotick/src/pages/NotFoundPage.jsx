import { useNavigate } from "react-router-dom";
import error404 from "../assets/illustrations/error_404.png";
import { ArrowLeft } from "lucide-react";

export default function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0B1220] px-6">

      <div className="text-center max-w-lg">

        <img
          src={error404}
          alt="404 Error"
          className="
            w-[340px]
            mx-auto
            mb-8
            transition-transform
            duration-500
            hover:scale-105
          "
        />

        <h2 className="text-3xl font-bold text-white">
          Página no encontrada
        </h2>

        <p className="mt-3 text-slate-400">
          La ruta que intentas acceder no existe.
        </p>

        <button
  onClick={() => navigate("/login")}
  className="
    mt-8
    flex items-center gap-2 mx-auto
    bg-white/5
    border border-white/10
    text-slate-300
    px-6 py-3
    rounded-xl
    font-medium
    transition-all duration-300
    hover:bg-blue-500
    hover:text-white
    hover:border-blue-500
    hover:shadow-xl hover:shadow-blue-500/25
  "
>
  <ArrowLeft size={18} />
  Volver al inicio
</button>

      </div>

    </div>
  );
}