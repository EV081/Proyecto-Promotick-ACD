import { useEffect, useState } from "react";

import {
  getOperationalMetrics,
  getPriorities,
  getCategories,
  getAnalysts
} from "../api/metrics/operational.service";

import { objectToChartData } from "../utils/chartTransform";

export const useOperationalMetrics = () => {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {

    const loadData = async () => {

      try {

        const [
          metrics,
          priorities,
          categories,
          analysts
        ] = await Promise.all([
          getOperationalMetrics(),
          getPriorities(),
          getCategories(),
          getAnalysts()
        ]);

        setData({

          kpis: metrics.data,

          priorities:
            objectToChartData(
              priorities.data
            ),

          categories:
            objectToChartData(
              categories.data
            ),

          analysts:
            objectToChartData(
              analysts.data
            )

        });

      } finally {
        setLoading(false);
      }

    };

    loadData();

  }, []);

  return { data, loading };
};