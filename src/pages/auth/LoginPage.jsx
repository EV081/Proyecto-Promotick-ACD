import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { loginUser } from "../../api/auth/auth.service";
import { useAuth } from "../../context/AuthContext";

import AuthLayout from "../../layouts/AuthLayout";
import AuthCard from "../../components/auth/AuthCard";

export default function LoginPage() {

  const navigate = useNavigate();
  const { login } = useAuth();

  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");

      const response = await loginUser(form);

      login(response.user);
      navigate("/upload");

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Error al iniciar sesión"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>

      <AuthCard>

        {/* HEADER */}
        <div className="mb-8 text-center">

          <h1 className="text-3xl font-bold text-slate-900">
            Bienvenido de nuevo
          </h1>

          <p className="text-slate-500 mt-2">
            Inicia sesión en Promotick Analytics
          </p>

        </div>

        {/* FORM */}
        <form onSubmit={handleSubmit} className="space-y-5">

          <input
            type="text"
            name="username"
            placeholder="Usuario"
            value={form.username}
            onChange={handleChange}
            className="
              w-full
              p-3
              rounded-xl
              border border-slate-200
              bg-white
              text-slate-900
              placeholder-slate-400
              focus:outline-none
              focus:ring-2 focus:ring-blue-500
              dark:text-slate-900
            "
          />

          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            value={form.password}
            onChange={handleChange}
            className="
              w-full
              p-3
              rounded-xl
              border border-slate-200
              bg-white
              text-slate-900
              placeholder-slate-400
              focus:outline-none
              focus:ring-2 focus:ring-blue-500
              dark:text-slate-900
            "
          />

          {error && (
            <div className="text-red-500 text-sm">
              {error}
            </div>
          )}

          <button
            disabled={loading}
            className="
              w-full
              bg-[#0B1220]
              hover:bg-[#111a2e]
              text-white
              py-3
              rounded-xl
              font-semibold
              transition
              border border-white/10
              disabled:opacity-50
            "
          >
            {loading ? "Iniciando sesión..." : "Iniciar sesión"}
          </button>

        </form>

        {/* FOOTER */}
        <div className="text-center mt-6">

          <button
            onClick={() => navigate("/register")}
            className="text-state-900 font-medium"
          >
            Crear cuenta
          </button>

        </div>

      </AuthCard>

    </AuthLayout>
  );
}