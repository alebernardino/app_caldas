import Link from "next/link";
import { PageShell } from "@/components/PageShell";

export default function LandingPage() {
  return (
    <PageShell title="APP Caldas">
      <section className="grid gap-4 md:grid-cols-3">
        {[
          ["Empresas", "Hotéis e restaurantes contratam com rapidez.", "/signup/company"],
          ["Prestadores", "Agenda temporária com limite de 2 por semana.", "/signup/provider"],
          ["Treinamentos", "Trilha rápida para temporada.", "/dashboard/provider/training"]
        ].map(([title, desc, href]) => (
          <article key={title} className="card">
            <h2 className="text-lg font-semibold">{title}</h2>
            <p className="mt-2 text-sm text-zinc-400">{desc}</p>
            <Link href={href} className="btn mt-4 inline-block">Abrir</Link>
          </article>
        ))}
      </section>
    </PageShell>
  );
}
