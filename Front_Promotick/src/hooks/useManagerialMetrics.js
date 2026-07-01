import { useEffect, useState } from "react";

import {
  getTrend,
  getMonthlyComparison,
  getCriticalBacklog,
  getDemandByArea,
  getTopCategories,
  getOperationalSaturation,
  getSaturation,
  getRecurrentIncidents
} from "../api/metrics/managerial.service";

import { objectToChartData } from "../utils/chartTransform";

export const useManagerialMetrics = () => {

  const [data, setData] = useState({
    trend: null,
    comparison: null,
    backlog: null,
    demand: [],
    topCategories: [],
    operationalSaturation: null,
    saturation: null,
    recurrent: []
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const safeGet = (result) => {
      return result.status === "fulfilled"
        ? result.value?.data
        : null;
    };

    const safeTransform = (value) => {
      try {
        return objectToChartData(value ?? {});
      } catch (e) {
        return [];
      }
    };

    const loadData = async () => {

      try {

        const results = await Promise.allSettled([
          getTrend(),
          getMonthlyComparison(),
          getCriticalBacklog(),
          getDemandByArea(),
          getTopCategories(),
          getOperationalSaturation(),
          getSaturation(),
          getRecurrentIncidents()
        ]);

        setData({

          trend: safeGet(results[0]),
          comparison: safeGet(results[1]),
          backlog: safeGet(results[2]),

          demand: safeTransform(safeGet(results[3])),
          topCategories: safeTransform(safeGet(results[4])),

          operationalSaturation: safeGet(results[5]),
          saturation: safeGet(results[6]),

          recurrent: safeTransform(safeGet(results[7]))

        });

      } catch (error) {
        console.error("Error loading managerial metrics:", error);
      } finally {
        setLoading(false);
      }

    };

    loadData();

  }, []);

  return { data, loading };
};