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
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
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

  async function downloadQuotePdf() {
    submitError = "";

    try {
      const url = apiUrl(`${API_PREFIX}/quotes/pdf`);

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(toPayload(form)),
      });

      if (!response.ok) {
        throw new Error(`API ${response.status}: ${url}`);
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = "precotizacion-starcolors.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      submitError =
        error instanceof Error ? error.message : "No se pudo descargar el PDF.";
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
    const configuredBaseUrl = import.meta.env.PUBLIC_API_BASE_URL?.trim();
    const baseUrl =
      configuredBaseUrl && configuredBaseUrl.length > 0
        ? configuredBaseUrl
        : `http://${window.location.hostname}:8000`;

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

<section class="wizard-shell" aria-label="Cotizador automatico">
  <div class="wizard-card">
    <header class="wizard-header">
      <div class="wizard-title-row">
        <p class="wizard-kicker">Cotizador automatico</p>
        <p class="step-count">Paso {currentStep + 1} de {steps.length}</p>
      </div>

      <div class="progress-dots" aria-label="Progreso del formulario">
        {#each steps as step, index}
          <span
            class:active={index === currentStep}
            class:done={index < currentStep}
            title={step}
          ></span>
        {/each}
      </div>
    </header>

    <div class="wizard-content">
      {#if isLoadingOptions}
        <div class="state-box">Cargando opciones del cotizador...</div>
      {:else if optionsError}
        <div class="state-box state-box--error">
          <p>{optionsError}</p>
          <button type="button" class="button-secondary" on:click={loadOptions}>
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

    {#if submitError}
      <p class="submit-error" role="alert">{submitError}</p>
    {/if}

    <footer class="wizard-actions">
      {#if currentStep === steps.length - 1}
        <button
          type="button"
          class="button-secondary"
          on:click={startNewQuote}
          disabled={isSubmitting}
        >
          Crear nuevo
        </button>

        <button
          type="button"
          class="button-primary"
          on:click={goHome}
          disabled={isSubmitting}
        >
          Regresar a Inicio
        </button>
      {:else}
        <button
          type="button"
          class="button-secondary"
          on:click={goBack}
          disabled={currentStep === 0 || isSubmitting}
        >
          Atras
        </button>

        {#if currentStep === steps.length - 2}
          <button
            type="button"
            class="button-primary"
            on:click={submitQuote}
            disabled={!options || isSubmitting}
          >
            {isSubmitting ? "Calculando..." : "Enviar"}
          </button>
        {:else}
          <button
            type="button"
            class="button-primary"
            on:click={goNext}
            disabled={!options || isSubmitting}
          >
            Continuar
          </button>
        {/if}
      {/if}
    </footer>
  </div>
</section>

<style>
  .wizard-shell {
    display: grid;
    place-items: center;
    width: min(100%, 850px);
    height: min(720px, calc(100dvh - 1.25rem));
    min-height: 0;
  }

  .wizard-card {
    display: grid;
    grid-template-rows: auto minmax(0, 1fr) auto auto;
    width: 100%;
    height: 100%;
    border: 1px solid rgba(255, 255, 255, 0.5);
    border-radius: 28px;
    background: #f8fafc;
    box-shadow: 0 30px 90px rgba(0, 0, 0, 0.34);
    overflow: hidden;
  }

  .wizard-header {
    display: grid;
    gap: 0.55rem;
    padding: 0.9rem 1.1rem 0.75rem;
    border-bottom: 1px solid #e2e8f0;
    background: #fff;
  }

  .wizard-title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
  }

  .wizard-kicker,
  .step-count {
    margin: 0;
    color: #536173;
    font-size: 0.78rem;
    font-weight: 850;
    line-height: 1.1;
  }

  .step-count {
    white-space: nowrap;
  }

  .progress-dots {
    display: flex;
    gap: 0.42rem;
  }

  .progress-dots span {
    width: 0.62rem;
    height: 0.62rem;
    border-radius: 999px;
    background: #d8dee8;
    transition:
      width 0.16s ease,
      background 0.16s ease;
  }

  .progress-dots span.active {
    width: 1.7rem;
    background: #f5b700;
  }

  .progress-dots span.done {
    background: #172033;
  }

  .wizard-content {
    display: block;
    min-height: 0;
    overflow: hidden;
    padding: 1.35rem 1.45rem;
  }

  .wizard-actions {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.2fr);
    gap: 0.7rem;
    padding: 0.78rem 1.1rem 0.95rem;
    border-top: 1px solid #e2e8f0;
    background: #fff;
  }

  button {
    min-height: 42px;
    border: 0;
    border-radius: 999px;
    padding: 0.68rem 0.95rem;
    font-size: 0.9rem;
    font-weight: 850;
    cursor: pointer;
  }

  button:disabled {
    cursor: not-allowed;
    opacity: 0.45;
  }

  .button-primary {
    background: #f5b700;
    color: #172033;
  }

  .button-secondary {
    background: #f1f5f9;
    color: #172033;
  }

  .state-box {
    display: grid;
    gap: 0.75rem;
    align-content: center;
    min-height: 100%;
    border-radius: 16px;
    background: #f8fafc;
    color: #475569;
    padding: 1rem;
    text-align: center;
  }

  .state-box p {
    margin: 0;
  }

  .state-box--error {
    border: 1px solid #fecdd3;
    background: #fff1f2;
    color: #9f1239;
  }

  .submit-error {
    margin: 0 1rem;
    border: 1px solid #fecdd3;
    border-radius: 12px;
    background: #fff1f2;
    color: #9f1239;
    padding: 0.65rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 750;
  }

  @media (max-width: 520px) {
    .wizard-shell {
      width: 100%;
      height: calc(100svh - 5rem);
      max-height: 620px;
      min-height: 0;
      padding-inline: 0.25rem;
      padding-block: 0.5rem;
    }

    .wizard-card {
      height: 100%;
      border-radius: 22px;
    }

    .wizard-header {
      gap: 0.45rem;
      padding: 0.72rem 0.85rem 0.62rem;
    }

    .wizard-kicker,
    .step-count {
      font-size: 0.7rem;
    }

    .progress-dots {
      gap: 0.32rem;
    }

    .progress-dots span {
      width: 0.52rem;
      height: 0.52rem;
    }

    .progress-dots span.active {
      width: 1.35rem;
    }

    .wizard-content {
      padding: 1rem 0.9rem;
    }

    .wizard-actions {
      grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
      gap: 0.55rem;
      padding: 0.65rem 0.85rem 0.78rem;
    }

    button {
      width: 100%;
      min-height: 39px;
      padding: 0.58rem 0.7rem;
      font-size: 0.82rem;
    }

    .submit-error {
      margin: 0 0.85rem;
      padding: 0.55rem 0.7rem;
      font-size: 0.74rem;
    }
  }
</style>
