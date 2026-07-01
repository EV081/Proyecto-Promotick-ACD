import { useEffect, useState } from "react";

import iconLogo from "../../assets/logos/promotick-icon.png";

export default function LoadingSpinner() {

  const steps = [
    "Validando estructura del dataset...",
    "Limpiando registros...",
    "Calculando métricas operativas...",
    "Generando indicadores gerenciales...",
    "Preparando dashboards..."
  ];

  const [step, setStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStep((prev) => (prev + 1) % steps.length);
    }, 1800);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center py-16">

      {/* LOGO */}
      <div className="relative">

        <div
          className="
            absolute inset-0
            rounded-full
            bg-blue-500/20
            blur-xl
            animate-pulse
          "
        />

        <img
          src={iconLogo}
          alt="Promotick"
          className="
            relative
            w-20
            h-20
            object-contain
            animate-pulse
          "
        />

      </div>

      {/* TITLE */}
      <h3 className="mt-6 text-lg font-semibold text-slate-800">
        Procesando dataset
      </h3>

      {/* STEP */}
      <p
        className="
          mt-2
          text-sm
          text-slate-500
          transition-all
          duration-300
        "
      >
        {steps[step]}
      </p>

      {/* PROGRESS EFFECT */}
      <div
        className="
          mt-6
          w-72
          h-2
          bg-slate-200
          rounded-full
          overflow-hidden
        "
      >
        <div
          className="
            h-full
            w-1/2
            bg-blue-600
            rounded-full
            animate-pulse
          "
        />
      </div>

    </div>
  );
}