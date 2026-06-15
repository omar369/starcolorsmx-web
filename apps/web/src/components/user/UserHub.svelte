<script lang="ts">
  import { onMount } from "svelte";
  import {
    getCurrentUser,
    getStoredUser,
    logoutUser,
    type AuthUser,
  } from "../../lib/auth";
  import {
    getRaffleStatus,
    getMyRaffleEntries,
    type RaffleStatus,
    type RaffleEntry,
  } from "../../lib/raffle";
  import * as Card from "$lib/components/ui/card/index.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import {
    User,
    Ticket,
    Award,
    LogOut,
    ArrowRight,
    HelpCircle,
    Phone,
    Info,
    FileText,
    Download,
    Mail,
    Calendar,
    Send,
  } from "@lucide/svelte";
  import { getToken } from "../../lib/auth";

  let user = $state<AuthUser | null>(null);
  let loading = $state(true);

  let raffle = $state<RaffleStatus | null>(null);
  let myEntries = $state<RaffleEntry[]>([]);
  let loadingRaffle = $state(true);

  let quotes = $state<any[]>([]);
  let loadingQuotes = $state(true);
  let sendingEmailId = $state<number | null>(null);
  let emailStatusMsg = $state<string>("");
  let emailStatusType = $state<"success" | "error" | "">("");
  let customEmailDest = $state<string>("");
  let activeEmailModalId = $state<number | null>(null);

  onMount(async () => {
    const storedUser = getStoredUser();
    if (storedUser) user = storedUser;

    try {
      const currentUser = await getCurrentUser();
      if (!currentUser) {
        window.location.href = "/inscribete?redirect=/hub";
        return;
      }
      user = currentUser;
    } catch {
      logoutUser();
      window.location.href = "/inscribete";
      return;
    }

    try {
      // Intentar cargar sorteo y entradas de forma segura sin romper el portal entero
      raffle = await getRaffleStatus();
      myEntries = await getMyRaffleEntries();
    } catch (err) {
      console.warn("Sorteo no disponible o error de comunicación:", err);
      raffle = null;
      myEntries = [];
    }

    try {
      const token = getToken();
      if (token) {
        const url = apiUrl(`/api/v1/quotes/my`);
        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          quotes = await response.json();
        }
      }
    } catch (err) {
      console.error("Error al cargar cotizaciones:", err);
    } finally {
      loading = false;
      loadingRaffle = false;
      loadingQuotes = false;
    }
  });

  async function sendQuoteByEmail(quoteId: number, defaultEmail: string) {
    sendingEmailId = quoteId;
    emailStatusMsg = "";
    emailStatusType = "";

    const emailDest = customEmailDest.trim() || defaultEmail;
    if (!emailDest || !emailDest.includes("@")) {
      emailStatusMsg = "Por favor ingresa un correo válido.";
      emailStatusType = "error";
      sendingEmailId = null;
      return;
    }

    try {
      const token = getToken();
      const url = apiUrl(`/api/v1/quotes/${quoteId}/send-email`);
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ email: emailDest }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Error al enviar el correo.");
      }

      emailStatusMsg = "¡Correo enviado exitosamente con tu PDF!";
      emailStatusType = "success";
      customEmailDest = "";
      setTimeout(() => {
        activeEmailModalId = null;
        emailStatusMsg = "";
        emailStatusType = "";
      }, 3000);
    } catch (err: any) {
      emailStatusMsg = err.message || "No se pudo enviar el correo.";
      emailStatusType = "error";
    } finally {
      sendingEmailId = null;
    }
  }

  function apiUrl(path: string) {
    const configuredBaseUrl =
      import.meta.env.PUBLIC_API_BASE_URL?.trim() ||
      import.meta.env.PUBLIC_API_URL?.trim();
    const baseUrl =
      configuredBaseUrl && configuredBaseUrl.length > 0
        ? configuredBaseUrl
        : "http://localhost:8000";

    const normalizedBaseUrl = baseUrl.replace(/\/+$/, "");
    const normalizedPath = path.startsWith("/") ? path : `/${path}`;

    // Avoid double /api/v1 if the base URL already ends with it
    if (
      normalizedBaseUrl.endsWith("/api/v1") &&
      normalizedPath.startsWith("/api/v1")
    ) {
      return `${normalizedBaseUrl}${normalizedPath.slice("/api/v1".length)}`;
    }

    return `${normalizedBaseUrl}${normalizedPath}`;
  }

  function goToRaffle() {
    window.location.href = "/tools/raffle";
  }

  function logout() {
    logoutUser();
    window.location.href = "/inscribete";
  }

  // Helper para obtener las iniciales del nombre
  function getInitials(name: string) {
    if (!name) return "U";
    return name
      .split(" ")
      .slice(0, 2)
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  }
</script>

{#if loading}
  <div
    class="flex h-full min-h-[50vh] flex-col items-center justify-center gap-4"
  >
    <div
      class="h-10 w-10 animate-spin rounded-full border-4 border-[#e67a25]/20 border-t-[#e67a25]"
    ></div>
    <p
      class="text-[#e67a25] font-black tracking-widest uppercase text-xs animate-pulse"
    >
      Cargando tu portal de cliente...
    </p>
  </div>
{:else if user}
  <div
    class="w-full space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500"
  >
    <!-- TARJETA DE BIENVENIDA (PERFIL) -->
    <Card.Root
      class="border-0 shadow-xl rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm"
    >
      <div
        class="p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6"
      >
        <div
          class="flex flex-col sm:flex-row items-center gap-5 text-center sm:text-left"
        >
          <!-- Avatar de cliente premium -->
          <div
            class="relative flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-tr from-[#e67a25] to-[#f59e0b] text-white font-black text-2xl shadow-md border-2 border-white"
          >
            {getInitials(user.full_name)}
            <div
              class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"
            ></div>
          </div>
          <div>
            <div
              class="flex flex-wrap items-center justify-center sm:justify-start gap-2 mb-1.5"
            >
              <h1
                class="text-2xl sm:text-3xl font-black text-[#111111] leading-none"
              >
                {user.full_name}
              </h1>
              <span
                class="inline-flex items-center rounded-full bg-[#e67a25]/10 px-2.5 py-0.5 text-xs font-black uppercase tracking-wider text-[#e67a25]"
              >
                Cliente StarColors
              </span>
            </div>
            <p class="text-sm text-gray-500 font-medium">
              {user.email} • {user.phone || "Sin teléfono registrado"}
            </p>
          </div>
        </div>

        <Button
          variant="outline"
          onclick={logout}
          class="rounded-xl border-gray-200 text-gray-600 hover:bg-red-50 hover:text-red-600 hover:border-red-100 font-bold transition-all flex items-center gap-2 h-11 px-5"
        >
          <LogOut class="h-4 w-4" />
          Cerrar sesión
        </Button>
      </div>
    </Card.Root>

    <!-- GRID DE ESTADÍSTICAS DEL CLIENTE -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
      <!-- Stat 1: Boletos -->
      <Card.Root
        class="border-0 shadow-md rounded-2xl bg-white/95 overflow-hidden"
      >
        <Card.Content class="p-5 flex items-center gap-4">
          <div
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#e67a25]/10 text-[#e67a25]"
          >
            <Ticket class="h-6 w-6" />
          </div>
          <div>
            <p
              class="text-xs font-black text-gray-400 uppercase tracking-widest"
            >
              Mis Boletos
            </p>
            <p class="text-2xl font-black text-[#111111] mt-0.5">
              {myEntries.length}
              {myEntries.length === 1 ? "número" : "números"}
            </p>
            {#if myEntries.length > 0}
              <div class="flex flex-wrap gap-1 mt-1.5 max-w-[180px]">
                {#each myEntries as entry}
                  <span
                    class="inline-flex items-center justify-center px-2 py-0.5 rounded-md bg-[#e67a25]/10 text-[0.7rem] font-black text-[#e67a25]"
                  >
                    #{entry.selected_number}
                  </span>
                {/each}
              </div>
            {/if}
          </div>
        </Card.Content>
      </Card.Root>

      <!-- Stat 2: Puntos -->
      <Card.Root
        class="border-0 shadow-md rounded-2xl bg-white/95 overflow-hidden"
      >
        <Card.Content class="p-5 flex items-center gap-4">
          <div
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#e67a25]/10 text-[#e67a25]"
          >
            <Award class="h-6 w-6" />
          </div>
          <div>
            <p
              class="text-xs font-black text-gray-400 uppercase tracking-widest"
            >
              Mis Puntos
            </p>
            <p class="text-2xl font-black text-[#111111] mt-0.5">0 pts</p>
          </div>
        </Card.Content>
      </Card.Root>

      <!-- Stat 3: Nivel -->
      <Card.Root
        class="border-0 shadow-md rounded-2xl bg-white/95 overflow-hidden"
      >
        <Card.Content class="p-5 flex items-center gap-4">
          <div
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#e67a25]/10 text-[#e67a25]"
          >
            <User class="h-6 w-6" />
          </div>
          <div>
            <p
              class="text-xs font-black text-gray-400 uppercase tracking-widest"
            >
              Nivel Cliente
            </p>
            <p class="text-2xl font-black text-[#111111] mt-0.5">Socio SC</p>
          </div>
        </Card.Content>
      </Card.Root>
    </div>

    <!-- SECCIÓN PRINCIPAL: SORTEOS Y HERRAMIENTAS -->
    <div class="grid gap-8 lg:grid-cols-3">
      <!-- COLUMNA IZQUIERDA Y CENTRAL: SORTEOS Y BOLETOS (2/3) -->
      <div class="lg:col-span-2 space-y-8">
        <!-- CARD DE SORTEO ACTIVO -->
        <Card.Root
          class="border-0 shadow-lg rounded-2xl bg-white overflow-hidden relative"
        >
          <!-- Detalle de color naranja sutil arriba -->
          <div
            class="h-1.5 w-full bg-gradient-to-r from-[#e67a25] to-[#f59e0b]"
          ></div>

          <Card.Header
            class="pb-3 flex flex-row items-start justify-between gap-4"
          >
            <div>
              <Card.Description
                class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1"
              >
                Dinámica de temporada
              </Card.Description>
              <Card.Title
                class="text-2xl sm:text-3xl font-black text-[#111111] leading-tight"
              >
                {#if raffle}
                  {raffle.prize_title ?? raffle.title}
                {:else}
                  Próximo sorteo de temporada
                {/if}
              </Card.Title>
            </div>
            {#if raffle}
              <span
                class="inline-flex items-center rounded-full bg-green-50 px-2.5 py-0.5 text-xs font-bold text-green-700 border border-green-200"
              >
                Activo
              </span>
            {/if}
          </Card.Header>

          <Card.Content class="pb-6">
            {#if raffle}
              <p class="text-sm text-gray-600 mb-6 leading-relaxed">
                ¡Compra y gana! Si tienes boletos físicos con códigos
                promocionales de StarColors, regístralos ahora y selecciona tus
                números de la suerte antes de que se agoten.
              </p>

              <div
                class="bg-gray-50/80 rounded-xl p-5 border border-gray-100 mb-6 space-y-3"
              >
                <p
                  class="text-xs font-black text-[#111111] uppercase tracking-wider mb-1"
                >
                  Pasos para participar:
                </p>
                {#each ["Elige la sucursal de compra e ingresa tus códigos.", "El sistema validará si tus boletos están disponibles.", "Elige tus números de la suerte en el tablero.", "Una vez confirmados, aparecerán registrados en tu cuenta."] as instruccion, i}
                  <div
                    class="flex items-center gap-3 text-sm text-[#444] font-medium"
                  >
                    <span
                      class="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-[#e67a25]/15 text-[#e67a25] text-[0.7rem] font-bold"
                    >
                      {i + 1}
                    </span>
                    {instruccion}
                  </div>
                {/each}
              </div>

              <Button
                onclick={goToRaffle}
                class="w-full sm:w-auto rounded-xl bg-[#111111] hover:bg-[#e67a25] text-white font-black uppercase tracking-wider px-8 h-12 shadow-md hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2"
              >
                Elegir mis números
                <ArrowRight class="h-4 w-4" />
              </Button>
            {:else}
              <div
                class="flex flex-col items-center justify-center py-6 text-center"
              >
                <div
                  class="flex h-16 w-16 items-center justify-center rounded-full bg-gray-50 text-gray-400 mb-4 border border-dashed border-gray-200"
                >
                  <Ticket class="h-8 w-8" />
                </div>
                <h3 class="text-lg font-black text-[#111111] mb-1">
                  Sin sorteos activos por ahora
                </h3>
                <p class="text-sm text-gray-500 max-w-sm leading-relaxed">
                  Actualmente no tenemos ninguna promoción de sorteo activa en
                  esta temporada. Mantente al pendiente de nuestras redes para
                  conocer la fecha del próximo sorteo.
                </p>
              </div>
            {/if}
          </Card.Content>
        </Card.Root>

        <!-- CARD DE HISTORIAL DE NÚMEROS REGISTRADOS -->
        <Card.Root
          class="border-0 shadow-lg rounded-2xl bg-white overflow-hidden"
        >
          <Card.Header class="pb-3">
            <Card.Title
              class="text-xl font-black text-[#111111] flex items-center gap-2"
            >
              <Ticket class="h-5 w-5 text-[#e67a25]" />
              Mis Números Seleccionados
            </Card.Title>
          </Card.Header>

          <Card.Content>
            {#if loadingRaffle}
              <div class="py-8 text-center">
                <div
                  class="h-6 w-6 animate-spin rounded-full border-2 border-[#e67a25]/20 border-t-[#e67a25] mx-auto mb-2"
                ></div>
                <p class="text-xs text-gray-400">Buscando tus boletos...</p>
              </div>
            {:else if myEntries.length > 0}
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {#each myEntries as entry}
                  <div
                    class="flex items-center gap-4 p-4 rounded-xl border border-gray-100 bg-gray-50/50 hover:bg-gray-50 transition-colors"
                  >
                    <div
                      class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[#e67a25] text-white font-black text-lg shadow-sm"
                    >
                      {entry.selected_number}
                    </div>
                    <div class="min-w-0">
                      <p
                        class="text-xs text-gray-400 font-bold uppercase tracking-wider"
                      >
                        Sucursal de registro
                      </p>
                      <p
                        class="text-[0.95rem] font-bold text-[#111111] truncate leading-tight mt-0.5"
                      >
                        {raffle?.branches.find((b) => b.id === entry.branch_id)
                          ?.name ?? "Sucursal"}
                      </p>
                      <p class="text-[0.75rem] text-gray-400 mt-0.5">
                        Registrado el {new Date(
                          entry.created_at,
                        ).toLocaleDateString("es-MX", {
                          day: "numeric",
                          month: "short",
                          year: "numeric",
                        })}
                      </p>
                    </div>
                  </div>
                {/each}
              </div>
            {:else}
              <div
                class="flex flex-col items-center justify-center py-8 text-center"
              >
                <p class="text-sm text-gray-500 font-medium mb-1">
                  Aún no tienes números registrados
                </p>
                <p class="text-xs text-gray-400 max-w-[280px]">
                  Ingresa los códigos de tus boletos y selecciona tus números
                  para participar.
                </p>
              </div>
            {/if}
          </Card.Content>
        </Card.Root>

        <!-- CARD DE HISTORIAL DE COTIZACIONES -->
        <Card.Root
          class="border-0 shadow-lg rounded-2xl bg-white overflow-hidden mt-8"
        >
          <Card.Header class="pb-3">
            <Card.Title
              class="text-xl font-black text-[#111111] flex items-center gap-2"
            >
              <FileText class="h-5 w-5 text-[#e67a25]" />
              Mis Presupuestos Guardados
            </Card.Title>
          </Card.Header>

          <Card.Content>
            {#if loadingQuotes}
              <div class="py-8 text-center">
                <div
                  class="h-6 w-6 animate-spin rounded-full border-2 border-[#e67a25]/20 border-t-[#e67a25] mx-auto mb-2"
                ></div>
                <p class="text-xs text-gray-400">Buscando tus presupuestos...</p>
              </div>
            {:else if quotes.length > 0}
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {#each quotes as quote}
                  <div
                    class="flex flex-col justify-between p-4 rounded-xl border border-gray-100 bg-gray-50/50 hover:bg-gray-50 transition-all relative"
                  >
                    <div>
                      <div class="flex items-center justify-between gap-2">
                        <span
                          class="inline-flex items-center justify-center px-2 py-0.5 rounded-md bg-[#e67a25]/10 text-[0.7rem] font-black text-[#e67a25]"
                        >
                          {quote.paint_product_name}
                        </span>
                        
                        {#if quote.is_expired}
                          <span
                            class="inline-flex items-center rounded-full bg-red-50 px-2 py-0.5 text-[0.65rem] font-bold text-red-600 border border-red-200"
                          >
                            Expirado
                          </span>
                        {:else}
                          <span
                            class="inline-flex items-center rounded-full bg-green-50 px-2 py-0.5 text-[0.65rem] font-bold text-green-700 border border-green-200"
                          >
                            Vigente
                          </span>
                        {/if}
                      </div>

                      <h4 class="text-base font-black text-[#111111] mt-2">
                        Precotización #{quote.id}
                      </h4>
                      
                      <p class="text-xs text-gray-500 mt-1">
                        Área: <span class="font-bold text-[#111111]">{quote.square_meters} m²</span>
                      </p>
                      <p class="text-xs text-gray-500 mt-0.5">
                        Estimado: <span class="text-[#e67a25] font-black text-sm">${quote.estimated_price.toLocaleString("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
                      </p>
                      
                      <p class="text-[0.75rem] text-gray-400 mt-2 flex items-center gap-1">
                        <Calendar class="h-3.5 w-3.5" />
                        {new Date(quote.created_at).toLocaleDateString("es-MX", {
                          day: "numeric",
                          month: "short",
                          year: "numeric",
                        })}
                      </p>
                    </div>

                    <!-- Botones de Acción -->
                    <div class="flex items-center gap-2 mt-4 pt-3 border-t border-gray-100/60">
                      <!-- Enlace de Descarga Directa PDF -->
                      <a
                        href={apiUrl(`/api/v1/quotes/${quote.id}/pdf?token=${encodeURIComponent(getToken() || "")}`)}
                        target="_blank"
                        class="flex-1 flex items-center justify-center gap-1 px-3 py-2 rounded-lg bg-gray-100 hover:bg-[#172033] hover:text-white text-gray-700 text-xs font-bold transition-all text-center"
                      >
                        <Download class="h-3 w-3" />
                        PDF
                      </a>

                      <!-- Compartir por correo -->
                      <button
                        type="button"
                        onclick={() => {
                          if (activeEmailModalId === quote.id) {
                            activeEmailModalId = null;
                          } else {
                            activeEmailModalId = quote.id;
                            customEmailDest = quote.contact_method === "email" ? quote.contact_value : "";
                            emailStatusMsg = "";
                            emailStatusType = "";
                          }
                        }}
                        class="flex-1 flex items-center justify-center gap-1 px-3 py-2 rounded-lg bg-[#e67a25]/10 hover:bg-[#e67a25] hover:text-white text-[#e67a25] text-xs font-bold transition-all"
                      >
                        <Mail class="h-3 w-3" />
                        Enviar
                      </button>
                    </div>

                    <!-- Modal/Input de Envío de Correo Inline -->
                    {#if activeEmailModalId === quote.id}
                      <div class="mt-3 p-3 rounded-lg bg-white border border-gray-200 shadow-inner space-y-2">
                        <p class="text-[0.7rem] font-bold text-gray-500 uppercase">Enviar PDF a correo:</p>
                        <div class="flex gap-2">
                          <input
                            type="email"
                            placeholder="correo@ejemplo.com"
                            bind:value={customEmailDest}
                            class="flex-1 text-xs px-2.5 py-1.5 rounded-md border border-gray-200 outline-none focus:border-[#e67a25]"
                          />
                          <button
                            type="button"
                            disabled={sendingEmailId === quote.id}
                            onclick={() => sendQuoteByEmail(quote.id, quote.contact_method === "email" ? quote.contact_value : "")}
                            class="px-3 py-1.5 rounded-md bg-[#172033] hover:bg-[#e67a25] text-white text-xs font-black transition-all flex items-center justify-center"
                          >
                            {#if sendingEmailId === quote.id}
                              ...
                            {:else}
                              <Send class="h-3 w-3" />
                            {/if}
                          </button>
                        </div>
                        {#if emailStatusMsg}
                          <p
                            class="text-[0.7rem] font-medium mt-1"
                            class:text-green-600={emailStatusType === "success"}
                            class:text-red-500={emailStatusType === "error"}
                          >
                            {emailStatusMsg}
                          </p>
                        {/if}
                      </div>
                    {/if}
                  </div>
                {/each}
              </div>
            {:else}
              <div
                class="flex flex-col items-center justify-center py-8 text-center"
              >
                <p class="text-sm text-gray-500 font-medium mb-1">
                  Aún no tienes presupuestos guardados
                </p>
                <p class="text-xs text-gray-400 max-w-[280px]">
                  Utiliza nuestro cotizador automático para calcular y guardar presupuestos de tus proyectos.
                </p>
                <a
                  href="/cotizador"
                  class="mt-3 inline-flex items-center gap-1.5 text-xs font-black text-[#e67a25] hover:text-[#172033] transition-colors"
                >
                  Ir al Cotizador
                  <ArrowRight class="h-3 w-3" />
                </a>
              </div>
            {/if}
          </Card.Content>
        </Card.Root>
      </div>

      <!-- COLUMNA DERECHA: SIDEBAR DE HERRAMIENTAS Y SOPORTE (1/3) -->
      <div class="space-y-8">
        <!-- CARD DE HERRAMIENTAS -->
        <Card.Root
          class="border-0 shadow-md rounded-2xl bg-white/95 overflow-hidden"
        >
          <Card.Header class="pb-3">
            <Card.Description
              class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1"
            >
              Herramientas
            </Card.Description>
            <Card.Title class="text-lg font-black text-[#111111]"
              >Servicios Disponibles</Card.Title
            >
          </Card.Header>
          <Card.Content class="space-y-4">
            <!-- Cotizador -->
            <a
              href="/cotizador"
              class="group block p-4 rounded-xl border border-gray-100 hover:border-[#e67a25]/50 bg-gray-50/50 hover:bg-white transition-all shadow-sm"
            >
              <h4
                class="font-bold text-[#111111] group-hover:text-[#e67a25] transition-colors leading-tight mb-1"
              >
                Cotizador de Pintura
              </h4>
              <p class="text-xs text-gray-500 leading-normal">
                Calcula cuánta pintura necesitas para renovar tus espacios de
                manera rápida.
              </p>
            </a>

            <!-- Productos -->
            <div
              class="p-4 rounded-xl border border-gray-100 bg-gray-50/20 opacity-70"
            >
              <div class="flex items-center justify-between">
                <h4 class="font-bold text-[#111111] leading-tight mb-1">
                  Catálogo de Productos
                </h4>
                <span
                  class="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-[0.65rem] font-bold text-gray-500 uppercase"
                  >Próximamente</span
                >
              </div>
              <p class="text-xs text-gray-400 leading-normal">
                Consulta toda nuestra gama de colores y acabados de pintura
                directamente desde aquí.
              </p>
            </div>
          </Card.Content>
        </Card.Root>

        <!-- CARD DE SOPORTE E INFORMACIÓN -->
        <Card.Root
          class="border-0 shadow-md rounded-2xl bg-white/95 overflow-hidden"
        >
          <Card.Header class="pb-3">
            <Card.Description
              class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1"
            >
              ¿Necesitas ayuda?
            </Card.Description>
            <Card.Title class="text-lg font-black text-[#111111]"
              >Soporte Express</Card.Title
            >
          </Card.Header>
          <Card.Content class="space-y-4">
            <p class="text-xs text-gray-500 leading-relaxed">
              ¿Tienes algún problema validando tus códigos o eligiendo tus
              números? Nuestro equipo está listo para asesorarte.
            </p>

            <a
              href="https://wa.me/524421878771?text=Hola,%20necesito%20ayuda%20con%20mis%20boletos%20de%20StarColors"
              target="_blank"
              class="w-full rounded-xl bg-[#25D366] hover:bg-[#20ba56] text-white font-bold h-11 transition-all flex items-center justify-center gap-2 text-sm shadow-sm"
            >
              <Phone class="h-4 w-4 fill-white" />
              Soporte por WhatsApp
            </a>

            <div
              class="flex items-start gap-2.5 text-xs text-gray-500 bg-gray-50 p-3 rounded-lg border border-gray-100"
            >
              <Info class="h-4 w-4 text-[#e67a25] shrink-0 mt-0.5" />
              <span>
                Los números ocupados no se pueden registrar. Las confirmaciones
                son finales y no se pueden cambiar.
              </span>
            </div>
          </Card.Content>
        </Card.Root>
      </div>
    </div>
  </div>
{/if}
