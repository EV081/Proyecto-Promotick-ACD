import api from "../axios";

export const getTrend = () =>
  api.get("/metrics/trend");

export const getMonthlyComparison = () =>
  api.get("/metrics/monthly-comparison");

export const getCriticalBacklog = () =>
  api.get("/metrics/critical-backlog");

export const getDemandByArea = () =>
  api.get("/metrics/demand-by-area");

export const getTopCategories = () =>
  api.get("/metrics/top-categories");

export const getOperationalSaturation = () =>
  api.get("/metrics/operational-saturation");

export const getSaturation = () =>
  api.get("/metrics/saturation");

export const getRecurrentIncidents = () =>
  api.get("/metrics/recurrent-incidents");