import Link from "next/link";
import { PageShell } from "@/components/PageShell";

export default function LandingPage() {
  const companyDemands = [
    {
      name: "Hotel Lago Azul",
      need: "2 recepcionistas e 1 copeira",
      when: "Inicio imediato"
    },
    {
      name: "Pousada Thermas do Sol",
      need: "1 porteiro noturno",
      when: "Escala fim de semana"
    },
    {
      name: "Restaurante Serra Verde",
      need: "2 garcons e 1 auxiliar de cozinha",
      when: "Alta temporada"
    }
  ];
  const providerProfiles = [
    { name: "Maria Clara", role: "Copeira", exp: "4 anos em resort" },
    { name: "Joao Pedro", role: "Porteiro", exp: "Turno noturno e eventos" },
    { name: "Ana Beatriz", role: "Recepcionista", exp: "Ingles intermediario" },
    { name: "Carlos Henrique", role: "Aux. cozinha", exp: "Buffet e producao" }
  ];
  const trainings = [
    "Boas praticas de atendimento em hotelaria",
    "Seguranca e organizacao para limpeza de piscina",
    "Padrao de atendimento em restaurantes de temporada",
    "Agilidade para equipes temporarias"
  ];

  return (
    <PageShell title="APP Caldas">
      <section className="mb-6 rounded-3xl border border-sky-200 bg-gradient-to-r from-white to-sky-50 p-8 shadow-sm">
        <p className="text-xs uppercase tracking-[0.28em] text-sky-700">Caldas Novas · Temporada</p>
        <h2 className="mt-3 max-w-4xl text-3xl font-semibold leading-tight text-slate-900 md:text-5xl">
          Conecte estabelecimentos e profissionais temporarios em uma unica plataforma.
        </h2>
        <p className="mt-4 max-w-3xl text-sm text-slate-600">
          MVP com foco em hotelaria e gastronomia, com visual limpo em tons de azul e
          experiencias de uso simples para apresentacao.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <article className="card">
          <div className="mb-4 flex items-start justify-between gap-3">
            <div>
              <h3 className="text-xl font-semibold text-slate-900">Estabelecimentos</h3>
              <p className="text-sm text-slate-600">Quem esta procurando profissionais</p>
            </div>
            <Link href="/signup/company" className="btn whitespace-nowrap">Cadastrar empresa</Link>
          </div>
          <div className="space-y-3">
            {companyDemands.map((item) => (
              <div key={item.name} className="rounded-xl border border-sky-100 bg-sky-50/70 p-3">
                <p className="font-semibold text-slate-800">{item.name}</p>
                <p className="text-sm text-slate-700">{item.need}</p>
                <p className="text-xs text-slate-500">{item.when}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="card">
          <div className="mb-4 flex items-start justify-between gap-3">
            <div>
              <h3 className="text-xl font-semibold text-slate-900">Profissionais</h3>
              <p className="text-sm text-slate-600">Quem esta procurando trabalho</p>
            </div>
            <Link href="/signup/provider" className="btn whitespace-nowrap">Cadastrar perfil</Link>
          </div>
          <div className="space-y-3">
            {providerProfiles.map((person) => (
              <div key={person.name} className="rounded-xl border border-cyan-100 bg-cyan-50/70 p-3">
                <p className="font-semibold text-slate-800">{person.name}</p>
                <p className="text-sm text-slate-700">{person.role}</p>
                <p className="text-xs text-slate-500">{person.exp}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="card">
          <h3 className="text-xl font-semibold text-slate-900">Treinamentos</h3>
          <p className="mb-4 text-sm text-slate-600">Capacitacao rapida para temporada</p>
          <div className="space-y-3">
            {trainings.map((topic) => (
              <div key={topic} className="rounded-xl border border-blue-100 bg-blue-50/70 p-3">
                <p className="text-sm font-medium text-slate-800">{topic}</p>
              </div>
            ))}
            <Link href="/dashboard/provider/training" className="btn inline-block">Ver treinamentos</Link>
          </div>
        </article>
      </section>
    </PageShell>
  );
}
