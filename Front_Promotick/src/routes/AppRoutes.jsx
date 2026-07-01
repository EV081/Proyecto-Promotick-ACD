import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";

import UploadPage from "../pages/upload/UploadPage";
import OperationalDashboard from "../pages/dashboard/OperationalDashboard";
import ManagerialDashboard from "../pages/dashboard/ManagerialDashboard";

import ProtectedRoute from "../components/common/ProtectedRoute";

import AppShell from "../layouts/AppShell";

import NotFoundPage from "../pages/NotFoundPage";

import DatasetRequiredRoute from "../components/common/DatasetRequiredRoute";

export default function AppRoutes() {

  return (
    <BrowserRouter>

      <Routes>

        {/* REDIRECT */}
        <Route
          path="/"
          element={<Navigate to="/login" />}
        />

        {/* AUTH (SIN SHELL) */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* APP (CON SHELL + PROTECCIÓN) */}
        <Route
          element={
            <ProtectedRoute>
              <AppShell />
            </ProtectedRoute>
          }
        >

          <Route path="/upload" element={<UploadPage />} />
          <Route path="/dashboard/operational" element={<DatasetRequiredRoute> <OperationalDashboard /> </DatasetRequiredRoute> } />
          <Route path="/dashboard/managerial" element={<DatasetRequiredRoute> <ManagerialDashboard /> </DatasetRequiredRoute>} />
        </Route>

        {/* 404 - SIEMPRE AL FINAL */}
       <Route path="*" element={<NotFoundPage />} />

      </Routes>

    </BrowserRouter>
  );
}