import { useAuth } from "../../context/AuthContext";
import { useTheme } from "../../context/ThemeContext";
import { Moon, Sun, CircleUser } from "lucide-react";

export default function Topbar() {
  const { user } = useAuth();
  const { dark, toggleTheme } = useTheme();

  return (
    <div
      className="
        h-16
        bg-white dark:bg-slate-900
        border-b border-slate-200 dark:border-slate-800
        flex items-center justify-between
        px-6
      "
    >
      <h1 className="text-lg font-semibold text-slate-800 dark:text-white">
        Promotick Analytics
      </h1>

      <div className="flex items-center gap-4">
        <button
          onClick={toggleTheme}
          className="
            flex items-center gap-2
            px-3 py-2
            rounded-xl
            bg-slate-100 dark:bg-slate-800
            text-slate-700 dark:text-slate-200
            hover:bg-slate-200 dark:hover:bg-slate-700
            transition-all
          "
        >
          {dark ? (
            <>
              <Moon size={16} />
              <span className="text-sm">Dark</span>
            </>
          ) : (
            <>
              <Sun size={16} />
              <span className="text-sm">Light</span>
            </>
          )}
        </button>

        <div
          className="
            flex items-center gap-2
            px-3 py-2
            rounded-xl
            bg-slate-100 dark:bg-slate-800
            hover:bg-slate-200 dark:hover:bg-slate-700
            transition-all
          "
        >
          <CircleUser
            size={18}
            className="text-slate-500 dark:text-slate-400"
          />

          <span className="text-sm font-medium text-slate-700 dark:text-slate-200">
            {user}
          </span>
        </div>
      </div>
    </div>
  );
}