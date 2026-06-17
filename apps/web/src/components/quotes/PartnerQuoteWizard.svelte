<script lang="ts">
  import { onMount } from "svelte";

  import IntroStep from "./steps/IntroStep.svelte";
  import ContactStep from "./steps/ContactStep.svelte";
  import LocationStep from "./steps/LocationStep.svelte";
  import PaintProductStep from "./steps/PaintProductStep.svelte";
  import ProjectStep from "./steps/ProjectStep.svelte";
  import ReviewSubmitStep from "./steps/ReviewSubmitStep.svelte";
  import SurfaceStep from "./steps/SurfaceStep.svelte";
  import WorkConditionsStep from "./steps/WorkConditionsStep.svelte";
  import QuoteSuccessStep from "./steps/QuoteSuccessStep.svelte";
  import { getToken } from "../../lib/auth";
  import { FileText } from "@lucide/svelte";

  import type {
    QuoteForm,
    QuoteOptions,
    QuotePayload,
    QuoteResult,
  } from "./types";

  const API_PREFIX = "/api/v1";

  const steps = [
    "Inicio",
    "Proyecto",
    "Pintura",
    "Superficie",
    "Condiciones",
    "Ubicacion",
    "Contacto",
    "Confirmar",
    "Resultado",
  ];

  const stepFields = [
    [],
    ["property_type", "work_location", "square_meters", "service_type"],
    ["paint_product", "color_intensity"],
    ["surface_state", "texture", "area_protection"],
    ["advance_difficulty", "occupancy", "height_risk", "schedule"],
    ["state", "city", "postal_code"],
    ["customer_name", "contact_method", "contact_value"],
    [],
  ] as const;

  let currentStep = 0;
  let options: QuoteOptions | null = null;
  let isLoadingOptions = true;
  let optionsError = "";
  let isSubmitting = false;
  let submitError = "";
  let quoteResult: QuoteResult | null = null;
  let errors: Record<string, string> = {};

  let userQuotesCount = 0;
  let isLimitReached = false;

  let form: QuoteForm = {
    property_type: "",
    work_location: "",
    square_meters: "",

    service_type: "",
    paint_product: "",
    color_intensity: "",

    surface_state: "",
    texture: "",
    advance_difficulty: "",
    occupancy: "",
    height_risk: "",
    area_protection: "",
    preparation: [],
    schedule: "",
    place_activities: "",

    state: "",
    city: "",
    postal_code: "",

    customer_name: "",
    contact_method: "",
    contact_value: "",
    wants_offers: false,
  };

  onMount(async () => {
    await loadOptions();
    await checkUserQuotesLimit();
  });

  async function checkUserQuotesLimit() {
    const token = getToken();
    if (!token) return;

    try {
      const url = apiUrl(`/api/v1/quotes/my`);
      const response = await fetch(url, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const quotesList = await response.json();
        userQuotesCount = quotesList.length;
        if (userQuotesCount >= 6) {
          isLimitReached = true;
        }
      }
    } catch (err) {
      console.error("Error al consultar límite de cotizaciones:", err);
    }
  }

  async function loadOptions() {
    isLoadingOptions = true;
    optionsError = "";

    try {
      const url = apiUrl(`${API_PREFIX}/quotes/options`);
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`API ${response.status}: ${url}`);
      }

      options = await response.json();
    } catch (error) {
      optionsError =
        error instanceof Error
          ? error.message
          : "No se pudieron cargar las opciones del cotizador.";
    } finally {
      isLoadingOptions = false;
    }
  }

  function goNext() {
    submitError = "";
    quoteResult = null;

    if (currentStep < steps.length - 2) {
      currentStep += 1;
    }
  }

  function goBack() {
    submitError = "";

    if (currentStep > 0) {
      currentStep -= 1;
    }
  }

  function startNewQuote() {
    window.location.reload();
  }

  function goHome() {
    window.location.href = "/";
  }

  function goToHub() {
    window.location.href = "/hub";
  }

  async function submitQuote() {
    submitError = "";
    quoteResult = null;

    if (!validateAll()) {
      submitError = "Revisa los campos marcados antes de enviar.";
      return;
    }

    isSubmitting = true;

    try {
      const url = apiUrl(`${API_PREFIX}/quotes/`);
      
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };
      const token = getToken();
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify(toPayload(form)),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => null);
        throw new Error(errData?.detail || `Error del servidor (${response.status})`);
      }

      quoteResult = await response.json();
      currentStep = steps.length - 1;
    } catch (error) {
      submitError =
        error instanceof Error
          ? error.message
          : "No se pudo generar la precotizacion.";
    } finally {
      isSubmitting = false;
    }
  }

  function validateAll() {
    return stepFields.every((_, index) => validateStep(index));
  }

  function validateStep(stepIndex: number) {
    const nextErrors = { ...errors };
    let isValid = true;

    for (const field of stepFields[stepIndex]) {
      const message = validateField(field);

      if (message) {
        nextErrors[field] = message;
        isValid = false;
      } else {
        delete nextErrors[field];
      }
    }

    errors = nextErrors;
    return isValid;
  }

  function downloadQuotePdf() {
    if (!quoteResult || !quoteResult.id) {
      submitError = "No se ha generado el identificador del presupuesto para la descarga.";
      return;
    }

    const token = getToken();
    const queryParams = token ? `?token=${encodeURIComponent(token)}` : "";
    const url = apiUrl(`${API_PREFIX}/quotes/${quoteResult.id}/pdf${queryParams}`);

    window.open(url, "_blank");
  }

  let isSendingEmail = false;
  let emailSuccess = "";
  let emailError = "";

  async function sendQuotePdfByEmail() {
    if (!quoteResult || !quoteResult.id) return;
    
    isSendingEmail = true;
    emailSuccess = "";
    emailError = "";

    // Determine target email
    let emailDest = form.contact_method === "email" ? form.contact_value : "";
    
    if (!emailDest) {
      const emailPrompt = prompt("Introduce el correo electrónico de destino:");
      if (!emailPrompt) {
        isSendingEmail = false;
        return;
      }
      emailDest = emailPrompt.trim();
    }

    if (!emailDest || !emailDest.includes("@")) {
      emailError = "Por favor ingresa un correo electrónico válido.";
      isSendingEmail = false;
      return;
    }

    try {
      const token = getToken();
      const url = apiUrl(`${API_PREFIX}/quotes/${quoteResult.id}/send-email`);
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

      emailSuccess = `¡Correo enviado exitosamente a ${emailDest}!`;
    } catch (error) {
      emailError = error instanceof Error ? error.message : "No se pudo enviar el correo.";
    } finally {
      isSendingEmail = false;
    }
  }

  function validateField(field: string) {
    const value = form[field as keyof QuoteForm];

    if (field === "square_meters") {
      const numericValue = Number(form.square_meters);
      if (
        !form.square_meters ||
        Number.isNaN(numericValue) ||
        numericValue <= 0
      ) {
        return "Ingresa metros cuadrados mayores a 0.";
      }
      return "";
    }

    if (field === "postal_code") {
      if (!/^\d{5}$/.test(form.postal_code)) {
        return "Ingresa un código postal de 5 dígitos.";
      }
      return "";
    }

    if (field === "contact_value") {
      if (
        form.contact_method === "email" &&
        !form.contact_value.includes("@")
      ) {
        return "Ingresa un correo válido.";
      }

      if (form.contact_method === "whatsapp") {
        const digits = form.contact_value.replace(/\D/g, "");
        if (digits.length < 10) {
          return "Ingresa un WhatsApp de al menos 10 dígitos.";
        }
      }
    }

    // Validación para campos de lista (preparation es array de strings)
    if (Array.isArray(value)) {
      if (value.length === 0) {
        return "Selecciona al menos una opción.";
      }
      return "";
    }

    if (typeof value === "string" && value.trim() === "") {
      return "Campo obligatorio.";
    }

    return "";
  }


  function toPayload(source: QuoteForm): QuotePayload {
    return {
      ...source,
      square_meters: Number(source.square_meters),
      // Pydantic espera null, no string vacío
      place_activities: source.place_activities.trim() || null,
    };
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

    if (
      normalizedBaseUrl.endsWith(API_PREFIX) &&
      normalizedPath.startsWith(API_PREFIX)
    ) {
      return `${normalizedBaseUrl}${normalizedPath.slice(API_PREFIX.length)}`;
    }

    return `${normalizedBaseUrl}${normalizedPath}`;
  }
</script>

<!-- ─── Wizard shell ─────────────────────────────────────────────────────── -->
<section
  class="grid place-items-center w-full max-w-[860px] mx-auto h-[min(720px,calc(100dvh-2.5rem))] px-3 sm:px-5 min-h-0"
  aria-label="Cotizador automático"
>
  <div
    class="
      grid grid-rows-[auto_minmax(0,1fr)_auto_auto]
      w-full h-full
      border border-white/50 rounded-[26px] sm:rounded-[28px]
      bg-[#f8fafc] shadow-[0_30px_90px_rgba(0,0,0,0.34)]
      overflow-hidden
    "
  >
    <!-- ── Header ── -->
    <header class="grid gap-2 px-4 pt-3 pb-2.5 border-b border-[#e2e8f0] bg-white">
      <div class="flex items-center justify-between gap-3">
        <p class="m-0 text-[#536173] text-[0.76rem] font-black leading-none">
          Cotizador automático
        </p>
        {#if !isLimitReached}
          <p class="m-0 text-[#536173] text-[0.76rem] font-black leading-none whitespace-nowrap">
            Paso {currentStep + 1} de {steps.length}
          </p>
        {/if}
      </div>

      {#if !isLimitReached}
        <!-- Progress dots -->
        <div class="flex gap-1.5" aria-label="Progreso del formulario">
          {#each steps as step, index}
            <span
              title={step}
              class="
                h-2 rounded-full transition-all duration-200 ease-out
                {index === currentStep
                  ? 'w-6 bg-[#f5b700]'
                  : index < currentStep
                    ? 'w-2 bg-[#172033]'
                    : 'w-2 bg-[#d8dee8]'}
              "
            ></span>
          {/each}
        </div>
      {/if}
    </header>

    <!-- ── Step content ── -->
    <div class="block min-h-0 overflow-y-auto overflow-x-hidden overscroll-contain px-4 py-4 sm:px-5">
      {#if isLimitReached}
        <div class="flex flex-col items-center justify-center py-10 text-center max-w-md mx-auto min-h-full animate-in fade-in duration-300">
          <div class="flex h-16 w-16 items-center justify-center rounded-2xl bg-[#e67a25]/10 text-[#e67a25] mb-6 shadow-sm">
            <FileText class="h-8 w-8" />
          </div>
          <h3 class="text-xl font-black text-[#111111] mb-3 leading-tight">
            Límite de presupuestos alcanzado
          </h3>
          <p class="text-sm text-gray-500 mb-8 leading-relaxed">
            Has alcanzado el límite máximo de <span class="font-bold text-[#e67a25]">6 presupuestos</span> guardados en tu cuenta. Para mantener tu portal rápido y organizado, debes eliminar al menos un presupuesto antiguo antes de poder generar uno nuevo.
          </p>
          <div class="flex flex-col sm:flex-row gap-3 w-full justify-center">
            <button
              type="button"
              on:click={goToHub}
              class="
                min-h-[44px] border-0 rounded-full
                bg-[#172033] hover:bg-[#e67a25] text-white
                text-sm font-bold px-6 cursor-pointer
                active:scale-[0.97] transition-all duration-150
              "
            >
              Ir a mi Portal de Cliente
            </button>
            <button
              type="button"
              on:click={goHome}
              class="
                min-h-[44px] border-0 rounded-full
                bg-gray-100 hover:bg-gray-200 text-gray-700
                text-sm font-bold px-6 cursor-pointer
                active:scale-[0.97] transition-all duration-150
              "
            >
              Volver al inicio
            </button>
          </div>
        </div>
      {:else if isLoadingOptions}
        <div class="grid gap-3 place-content-center min-h-full rounded-2xl bg-[#f8fafc] text-[#475569] text-sm text-center p-4">
          Cargando opciones del cotizador...
        </div>
      {:else if optionsError}
        <div class="grid gap-3 place-content-center min-h-full rounded-2xl border border-[#fecdd3] bg-[#fff1f2] text-[#9f1239] text-sm text-center p-4">
          <p class="m-0">{optionsError}</p>
          <button
            type="button"
            on:click={loadOptions}
            class="
              self-center mx-auto min-h-[38px]
              border-0 rounded-full bg-[#f1f5f9] text-[#172033]
              text-[0.88rem] font-bold px-5 py-2 cursor-pointer
              hover:bg-[#e2e8f0] transition-colors duration-150
            "
          >
            Reintentar
          </button>
        </div>
      {:else if options}
        {#if currentStep === 0}
          <IntroStep />
        {:else if currentStep === 1}
          <ProjectStep bind:form {options} {errors} />
        {:else if currentStep === 2}
          <PaintProductStep bind:form {options} {errors} />
        {:else if currentStep === 3}
          <SurfaceStep bind:form {options} {errors} />
        {:else if currentStep === 4}
          <WorkConditionsStep bind:form {options} {errors} />
        {:else if currentStep === 5}
          <LocationStep bind:form {options} {errors} />
        {:else if currentStep === 6}
          <ContactStep bind:form {errors} />
        {:else if currentStep === 7}
          <ReviewSubmitStep {form} {options} {quoteResult} />
        {:else if currentStep === 8 && quoteResult}
          <QuoteSuccessStep
            {form}
            {options}
            {quoteResult}
            onDownloadPdf={downloadQuotePdf}
            onSendEmail={sendQuotePdfByEmail}
            {isSendingEmail}
            {emailSuccess}
            {emailError}
          />
        {/if}
      {/if}
    </div>

    <!-- ── Submit error ── -->
    {#if submitError}
      <p
        role="alert"
        class="
          mx-4 mb-0 border border-[#fecdd3] rounded-xl
          bg-[#fff1f2] text-[#9f1239]
          text-[0.8rem] font-semibold leading-snug
          px-3.5 py-2.5
        "
      >
        {submitError}
      </p>
    {/if}

    <!-- ── Footer actions ── -->
    {#if !isLimitReached}
      <footer class="grid grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)] gap-2.5 px-4 pt-2.5 pb-3.5 border-t border-[#e2e8f0] bg-white sm:px-5">
        {#if currentStep === steps.length - 1}
          <!-- Last step buttons -->
          <button
            type="button"
            on:click={startNewQuote}
            disabled={isSubmitting}
            class="
              min-h-[44px] border-0 rounded-full
              bg-[#f1f5f9] text-[#172033]
              text-[0.9rem] font-bold px-4 cursor-pointer
              hover:bg-[#e2e8f0] transition-colors duration-150
              disabled:opacity-40 disabled:cursor-not-allowed
            "
          >
            Crear nuevo
          </button>
          <button
            type="button"
            on:click={goToHub}
            disabled={isSubmitting}
            class="
              min-h-[44px] border-0 rounded-full
              bg-[#f5b700] text-[#172033]
              text-[0.9rem] font-bold px-4 cursor-pointer
              hover:bg-[#e6ac00] active:scale-[0.97] transition-all duration-150
              disabled:opacity-40 disabled:cursor-not-allowed
            "
          >
            Regresar al Portal
          </button>
        {:else}
          <!-- Back button -->
          <button
            type="button"
            on:click={goBack}
            disabled={currentStep === 0 || isSubmitting}
            class="
              min-h-[44px] border-0 rounded-full
              bg-[#f1f5f9] text-[#172033]
              text-[0.9rem] font-bold px-4 cursor-pointer
              hover:bg-[#e2e8f0] transition-colors duration-150
              disabled:opacity-40 disabled:cursor-not-allowed
            "
          >
            Atrás
          </button>

          {#if currentStep === steps.length - 2}
            <!-- Submit button -->
            <button
              type="button"
              on:click={submitQuote}
              disabled={!options || isSubmitting}
              class="
                min-h-[44px] border-0 rounded-full
                bg-[#f5b700] text-[#172033]
                text-[0.9rem] font-bold px-4 cursor-pointer
                hover:bg-[#e6ac00] active:scale-[0.97] transition-all duration-150
                disabled:opacity-40 disabled:cursor-not-allowed
              "
            >
              {isSubmitting ? "Generando..." : "Generar"}
            </button>
          {:else}
            <!-- Next button -->
            <button
              type="button"
              on:click={goNext}
              disabled={!options || isSubmitting}
              class="
                min-h-[44px] border-0 rounded-full
                bg-[#f5b700] text-[#172033]
                text-[0.9rem] font-bold px-4 cursor-pointer
                hover:bg-[#e6ac00] active:scale-[0.97] transition-all duration-150
                disabled:opacity-40 disabled:cursor-not-allowed
              "
            >
              Continuar
            </button>
          {/if}
        {/if}
      </footer>
    {/if}
  </div>
</section>
