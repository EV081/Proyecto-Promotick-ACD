import LoadingSpinner from "../../components/common/LoadingSpinner";

import MetricCard from "../../components/common/MetricCard";

import LineChartCard from "../../components/charts/LineChartCard";
import AreaChartCard from "../../components/charts/AreaChartCard";

import SimpleTable from "../../components/charts/SimpleTable";

import { useManagerialMetrics } from "../../hooks/useManagerialMetrics";

export default function ManagerialDashboard() {

  const { data, loading } = useManagerialMetrics();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[70vh]">
        <LoadingSpinner />
      </div>
    );
  }

  if (!data || data.error) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-semibold text-slate-800">
          No dataset loaded
        </h2>

        <p className="mt-2 text-slate-500">
          Upload a CSV file to generate executive metrics.
        </p>
      </div>
    );
  }

  return (
  <div className="w-full h-full space-y-8">

    {/* EXECUTIVE SUMMARY */}
    <div className="p-8 rounded-3xl bg-gradient-to-r from-slate-900 to-slate-800 text-white shadow-lg">

      <h2 className="text-xl font-bold">
        Resumen Ejecutivo
      </h2>

      <p className="mt-3 text-slate-200 leading-relaxed">
        Los indicadores operativos actuales muestran{" "}
        <span className="font-semibold text-white">
          {data.backlog.backlog_critico}
        </span>{" "}
        tickets críticos atrasados y{" "}
        <span className="font-semibold text-white">
          {data.recurrent.length}
        </span>{" "}
        incidentes recurrentes que requieren atención gerencial.
      </p>

    </div>

    {/* HEADER */}
    <div>
      <h1 className="text-3xl font-bold text-slate-900">
        Managerial Dashboard
      </h1>

      <p className="mt-2 text-slate-500">
        Información estratégica para la toma de decisiones, la planificación operativa y el seguimiento de riesgos.
      </p>
    </div>

    {/* KPI GRID */}
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

      <MetricCard title="Backlog Crítico" value={data.backlog.backlog_critico} />
      <MetricCard title="Saturación Operativa" value={data.operationalSaturation?.[0]?.tickets_por_agente} />
      <MetricCard title="Incidentes Recurrentes" value={data.recurrent.length} />
      <MetricCard title="Áreas Activas" value={data.demand.length} />

    </div>

    {/* MAIN CHARTS */}
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <LineChartCard title="Tendencia de Tickets" data={data.trend} dataKey="tickets" />

      <AreaChartCard title="Comparativo Mensual" data={data.comparison} dataKey="tickets" />

    </div>

    {/* SECONDARY CHARTS */}
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <LineChartCard title="SLA Mensual" data={data.comparison} dataKey="tiempo_prom_resolucion" />

      <LineChartCard title="Saturación Operativa" data={data.saturation} dataKey="tickets_por_analista" />

    </div>

    {/* TABLE */}
    <div>
      <h2 className="text-xl font-semibold text-slate-900 mb-4">
        Incidentes recurrentes
      </h2>

      <SimpleTable data={data.recurrent} />
    </div>

  </div>
);
}