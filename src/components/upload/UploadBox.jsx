import { useRef } from "react";
import { CloudUpload } from "lucide-react";

export default function UploadBox({
  file,
  setFile
}) {
  const inputRef = useRef();

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();

    const droppedFile =
      e.dataTransfer.files[0];

    if (droppedFile) {
      setFile(droppedFile);
    }
  };

  return (
    <div
      onDragOver={(e) =>
        e.preventDefault()
      }
      onDrop={handleDrop}
      onClick={() =>
        inputRef.current.click()
      }
      className="
        group
        bg-white dark:bg-slate-900
        border-2
        border-dashed
        border-slate-300 dark:border-slate-700
        rounded-3xl
        py-16
        px-8
        text-center
        cursor-pointer
        hover:border-blue-500
        hover:bg-blue-50/40
        dark:hover:bg-blue-500/5
        transition-all
        duration-300
        shadow-sm
      "
    >
      <input
        type="file"
        accept=".csv"
        ref={inputRef}
        hidden
        onChange={handleFileChange}
      />

      {/* Icon */}
      <div className="mb-6 flex justify-center">
        <div
          className="
            w-24 h-24
            rounded-full
            bg-blue-50 dark:bg-blue-500/10
            flex items-center justify-center
            transition-all duration-300
            group-hover:scale-105
          "
        >
          <CloudUpload
            size={48}
            strokeWidth={1.5}
            className="
              text-blue-500
              opacity-70
            "
          />
        </div>
      </div>

      {/* Title */}
      <h2
        className="
          text-2xl
          font-semibold
          text-slate-900 dark:text-white
        "
      >
        Cargar tu Dataset de Tickets
      </h2>

      <p
        className="
          mt-3
          text-slate-500 dark:text-slate-400
        "
      >
        Arrastra y suelta tu archivo CSV aquí.
      </p>

      <p
        className="
          text-slate-400 dark:text-slate-500
          text-sm
          mt-1
        "
      >
        o haga clic para explorar los archivos
      </p>

      {/* Uploaded file */}
      {file && (
        <div
          className="
            mt-8
            inline-flex
            items-center
            gap-2
            px-5
            py-2
            bg-emerald-50 dark:bg-emerald-500/10
            text-emerald-700 dark:text-emerald-400
            rounded-full
            font-medium
          "
        >
          ✓ {file.name}
        </div>
      )}
    </div>
  );
}