import { PageShell } from "@/components/PageShell";

export default function SignupCompanyPage() {
  return (
    <PageShell title="Cadastro Empresa">
      <div className="card mx-auto max-w-2xl space-y-3">
        <input className="input" placeholder="Nome da empresa" />
        <textarea className="input min-h-24" placeholder="Descrição" />
        <input className="input" placeholder="Cidade" defaultValue="Caldas Novas" />
        <input className="input" placeholder="E-mail" />
        <input className="input" placeholder="Senha" type="password" />
        <button className="btn">Cadastrar empresa</button>
      </div>
    </PageShell>
  );
}
