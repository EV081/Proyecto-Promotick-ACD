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

  // 1. EXTRAER "NO AGENT" Y DARLE FORMATO DE GRÁFICO
  const noAgentRecord = data.analysts?.find(
    (item) => item.name.toLowerCase() === "no agent"
  );
  
  // Creamos un arreglo con un solo ítem estructurado para el BarChartCard
  const noAgentData = [
    {
      name: "Sin Asignar",
      value: noAgentRecord ? noAgentRecord.value : 0
    }
  ];

  // 2. FILTRAR LOS ANALISTAS REALES
  const filteredAnalysts = data.analysts?.filter(
    (item) => item.name.toLowerCase() !== "no agent"
  );

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

      {/* ANALYST SECTION */}
<div>
  <h2 className="text-xl font-semibold text-slate-900 mb-4">
    Rendimiento de los analistas
  </h2>

  {/* CAMBIO: Pasamos de grid-cols-4 a grid-cols-3 para dar más espacio a la izquierda */}
  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
    
    {/* CAMBIO: Al ser 1 de 3 columnas, tiene más espacio horizontal */}
    <div className="lg:col-span-1">
      <BarChartCard 
        title="Sin Agente Asignado" // CAMBIO: Nuevo título solicitado
        data={noAgentData} 
      />
    </div>

    {/* CAMBIO: col-span-2 toma las dos partes restantes */}
    <div className="lg:col-span-2">
      <BarChartCard 
        title="Tickets por Analista Asignado" 
        data={filteredAnalysts} 
      />
    </div>

  </div>
</div>
    </div>
  );
}