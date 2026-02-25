import { PageShell } from "@/components/PageShell";

const mockProviders = [
  { name: "Maria Silva", fn: "copeira", stars: "4.9", concept: "5 estrelas" },
  { name: "João Lima", fn: "porteiro", stars: "4.6", concept: "em avaliação" }
];

export default function CompanySearchPage() {
  return (
    <PageShell title="Busca e Filtros">
      <div className="card mb-4 grid gap-3 md:grid-cols-4">
        <input className="input" placeholder="Função" />
        <input className="input" placeholder="Nota mínima" />
        <select className="input"><option>Conceito</option><option>5 estrelas</option></select>
        <select className="input"><option>Disponibilidade</option><option>Disponível</option></select>
      </div>
      <div className="grid gap-3">
        {mockProviders.map((p) => (
          <article key={p.name} className="card">
            <h3 className="font-semibold">{p.name}</h3>
            <p className="text-sm text-zinc-400">{p.fn} · {p.stars} estrelas · {p.concept}</p>
          </article>
        ))}
      </div>
    </PageShell>
  );
}
