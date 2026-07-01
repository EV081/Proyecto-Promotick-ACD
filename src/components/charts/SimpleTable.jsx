export default function SimpleTable({ data }) {

  return (

    <div
      className="
        bg-white dark:bg-slate-900
        border border-slate-200 dark:border-slate-800
        rounded-3xl
        p-6
        shadow-sm dark:shadow-black/30
        transition
      "
    >

      <div className="mb-6">

        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          Incidentes Recurrentes
        </h2>

        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Categorias de problemas mas frecuentes
        </p>

      </div>

      <div className="overflow-hidden rounded-2xl border border-slate-100 dark:border-slate-800">

        <table className="w-full text-left">

          <thead className="bg-slate-50 dark:bg-slate-800">
            <tr>

              <th className="py-3 px-4 text-sm font-semibold text-slate-600 dark:text-slate-300">
                Asunto
              </th>

              <th className="py-3 px-4 text-sm font-semibold text-slate-600 dark:text-slate-300">
                Cantidad
              </th>

            </tr>
          </thead>

          <tbody>

            {data.map((item, index) => (
              <tr
                key={index}
                className="
                  border-t border-slate-100 dark:border-slate-800
                  hover:bg-slate-50 dark:hover:bg-slate-800/60
                  transition
                "
              >

                <td className="py-3 px-4 text-slate-700 dark:text-slate-300">
                  {item.name}
                </td>

                <td className="py-3 px-4 font-semibold text-slate-900 dark:text-white">
                  {item.value}
                </td>

              </tr>
            ))}

          </tbody>

        </table>

      </div>

    </div>

  );
}