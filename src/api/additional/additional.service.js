import api from "../axios";

export const getDatasetStatus = async () => {
  const response = await api.get("/additional/dataset-status");
  return response.data;
};

export const getProcessedDataset = async () => {
  const response = await api.get("/additional/processed-dataset");
  return response.data;
};