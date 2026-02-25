import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "APP Caldas",
  description: "Marketplace regional de Caldas Novas"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
