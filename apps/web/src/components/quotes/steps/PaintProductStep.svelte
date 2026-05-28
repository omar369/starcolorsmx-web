<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};
</script>

<section class="step">
  <div class="step-heading">
    <p class="eyebrow">Pintura</p>
    <h2>Producto y color</h2>
    <p class="subtitle">
      Elige la pintura vinilica y la intensidad del color. El calculo interno
      aplica el costo correspondiente.
    </p>
  </div>

  <div class="form-grid">
    <label class="field" for="paint_product">
      <span class="field-label">Pintura vinilica <strong>*</strong></span>
      <select
        id="paint_product"
        bind:value={form.paint_product}
        aria-invalid={Boolean(errors.paint_product)}
      >
        <option value="">Selecciona una pintura</option>
        {#each options.paints as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.paint_product}
        <span class="field-error">{errors.paint_product}</span>
      {/if}
    </label>

    <label class="field" for="color_intensity">
      <span class="field-label">Intensidad del color <strong>*</strong></span>
      <select
        id="color_intensity"
        bind:value={form.color_intensity}
        aria-invalid={Boolean(errors.color_intensity)}
      >
        <option value="">Selecciona una opcion</option>
        {#each options.color_intensities as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.color_intensity}
        <span class="field-error">{errors.color_intensity}</span>
      {/if}
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

  select {
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

  select:focus {
    border-color: #f5b700;
    box-shadow: 0 0 0 3px rgba(245, 183, 0, 0.18);
    outline: none;
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
</style>
