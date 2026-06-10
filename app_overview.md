# StarColors Servicios — App Overview

> Portal web moderno para una tienda de pinturas local (StarColors MX). Monorepo con frontend en Astro + Svelte y backend en FastAPI + SQLite/Neon.

---

## Estructura del Monorepo

```
starcolors_servicios/
├── apps/
│   ├── api/          # Backend FastAPI (Python)
│   └── web/          # Frontend Astro + Svelte
└── app_overview.md
```

---

## `apps/api` — Backend (FastAPI)

### Stack
| Capa | Tecnología |
|---|---|
| Framework | FastAPI |
| Base de datos local | SQLite (`dev.db`) |
| Base de datos en la nube | Neon (PostgreSQL serverless) |
| Hosting | Railway |
| Migraciones | Alembic |
| Linting | Ruff |

### Estructura interna (`app/`)

```
app/
├── api/
│   └── v1/
│       ├── auth/       # Registro, login, /me
│       ├── raffle/     # Sorteos, boletos, números
│       ├── quotes/     # Cotizaciones
│       ├── health/     # Health check
│       └── routes.py   # Router principal v1
├── core/
│   └── config.py       # Settings (env vars, CORS, etc.)
├── db/                 # Modelos SQLAlchemy, sesión
├── static/
└── main.py             # Entry point FastAPI + CORS
```

### Endpoints principales

| Módulo | Ruta base | Notas |
|---|---|---|
| Auth | `/api/v1/auth` | Register, login, `/me` con JWT Bearer |
| Raffle | `/api/v1/raffle` | Status, branches, tickets, números, mis entradas |
| Quotes | `/api/v1/quotes` | Cotizaciones (WIP) |
| Health | `/health` | Health check simple |

### Auth & Sesión
- JWT Bearer tokens
- Sesión del lado cliente: 24 h, guardada en `localStorage` (`starcolors_access_token`, `starcolors_user`, `starcolors_session_expires_at`)
- `logoutUser()` limpia los 3 keys automáticamente

---

## `apps/web` — Frontend (Astro + Svelte)

### Stack
| Capa | Tecnología |
|---|---|
| Framework | Astro 6 |
| Componentes interactivos | Svelte 5 (runes: `$state`) |
| CSS | TailwindCSS v4 + CSS vanilla scoped |
| UI primitivos | shadcn/ui (Svelte) + bits-ui + lucide-svelte |
| Fuente | Nunito Sans Variable (`@fontsource-variable`) |
| Hosting | Cloudflare Pages |
| Build tool | Vite (via Astro) |

### Alias de paths
- `$lib` → `src/lib`

### Estructura de `src/`

```
src/
├── components/
│   ├── auth/
│   │   └── AuthForm.svelte       # Formulario de registro/login
│   ├── raffle/
│   │   ├── RaffleTool.svelte     # Orchestrator del flujo de rifa (6 pasos)
│   │   ├── BranchStep.svelte     # Paso 1: selección de sucursal
│   │   ├── CodesStep.svelte      # Paso 2: ingreso de códigos de boleto
│   │   ├── ValidationStep.svelte # Paso 3: resultado de validación de boletos
│   │   ├── NumbersStep.svelte    # Paso 4: selección de números disponibles
│   │   ├── ConfirmStep.svelte    # Paso 5: confirmación
│   │   ├── SuccessStep.svelte    # Paso 6: éxito
│   │   └── StepIndicator.svelte  # Indicador de progreso de pasos
│   ├── site/
│   │   ├── Header.astro          # Header estático simple (legacy)
│   │   ├── Footer.astro          # Footer
│   │   ├── Hero.astro            # Hero section (WIP)
│   │   └── ServiceCard.astro     # Tarjeta de servicio (WIP)
│   └── user/
│       └── UserHub.svelte        # Hub/perfil del cliente autenticado
├── layouts/
│   ├── BaseLayout.astro          # Layout principal (incluye Navbar)
│   └── QuoteLayout.astro         # Layout para cotizaciones
├── lib/
│   ├── auth.ts                   # Lógica de auth: login, register, sesión
│   ├── raffle.ts                 # Lógica de sorteo: fetch, validar, confirmar
│   └── components/
│       ├── Navbar.svelte         # Navbar sticky con SVG wave + mobile menu
│       └── ui/                   # Componentes shadcn generados
├── pages/
│   ├── index.astro               # Landing: hero del sorteo de temporada
│   ├── hub.astro                 # Portal del cliente (auth-gated)
│   ├── inscribete.astro          # Página de registro/login
│   ├── cotizador.astro           # Cotizador (WIP)
│   ├── admin/                    # Sección admin (WIP)
│   ├── app/                      # Sub-rutas de app (WIP)
│   └── tools/
│       └── raffle.astro          # Flujo completo del sorteo
└── styles/
    └── global.css                # Tokens de diseño Tailwind v4 + dark mode
```

---

## Flujos de usuario

### 1. Sorteo (Rifa)
```
/ (landing) → /inscribete → /hub → /tools/raffle
```
Flujo en `/tools/raffle` (6 pasos orquestados por `RaffleTool.svelte`):
1. **BranchStep** — El usuario elige su sucursal
2. **CodesStep** — Ingresa los códigos de sus boletos físicos (hasta 10)
3. **ValidationStep** — Se muestran qué boletos fueron aceptados/rechazados
4. **NumbersStep** — Elige un número de rifa por cada boleto aceptado
5. **ConfirmStep** — Revisión antes de confirmar
6. **SuccessStep** — Confirmación exitosa, muestra los números asignados

### 2. Auth
- **Registro** y **Login** en `AuthForm.svelte` con toggle de modo
- Al autenticarse, redirige a `/hub` (o al `?redirect=` param)
- `UserHub.svelte` verifica sesión en `onMount`, redirige a `/inscribete` si no hay token

---

## Design System

### Paleta de colores de marca
| Token | Valor | Uso |
|---|---|---|
| Verde oscuro | `#006b3f` | Color primario (banner, botones de acción) |
| Verde claro acento | `#b4f0b0` | Eyebrows/labels sobre verde |
| Naranja StarColors | `#e67a25` / `#d96f20` | Navbar wave, CTAs |
| Crema/fondo cálido | `#f3eadb` | Navbar bg, hero shell |
| Oscuro casi negro | `#080808` | Fondo de páginas auth-gated (hub, raffle) |
| Blanco | `#ffffff` | Texto sobre oscuro, tarjetas |

### Tipografía
- **Display**: Georgia / Times New Roman (serif) — headings del hero
- **UI**: Nunito Sans Variable — todo el resto (via `@fontsource-variable`)
- **Fallback global**: Inter, ui-sans-serif, system-ui

### Layout patterns
- `width: min(100% - 1.5rem, Npx)` para centrado con gutters
- Grid con `clamp()` para fluidos
- `sticky top-0 z-50` en Navbar

### Temas
- `global.css` define tokens oklch para light/dark mode (TW v4 custom vars)
- El dark mode actual es opt-in via `.dark` class
- Las páginas de hub/rifa usan fondo oscuro `#080808` hardcoded (no siguen el sistema de tokens todavía)

---

## Variables de entorno

### Web (`apps/web/.env`)
```env
PUBLIC_API_BASE_URL=https://...railway.app   # URL del backend en Railway
```

### API (`apps/api/.env`)
```env
APP_NAME=...
APP_ENV=production
DEBUG=false
API_VERSION=...
DATABASE_URL=...                # SQLite local o Neon PostgreSQL
SECRET_KEY=...
BACKEND_CORS_ORIGINS=[...]
```

---

## Estado actual del proyecto

| Feature | Estado |
|---|---|
| Auth (registro + login) | ✅ Funcional y en producción |
| Portal de clientes (Hub) | ✅ Funcional y en producción |
| Sistema de rifas (6 pasos) | ✅ Funcional y en producción |
| Navbar | ✅ Implementada, pendiente mejoras de UX |
| Landing page | 🔨 Borrador funcional, requiere imágenes reales |
| Cotizador | 🚧 Estructura creada, sin lógica |
| Admin panel | 🚧 Carpeta creada, sin implementar |
| Footer | 🚧 Archivo vacío |
| Hero / ServiceCard | 🚧 Archivos vacíos |
| Dark mode sistema | 🚧 Tokens definidos pero no integrado en todas las páginas |

---

## Notas para el desarrollo del frontend

- **Svelte 5 runes**: El proyecto usa `$state()` en lugar del viejo `let` reactivo. Usar `$props()`, `$derived()`, etc.
- **TailwindCSS v4**: Sin `tailwind.config.js`, toda la config va en `global.css` via `@theme` / `@custom-variant`.
- **No usar `on:click` en Svelte 5**: usar `onclick={fn}` directamente (event handlers como props).
- **shadcn/ui**: Hay primitivos instalados bajo `src/lib/components/ui/`. Revisar antes de crear componentes nuevos.
- **bits-ui + lucide-svelte**: disponibles como devDependencies, usando iconos `Menu`, `X` en Navbar.
- **`client:load`**: Todos los componentes Svelte interactivos se montan con esta directiva en las páginas `.astro`.
- **Alias**: importar desde `$lib/...` en lugar de rutas relativas largas.
