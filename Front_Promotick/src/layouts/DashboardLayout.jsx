import Navbar from "../components/common/Navbar";
import Sidebar from "../components/common/Sidebar";

export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-slate-50">

      <Navbar />

      <div className="flex">

        {/* Sidebar fijo estilo SaaS */}
        <div className="w-72 hidden md:block">
          <div className="fixed h-full">
            <Sidebar />
          </div>
        </div>

        {/* Main content */}
        <main className="flex-1 md:ml-72 p-6 lg:p-10">
          {children}
        </main>

      </div>

    </div>
  );
}