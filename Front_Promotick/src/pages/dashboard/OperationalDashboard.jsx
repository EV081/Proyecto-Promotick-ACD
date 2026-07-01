import MetricCard from "../../components/common/MetricCard";

import PieChartCard from "../../components/charts/PieChartCard";
import BarChartCard from "../../components/charts/BarChartCard";

import LoadingSpinner from "../../components/common/LoadingSpinner";

import { useOperationalMetrics } from "../../hooks/useOperationalMetrics";

export default function OperationalDashboard() {

  const { data, loading } = useOperationalMetrics();

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
          Upload a CSV file to start generating metrics.
        </p>
      </div>
    );
  }

  return (
  <div className="w-full h-full space-y-8">

    {/* HEADER */}
    <div>
      <h1 className="text-3xl font-bold text-slate-900">
        Operational Dashboard
      </h1>

      <p className="mt-2 text-slate-500">
        Supervise el rendimiento operativo, el cumplimiento del SLA y la carga de trabajo de los tickets.
      </p>
    </div>

    {/* KPI GRID */}
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

      <MetricCard title="Tickets Abiertos" value={data.kpis.tickets_abiertos} />
      <MetricCard title="Tickets Cerrados" value={data.kpis.tickets_cerrados} />
      <MetricCard title="Tickets Resueltos" value={data.kpis.tickets_resueltos} />
      <MetricCard title="Backlog" value={data.kpis.backlog} />

      <MetricCard title="Tiempo Atención" value={data.kpis.tiempo_promedio_atencion} />
      <MetricCard title="Primera Respuesta" value={data.kpis.tiempo_primera_respuesta} />
      <MetricCard title="SLA %" value={data.kpis.cumplimiento_sla} />

    </div>

    {/* CHARTS */}
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

      <PieChartCard title="Tickets por Prioridad" data={data.priorities} />

      <BarChartCard title="Tickets por Categoría" data={data.categories} />

    </div>

    {/* ANALYST */}
    <div>
      <h2 className="text-xl font-semibold text-slate-900 mb-4">
        Rendimiento de los analistas
      </h2>

      <BarChartCard title="Tickets por Analista" data={data.analysts} />
    </div>

  </div>
);
}