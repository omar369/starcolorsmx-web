<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};

  function togglePreparation(optionId: string) {
    if (form.preparation.includes(optionId)) {
      form.preparation = form.preparation.filter((id) => id !== optionId);
      return;
    }

    form.preparation = [...form.preparation, optionId];
  }

  function isPreparationSelected(optionId: string) {
    return form.preparation.includes(optionId);
  }
</script>

<section class="step">
  <div class="step-heading">
    <p class="eyebrow">Superficie</p>
    <h2>Estado del área</h2>
    <p class="subtitle">
      Describe cómo está la superficie y qué preparación necesita antes de
      pintar.
    </p>
  </div>

  <div class="form-grid">
    <label class="field field-half" for="surface_state">
      <span class="field-label">Estado <strong>*</strong></span>
      <select
        id="surface_state"
        bind:value={form.surface_state}
        aria-invalid={Boolean(errors.surface_state)}
      >
        <option value="">Selecciona</option>
        {#each options.surface_states as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.surface_state}
        <span class="field-error">{errors.surface_state}</span>
      {/if}
    </label>

    <label class="field field-half" for="texture">
      <span class="field-label">Textura <strong>*</strong></span>
      <select
        id="texture"
        bind:value={form.texture}
        aria-invalid={Boolean(errors.texture)}
      >
        <option value="">Selecciona</option>
        {#each options.textures as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.texture}
        <span class="field-error">{errors.texture}</span>
      {/if}
    </label>

    <label class="field field-full" for="area_protection">
      <span class="field-label">Protección del área <strong>*</strong></span>
      <select
        id="area_protection"
        bind:value={form.area_protection}
        aria-invalid={Boolean(errors.area_protection)}
      >
        <option value="">Selecciona una opción</option>
        {#each options.area_protections as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.area_protection}
        <span class="field-error">{errors.area_protection}</span>
      {/if}
    </label>

    <div class="field field-full">
      <div class="preparation-header">
        <span class="field-label"
          >Preparación de superficie <strong>*</strong></span
        >
        <span class="field-hint">Puedes elegir más de una</span>
      </div>

      <div class="preparation-grid" aria-invalid={Boolean(errors.preparation)}>
        {#each options.preparations as option}
          <button
            type="button"
            class:selected={isPreparationSelected(option.id)}
            class="preparation-option"
            on:click={() => togglePreparation(option.id)}
            aria-pressed={isPreparationSelected(option.id)}
          >
            <span class="radio-dot" aria-hidden="true"></span>
            <span>{option.name}</span>
          </button>
        {/each}
      </div>

      {#if errors.preparation}
        <span class="field-error">{errors.preparation}</span>
      {/if}
    </div>
  </div>
</section>

<style>
  .step {
    display: grid;
    gap: 0.9rem;
  }

  .step-heading {
    display: grid;
    gap: 0.34rem;
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
    font-size: clamp(1.38rem, 5.6vw, 2rem);
    line-height: 1;
    letter-spacing: -0.035em;
  }

  .subtitle {
    margin: 0;
    color: #526070;
    font-size: 0.82rem;
    line-height: 1.4;
  }

  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.72rem;
    align-items: start;
  }

  .field {
    display: grid;
    gap: 0.28rem;
    min-width: 0;
  }

  .field-half {
    grid-column: span 1;
  }

  .field-full {
    grid-column: 1 / -1;
  }

  .field-label {
    color: #273549;
    font-size: 0.78rem;
    font-weight: 850;
    line-height: 1.2;
  }

  .field-label strong {
    color: #d97706;
  }

  .field-hint {
    color: #64748b;
    font-size: 0.7rem;
    font-weight: 750;
  }

  select {
    width: 100%;
    min-height: 40px;
    border: 1.5px solid #d9e0ea;
    border-radius: 10px;
    background: #fff;
    color: #172033;
    font: inherit;
    font-size: 0.86rem;
    padding: 0.56rem 0.68rem;
  }

  select:focus {
    border-color: #f5b700;
    box-shadow: 0 0 0 3px rgba(245, 183, 0, 0.16);
    outline: none;
  }

  [aria-invalid="true"] {
    border-color: #e11d48;
  }

  .preparation-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.75rem;
  }

  .preparation-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.45rem;
  }

  .preparation-option {
    display: flex;
    align-items: center;
    gap: 0.42rem;
    min-height: 36px;
    border: 1.5px solid #d9e0ea;
    border-radius: 10px;
    background: #fff;
    color: #273549;
    padding: 0.45rem 0.52rem;
    font: inherit;
    font-size: 0.76rem;
    font-weight: 780;
    text-align: left;
    cursor: pointer;
  }

  .preparation-option.selected {
    border-color: #f5b700;
    background: #fff8dc;
    color: #172033;
  }

  .radio-dot {
    width: 0.72rem;
    height: 0.72rem;
    flex: 0 0 auto;
    border: 2px solid #cbd5e1;
    border-radius: 999px;
    background: #fff;
  }

  .preparation-option.selected .radio-dot {
    border-color: #172033;
    box-shadow: inset 0 0 0 3px #f5b700;
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
      gap: 0.9rem;
    }

    select {
      min-height: 44px;
      font-size: 0.92rem;
      padding: 0.68rem 0.82rem;
    }

    .field-label {
      font-size: 0.84rem;
    }

    .subtitle {
      font-size: 0.9rem;
    }

    .preparation-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 0.55rem;
    }

    .preparation-option {
      min-height: 40px;
      font-size: 0.82rem;
      padding: 0.55rem 0.62rem;
    }
  }
</style>
