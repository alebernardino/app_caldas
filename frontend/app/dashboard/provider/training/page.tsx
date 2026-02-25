import { PageShell } from "@/components/PageShell";

export default function TrainingPage() {
  return (
    <PageShell title="Treinamentos (Mock)">
      <div className="grid gap-3 md:grid-cols-3">
        {["Boas práticas em hotel", "Atendimento em restaurante", "Segurança operacional"].map((item) => (
          <article key={item} className="card">
            <h2 className="font-semibold">{item}</h2>
            <p className="mt-2 text-sm text-zinc-400">Conteúdo ilustrativo para apresentação do MVP.</p>
          </article>
        ))}
      </div>
    </PageShell>
  );
}
