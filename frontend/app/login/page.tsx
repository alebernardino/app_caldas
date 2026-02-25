import { PageShell } from "@/components/PageShell";

export default function LoginPage() {
  return (
    <PageShell title="Login">
      <div className="card mx-auto max-w-md space-y-4">
        <input className="input" placeholder="E-mail" />
        <input className="input" placeholder="Senha" type="password" />
        <button className="btn w-full">Entrar</button>
      </div>
    </PageShell>
  );
}
