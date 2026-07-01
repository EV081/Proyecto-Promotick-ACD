import { ChartColumnBig } from "lucide-react";

export default function MetricCard({ title, value }) {
  return (
    <div
      className="
        group
        bg-white dark:bg-slate-900
        border border-slate-200 dark:border-slate-800
        hover:border-blue-200 dark:hover:border-blue-900
        rounded-3xl
        p-6
        shadow-sm dark:shadow-black/30
        hover:shadow-md
        transition-all duration-300
      "
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
            {title}
          </p>

          <h2 className="mt-3 text-4xl font-bold text-slate-900 dark:text-white">
            {value}
          </h2>
        </div>

        <div
          className="
            w-12 h-12
            rounded-2xl
            bg-blue-50 dark:bg-blue-500/10
            flex items-center justify-center
          "
        >
          <ChartColumnBig
            size={24}
            className="
              text-blue-600 dark:text-blue-400
              transition-transform duration-300
              group-hover:scale-110
            "
          />
        </div>
      </div>

      <div className="mt-5 flex items-center gap-2 text-sm">
        <span className="font-medium text-emerald-600 dark:text-emerald-400">
          Active
        </span>

        <span className="text-slate-400">
          Current dataset
        </span>
      </div>
    </div>
  );
}