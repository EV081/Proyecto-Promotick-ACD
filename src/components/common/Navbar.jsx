import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
  const { user } = useAuth();

  return (
    <nav
      className="
      bg-white
      border-b
      border-slate-200
      px-8
      py-4
      flex
      justify-between
      items-center
      "
    >
      <div>
        <h2
          className="
          text-xl
          font-semibold
          text-slate-900
          "
        >
          Analytics Dashboard
        </h2>

        <p
          className="
          text-sm
          text-slate-500
          "
        >
          Monitor ticket performance and operational metrics
        </p>
      </div>

      <div
        className="
        bg-slate-100
        px-4
        py-2
        rounded-full
        text-sm
        font-medium
        text-slate-700
        "
      >
        {user}
      </div>
    </nav>
  );
}