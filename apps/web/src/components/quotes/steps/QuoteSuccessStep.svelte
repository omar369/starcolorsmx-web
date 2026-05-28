<script lang="ts">
  import type {
    BasicOption,
    QuoteAdjustment,
    QuoteForm,
    QuoteOptions,
    QuoteResult,
  } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let quoteResult: QuoteResult;

  function optionName(list: BasicOption[], id: string) {
    return list.find((option) => option.id === id)?.name ?? "No especificado";
  }

  function optionNames(list: BasicOption[], ids: string[]) {
    const names = ids.map((id) => optionName(list, id));
    return names.length > 0 ? names.join(", ") : "No especificado";
  }

  function val(value: string | boolean | undefined) {
    if (typeof value === "boolean") return value ? "Sí" : "No";
    return value && value.trim() !== "" ? value : "No especificado";
  }

  function money(value: number) {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  }

  function contactMethodLabel(value: string) {
    if (value === "whatsapp") return "WhatsApp";
    if (value === "email") return "correo electrónico";
    return "medio seleccionado";
  }

  function getProjectDescription() {
    return [
      optionName(options.property_types, form.property_type),
      optionName(options.work_locations, form.work_location),
      optionName(options.service_types, form.service_type),
      optionName(options.paints, form.paint_product),
    ].join(" / ");
  }

  function getSurfaceSummary() {
    const importantAdjustments = quoteResult.adjustments
      .filter((adjustment) => adjustment.percentage !== 0)
      .map(formatAdjustment);

    if (importantAdjustments.length > 0) {
      return importantAdjustments.join(", ");
    }

    return [
      optionName(options.surface_states, form.surface_state),
      optionName(options.textures, form.texture),
      optionNames(options.preparations, form.preparation),
      optionName(options.area_protections, form.area_protection),
    ].join(", ");
  }

  function formatAdjustment(adjustment: QuoteAdjustment) {
    const category = adjustment.category.toLowerCase();

    if (category.includes("preparación")) {
      return adjustment.option_name;
    }

    if (category.includes("textura")) {
      return `superficie ${adjustment.option_name.toLowerCase()}`;
    }

    if (category.includes("altura")) {
      return `trabajo en altura ${adjustment.option_name.toLowerCase()}`;
    }

    return adjustment.option_name;
  }
</script>

<section class="step">
  <div class="success-header">
    <p class="eyebrow">Precotización generada</p>
    <h2>Gracias por usar la herramienta de pre-cotizaciones.</h2>
    <p class="success-message">
      Ya preparamos tu cotización. En el futuro también podrás recibirla por
      <strong>{contactMethodLabel(form.contact_method)}</strong>.
    </p>
  </div>

  <article class="quote-document" aria-live="polite">
    <header class="document-header">
      <div>
        <p class="document-kicker">StarColors</p>
        <h3>Precotización de servicio de pintura</h3>
      </div>

      <div class="client-box">
        <span>Cliente</span>
        <strong>{val(form.customer_name)}</strong>
        <small>
          {contactMethodLabel(form.contact_method)}: {val(form.contact_value)}
        </small>
      </div>
    </header>

    <div class="meta-grid">
      <div>
        <span>Ubicación</span>
        <strong>
          {optionName(options.states, form.state)}, {val(form.city)}
        </strong>
        <small>CP {val(form.postal_code)}</small>
      </div>

      <div>
        <span>Proyecto</span>
        <strong>{getProjectDescription()}</strong>
      </div>
    </div>

    <div class="quote-table" role="table" aria-label="Resumen de cotización">
      <div class="quote-row quote-row-head" role="row">
        <span role="columnheader">Cantidad</span>
        <span role="columnheader">Servicio requerido</span>
        <span role="columnheader">Importe</span>
      </div>

      <div class="quote-row" role="row">
        <div class="quantity-cell" role="cell">
          <strong>{quoteResult.square_meters}</strong>
          <span>m²</span>
        </div>

        <div class="service-cell" role="cell">
          <strong>{quoteResult.paint_product_name}</strong>
          <p>{getSurfaceSummary()}</p>
        </div>

        <div class="amount-cell" role="cell">
          <strong>{money(quoteResult.estimated_price)}</strong>
        </div>
      </div>
    </div>

    <div class="document-note">
      <strong>Importante:</strong>
      Este resultado es una pre-cotización generada con los datos capturados. El
      importe final puede cambiar después de una revisión técnica o validación presencial.
    </div>
  </article>

  <div class="future-files">
    <p>Próximamente podrás descargar aquí:</p>

    <div class="file-actions">
      <button type="button" disabled>Cotización PDF</button>
      <button type="button" disabled>Aviso de privacidad PDF</button>
    </div>
  </div>

  <a class="home-link" href="/">Regresar al inicio</a>
</section>

<style>
  .step {
    display: grid;
    gap: 0.7rem;
    min-height: 0;
  }

  .success-header {
    display: grid;
    gap: 0.34rem;
  }

  .eyebrow,
  .document-kicker {
    margin: 0;
    color: #8a6b00;
    font-size: 0.66rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  h2 {
    margin: 0;
    color: #172033;
    font-size: clamp(1.25rem, 5.6vw, 1.8rem);
    line-height: 1;
    letter-spacing: -0.04em;
  }

  h3 {
    margin: 0;
    color: #172033;
    font-size: clamp(0.95rem, 4vw, 1.25rem);
    line-height: 1.08;
    letter-spacing: -0.03em;
  }

  .success-message {
    margin: 0;
    color: #475569;
    font-size: 0.78rem;
    line-height: 1.38;
  }

  .success-message strong {
    color: #172033;
  }

  .quote-document,
  .future-files {
    border: 1.5px solid #e2e8f0;
    border-radius: 15px;
    background: #fff;
  }

  .quote-document {
    display: grid;
    gap: 0.6rem;
    padding: 0.7rem;
  }

  .document-header {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(125px, 0.7fr);
    gap: 0.65rem;
    align-items: start;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 0.55rem;
  }

  .client-box,
  .meta-grid div {
    display: grid;
    gap: 0.14rem;
    border-radius: 11px;
    background: #f8fafc;
    padding: 0.52rem;
  }

  .client-box span,
  .meta-grid span {
    color: #64748b;
    font-size: 0.62rem;
    font-weight: 850;
    text-transform: uppercase;
  }

  .client-box strong,
  .meta-grid strong {
    color: #172033;
    font-size: 0.74rem;
    line-height: 1.22;
  }

  .client-box small,
  .meta-grid small {
    color: #64748b;
    font-size: 0.66rem;
    line-height: 1.2;
  }

  .meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.45rem;
  }

  .quote-table {
    display: grid;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
  }

  .quote-row {
    display: grid;
    grid-template-columns: 0.5fr 1.45fr 0.9fr;
  }

  .quote-row > * {
    padding: 0.5rem;
    border-right: 1px solid #e2e8f0;
  }

  .quote-row > *:last-child {
    border-right: 0;
  }

  .quote-row-head {
    background: #172033;
    color: #fff;
  }

  .quote-row-head span {
    font-size: 0.58rem;
    font-weight: 900;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .quantity-cell,
  .amount-cell,
  .service-cell {
    display: grid;
    align-content: center;
    gap: 0.12rem;
  }

  .quantity-cell strong {
    color: #172033;
    font-size: 0.98rem;
    line-height: 1;
  }

  .quantity-cell span {
    color: #64748b;
    font-size: 0.68rem;
    font-weight: 800;
  }

  .service-cell strong {
    color: #172033;
    font-size: 0.74rem;
  }

  .service-cell p {
    margin: 0;
    color: #475569;
    font-size: 0.68rem;
    line-height: 1.32;
  }

  .amount-cell {
    justify-items: end;
    text-align: right;
  }

  .amount-cell strong {
    color: #14532d;
    font-size: clamp(0.92rem, 4.2vw, 1.2rem);
    line-height: 1;
  }

  .document-note {
    border-radius: 11px;
    background: #fffbeb;
    color: #78350f;
    font-size: 0.68rem;
    line-height: 1.34;
    padding: 0.55rem;
  }

  .future-files {
    display: grid;
    gap: 0.45rem;
    padding: 0.62rem;
    background: #f8fafc;
  }

  .future-files p {
    margin: 0;
    color: #475569;
    font-size: 0.72rem;
    font-weight: 750;
  }

  .file-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.45rem;
  }

  .file-actions button {
    min-height: 33px;
    border: 1px dashed #cbd5e1;
    border-radius: 999px;
    background: #fff;
    color: #64748b;
    font-size: 0.66rem;
    font-weight: 850;
  }

  .file-actions button:disabled {
    opacity: 0.72;
  }

  .home-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 36px;
    border-radius: 999px;
    background: #172033;
    color: #fff;
    font-size: 0.76rem;
    font-weight: 900;
    text-decoration: none;
  }

  @media (max-width: 520px) {
    .document-header {
      grid-template-columns: 1fr;
      gap: 0.42rem;
    }

    .meta-grid {
      grid-template-columns: 1fr 1fr;
    }

    .quote-row > * {
      padding: 0.42rem;
    }
  }
</style>
