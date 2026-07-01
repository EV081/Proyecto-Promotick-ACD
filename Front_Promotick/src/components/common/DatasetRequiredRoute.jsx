import { useDataset } from "../../context/DatasetContext";
import NoDatasetPage from "../../pages/NoDatasetPage";

export default function DatasetRequiredRoute({ children }) {

  const { datasetLoaded, loading } = useDataset();

  if (loading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center text-slate-500">
        Verificando dataset...
      </div>
    );
  }

  if (!datasetLoaded) {
    return <NoDatasetPage />;
  }

  return children;
}