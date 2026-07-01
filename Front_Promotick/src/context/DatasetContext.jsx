import {
  createContext,
  useContext,
  useEffect,
  useState
} from "react";

import {
  getDatasetStatus
} from "../api/additional/additional.service";

const DatasetContext = createContext();

export function DatasetProvider({ children }) {

  const [datasetLoaded, setDatasetLoaded] = useState(false);

  const [datasetInfo, setDatasetInfo] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    checkDataset();

  }, []);

  const checkDataset = async () => {

    try {

      const response =
        await getDatasetStatus();

      setDatasetLoaded(response.exists);

      setDatasetInfo(response);

    } catch (error) {

      setDatasetLoaded(false);

      setDatasetInfo(null);

    } finally {

      setLoading(false);

    }
  };

  const refreshDatasetStatus = async () => {

    await checkDataset();

  };

  return (
    <DatasetContext.Provider
      value={{
        datasetLoaded,
        datasetInfo,
        loading,
        setDatasetLoaded,
        setDatasetInfo,
        refreshDatasetStatus
      }}
    >
      {children}
    </DatasetContext.Provider>
  );
}

export function useDataset() {

  return useContext(DatasetContext);

}