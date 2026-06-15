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
    ["surface_state", "texture", "preparation", "area_protection"],
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
  });

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
        throw new Error(`API ${response.status}: ${url}`);
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
        return "Ingresa un codigo postal de 5 digitos.";
      }
      return "";
    }

    if (field === "contact_value") {
      if (
        form.contact_method === "email" &&
        !form.contact_value.includes("@")
      ) {
        return "Ingresa un correo valido.";
      }

      if (form.contact_method === "whatsapp") {
        const digits = form.contact_value.replace(/\D/g, "");
        if (digits.length < 10) {
          return "Ingresa un WhatsApp de al menos 10 digitos.";
        }
      }
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
      place_activities: source.place_activities.trim(),
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
  class="grid place-items-center w-full h-full min-h-0"
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
        <p class="m-0 text-[#536173] text-[0.76rem] font-black leading-none whitespace-nowrap">
          Paso {currentStep + 1} de {steps.length}
        </p>
      </div>

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
    </header>

    <!-- ── Step content ── -->
    <div class="block min-h-0 overflow-y-auto overflow-x-hidden overscroll-contain px-4 py-4 sm:px-5">
      {#if isLoadingOptions}
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
          on:click={goHome}
          disabled={isSubmitting}
          class="
            min-h-[44px] border-0 rounded-full
            bg-[#f5b700] text-[#172033]
            text-[0.9rem] font-bold px-4 cursor-pointer
            hover:bg-[#e6ac00] active:scale-[0.97] transition-all duration-150
            disabled:opacity-40 disabled:cursor-not-allowed
          "
        >
          Regresar a Inicio
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
            {isSubmitting ? "Calculando..." : "Enviar"}
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
  </div>
</section>
