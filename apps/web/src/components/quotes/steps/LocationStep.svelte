<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};
</script>

<section class="step">
  <div class="step-heading">
    <p class="eyebrow">Ubicacion</p>
    <h2>Donde se hara el trabajo</h2>
    <p class="subtitle">
      El estado se usa en el calculo y el codigo postal ayuda a revisar la zona.
    </p>
  </div>

  <div class="form-grid">
    <label class="field" for="state">
      <span class="field-label">Estado <strong>*</strong></span>
      <select
        id="state"
        bind:value={form.state}
        aria-invalid={Boolean(errors.state)}
      >
        <option value="">Selecciona un estado</option>
        {#each options.states as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.state}
        <span class="field-error">{errors.state}</span>
      {/if}
    </label>

    <label class="field" for="city">
      <span class="field-label">Ciudad / municipio <strong>*</strong></span>
      <input
        id="city"
        type="text"
        placeholder="Ej. Queretaro"
        bind:value={form.city}
        autocomplete="address-level2"
        aria-invalid={Boolean(errors.city)}
      />
      {#if errors.city}
        <span class="field-error">{errors.city}</span>
      {/if}
    </label>

    <label class="field" for="postal_code">
      <span class="field-label">Codigo postal <strong>*</strong></span>
      <input
        id="postal_code"
        type="text"
        inputmode="numeric"
        placeholder="Ej. 76000"
        maxlength="5"
        bind:value={form.postal_code}
        autocomplete="postal-code"
        aria-invalid={Boolean(errors.postal_code)}
      />
      {#if errors.postal_code}
        <span class="field-error">{errors.postal_code}</span>
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

  select,
  input {
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
