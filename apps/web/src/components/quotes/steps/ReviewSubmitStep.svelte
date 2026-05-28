<script lang="ts">
  import type {
    BasicOption,
    QuoteForm,
    QuoteOptions,
    QuoteResult,
  } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let quoteResult: QuoteResult | null = null;

  function optionName(list: BasicOption[], id: string) {
    return list.find((option) => option.id === id)?.name ?? "No especificado";
  }

  function optionNames(list: BasicOption[], ids: string[]) {
    if (!Array.isArray(ids) || ids.length === 0) {
      return "No especificado";
    }

    const names = ids.map((id) => optionName(list, id));

    return names.join(", ");
  }

  function val(value: unknown) {
    if (Array.isArray(value)) {
      return value.length > 0 ? value.join(", ") : "No especificado";
    }

    if (typeof value === "boolean") {
      return value ? "Sí" : "No";
    }

    if (typeof value === "number") {
      return String(value);
    }

    if (typeof value === "string") {
      return value.trim() !== "" ? value : "No especificado";
    }

    return "No especificado";
  }

  function money(value: number) {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  }
</script>

<section class="step">
  <div class="step-header">
    <h2>Confirmar y enviar</h2>
    <p class="step-desc">
      Revisa el resumen antes de enviar. Puedes regresar si necesitas corregir.
    </p>
  </div>

  <dl class="summary-card">
    <div>
      <dt>Proyecto</dt>
      <dd>
        {optionName(options.property_types, form.property_type)} /
        {optionName(options.work_locations, form.work_location)} /
        {optionName(options.service_types, form.service_type)}
      </dd>
    </div>
    <div>
      <dt>Area</dt>
      <dd>{val(form.square_meters)} m2</dd>
    </div>
    <div>
      <dt>Pintura</dt>
      <dd>
        {optionName(options.paints, form.paint_product)} /
        {optionName(options.color_intensities, form.color_intensity)}
      </dd>
    </div>
    <div>
      <dt>Superficie</dt>
      <dd>
        {optionName(options.surface_states, form.surface_state)} /
        {optionName(options.textures, form.texture)} /
        {optionNames(options.preparations, form.preparation)}
      </dd>
    </div>
    <div>
      <dt>Trabajo</dt>
      <dd>
        {optionName(options.advance_difficulties, form.advance_difficulty)} /
        {optionName(options.height_risks, form.height_risk)} /
        {optionName(options.schedules, form.schedule)}
      </dd>
    </div>
    <div>
      <dt>Ubicacion</dt>
      <dd>
        {optionName(options.states, form.state)} / {val(form.city)} /
        {val(form.postal_code)}
      </dd>
    </div>
    <div>
      <dt>Contacto</dt>
      <dd>
        {val(form.customer_name)} /
        {form.contact_method === "whatsapp" ? "WhatsApp" : "Email"}
      </dd>
    </div>
  </dl>

  {#if quoteResult}
    <article class="result-card" aria-live="polite">
      <div>
        <p class="result-label">Precotizacion estimada</p>
        <strong>{money(quoteResult.estimated_price)}</strong>
      </div>
      <p class="result-note">
        El calculo ya incluye las condiciones seleccionadas. Un asesor puede
        confirmar el precio final si el trabajo requiere visita tecnica.
      </p>
    </article>
  {/if}
</section>

<style>
  .step {
    display: grid;
    gap: 1rem;
    min-height: 0;
  }

  .step-header {
    display: grid;
    gap: 0.5rem;
  }

  h2 {
    margin: 0;
    color: #172033;
    font-size: clamp(1.75rem, 7vw, 2.6rem);
    line-height: 1.05;
  }

  .step-desc {
    margin: 0;
    color: #475569;
    line-height: 1.6;
    font-size: 0.92rem;
  }

  .summary-card,
  .result-card {
    display: grid;
    gap: 0.5rem;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    background: #f8fafc;
    padding: 0.85rem;
  }

  dl {
    margin: 0;
  }

  dl div {
    display: flex;
    justify-content: space-between;
    gap: 0.75rem;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.35rem;
  }

  dl div:last-child {
    border-bottom: 0;
    padding-bottom: 0;
  }

  dt {
    color: #64748b;
    font-size: 0.78rem;
    font-weight: 850;
    text-transform: uppercase;
  }

  dd {
    margin: 0;
    color: #172033;
    font-size: 0.82rem;
    font-weight: 750;
    text-align: right;
  }

  .result-card {
    background: #f0fdf4;
    border-color: #bbf7d0;
  }

  .result-label {
    margin: 0;
    color: #166534;
    font-size: 0.82rem;
    font-weight: 800;
    text-transform: uppercase;
  }

  .result-card strong {
    display: block;
    color: #14532d;
    font-size: clamp(2rem, 9vw, 3rem);
    line-height: 1;
  }

  .result-note {
    margin: 0;
    border-top: 1px solid #bbf7d0;
    color: #166534;
    font-size: 0.88rem;
    line-height: 1.55;
    padding-top: 0.75rem;
  }

  @media (max-width: 520px) {
    dl div {
      display: grid;
      gap: 0.15rem;
    }

    dd {
      text-align: left;
    }
  }
</style>
