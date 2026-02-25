import { PageShell } from "@/components/PageShell";

export default function NewBookingPage() {
  return (
    <PageShell title="Novo Agendamento">
      <div className="card mx-auto max-w-2xl space-y-3">
        <input className="input" placeholder="ID da empresa" />
        <input className="input" placeholder="ID do prestador" />
        <input className="input" placeholder="Função" />
        <input className="input" type="date" />
        <label className="flex items-center gap-2 text-sm text-zinc-300">
          <input type="checkbox" />
          Temporada (prioridade por antecedência)
        </label>
        <button className="btn">Criar solicitação</button>
      </div>
    </PageShell>
  );
}
