import lightLogo from "../assets/logos/promotick-light.png";
import darkLogo from "../assets/logos/promotick-dark.png";
import utecLogo from "../assets/logos/utec-logo.png";

import dashboardIllustration from "../assets/illustrations/data-analytics.png";

export default function AuthLayout({ children }) {
  return (
    <div className="min-h-screen flex">

      {/* LEFT SIDE */}
      <div className="hidden lg:flex w-1/2 relative overflow-hidden">

        {/* BACKGROUND */}
        <div className="absolute inset-0 bg-[#0B1220]" />

        {/* GLOW */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute w-[500px] h-[500px] bg-blue-500/10 rounded-full blur-3xl top-[-160px] left-[-140px]" />
          <div className="absolute w-[400px] h-[400px] bg-indigo-500/10 rounded-full blur-3xl bottom-[-140px] right-[-140px]" />
        </div>

        {/* CONTENT */}
        <div className="relative z-10 flex flex-col justify-start gap-8 p-10 pl-6 pr-16 text-white w-full max-w-none">

          {/* LOGOS */}
          <div className="flex items-center gap-4 relative left-[-26px]">
            <img src={darkLogo} className="h-14" alt="Promotick" />
            <div className="w-px h-8 bg-white/20" />
            <img src={utecLogo} className="h-12 opacity-90" alt="UTEC" />
          </div>

          {/* TITLE */}
          <div className="max-w-xl">
            <h1 className="text-4xl font-bold tracking-tight">
              Promotick Analytics
            </h1>

            <p className="mt-3 text-slate-300 text-lg leading-relaxed w-full" >
              Plataforma de análisis de tickets y métricas operativas para la toma de decisiones en tiempo real.
            </p>
          </div>

          {/* (VACÍO CONTROLADO - ZONA LIBRE DONDE ANTES HABÍA ANIMACIÓN) */}
          <div className="h-10" />

          {/* FOOTER EXPANDIDO */}
          <div className="flex justify-between border-t border-white/10 pt-4 mt-auto text-sm w-full px-2">

            <span className="text-slate-300 tracking-wide max-w-[90%]">
              Análisis Computacional de Datos - Grupo 1
            </span>

            <span className="text-slate-400 tracking-widest whitespace-nowrap">
              UTEC - ACD
            </span>

          </div>

        </div>

        {/* 🧑‍💻 ILUSTRACIÓN (MÁS ARRIBA + MÁS GRANDE + OCUPA ESPACIO LIBRE) */}
        <div className="absolute right-[155px] bottom-[90px] w-[390px] opacity-85 pointer-events-none">
          <img
            src={dashboardIllustration}
            alt="Dashboard Illustration"
            className="w-full object-contain"
          />
        </div>

      </div>

      {/* RIGHT SIDE */}
      <div className="w-full lg:w-1/2 flex items-center justify-center bg-slate-50 p-6">

        <div className="absolute inset-0 opacity-[0.03] pointer-events-none">
          <div className="w-full h-full bg-[radial-gradient(#000_1px,transparent_1px)] [background-size:20px_20px]" />
        </div>

        <div className="relative z-10 w-full max-w-md">
          {children}
        </div>

      </div>

    </div>
  );
}