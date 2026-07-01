import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

import { useTheme } from "../../context/ThemeContext";

export default function AreaChartCard({ data, title, dataKey }) {

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
          Comparar evolucion
        </p>

      </div>

      <ResponsiveContainer width="100%" height={320}>

        <AreaChart data={data}>

          <defs>
            <linearGradient id="colorArea" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={dark ? 0.35 : 0.4} />
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid
            strokeDasharray="3 3"
            stroke={dark ? "#334155" : "#e2e8f0"}
            opacity={0.4}
          />

          <XAxis
            dataKey="mes"
            tick={{ fill: dark ? "#94a3b8" : "#64748b" }}
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

          <Area
            type="monotone"
            dataKey={dataKey}
            stroke="#3b82f6"
            strokeWidth={3}
            fill="url(#colorArea)"
          />

        </AreaChart>

      </ResponsiveContainer>

    </div>
  );
}