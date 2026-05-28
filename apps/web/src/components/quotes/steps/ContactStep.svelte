<script lang="ts">
  import type { QuoteForm } from "../types";

  export let form: QuoteForm;
  export let errors: Record<string, string> = {};

  $: contactLabel =
    form.contact_method === "whatsapp"
      ? "Numero de WhatsApp"
      : form.contact_method === "email"
        ? "Correo electronico"
        : "Dato de contacto";

  $: contactPlaceholder =
    form.contact_method === "whatsapp"
      ? "Ej. 4421234567"
      : form.contact_method === "email"
        ? "ejemplo@correo.com"
        : "Selecciona primero un metodo";

  $: contactType =
    form.contact_method === "whatsapp"
      ? "tel"
      : form.contact_method === "email"
        ? "email"
        : "text";
</script>

<section class="step">
  <div class="step-heading">
    <p class="eyebrow">Contacto</p>
    <h2>A donde enviamos la precotizacion</h2>
    <p class="subtitle">
      No necesitas crear cuenta para recibir la primera estimacion.
    </p>
  </div>

  <div class="form-grid">
    <label class="field" for="customer_name">
      <span class="field-label">Nombre del cliente <strong>*</strong></span>
      <input
        id="customer_name"
        type="text"
        placeholder="Ej. Omar Castillo"
        bind:value={form.customer_name}
        autocomplete="name"
        aria-invalid={Boolean(errors.customer_name)}
      />
      {#if errors.customer_name}
        <span class="field-error">{errors.customer_name}</span>
      {/if}
    </label>

    <label class="field" for="contact_method">
      <span class="field-label">Metodo de contacto <strong>*</strong></span>
      <select
        id="contact_method"
        bind:value={form.contact_method}
        aria-invalid={Boolean(errors.contact_method)}
      >
        <option value="">Selecciona una opcion</option>
        <option value="whatsapp">WhatsApp</option>
        <option value="email">Email</option>
      </select>
      {#if errors.contact_method}
        <span class="field-error">{errors.contact_method}</span>
      {/if}
    </label>

    <label class="field" for="contact_value">
      <span class="field-label">{contactLabel} <strong>*</strong></span>
      <input
        id="contact_value"
        type={contactType}
        placeholder={contactPlaceholder}
        bind:value={form.contact_value}
        disabled={!form.contact_method}
        autocomplete={form.contact_method === "email" ? "email" : "tel"}
        aria-invalid={Boolean(errors.contact_value)}
      />
      {#if errors.contact_value}
        <span class="field-error">{errors.contact_value}</span>
      {/if}
    </label>

    <label class="checkbox-label">
      <input type="checkbox" bind:checked={form.wants_offers} />
      <span>Quiero recibir ofertas y recomendaciones de pintura.</span>
    </label>
  </div>
</section>

<style>
  .step {
    display: grid;
    gap: 1.1rem;
  }

  .step-heading {
    display: grid;
    gap: 0.45rem;
  }

  .eyebrow {
    margin: 0;
    color: #8a6b00;
    font-size: 0.72rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  h2 {
    margin: 0;
    color: #101827;
    font-size: clamp(1.55rem, 6vw, 2.2rem);
    line-height: 1.05;
  }

  .subtitle {
    margin: 0;
    color: #526070;
    font-size: 0.9rem;
    line-height: 1.55;
  }

  .form-grid {
    display: grid;
    gap: 0.9rem;
  }

  .field {
    display: grid;
    gap: 0.35rem;
  }

  .field-label {
    color: #273549;
    font-size: 0.86rem;
    font-weight: 850;
  }

  .field-label strong {
    color: #d97706;
  }

  select,
  input[type="text"],
  input[type="tel"],
  input[type="email"] {
    width: 100%;
    min-height: 46px;
    border: 1.5px solid #d9e0ea;
    border-radius: 12px;
    background: #fff;
    color: #172033;
    font: inherit;
    font-size: 0.95rem;
    padding: 0.72rem 0.9rem;
  }

  select:focus,
  input:focus {
    border-color: #f5b700;
    box-shadow: 0 0 0 3px rgba(245, 183, 0, 0.18);
    outline: none;
  }

  input:disabled {
    background: #f1f5f9;
    color: #94a3b8;
    cursor: not-allowed;
  }

  [aria-invalid="true"] {
    border-color: #e11d48;
  }

  .field-error {
    color: #be123c;
    font-size: 0.78rem;
    font-weight: 750;
    line-height: 1.45;
  }

  .checkbox-label {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    color: #526070;
    font-size: 0.875rem;
    line-height: 1.45;
  }

  .checkbox-label input {
    margin-top: 0.2rem;
  }
</style>
