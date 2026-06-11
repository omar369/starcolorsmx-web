# StarColors Servicios — App Overview

> Portal web para una tienda de pinturas local (StarColors MX). Monorepo con frontend en Astro + Svelte y backend en FastAPI + SQLite/Neon.
> Última revisión: Junio 2026.

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
| Contenedor | Docker (`Dockerfile` + `railway.json`) |

### Estructura interna (`app/`)

```
app/
├── api/
│   └── v1/
│       ├── auth/         # Registro, login, /me
│       │   ├── models.py
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   ├── security.py
│       │   └── service.py
│       ├── raffle/       # Sorteos, boletos, números
│       │   ├── models.py
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   ├── seed.py
│       │   └── service.py
│       ├── quotes/       # Cotizaciones con PDF
│       │   ├── catalog.py    # Catálogo de opciones y ajustes de precio
│       │   ├── pdf.py        # Generación de PDF con WeasyPrint/reportlab
│       │   ├── pricing.py    # Lógica de cálculo de precio
│       │   ├── repository.py # Persistencia de cotizaciones
│       │   ├── routes.py
│       │   ├── schemas.py
│       │   └── service.py
│       ├── health/       # Health check
│       └── routes.py     # Router principal v1
├── core/
│   └── config.py         # Settings (env vars, CORS, etc.)
├── db/
│   ├── base.py
│   ├── models.py         # Modelos Quote + QuoteRequest (SQLAlchemy)
│   └── session.py        # Sesión de DB
├── static/
└── main.py               # Entry point FastAPI + CORS
```

### Endpoints principales

| Módulo | Ruta base | Notas |
|---|---|---|
| Auth | `/api/v1/auth` | Register, login, `/me` con JWT Bearer |
| Raffle | `/api/v1/raffle` | Status, branches, tickets, números, mis entradas |
| Quotes | `/api/v1/quotes` | GET `/options`, POST `/`, POST `/pdf` (descarga PDF) |
| Health | `/health` | Health check simple |

### Módulo Quotes — Detalle

El módulo de cotizaciones es **funcional completo**. Incluye:
- **`catalog.py`**: Catálogo estático de opciones (13 productos de pintura, 7 intensidades de color, estados de México con factor de ajuste geográfico, condiciones de trabajo, etc.)
- **`pricing.py`**: Cálculo de precio base por m² con ajustes aditivos por cada condición.
- **`pdf.py`**: Generación de PDF descargable con el resultado de la precotización.
- **`repository.py`**: Guarda cada cotización generada en la tabla `quotes` y registra en `quote_results` para rate-limiting por IP/UA.
- **Schemas**: Validación estricta con Pydantic (14+ campos, field validators por catálogo).

### Modelos de base de datos

| Tabla | Descripción |
|---|---|
| `quotes` | Cotizaciones guardadas: nombre, contacto, ubicación, producto, precio estimado, JSON completo de inputs y resultado |
| `quote_results` | Registro de peticiones para rate-limiting: contact_value, ip_hash, ua_hash |
| (Raffle) | Boletos, sucursales, números de rifa, usuarios vinculados a sorteos |

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
| Componentes interactivos | Svelte 5 (runes: `$state`, `$props`, `$derived`) |
| CSS | TailwindCSS v4 + CSS vanilla scoped |
| UI primitivos | shadcn/ui (Svelte) + bits-ui + lucide-svelte (`@lucide/svelte`) |
| Carousel | embla-carousel-svelte v8 |
| Fuente | Nunito Sans Variable (`@fontsource-variable`) |
| Hosting | Cloudflare Pages (vía `wrangler.jsonc`) |
| Build tool | Vite (via Astro) |
| Node requerido | ≥22.12.0 |

### Alias de paths
- `$lib` → `src/lib`

### Estructura de `src/`

```
src/
├── components/
│   ├── auth/
│   │   └── AuthForm.svelte           # Formulario de registro/login
│   ├── quotes/
│   │   ├── PartnerQuoteWizard.svelte # Wizard cotizador (9 pasos, completo)
│   │   ├── types.ts                  # Tipos TS: QuoteForm, QuoteOptions, QuoteResult
│   │   └── steps/                    # Pasos individuales del wizard
│   │       ├── IntroStep.svelte
│   │       ├── ProjectStep.svelte
│   │       ├── PaintProductStep.svelte
│   │       ├── SurfaceStep.svelte
│   │       ├── WorkConditionsStep.svelte
│   │       ├── LocationStep.svelte
│   │       ├── ContactStep.svelte
│   │       ├── ReviewSubmitStep.svelte
│   │       └── QuoteSuccessStep.svelte
│   ├── raffle/
│   │   ├── RaffleTool.svelte         # Orchestrator del flujo de rifa (6 pasos)
│   │   ├── BranchStep.svelte         # Paso 1: selección de sucursal
│   │   ├── CodesStep.svelte          # Paso 2: ingreso de códigos de boleto
│   │   ├── ValidationStep.svelte     # Paso 3: resultado de validación de boletos
│   │   ├── NumbersStep.svelte        # Paso 4: selección de números disponibles
│   │   ├── ConfirmStep.svelte        # Paso 5: confirmación
│   │   ├── SuccessStep.svelte        # Paso 6: éxito
│   │   └── StepIndicator.svelte      # Indicador de progreso de pasos
│   ├── site/
│   │   ├── Header.astro              # Header estático simple (legacy, sin uso activo)
│   │   ├── Footer.astro              # Footer (contenido mínimo)
│   │   ├── Hero.astro                # Sin implementar (archivo vacío)
│   │   └── ServiceCard.astro         # Sin implementar (archivo vacío)
│   └── user/
│       └── UserHub.svelte            # Hub/perfil del cliente autenticado
├── layouts/
│   ├── BaseLayout.astro              # Layout principal (incluye Navbar de $lib)
│   └── QuoteLayout.astro             # Layout especial para cotizador (dark, fullscreen)
├── lib/
│   ├── auth.ts                       # Lógica de auth: login, register, sesión
│   ├── raffle.ts                     # Lógica de sorteo: fetch, validar, confirmar
│   └── components/
│       ├── MainBanner.svelte         # Banner del sorteo: animaciones CSS, premios flotantes
│       ├── LandingCarousel.svelte    # Carousel (embla) con cards de video/imagen para secciones
│       ├── Navbar.svelte             # Navbar sticky con SVG wave + mobile menu
│       ├── pages/
│       │   ├── ServiceCard.svelte    # Tarjeta de servicio con themeColor dinámico
│       │   ├── ProductCard.svelte    # Tarjeta de producto con tabla de precios e intensidades
│       │   ├── AnimatedTestimonials.svelte  # Stack de imágenes con transición y controles
│       │   └── AnimatedText.svelte   # Texto con animación de entrada (ink reveal)
│       └── ui/                       # Componentes shadcn generados
│           ├── button/
│           ├── card/
│           ├── carousel/
│           ├── input/
│           ├── label/
│           ├── navigation-menu/
│           └── tabs/
└── pages/
    ├── index.astro                   # Landing: MainBanner + LandingCarousel
    ├── hub.astro                     # Portal del cliente (auth-gated, layout propio sin Navbar)
    ├── inscribete.astro              # Página de registro/login
    ├── cotizador.astro               # Cotizador completo (QuoteLayout + PartnerQuoteWizard)
    ├── productos.astro               # Catálogo de productos (BaseLayout + productos/+page.svelte)
    ├── servicios.astro               # Servicios (BaseLayout + servicios/+page.svelte)
    ├── sobre-nosotros.astro          # Sobre nosotros (BaseLayout + sobre-nosotros/+page.svelte)
    ├── contacto.astro                # Contacto / sucursales (BaseLayout + contacto/+page.svelte)
    ├── productos/
    │   └── +page.svelte              # Listado de 6 productos con ProductCard
    ├── servicios/
    │   └── +page.svelte              # 4 servicios de pintura + 3 impermeabilizantes con ServiceCard
    ├── sobre-nosotros/
    │   └── +page.svelte              # Historia de la empresa con AnimatedText + ink reveal
    ├── contacto/
    │   └── +page.svelte              # 3 sucursales con AnimatedTestimonials
    └── tools/
        └── raffle.astro              # Flujo completo del sorteo
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

### 3. Cotizador (`/cotizador`)
Wizard de 9 pasos orquestado por `PartnerQuoteWizard.svelte`:
1. **IntroStep** — Pantalla de bienvenida
2. **ProjectStep** — Tipo de inmueble, ubicación del trabajo, m², tipo de servicio
3. **PaintProductStep** — Producto y intensidad de color
4. **SurfaceStep** — Estado de superficie, textura, preparación, protección de área
5. **WorkConditionsStep** — Dificultad de avance, ocupación, riesgo de altura, horario
6. **LocationStep** — Estado, ciudad, código postal
7. **ContactStep** — Nombre, método de contacto (WhatsApp/email), datos
8. **ReviewSubmitStep** — Resumen de inputs + botón de envío
9. **QuoteSuccessStep** — Resultado con precio estimado + descarga de PDF

El cotizador usa su propio `QuoteLayout` (dark fullscreen, sin Navbar principal). La URL de la API se toma de `PUBLIC_API_BASE_URL` o fallback a `localhost:8000`.

### 4. Páginas de contenido
- **`/productos`** — Catálogo de 6 pinturas StarColors propias (VIN J, VIN I, VIN M, VIN R, VIN E Mate, VIN E Satín) con precios por medida, cobertura, acabado e intensidades disponibles.
- **`/servicios`** — 4 servicios de aplicación de pintura (AP Vin R/E/Es/Pro) + 3 de impermeabilizante (Acristar 4/6/8 años). Incluye descripción de lo que cubre el servicio básico y los servicios con costo adicional.
- **`/sobre-nosotros`** — Historia de la empresa desde 1994, con animación ink-reveal en SVG y texto animado por línea (AnimatedText).
- **`/contacto`** — 3 sucursales (Burócrata, El Pueblito, Constituyentes) con fotos, dirección, horario y teléfono usando `AnimatedTestimonials`.

---

## Design System

### Paleta de colores de marca
| Token | Valor | Uso |
|---|---|---|
| Verde oscuro | `#006b3f` | Color primario (banner, botones de acción) |
| Verde claro acento | `#b4f0b0` | Eyebrows/labels sobre verde |
| Naranja StarColors | `#e67a25` / `#d96f20` | Navbar wave, CTAs, acentos en carousel |
| Crema/fondo cálido | `#f3eadb` | Fondo de páginas públicas, Navbar bg |
| Oscuro casi negro | `#172033` | Fondo del cotizador (QuoteLayout) |
| Hub claro | `#DBD3C6` | Fondo del portal de clientes |
| Blanco | `#ffffff` | Texto sobre oscuro, tarjetas |

### Tipografía
- **Display**: Georgia / Times New Roman (serif) — headings del hero banner
- **UI**: Nunito Sans Variable — todo el resto (via `@fontsource-variable`)
- **Cotizador**: Inter, ui-sans-serif, system-ui (fallback del QuoteLayout)

### Layout patterns
- `width: min(100% - 1.5rem, Npx)` para centrado con gutters
- `clamp()` para tamaños fluidos (fuente del h1, padding)
- `sticky top-0 z-50` en Navbar (en BaseLayout)
- Hub y cotizador tienen layouts propios (no usan BaseLayout)

### Temas
- `global.css` define tokens oklch para light/dark mode (TW v4 custom vars)
- Las páginas públicas usan fondo crema `#f3eadb` via `is:global body` en cada `.astro`
- El Hub usa fondo `#DBD3C6` con header propio inline en `hub.astro`
- El cotizador usa dark theme en `QuoteLayout.astro` (radial gradient + linear)

### Animaciones notables
- **MainBanner**: `fade-in`, `slide-up`, `pop-in` para premios flotantes (balón × 3, pantalla)
- **LandingCarousel**: hover `scale-105` + transición de overlay glassmorphism
- **QuoteWizard progress dots**: dot activo ensancha (`1.7rem`) en transición CSS
- **AnimatedText**: revelación de texto con animación inkdrop/clip-path en `sobre-nosotros`
- **AnimatedTestimonials**: stack de imágenes con rotaciones aleatorias, transición `fly` Svelte

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
| Navbar | ✅ Implementada |
| Landing page (banner + carousel) | ✅ Funcional con `MainBanner` + `LandingCarousel` |
| Cotizador automático (9 pasos) | ✅ Funcional — calcula precio, guarda en DB, genera PDF descargable |
| Catálogo de Productos (`/productos`) | ✅ 6 productos con precios, cobertura, intensidades |
| Servicios (`/servicios`) | ✅ 4 pintura + 3 impermeabilizante con descripción detallada |
| Sobre Nosotros (`/sobre-nosotros`) | ✅ Historia con animación ink-reveal + AnimatedText |
| Contacto / Sucursales (`/contacto`) | ✅ 3 sucursales con fotos y datos reales |
| Footer | 🚧 Archivo creado (`Footer.astro`), contenido mínimo |
| `Header.astro`, `Hero.astro` (legacy) | 🚧 Archivos existentes, sin uso activo en rutas actuales |
| Dark mode sistema | 🚧 Tokens definidos en global.css pero no integrado globalmente |

---

## Notas para el desarrollo del frontend

- **Svelte 5 runes**: El proyecto usa `$state()`, `$props()`, `$derived()`. **No usar el viejo `let` reactivo ni `export let`** (excepto en componentes de cotizador que aún usan `export let`/`bind:`).
- **TailwindCSS v4**: Sin `tailwind.config.js`, toda la config va en `global.css` via `@theme` / `@custom-variant`.
- **No usar `on:click` en Svelte 5**: usar `onclick={fn}` directamente (event handlers como props). El `PartnerQuoteWizard` aún usa `on:click`, revisar al refactorizar.
- **shadcn/ui**: Primitivos disponibles en `src/lib/components/ui/` (button, card, carousel, input, label, navigation-menu, tabs). Revisar antes de crear componentes nuevos.
- **`@lucide/svelte`** (devDep): iconos. Importar desde `@lucide/svelte`.
- **bits-ui** (devDep): disponible.
- **`client:load`**: Todos los componentes Svelte interactivos se montan con esta directiva en las páginas `.astro`.
- **Alias**: importar desde `$lib/...` en lugar de rutas relativas largas.
- **Rutas de páginas**: El patrón actual mezcla archivos `.astro` wrapper + `+page.svelte` como componente para las páginas de contenido (productos, servicios, sobre-nosotros, contacto). Esto permite usar `client:load` fácilmente desde el wrapper.
- **Cotizador y Hub**: tienen `QuoteLayout` y layout inline propios respectivamente — **no** usan `BaseLayout` ni la Navbar principal.
