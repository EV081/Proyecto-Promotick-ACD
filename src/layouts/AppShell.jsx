import Sidebar from "../components/common/Sidebar";
import Topbar from "../components/layout/Topbar";
import { useState } from "react";
import { Outlet } from "react-router-dom";

export default function AppShell() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="h-screen w-screen flex overflow-hidden bg-slate-50">

      {/* SIDEBAR */}
      <Sidebar
        collapsed={collapsed}
        setCollapsed={setCollapsed}
      />

      {/* RIGHT SIDE */}
      <div className="flex flex-col flex-1 min-w-0">

        {/* TOPBAR */}
        <Topbar />

        {/* CONTENT */}
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>

      </div>
    </div>
  );
}