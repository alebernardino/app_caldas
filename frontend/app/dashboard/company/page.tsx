import Link from "next/link";
import { PageShell } from "@/components/PageShell";

export default function CompanyDashboardPage() {
  return (
    <PageShell title="Dashboard Empresa">
      <div className="grid gap-4 md:grid-cols-2">
        <div className="card">
          <h2 className="text-lg font-semibold">Operações</h2>
          <div className="mt-3 flex flex-wrap gap-3">
            <Link className="btn" href="/dashboard/company/search">Buscar prestadores</Link>
            <Link className="btn" href="/dashboard/company/bookings/new">Novo agendamento</Link>
          </div>
        </div>
        <div className="card">
          <h2 className="text-lg font-semibold">Prioridade de temporada</h2>
          <p className="mt-2 text-sm text-zinc-400">
            Com `season=true`, a listagem prioriza pedidos com maior antecedência.
          </p>
        </div>
      </div>
    </PageShell>
  );
}
