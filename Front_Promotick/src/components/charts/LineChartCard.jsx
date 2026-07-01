import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

import { useTheme } from "../../context/ThemeContext";

export default function LineChartCard({ data, title, dataKey }) {

  const { dark } = useTheme();

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm dark:shadow-black/30 transition">

      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          {title}
        </h2>

        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Historical trend
        </p>
      </div>

      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data}>

          <CartesianGrid
            strokeDasharray="3 3"
            stroke={dark ? "#1e293b" : "#e2e8f0"}
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

          <Line
            type="monotone"
            dataKey={dataKey}
            stroke="#3b82f6"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 7 }}
          />

        </LineChart>
      </ResponsiveContainer>

    </div>
  );
}