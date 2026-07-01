import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { registerUser } from "../../api/auth/auth.service";

import AuthLayout from "../../layouts/AuthLayout";
import AuthCard from "../../components/auth/AuthCard";

export default function RegisterPage() {

  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setError("");

      const response = await registerUser(form);

      setMessage(response.message);

      setTimeout(() => {
        navigate("/login");
      }, 1200);

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Error al registrar"
      );
    }
  };

  return (
    <AuthLayout>

      <AuthCard>

        {/* HEADER */}
        <div className="mb-8 text-center">

          <h1 className="text-3xl font-bold text-slate-900">
            Crear cuenta
          </h1>

          <p className="text-slate-500 mt-2">
            Empieza a analizar tus datos de tickets
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

          {message && (
            <div className="text-green-600 text-sm">
              {message}
            </div>
          )}

          {error && (
            <div className="text-red-500 text-sm">
              {error}
            </div>
          )}

          <button
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
            "
          >
            Crear cuenta
          </button>

        </form>

        {/* FOOTER */}
        <div className="text-center mt-6">

          <button
            onClick={() => navigate("/login")}
            className="text-state-900 font-medium"
          >
            Ya tengo una cuenta
          </button>

        </div>

      </AuthCard>

    </AuthLayout>
  );
}