import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

import { useTheme } from "../../context/ThemeContext";

export default function BarChartCard({ data, title }) {

  const { dark } = useTheme();

  return (
    <div
      className="
        bg-white dark:bg-slate-900
        border border-slate-200 dark:border-slate-800
        rounded-3xl
        p-6
        shadow-sm dark:shadow-black/30
        transition
      "
    >

      <div className="mb-6">

        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          {title}
        </h2>

        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Panorama general de la distribucion
        </p>

      </div>

      {/* 1. CAMBIO: Subimos la altura total del contenedor de 320 a 370 para que las barras recuperen su tamaño */}
      <ResponsiveContainer width="100%" height={370}>

        {/* 2. CAMBIO: Reducimos bottom de 80 a 55 para subir el borde inferior y quitar el vacío inútil */}
        <BarChart
          data={data}
          margin={{ top: 10, right: 20, left: 15, bottom: 55 }}
        >

          <CartesianGrid
            strokeDasharray="3 3"
            stroke={dark ? "#334155" : "#e2e8f0"}
            opacity={0.4}
          />

          {/* 3. CAMBIO: Ajustamos el height de 90 a 65 para que encaje exacto con el nuevo margen */}
          <XAxis
            dataKey="name"
            tick={{ fill: dark ? "#94a3b8" : "#64748b" }}
            angle={-45}
            textAnchor="end"
            height={65}
            interval={0} 
            tickFormatter={(value) => 
              value && value.length > 14 ? `${value.slice(0, 14)}...` : value
            }
          />

          <YAxis
            tick={{ fill: dark ? "#94a3b8" : "#64748b" }}
          />

          <Tooltip
            contentStyle={{
              backgroundColor: dark ? "#0f172a" : "#ffffff",
              border: dark ? "1px solid #1e293b" : "1px solid #e2e8f0",
              borderRadius: "12px",
              color: dark ? "#fff" : "#0f172a"
            }}
          />

          <Bar
            dataKey="value"
            fill="#3b82f6"
            radius={[8, 8, 0, 0]}
          />

        </BarChart>

      </ResponsiveContainer>

    </div>
  );
}