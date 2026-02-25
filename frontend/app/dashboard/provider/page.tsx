import Link from "next/link";
import { PageShell } from "@/components/PageShell";

export default function ProviderDashboardPage() {
  return (
    <PageShell title="Dashboard Prestador">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="card">
          <h2 className="text-lg font-semibold">Agenda</h2>
          <p className="mt-2 text-sm text-zinc-400">Regra ativa: máximo de 2 aceites por semana.</p>
        </div>
        <div className="card">
          <h2 className="text-lg font-semibold">Treinamentos</h2>
          <Link className="btn mt-3 inline-block" href="/dashboard/provider/training">Abrir mock</Link>
        </div>
      </div>
    </PageShell>
  );
}
