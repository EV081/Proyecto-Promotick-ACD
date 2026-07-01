import api from "../axios";

export const getOperationalMetrics = () =>
  api.get("/metrics/operational");

export const getPriorities = () =>
  api.get("/metrics/priorities");

export const getCategories = () =>
  api.get("/metrics/categories");

export const getAnalysts = () =>
  api.get("/metrics/analysts");