<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};
</script>

<section class="step">
  <div class="step-heading">
    <p class="eyebrow">Proyecto</p>
    <h2>¿Qué espacio se va a pintar?</h2>
    <p class="subtitle">
      Indica el inmueble, la zona del trabajo y el área aproximada.
    </p>
  </div>

  <div class="form-grid">
    <label class="field field-full" for="property_type">
      <span class="field-label">Tipo de inmueble <strong>*</strong></span>
      <select
        id="property_type"
        bind:value={form.property_type}
        aria-invalid={Boolean(errors.property_type)}
      >
        <option value="">Selecciona una opción</option>
        {#each options.property_types as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.property_type}
        <span class="field-error">{errors.property_type}</span>
      {/if}
    </label>

    <label class="field field-full" for="work_location">
      <span class="field-label">Ubicación del trabajo <strong>*</strong></span>
      <select
        id="work_location"
        bind:value={form.work_location}
        aria-invalid={Boolean(errors.work_location)}
      >
        <option value="">Selecciona una opción</option>
        {#each options.work_locations as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.work_location}
        <span class="field-error">{errors.work_location}</span>
      {/if}
    </label>

    <label class="field field-service" for="service_type">
      <span class="field-label">Tipo de servicio <strong>*</strong></span>
      <select
        id="service_type"
        bind:value={form.service_type}
        aria-invalid={Boolean(errors.service_type)}
      >
        <option value="">Selecciona</option>
        {#each options.service_types as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.service_type}
        <span class="field-error">{errors.service_type}</span>
      {/if}
    </label>

    <label class="field field-meters" for="square_meters">
      <span class="field-label">Área <strong>*</strong></span>
      <div class="input-wrapper">
        <input
          id="square_meters"
          bind:value={form.square_meters}
          type="number"
          min="1"
          step="0.01"
          placeholder="40"
          aria-invalid={Boolean(errors.square_meters)}
        />
        <span class="input-suffix" aria-hidden="true">m²</span>
      </div>
      {#if errors.square_meters}
        <span class="field-error">{errors.square_meters}</span>
      {/if}
    </label>
  </div>
</section>

<style>
  .step {
    display: grid;
    gap: 0.95rem;
  }

  .step-heading {
    display: grid;
    gap: 0.38rem;
  }

  .eyebrow {
    margin: 0;
    color: #8a6b00;
    font-size: 0.68rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  h2 {
    margin: 0;
    color: #101827;
    font-size: clamp(1.42rem, 6vw, 2.05rem);
    line-height: 1;
    letter-spacing: -0.04em;
  }

  .subtitle {
    margin: 0;
    color: #526070;
    font-size: 0.84rem;
    line-height: 1.42;
  }

  .form-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(108px, 0.58fr);
    gap: 0.75rem;
    align-items: start;
  }

  .field {
    display: grid;
    gap: 0.3rem;
    min-width: 0;
  }

  .field-full {
    grid-column: 1 / -1;
  }

  .field-service {
    grid-column: 1 / 2;
  }

  .field-meters {
    grid-column: 2 / 3;
  }

  .field-label {
    color: #273549;
    font-size: 0.8rem;
    font-weight: 850;
    line-height: 1.2;
  }

  .field-label strong {
    color: #d97706;
  }

  select,
  input {
    width: 100%;
    min-height: 41px;
    border: 1.5px solid #d9e0ea;
    border-radius: 11px;
    background: #fff;
    color: #172033;
    font: inherit;
    font-size: 0.88rem;
    padding: 0.6rem 0.72rem;
  }

  select {
    text-overflow: ellipsis;
  }

  select:focus,
  input:focus {
    border-color: #f5b700;
    box-shadow: 0 0 0 3px rgba(245, 183, 0, 0.16);
    outline: none;
  }

  [aria-invalid="true"] {
    border-color: #e11d48;
  }

  .input-wrapper {
    position: relative;
  }

  .input-wrapper input {
    padding-right: 2.35rem;
  }

  .input-suffix {
    position: absolute;
    right: 0.68rem;
    top: 50%;
    transform: translateY(-50%);
    color: #64748b;
    font-size: 0.75rem;
    font-weight: 850;
  }

  .field-error {
    color: #be123c;
    font-size: 0.68rem;
    font-weight: 750;
    line-height: 1.25;
  }

  @media (min-width: 680px) {
    .step {
      gap: 1.05rem;
    }

    .form-grid {
      grid-template-columns: minmax(0, 1fr) minmax(140px, 0.5fr);
      gap: 0.9rem;
    }

    select,
    input {
      min-height: 44px;
      font-size: 0.93rem;
      padding: 0.68rem 0.82rem;
    }

    .field-label {
      font-size: 0.84rem;
    }

    .subtitle {
      font-size: 0.9rem;
    }
  }
</style>
