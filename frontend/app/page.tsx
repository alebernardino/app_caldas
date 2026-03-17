"use client";

import Link from "next/link";
import { ReactNode, useMemo, useRef, useState } from "react";

type ActiveTab = "professionals" | "establishments" | "trainings";

type ProfessionalCard = {
  id: string;
  name: string;
  role: string;
  city: string;
  availability: string;
  experience: string;
  price: string;
  highlight: string;
  color: string;
};

type EstablishmentCard = {
  id: string;
  name: string;
  specialty: string;
  city: string;
  when: string;
  shift: string;
  budget: string;
  demand: string;
  color: string;
};

type TrainingCard = {
  id: string;
  title: string;
  category: string;
  city: string;
  format: string;
  duration: string;
  audience: string;
  color: string;
};

type FilterState = {
  date: string;
  specialty: string;
  city: string;
};

type Section<T> = {
  title: string;
  subtitle: string;
  items: T[];
};

const specialtyOptions = [
  "Todas especialidades",
  "Garcom",
  "Barman",
  "Caixa",
  "Copeira",
  "Recepcionista",
  "Auxiliar de cozinha",
  "Camareira",
];

const cityOptions = [
  "Todas localidades",
  "Caldas Novas",
  "Rio Quente",
  "Morrinhos",
  "Goiatuba",
  "Itumbiara",
];

const professionalSections: Section<ProfessionalCard>[] = [
  {
    title: "Garcom",
    subtitle: "Atendimento agil para restaurantes, bares e eventos.",
    items: [
      { id: "garcom-1", name: "Mateus Ribeiro", role: "Garcom lider", city: "Caldas Novas", availability: "Disponivel no fim de semana", experience: "6 anos em bares e festivais", price: "R$ 180 / diaria", highlight: "Atendimento premium", color: "from-amber-200 via-orange-100 to-white" },
      { id: "garcom-2", name: "Renata Alves", role: "Garcom de salao", city: "Rio Quente", availability: "Livre a partir de sexta", experience: "Treinada para alto giro", price: "R$ 160 / diaria", highlight: "Rapidez no fechamento", color: "from-rose-200 via-pink-100 to-white" },
      { id: "garcom-3", name: "Lucas Martins", role: "Garcom para buffet", city: "Caldas Novas", availability: "Escala noturna", experience: "Eventos corporativos e casamentos", price: "R$ 170 / diaria", highlight: "Servico organizado", color: "from-sky-200 via-cyan-100 to-white" },
      { id: "garcom-4", name: "Felipe Nunes", role: "Garcom volante", city: "Morrinhos", availability: "Escala sexta e sabado", experience: "Atendimento em casas cheias", price: "R$ 165 / diaria", highlight: "Boa cadencia de salao", color: "from-lime-200 via-emerald-100 to-white" },
      { id: "garcom-5", name: "Juliana Prado", role: "Garcom de restaurante", city: "Rio Quente", availability: "Livre para feriado", experience: "Treino em hotelaria", price: "R$ 175 / diaria", highlight: "Excelente atendimento", color: "from-orange-200 via-amber-100 to-white" },
      { id: "garcom-6", name: "Vitor Souza", role: "Garcom de evento", city: "Caldas Novas", availability: "Disponivel esta semana", experience: "Casamentos e eventos sociais", price: "R$ 185 / diaria", highlight: "Agilidade com bandeja", color: "from-teal-200 via-cyan-100 to-white" },
    ],
  },
  {
    title: "Barman",
    subtitle: "Perfis com experiencia em carta autoral e operacao rapida.",
    items: [
      { id: "barman-1", name: "Thiago Costa", role: "Barman", city: "Caldas Novas", availability: "Hoje e amanha", experience: "Coquetelaria para beach clubs", price: "R$ 220 / diaria", highlight: "Menu autoral", color: "from-emerald-200 via-lime-100 to-white" },
      { id: "barman-2", name: "Patricia Rocha", role: "Bartender", city: "Morrinhos", availability: "Alta temporada", experience: "Open bar e eventos premium", price: "R$ 240 / diaria", highlight: "Excelente upsell", color: "from-violet-200 via-fuchsia-100 to-white" },
      { id: "barman-3", name: "Diego Freitas", role: "Barman de apoio", city: "Rio Quente", availability: "Escala vespertina", experience: "Hotelaria e pools bar", price: "R$ 190 / diaria", highlight: "Agilidade no pico", color: "from-slate-300 via-slate-100 to-white" },
      { id: "barman-4", name: "Rafaela Campos", role: "Bartender de eventos", city: "Caldas Novas", availability: "Quinta a domingo", experience: "Cartas leves e autorais", price: "R$ 235 / diaria", highlight: "Drinkeria enxuta", color: "from-cyan-200 via-sky-100 to-white" },
      { id: "barman-5", name: "Caio Braga", role: "Barman de pool bar", city: "Rio Quente", availability: "Disponivel imediato", experience: "Operacao sob alta demanda", price: "R$ 210 / diaria", highlight: "Rapidez com ficha", color: "from-emerald-200 via-teal-100 to-white" },
      { id: "barman-6", name: "Helena Faria", role: "Bartender", city: "Itumbiara", availability: "Escala noturna", experience: "Rooftops e gastrobar", price: "R$ 250 / diaria", highlight: "Boa venda de carta", color: "from-fuchsia-200 via-rose-100 to-white" },
    ],
  },
  {
    title: "Caixa",
    subtitle: "Atendimento de frente, conferencia e fechamento seguro.",
    items: [
      { id: "caixa-1", name: "Bruna Melo", role: "Caixa", city: "Caldas Novas", availability: "Disponivel para feriados", experience: "PDV e conciliacao", price: "R$ 150 / diaria", highlight: "Fechamento sem retrabalho", color: "from-teal-200 via-cyan-100 to-white" },
      { id: "caixa-2", name: "Marcos Viana", role: "Caixa senior", city: "Goiatuba", availability: "Escala integral", experience: "Resorts e restaurantes", price: "R$ 165 / diaria", highlight: "Controle de fluxo", color: "from-yellow-200 via-amber-100 to-white" },
      { id: "caixa-3", name: "Nayara Souza", role: "Operadora de caixa", city: "Caldas Novas", availability: "A partir de 20/03", experience: "Atendimento cordial", price: "R$ 145 / diaria", highlight: "Boa avaliacao em pico", color: "from-cyan-200 via-sky-100 to-white" },
      { id: "caixa-4", name: "Larissa Cunha", role: "Caixa de loja", city: "Caldas Novas", availability: "Turno tarde", experience: "Conferencia e fechamento", price: "R$ 148 / diaria", highlight: "Fluxo bem controlado", color: "from-emerald-200 via-cyan-100 to-white" },
      { id: "caixa-5", name: "Samuel Rocha", role: "Caixa de apoio", city: "Rio Quente", availability: "Fim de semana", experience: "Operacao rapida em PDV", price: "R$ 155 / diaria", highlight: "Bom controle de fila", color: "from-amber-200 via-yellow-100 to-white" },
      { id: "caixa-6", name: "Elisa Tavares", role: "Caixa senior", city: "Goiatuba", availability: "Livre para temporada", experience: "Resort e food service", price: "R$ 170 / diaria", highlight: "Fechamento seguro", color: "from-indigo-200 via-sky-100 to-white" },
    ],
  },
  {
    title: "Copeira",
    subtitle: "Perfis para copa, reposicao, limpeza leve e apoio de salao.",
    items: [
      { id: "copeira-1", name: "Sandra Lemos", role: "Copeira", city: "Caldas Novas", availability: "Disponivel imediata", experience: "4 anos em pousadas", price: "R$ 130 / diaria", highlight: "Rotina padronizada", color: "from-orange-200 via-amber-100 to-white" },
      { id: "copeira-2", name: "Alessandra Lima", role: "Copeira de apoio", city: "Rio Quente", availability: "Turno da manha", experience: "Hotel e cafe da manha", price: "R$ 125 / diaria", highlight: "Otima reposicao", color: "from-pink-200 via-rose-100 to-white" },
      { id: "copeira-3", name: "Celia Fernandes", role: "Copeira senior", city: "Caldas Novas", availability: "Finais de semana", experience: "Eventos e buffet", price: "R$ 140 / diaria", highlight: "Operacao sem pausa", color: "from-indigo-200 via-blue-100 to-white" },
      { id: "copeira-4", name: "Marta Assis", role: "Copeira de hotel", city: "Caldas Novas", availability: "Disponivel fim de semana", experience: "Cafe da manha e reposicao", price: "R$ 132 / diaria", highlight: "Reposicao constante", color: "from-rose-200 via-orange-100 to-white" },
      { id: "copeira-5", name: "Simone Prado", role: "Copeira", city: "Morrinhos", availability: "Escala de manha", experience: "Rotina de pousada", price: "R$ 128 / diaria", highlight: "Boa organizacao", color: "from-lime-200 via-emerald-100 to-white" },
      { id: "copeira-6", name: "Paula Venceslau", role: "Copeira de apoio", city: "Rio Quente", availability: "A partir de amanha", experience: "Eventos e buffet", price: "R$ 138 / diaria", highlight: "Agilidade na limpeza", color: "from-cyan-200 via-sky-100 to-white" },
    ],
  },
];

const establishmentSections: Section<EstablishmentCard>[] = [
  {
    title: "Garcom",
    subtitle: "Estabelecimentos com demanda imediata para salao e eventos.",
    items: [
      { id: "hotel-garcom-1", name: "Casa Serra Botequim", specialty: "Garcom", city: "Caldas Novas", when: "21 a 23 mar", shift: "Noite", budget: "R$ 190 / diaria", demand: "3 vagas para atendimento de varanda", color: "from-amber-200 via-orange-100 to-white" },
      { id: "hotel-garcom-2", name: "Pousada Vale das Aguas", specialty: "Garcom", city: "Rio Quente", when: "Feriado prolongado", shift: "Cafe da manha", budget: "R$ 175 / diaria", demand: "2 profissionais para buffet", color: "from-sky-200 via-cyan-100 to-white" },
      { id: "hotel-garcom-3", name: "Bora Churrasco", specialty: "Garcom", city: "Caldas Novas", when: "Inicio imediato", shift: "Almoco e jantar", budget: "R$ 185 / diaria", demand: "4 vagas para alto giro", color: "from-rose-200 via-pink-100 to-white" },
      { id: "hotel-garcom-4", name: "Villa do Lago Bar", specialty: "Garcom", city: "Caldas Novas", when: "Sexta a domingo", shift: "Noite", budget: "R$ 195 / diaria", demand: "2 vagas para deck externo", color: "from-teal-200 via-cyan-100 to-white" },
      { id: "hotel-garcom-5", name: "Pousada Horizonte", specialty: "Garcom", city: "Rio Quente", when: "Pacote 4 dias", shift: "Cafe da manha", budget: "R$ 180 / diaria", demand: "3 vagas para buffet", color: "from-amber-200 via-orange-100 to-white" },
      { id: "hotel-garcom-6", name: "Rancho das Thermas", specialty: "Garcom", city: "Morrinhos", when: "Inicio imediato", shift: "Almoco", budget: "R$ 170 / diaria", demand: "2 vagas para salao principal", color: "from-sky-200 via-blue-100 to-white" },
    ],
  },
  {
    title: "Barman",
    subtitle: "Bares e resorts reforcando operacao de drinks e pool bar.",
    items: [
      { id: "hotel-barman-1", name: "Resort Lago Quente", specialty: "Barman", city: "Caldas Novas", when: "22 a 24 mar", shift: "Pool bar", budget: "R$ 260 / diaria", demand: "2 barmans para temporada", color: "from-emerald-200 via-lime-100 to-white" },
      { id: "hotel-barman-2", name: "Terraza Rooftop", specialty: "Barman", city: "Itumbiara", when: "Sabado", shift: "Noite", budget: "R$ 280 / diaria", demand: "1 bartender com carta autoral", color: "from-violet-200 via-fuchsia-100 to-white" },
      { id: "hotel-barman-3", name: "Deck 58 Gastrobar", specialty: "Barman", city: "Caldas Novas", when: "Toda sexta", shift: "Happy hour", budget: "R$ 240 / diaria", demand: "2 vagas para operacao rapida", color: "from-slate-300 via-slate-100 to-white" },
      { id: "hotel-barman-4", name: "Piano Lounge", specialty: "Barman", city: "Caldas Novas", when: "Sabado", shift: "Noite", budget: "R$ 255 / diaria", demand: "1 vaga para carta enxuta", color: "from-fuchsia-200 via-rose-100 to-white" },
      { id: "hotel-barman-5", name: "Termas Beach Club", specialty: "Barman", city: "Rio Quente", when: "Toda semana", shift: "Pool bar", budget: "R$ 245 / diaria", demand: "3 vagas para rotacao", color: "from-emerald-200 via-teal-100 to-white" },
      { id: "hotel-barman-6", name: "Mirante Rooftop", specialty: "Barman", city: "Itumbiara", when: "Sexta e sabado", shift: "Noite", budget: "R$ 270 / diaria", demand: "2 vagas para drinks classicos", color: "from-violet-200 via-sky-100 to-white" },
    ],
  },
  {
    title: "Caixa",
    subtitle: "Operacoes que precisam reforcar frente de caixa e fluxo.",
    items: [
      { id: "hotel-caixa-1", name: "Mercado das Termas", specialty: "Caixa", city: "Caldas Novas", when: "Fim de semana", shift: "Integral", budget: "R$ 160 / diaria", demand: "2 caixas para alta demanda", color: "from-teal-200 via-cyan-100 to-white" },
      { id: "hotel-caixa-2", name: "Padaria Estacao Quente", specialty: "Caixa", city: "Rio Quente", when: "Quinta a domingo", shift: "Abertura", budget: "R$ 150 / diaria", demand: "1 vaga para caixa principal", color: "from-yellow-200 via-amber-100 to-white" },
      { id: "hotel-caixa-3", name: "Parque Thermas Food Hall", specialty: "Caixa", city: "Caldas Novas", when: "Alta temporada", shift: "Rotativo", budget: "R$ 170 / diaria", demand: "3 vagas para PDV", color: "from-cyan-200 via-sky-100 to-white" },
      { id: "hotel-caixa-4", name: "Emporio Central", specialty: "Caixa", city: "Caldas Novas", when: "Fim de semana", shift: "Abertura", budget: "R$ 155 / diaria", demand: "2 vagas para frente de loja", color: "from-amber-200 via-yellow-100 to-white" },
      { id: "hotel-caixa-5", name: "Cantina da Serra", specialty: "Caixa", city: "Morrinhos", when: "Quinta a domingo", shift: "Noite", budget: "R$ 150 / diaria", demand: "1 vaga para caixa principal", color: "from-emerald-200 via-cyan-100 to-white" },
      { id: "hotel-caixa-6", name: "Arena Food Point", specialty: "Caixa", city: "Caldas Novas", when: "Alta temporada", shift: "Rotativo", budget: "R$ 168 / diaria", demand: "4 vagas para operacao continua", color: "from-indigo-200 via-blue-100 to-white" },
    ],
  },
  {
    title: "Copeira",
    subtitle: "Demandas para copa, reposicao e suporte de limpeza leve.",
    items: [
      { id: "hotel-copeira-1", name: "Hotel Estancia do Lago", specialty: "Copeira", city: "Caldas Novas", when: "Inicio imediato", shift: "Manha", budget: "R$ 140 / diaria", demand: "2 vagas para cafe da manha", color: "from-orange-200 via-amber-100 to-white" },
      { id: "hotel-copeira-2", name: "Cantina Dona Rita", specialty: "Copeira", city: "Morrinhos", when: "Sexta e sabado", shift: "Noite", budget: "R$ 135 / diaria", demand: "1 vaga para apoio de salao", color: "from-pink-200 via-rose-100 to-white" },
      { id: "hotel-copeira-3", name: "Pousada Bela Serra", specialty: "Copeira", city: "Caldas Novas", when: "Pacote de 5 dias", shift: "Cafe da manha", budget: "R$ 145 / diaria", demand: "2 profissionais para reposicao", color: "from-indigo-200 via-blue-100 to-white" },
      { id: "hotel-copeira-4", name: "Serra Dourada Hotel", specialty: "Copeira", city: "Caldas Novas", when: "Inicio imediato", shift: "Cafe da manha", budget: "R$ 138 / diaria", demand: "3 vagas para reposicao e apoio", color: "from-orange-200 via-amber-100 to-white" },
      { id: "hotel-copeira-5", name: "Bistro do Lago", specialty: "Copeira", city: "Rio Quente", when: "Sexta e sabado", shift: "Noite", budget: "R$ 136 / diaria", demand: "2 vagas para copa e salao", color: "from-pink-200 via-rose-100 to-white" },
      { id: "hotel-copeira-6", name: "Thermas Suites", specialty: "Copeira", city: "Caldas Novas", when: "Pacote 5 dias", shift: "Manha", budget: "R$ 142 / diaria", demand: "2 vagas para buffet matinal", color: "from-cyan-200 via-sky-100 to-white" },
    ],
  },
];

const trainingSections: Section<TrainingCard>[] = [
  {
    title: "Garcom",
    subtitle: "Conteudos curtos para atendimento e rotina de salao.",
    items: [
      { id: "treino-g-1", title: "Etiqueta de salao para alto giro", category: "Garcom", city: "Caldas Novas", format: "Presencial", duration: "2h", audience: "Garcons iniciantes", color: "from-amber-200 via-orange-100 to-white" },
      { id: "treino-g-2", title: "Comandas e sequencia de servico", category: "Garcom", city: "Rio Quente", format: "Workshop", duration: "1h30", audience: "Times de pousada", color: "from-sky-200 via-cyan-100 to-white" },
      { id: "treino-g-3", title: "Atendimento para eventos sociais", category: "Garcom", city: "Caldas Novas", format: "Imersao", duration: "3h", audience: "Freelas de evento", color: "from-rose-200 via-pink-100 to-white" },
      { id: "treino-g-4", title: "Bandeja, postura e agilidade", category: "Garcom", city: "Morrinhos", format: "Pratica guiada", duration: "2h", audience: "Escalas rotativas", color: "from-teal-200 via-cyan-100 to-white" },
      { id: "treino-g-5", title: "Buffet de cafe da manha", category: "Garcom", city: "Rio Quente", format: "Presencial", duration: "1h", audience: "Pousadas e resorts", color: "from-lime-200 via-emerald-100 to-white" },
      { id: "treino-g-6", title: "Upsell com atendimento natural", category: "Garcom", city: "Caldas Novas", format: "Aula rapida", duration: "1h15", audience: "Garcons de restaurante", color: "from-orange-200 via-amber-100 to-white" },
    ],
  },
  {
    title: "Barman",
    subtitle: "Operacao de drinks, ficha tecnica e ritmo de bar.",
    items: [
      { id: "treino-b-1", title: "Drinks classicos de alto giro", category: "Barman", city: "Caldas Novas", format: "Masterclass", duration: "2h", audience: "Barmans de pool bar", color: "from-emerald-200 via-lime-100 to-white" },
      { id: "treino-b-2", title: "Pre-batch e mise en place", category: "Barman", city: "Rio Quente", format: "Workshop", duration: "1h30", audience: "Equipes de resort", color: "from-violet-200 via-fuchsia-100 to-white" },
      { id: "treino-b-3", title: "Ficha tecnica sem desperdicio", category: "Barman", city: "Itumbiara", format: "Presencial", duration: "1h", audience: "Gastrobares", color: "from-slate-300 via-slate-100 to-white" },
      { id: "treino-b-4", title: "Carta enxuta para temporada", category: "Barman", city: "Caldas Novas", format: "Oficina", duration: "2h", audience: "Casas de evento", color: "from-cyan-200 via-sky-100 to-white" },
      { id: "treino-b-5", title: "Atendimento de rooftop", category: "Barman", city: "Rio Quente", format: "Imersao", duration: "2h30", audience: "Operacao noturna", color: "from-emerald-200 via-teal-100 to-white" },
      { id: "treino-b-6", title: "Velocidade com qualidade", category: "Barman", city: "Caldas Novas", format: "Pratica guiada", duration: "1h45", audience: "Freelas recorrentes", color: "from-fuchsia-200 via-rose-100 to-white" },
    ],
  },
  {
    title: "Caixa",
    subtitle: "Frente de caixa, fechamento e controle de fluxo.",
    items: [
      { id: "treino-c-1", title: "Fechamento de caixa sem retrabalho", category: "Caixa", city: "Caldas Novas", format: "Presencial", duration: "1h30", audience: "Caixas de restaurante", color: "from-teal-200 via-cyan-100 to-white" },
      { id: "treino-c-2", title: "PDV e conciliacao rapida", category: "Caixa", city: "Rio Quente", format: "Workshop", duration: "1h", audience: "Operacao de food hall", color: "from-yellow-200 via-amber-100 to-white" },
      { id: "treino-c-3", title: "Fila e atendimento cordial", category: "Caixa", city: "Caldas Novas", format: "Aula rapida", duration: "50 min", audience: "Mercados e bistro", color: "from-cyan-200 via-sky-100 to-white" },
      { id: "treino-c-4", title: "Conferencia de numerario", category: "Caixa", city: "Morrinhos", format: "Pratica", duration: "1h20", audience: "Caixas de apoio", color: "from-emerald-200 via-cyan-100 to-white" },
      { id: "treino-c-5", title: "Turno de abertura eficiente", category: "Caixa", city: "Goiatuba", format: "Presencial", duration: "45 min", audience: "Padarias e cafeterias", color: "from-amber-200 via-yellow-100 to-white" },
      { id: "treino-c-6", title: "Rotina de temporada", category: "Caixa", city: "Caldas Novas", format: "Oficina", duration: "1h30", audience: "Escalas reforcadas", color: "from-indigo-200 via-sky-100 to-white" },
    ],
  },
  {
    title: "Copeira",
    subtitle: "Copa, reposicao, limpeza leve e suporte continuo.",
    items: [
      { id: "treino-co-1", title: "Cafe da manha sem ruptura", category: "Copeira", city: "Caldas Novas", format: "Presencial", duration: "1h", audience: "Pousadas e hoteis", color: "from-orange-200 via-amber-100 to-white" },
      { id: "treino-co-2", title: "Reposicao e organizacao de copa", category: "Copeira", city: "Rio Quente", format: "Workshop", duration: "1h15", audience: "Equipe de apoio", color: "from-pink-200 via-rose-100 to-white" },
      { id: "treino-co-3", title: "Fluxo de buffet e limpeza leve", category: "Copeira", city: "Caldas Novas", format: "Pratica guiada", duration: "1h30", audience: "Freelas de evento", color: "from-indigo-200 via-blue-100 to-white" },
      { id: "treino-co-4", title: "Padrao visual de reposicao", category: "Copeira", city: "Morrinhos", format: "Aula rapida", duration: "45 min", audience: "Copa de restaurante", color: "from-rose-200 via-orange-100 to-white" },
      { id: "treino-co-5", title: "Ritmo de apoio em salao", category: "Copeira", city: "Rio Quente", format: "Oficina", duration: "1h", audience: "Escalas de fim de semana", color: "from-lime-200 via-emerald-100 to-white" },
      { id: "treino-co-6", title: "Boas praticas de higienizacao", category: "Copeira", city: "Caldas Novas", format: "Presencial", duration: "1h20", audience: "Times de hotelaria", color: "from-cyan-200 via-sky-100 to-white" },
    ],
  },
];

const tabMeta: Record<ActiveTab, { eyebrow: string; title: string }> = {
  professionals: {
    eyebrow: "Profissionais em destaque",
    title: "Escalas por especialidade, com profissionais prontos para entrar na operacao.",
  },
  establishments: {
    eyebrow: "Estabelecimentos contratando",
    title: "Demandas abertas de bares, pousadas e restaurantes que precisam de freelance.",
  },
  trainings: {
    eyebrow: "Treinamentos disponiveis",
    title: "Capacitacoes praticas para elevar o padrao das escalas e acelerar a reposicao.",
  },
};

function matchesDate(text: string, filterDate: string) {
  if (!filterDate) {
    return true;
  }

  const [year, month, day] = filterDate.split("-");
  const normalizedDate = `${day}/${month}`;
  return text.toLowerCase().includes(normalizedDate.toLowerCase()) || text.toLowerCase().includes(year);
}

export default function LandingPage() {
  const [activeTab, setActiveTab] = useState<ActiveTab>("professionals");
  const [filters, setFilters] = useState<FilterState>({
    date: "",
    specialty: specialtyOptions[0],
    city: cityOptions[0],
  });

  const dateInputRef = useRef<HTMLInputElement | null>(null);
  const resultsRef = useRef<HTMLElement | null>(null);
  const rowRefs = useRef<Record<string, HTMLDivElement | null>>({});

  const sections = useMemo(() => {
    const specialtyMatch = (title: string) =>
      filters.specialty === specialtyOptions[0] || title === filters.specialty;

    if (activeTab === "professionals") {
      return professionalSections
        .filter((section) => specialtyMatch(section.title))
        .map((section) => ({
          ...section,
          items: section.items.filter((item) => {
            const cityMatches = filters.city === cityOptions[0] || item.city === filters.city;
            return cityMatches && matchesDate(item.availability, filters.date);
          }),
        }))
        .filter((section) => section.items.length > 0);
    }

    if (activeTab === "establishments") {
      return establishmentSections
        .filter((section) => specialtyMatch(section.title))
        .map((section) => ({
          ...section,
          items: section.items.filter((item) => {
            const cityMatches = filters.city === cityOptions[0] || item.city === filters.city;
            return cityMatches && matchesDate(item.when, filters.date);
          }),
        }))
        .filter((section) => section.items.length > 0);
    }

    return trainingSections
      .filter((section) => specialtyMatch(section.title))
      .map((section) => ({
        ...section,
        items: section.items.filter((item) => {
          const cityMatches = filters.city === cityOptions[0] || item.city === filters.city;
          return cityMatches && matchesDate(item.duration, filters.date);
        }),
      }))
      .filter((section) => section.items.length > 0);
  }, [activeTab, filters]);

  const meta = tabMeta[activeTab];
  const pageBackground =
    activeTab === "professionals"
      ? "bg-[linear-gradient(180deg,#fcfbf8_0%,#fffdfb_20%,#ffffff_42%,#faf8f4_100%)]"
      : activeTab === "establishments"
        ? "bg-[linear-gradient(180deg,#f9fbfc_0%,#fcfeff_20%,#ffffff_42%,#f5f8f9_100%)]"
        : "bg-[linear-gradient(180deg,#fbfafc_0%,#fdfcff_20%,#ffffff_42%,#f7f6fb_100%)]";
  const heroAccent =
    activeTab === "professionals"
      ? "bg-[radial-gradient(circle_at_top_left,_rgba(251,113,133,0.16),_transparent_38%),linear-gradient(135deg,#fffaf6,#ffffff)]"
      : activeTab === "establishments"
        ? "bg-[radial-gradient(circle_at_top_left,_rgba(56,189,248,0.14),_transparent_38%),linear-gradient(135deg,#f7fbfc,#ffffff)]"
        : "bg-[radial-gradient(circle_at_top_left,_rgba(129,140,248,0.14),_transparent_38%),linear-gradient(135deg,#faf8ff,#ffffff)]";
  const registerAccent =
    activeTab === "establishments"
      ? "bg-[radial-gradient(circle_at_top_left,_rgba(56,189,248,0.18),_transparent_40%),linear-gradient(135deg,#f3fcfd,#ffffff)]"
      : "bg-[radial-gradient(circle_at_top_left,_rgba(251,113,133,0.16),_transparent_40%),linear-gradient(135deg,#fff8f4,#ffffff)]";

  function openDatePicker() {
    const input = dateInputRef.current;
    if (!input) {
      return;
    }
    input.focus();
    input.showPicker?.();
  }

  function handlePrimaryAction() {
    resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function scrollRow(key: string, direction: "left" | "right") {
    const row = rowRefs.current[key];
    if (!row) {
      return;
    }
    row.scrollBy({ left: direction === "right" ? 320 : -320, behavior: "smooth" });
  }

  return (
    <main className={`min-h-screen text-slate-900 transition-colors duration-300 ${pageBackground}`}>
      <header className="sticky top-0 z-50 border-b border-black/5 bg-white/85 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[96rem] items-center justify-between gap-6 px-5 py-5 md:px-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-rose-500 to-orange-400 text-lg font-black text-white">
              AC
            </div>
            <div>
              <p className="text-2xl font-bold tracking-tight text-rose-500">app caldas</p>
              <p className="text-xs uppercase tracking-[0.28em] text-slate-400">freelas regionais</p>
            </div>
          </Link>

          <nav className="hidden items-center gap-3 rounded-full border border-black/10 bg-white px-2 py-2 shadow-[0_12px_40px_rgba(15,23,42,0.06)] lg:flex">
            <TabButton active={activeTab === "professionals"} label="Profissionais" description="Perfis disponiveis" onClick={() => setActiveTab("professionals")} />
            <TabButton active={activeTab === "establishments"} label="Estabelecimentos" description="Demandas abertas" onClick={() => setActiveTab("establishments")} />
            <TabButton active={activeTab === "trainings"} label="Treinamentos" description="Capacitacao rapida" onClick={() => setActiveTab("trainings")} />
          </nav>

          <div className="hidden items-center gap-3 md:flex">
            <Link href="/signup/provider" className="rounded-full px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-[#dff6f7]">
              Sou profissional
            </Link>
            <Link href="/signup/company" className="rounded-full border border-[#8fd7dc] bg-[#dff6f7] px-4 py-2 text-sm font-semibold text-[#135d66] shadow-sm transition hover:bg-[#cfeff1] hover:shadow-md">
              Sou estabelecimento
            </Link>
          </div>
        </div>

        <div className="mx-auto max-w-[96rem] px-5 pb-5 md:px-8 lg:hidden">
          <div className="grid grid-cols-3 gap-3">
            <TabButton active={activeTab === "professionals"} label="Profissionais" description="Perfis" onClick={() => setActiveTab("professionals")} />
            <TabButton active={activeTab === "establishments"} label="Estabelecimentos" description="Demandas" onClick={() => setActiveTab("establishments")} />
            <TabButton active={activeTab === "trainings"} label="Treinamentos" description="Cursos" onClick={() => setActiveTab("trainings")} />
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-[96rem] px-5 pb-10 pt-8 md:px-8">
        <div className="rounded-[2.2rem] border border-black/5 bg-white px-5 py-5 shadow-[0_20px_80px_rgba(15,23,42,0.08)] md:px-8 md:py-6">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">{meta.eyebrow}</p>
          <div className="mt-3 grid gap-4 lg:grid-cols-[1.12fr_0.44fr_0.44fr] lg:items-stretch">
            <div>
              <h1 className="max-w-4xl text-3xl font-semibold tracking-tight text-slate-950 md:text-5xl">{meta.title}</h1>
            </div>
            <PromoCard
              title="Cadastros em alta"
              description="Entre na vitrine principal com perfil profissional ou demanda ativa da sua operacao."
              ctaLabel={activeTab === "establishments" ? "Cadastrar estabelecimento" : "Cadastrar profissional"}
              href={activeTab === "establishments" ? "/signup/company" : "/signup/provider"}
              className={registerAccent}
            />
            <PromoCard
              title="Treinamentos express"
              description="Ative trilhas curtas de atendimento, bar, caixa e copa para subir o padrao da escala."
              ctaLabel="Explorar treinamentos"
              href="/dashboard/provider/training"
              className={heroAccent}
            />
          </div>
        </div>

        <section className="mt-4 rounded-[1.5rem] border border-black/6 bg-white/92 p-2 shadow-[0_18px_40px_rgba(15,23,42,0.06)] backdrop-blur">
          <div className="grid gap-2 md:grid-cols-[1.1fr_0.95fr_0.95fr_auto]">
            <FilterField label="Data" helper="Quando" className="rounded-[1rem] md:border-r md:border-black/8" onClick={openDatePicker}>
              <input
                ref={dateInputRef}
                type="date"
                value={filters.date}
                onChange={(event) => setFilters((current) => ({ ...current, date: event.target.value }))}
                className="w-full cursor-pointer bg-transparent text-sm text-slate-700 outline-none"
              />
            </FilterField>

            <FilterField label="Filtro" helper={activeTab === "trainings" ? "Especialidade" : "Funcao"} className="rounded-[1rem] md:border-r md:border-black/8">
              <select
                value={filters.specialty}
                onChange={(event) => setFilters((current) => ({ ...current, specialty: event.target.value }))}
                className="w-full bg-transparent text-sm text-slate-700 outline-none"
              >
                {specialtyOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </FilterField>

            <FilterField label="Localidade" helper="Onde" className="rounded-[1rem]">
              <select
                value={filters.city}
                onChange={(event) => setFilters((current) => ({ ...current, city: event.target.value }))}
                className="w-full bg-transparent text-sm text-slate-700 outline-none"
              >
                {cityOptions.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </FilterField>

            <button
              type="button"
              onClick={handlePrimaryAction}
              className="flex h-12 w-12 items-center justify-center self-center rounded-full bg-[#1aa7b3] text-lg font-semibold text-white shadow-[0_14px_28px_rgba(26,167,179,0.22)] transition hover:scale-[1.02] hover:bg-[#1596a1]"
              aria-label="Ir para resultados"
            >
              +
            </button>
          </div>
        </section>

        <section className="mt-4 overflow-hidden rounded-2xl border border-rose-100 bg-gradient-to-r from-rose-50 via-orange-50 to-amber-50 px-4 py-3 shadow-sm">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <p className="text-sm font-medium text-slate-700">
              Profissionais e estabelecimentos podem se cadastrar em poucos minutos e aparecer aqui com destaque.
            </p>
            <div className="flex flex-wrap gap-2">
              <Link href="/signup/provider" className="rounded-full border border-[#8fd7dc] bg-white px-4 py-2 text-sm font-semibold text-[#135d66] shadow-sm transition hover:bg-[#f3fcfc] hover:shadow-md">
                Cadastrar profissional
              </Link>
              <Link href="/signup/company" className="rounded-full bg-[#1aa7b3] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#1596a1]">
                Cadastrar estabelecimento
              </Link>
            </div>
          </div>
        </section>

        <section ref={resultsRef} className="mt-6 space-y-6">
          {sections.length === 0 ? (
            <div className="rounded-[2rem] border border-dashed border-slate-200 bg-white px-6 py-16 text-center shadow-sm">
              <p className="text-lg font-semibold text-slate-900">Nenhum resultado com esses filtros.</p>
              <p className="mt-2 text-sm text-slate-500">Ajuste a data, a especialidade ou a localidade para ampliar a busca.</p>
            </div>
          ) : null}

          {sections.map((section) => (
            <section key={section.title} className="space-y-3">
              <div className="flex items-end justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-semibold tracking-tight text-slate-950 md:text-[1.9rem]">{section.title}</h2>
                  <p className="mt-1 text-sm text-slate-500">{section.subtitle}</p>
                </div>
                <div className="hidden items-center gap-2 md:flex">
                  <ScrollHint reverse onClick={() => scrollRow(section.title, "left")} />
                  <ScrollHint onClick={() => scrollRow(section.title, "right")} />
                </div>
              </div>

              <div
                ref={(node) => {
                  rowRefs.current[section.title] = node;
                }}
                className="-mx-4 overflow-x-auto px-4 pb-2 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
              >
                <div className="flex min-w-max gap-4">
                  {activeTab === "professionals" &&
                    (section.items as ProfessionalCard[]).map((item) => <ProfessionalListingCard key={item.id} item={item} />)}
                  {activeTab === "establishments" &&
                    (section.items as EstablishmentCard[]).map((item) => <EstablishmentListingCard key={item.id} item={item} />)}
                  {activeTab === "trainings" &&
                    (section.items as TrainingCard[]).map((item) => <TrainingListingCard key={item.id} item={item} />)}
                </div>
              </div>
            </section>
          ))}
        </section>
      </section>
    </main>
  );
}

function TabButton({
  active,
  label,
  description,
  onClick,
}: {
  active: boolean;
  label: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-full px-5 py-3 text-left transition ${
        active
          ? "bg-[#1aa7b3] text-white shadow-[0_12px_28px_rgba(26,167,179,0.22)]"
          : "bg-[#dff6f7] text-[#135d66] hover:bg-[#cfeff1]"
      }`}
    >
      <div className="text-base font-semibold">{label}</div>
      <div className={`text-xs ${active ? "text-white/80" : "text-[#4d7f84]"}`}>{description}</div>
    </button>
  );
}

function FilterField({
  label,
  helper,
  className,
  children,
  onClick,
}: {
  label: string;
  helper: string;
  className?: string;
  children: ReactNode;
  onClick?: () => void;
}) {
  return (
    <label onClick={onClick} className={`bg-white px-4 py-3 ${className ?? ""}`}>
      <span className="block text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-300">{label}</span>
      <span className="mb-1 block text-xs font-medium text-slate-500">{helper}</span>
      {children}
    </label>
  );
}

function ProfessionalListingCard({ item }: { item: ProfessionalCard }) {
  return (
    <article className="w-[248px] flex-none">
      <div className={`relative h-[236px] rounded-[1.55rem] border border-black/5 bg-gradient-to-br ${item.color} p-4 shadow-[0_14px_34px_rgba(15,23,42,0.08)]`}>
        <span className="inline-flex rounded-full bg-white/88 px-3 py-1.5 text-[11px] font-medium text-slate-700 shadow-sm">{item.highlight}</span>
        <div className="absolute inset-x-4 bottom-4 rounded-[1.1rem] bg-white/80 p-4 backdrop-blur">
          <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-400">{item.role}</p>
          <p className="mt-1.5 text-base font-semibold text-slate-900">{item.name}</p>
          <p className="mt-1 text-xs leading-5 text-slate-600">{item.experience}</p>
          <div className="mt-3 space-y-1 border-t border-slate-200/70 pt-3 text-xs text-slate-600">
            <p>{item.city}</p>
            <p>{item.availability}</p>
            <p className="font-medium text-slate-800">{item.price}</p>
          </div>
        </div>
      </div>
    </article>
  );
}

function EstablishmentListingCard({ item }: { item: EstablishmentCard }) {
  return (
    <article className="w-[248px] flex-none">
      <div className={`relative h-[236px] rounded-[1.55rem] border border-black/5 bg-gradient-to-br ${item.color} p-4 shadow-[0_14px_34px_rgba(15,23,42,0.08)]`}>
        <span className="inline-flex rounded-full bg-white/88 px-3 py-1.5 text-[11px] font-medium text-slate-700 shadow-sm">{item.specialty}</span>
        <div className="absolute inset-x-4 bottom-4 rounded-[1.1rem] bg-white/80 p-4 backdrop-blur">
          <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-400">{item.shift}</p>
          <p className="mt-1.5 text-base font-semibold text-slate-900">{item.name}</p>
          <p className="mt-1 text-xs leading-5 text-slate-600">{item.demand}</p>
          <div className="mt-3 space-y-1 border-t border-slate-200/70 pt-3 text-xs text-slate-600">
            <p>{item.city}</p>
            <p>{item.when}</p>
            <p className="font-medium text-slate-800">{item.budget}</p>
          </div>
        </div>
      </div>
    </article>
  );
}

function TrainingListingCard({ item }: { item: TrainingCard }) {
  return (
    <article className="w-[248px] flex-none">
      <div className={`relative h-[236px] rounded-[1.55rem] border border-black/5 bg-gradient-to-br ${item.color} p-4 shadow-[0_14px_34px_rgba(15,23,42,0.08)]`}>
        <span className="inline-flex rounded-full bg-white/88 px-3 py-1.5 text-[11px] font-medium text-slate-700 shadow-sm">{item.category}</span>
        <div className="absolute inset-x-4 bottom-4 rounded-[1.1rem] bg-white/80 p-4 backdrop-blur">
          <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-400">{item.format}</p>
          <p className="mt-1.5 text-base font-semibold text-slate-900">{item.title}</p>
          <p className="mt-1 text-xs leading-5 text-slate-600">{item.audience}</p>
          <div className="mt-3 space-y-1 border-t border-slate-200/70 pt-3 text-xs text-slate-600">
            <p>{item.city}</p>
            <p>{item.duration}</p>
            <p className="font-medium text-slate-800">{item.format}</p>
          </div>
        </div>
      </div>
    </article>
  );
}

function ScrollHint({
  reverse = false,
  onClick,
}: {
  reverse?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="grid h-10 w-10 place-items-center rounded-full border border-black/5 bg-white text-lg text-slate-500 shadow-sm transition hover:bg-slate-50"
      aria-label={reverse ? "Rolar para a esquerda" : "Rolar para a direita"}
    >
      {reverse ? "<" : ">"}
    </button>
  );
}

function PromoCard({
  title,
  description,
  ctaLabel,
  href,
  className,
}: {
  title: string;
  description: string;
  ctaLabel: string;
  href: string;
  className: string;
}) {
  return (
    <aside className={`flex min-h-[156px] flex-col justify-between rounded-[1.6rem] px-5 py-5 ${className}`}>
      <div>
        <p className="text-[10px] font-semibold uppercase tracking-[0.24em] text-slate-400">{title}</p>
        <p className="mt-3 text-sm leading-6 text-slate-700">{description}</p>
      </div>
      <Link
        href={href}
        className="mt-5 inline-flex w-fit rounded-full bg-white/90 px-4 py-2 text-sm font-semibold text-[#135d66] shadow-sm transition hover:bg-white"
      >
        {ctaLabel}
      </Link>
    </aside>
  );
}
