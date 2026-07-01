import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

import { useTheme } from "../../context/ThemeContext";

const COLORS = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444"];

export default function PieChartCard({ data, title }) {

  const { dark } = useTheme();

  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm dark:shadow-black/30 transition">

      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          {title}
        </h2>

        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Desglose de la distribucion
        </p>
      </div>

      <ResponsiveContainer width="100%" height={280}>
        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={3}
          >
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>

          <Tooltip
            contentStyle={{
              backgroundColor: dark ? "#0f172a" : "#ffffff",
              border: dark ? "1px solid #1e293b" : "1px solid #e2e8f0",
              borderRadius: "12px",
              color: dark ? "#fff" : "#0f172a"
            }}
          />

          <Legend
            verticalAlign="bottom"
            height={36}
            wrapperStyle={{
              color: dark ? "#94a3b8" : "#64748b"
            }}
          />

        </PieChart>
      </ResponsiveContainer>

    </div>
  );
}