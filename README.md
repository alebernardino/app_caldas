# APP Caldas MVP

Monorepo do MVP web responsivo do marketplace regional **APP Caldas**.

## Stack
- Backend: FastAPI + PostgreSQL + SQLAlchemy 2.0 async + Alembic
- Auth: JWT access/refresh + passlib/bcrypt
- Frontend: Next.js App Router + TypeScript + Tailwind
- Infra: Docker Compose

## Estrutura
- `backend/`: API, regras de negócio, migrações e testes
- `frontend/`: interface web responsiva
- `infra/`: reservado para scripts/artefatos de infraestrutura

## Endpoints MVP (backend)
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /users/me`
- `POST/GET/PUT/DELETE /companies`
- `POST/GET/PUT/DELETE /providers`
- `GET /search/providers` (filtros: função, estrelas/conceito, disponibilidade)
- `POST /bookings`
- `POST /bookings/{id}/accept`
- `POST /bookings/{id}/reject`
- `POST /bookings/{id}/cancel`
- `POST /bookings/{id}/complete`
- `GET /bookings/company/{company_id}?season=true`
- `GET /bookings/provider/{provider_id}`
- `POST /reviews`

## Regras implementadas
- Prestador aceita no máximo **2** agendamentos na mesma semana.
- Em temporada (`season=true`), a listagem da empresa prioriza maior antecedência.
- Conceito `5 estrelas` somente quando `five_star_ratio >= 0.7`.

## Setup rápido
1. Copie variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
2. Crie e ative ambiente virtual Python (desenvolvimento local):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
   No Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r backend/requirements.txt
   ```
2. Suba os serviços:
   ```bash
   docker compose up --build
   ```
3. Acesse:
- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

## Testes backend
```bash
cd backend
pytest -q
```

## Lint
```bash
cd backend && ruff check .
cd frontend && npm run lint
```

## Observações
- Não commitar `.env`.
- Sem pagamentos neste MVP.
- Regra de limite: prestador aceita no máximo 2 agendamentos por semana.

## Publicar no GitHub
1. Inicialize git local (se necessário):
   ```bash
   git init
   git branch -M main
   ```
2. Primeiro commit:
   ```bash
   git add .
   git commit -m "feat: base MVP APP Caldas"
   ```
3. Crie um repositório vazio no GitHub (site ou CLI).
4. Conecte e envie:
   ```bash
   git remote add origin git@github.com:SEU_USUARIO/app-caldas.git
   git push -u origin main
   ```
