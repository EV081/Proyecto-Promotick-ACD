import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import {
  FolderUp,
  Truck,
  ChartNoAxesCombined,
  LogOut,
  ChevronFirst,
  ChevronLast,
  Lock,
} from "lucide-react";

import { useTheme } from "../../context/ThemeContext";
import { useDataset } from "../../context/DatasetContext";

// LOGOS
import lightLogo from "../../assets/logos/promotick-light.png";
import darkLogo from "../../assets/logos/promotick-dark.png";
import iconLogo from "../../assets/logos/promotick-icon.png";

export default function Sidebar({ collapsed, setCollapsed }) {
  const { logout } = useAuth();
  const location = useLocation();
  const { dark } = useTheme();
  const { datasetLoaded } = useDataset();

  const isActive = (path) => location.pathname === path;

  const baseLink =
    "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all whitespace-nowrap hover:translate-x-1";

  const activeLink =
    "bg-slate-200 dark:bg-slate-800 text-slate-900 dark:text-white shadow-sm";

  const inactiveLink =
    "text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-white";

  const lockedStyle =
    "opacity-40 cursor-not-allowed pointer-events-none";

  return (
    <aside
      className={`
        h-screen
        bg-white dark:bg-slate-950
        text-slate-700 dark:text-slate-300
        flex flex-col
        border-r border-slate-200 dark:border-slate-800
        overflow-hidden
        transition-all duration-300
        ${collapsed ? "w-24" : "w-72"}
      `}
    >
      {/* BRAND */}
      <div className="px-4 py-5 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">

        {!collapsed ? (
          <div className="flex items-center justify-center h-20 w-full overflow-hidden">
            <img
              src={dark ? darkLogo : lightLogo}
              className="h-full w-auto object-contain transition-all duration-300"
              alt="Promotick Logo"
            />
          </div>
        ) : (
          <div className="w-full flex flex-col items-center gap-3 py-2">

            <div className="
              w-12 h-12 flex items-center justify-center
              rounded-xl bg-white dark:bg-slate-900
              border border-slate-200 dark:border-slate-800
            ">
              <img
                src={iconLogo}
                className="w-8 h-8 object-contain"
                alt="Promotick Icon"
              />
            </div>

            <button
              onClick={() => setCollapsed(!collapsed)}
              className="flex items-center justify-center w-8 h-8 rounded-lg
              text-slate-500 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white
              hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <ChevronLast size={20} />
            </button>

          </div>
        )}

        {!collapsed && (
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="ml-2 flex items-center justify-center w-8 h-8 rounded-lg
            text-slate-500 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white
            hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <ChevronFirst size={20} />
          </button>
        )}
      </div>

      {/* NAV */}
      <nav className="flex-1 py-4 px-2 space-y-6">

        {/* UPLOAD (SIEMPRE ACTIVO) */}
        <div>
          {!collapsed && (
            <p className="px-3 mb-2 text-[11px] uppercase tracking-widest text-slate-500">
              Data
            </p>
          )}

          <Link
            to="/upload"
            className={`${baseLink} ${
              isActive("/upload") ? activeLink : inactiveLink
            } ${collapsed ? "justify-center" : "justify-start"}`}
          >
            <FolderUp size={18} />
            {!collapsed && <span>Upload</span>}
          </Link>
        </div>

        {/* DASHBOARDS */}
        <div>
          {!collapsed && (
            <p className="px-3 mb-2 text-[11px] uppercase tracking-widest text-slate-500">
              Dashboards
            </p>
          )}

          <div className="space-y-1">

            {/* OPERACIONAL */}
            <div
              className={`${!datasetLoaded ? lockedStyle : ""}`}
            >
              <Link
                to={datasetLoaded ? "/dashboard/operational" : "#"}
                className={`${baseLink} ${
                  isActive("/dashboard/operational")
                    ? activeLink
                    : inactiveLink
                } ${collapsed ? "justify-center" : "justify-start"}`}
              >
                {datasetLoaded ? (
                  <Truck size={18} />
                ) : (
                  <Lock size={18} />
                )}

                {!collapsed && (
                  <span>
                    {datasetLoaded ? "Operational" : "Locked"}
                  </span>
                )}
              </Link>
            </div>

            {/* GERENCIAL */}
            <div
              className={`${!datasetLoaded ? lockedStyle : ""}`}
            >
              <Link
                to={datasetLoaded ? "/dashboard/managerial" : "#"}
                className={`${baseLink} ${
                  isActive("/dashboard/managerial")
                    ? activeLink
                    : inactiveLink
                } ${collapsed ? "justify-center" : "justify-start"}`}
              >
                {datasetLoaded ? (
                  <ChartNoAxesCombined size={18} />
                ) : (
                  <Lock size={18} />
                )}

                {!collapsed && (
                  <span>
                    {datasetLoaded ? "Managerial" : "Locked"}
                  </span>
                )}
              </Link>
            </div>

          </div>
        </div>
      </nav>

      {/* FOOTER */}
      <div className="border-t border-slate-200 dark:border-slate-800 p-3">
        <button
          onClick={logout}
          className={`
            w-full flex items-center gap-3 px-3 py-3 rounded-xl
            text-red-500 dark:text-red-400
            hover:bg-red-100 dark:hover:bg-red-500/10
            transition-all
            ${collapsed ? "justify-center" : "justify-start"}
          `}
        >
          <LogOut size={18} />
          {!collapsed && "Logout"}
        </button>
      </div>
    </aside>
  );
}