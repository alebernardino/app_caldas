import Link from "next/link";
import { ReactNode } from "react";

export function PageShell({ title, children }: { title: string; children: ReactNode }) {
  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{title}</h1>
          <p className="text-sm text-zinc-400">APP Caldas · Marketplace Regional</p>
        </div>
        <nav className="flex flex-wrap gap-3 text-sm text-zinc-300">
          <Link href="/">Home</Link>
          <Link href="/login">Login</Link>
          <Link href="/dashboard/company">Empresa</Link>
          <Link href="/dashboard/provider">Prestador</Link>
        </nav>
      </header>
      {children}
    </main>
  );
}
