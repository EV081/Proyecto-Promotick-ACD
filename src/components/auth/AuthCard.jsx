export default function AuthCard({ children }) {
  return (
    <div
      className="
      w-full
      max-w-md
      bg-white/70
      backdrop-blur-xl
      border
      border-slate-200
      rounded-3xl
      p-8
      shadow-sm
      "
    >
      {children}
    </div>
  );
}