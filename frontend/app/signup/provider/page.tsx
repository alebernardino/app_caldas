import { PageShell } from "@/components/PageShell";

export default function SignupProviderPage() {
  return (
    <PageShell title="Cadastro Prestador">
      <div className="card mx-auto max-w-2xl space-y-3">
        <input className="input" placeholder="Nome completo" />
        <input className="input" placeholder="Função principal" defaultValue="garçom" />
        <textarea className="input min-h-24" placeholder="Resumo profissional" />
        <input className="input" placeholder="E-mail" />
        <input className="input" placeholder="Senha" type="password" />
        <button className="btn">Cadastrar prestador</button>
      </div>
    </PageShell>
  );
}
