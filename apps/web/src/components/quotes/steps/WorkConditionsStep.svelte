<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};
</script>

<section class="step">
  <div class="step-heading">
    <p class="eyebrow">Condiciones</p>
    <h2>Como se puede trabajar ahi</h2>
    <p class="subtitle">
      Estos datos ayudan a estimar complejidad, acceso, horario y riesgo.
    </p>
  </div>

  <div class="form-grid">
    <label class="field" for="advance_difficulty">
      <span class="field-label">Dificultad de avance <strong>*</strong></span>
      <select
        id="advance_difficulty"
        bind:value={form.advance_difficulty}
        aria-invalid={Boolean(errors.advance_difficulty)}
      >
        <option value="">Selecciona una opcion</option>
        {#each options.advance_difficulties as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.advance_difficulty}
        <span class="field-error">{errors.advance_difficulty}</span>
      {/if}
    </label>

    <label class="field" for="occupancy">
      <span class="field-label">Ocupacion del inmueble <strong>*</strong></span>
      <select
        id="occupancy"
        bind:value={form.occupancy}
        aria-invalid={Boolean(errors.occupancy)}
      >
        <option value="">Selecciona una opcion</option>
        {#each options.occupancies as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.occupancy}
        <span class="field-error">{errors.occupancy}</span>
      {/if}
    </label>

    <label class="field" for="height_risk">
      <span class="field-label">Altura y riesgo <strong>*</strong></span>
      <select
        id="height_risk"
        bind:value={form.height_risk}
        aria-invalid={Boolean(errors.height_risk)}
      >
        <option value="">Selecciona una opcion</option>
        {#each options.height_risks as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.height_risk}
        <span class="field-error">{errors.height_risk}</span>
      {/if}
    </label>

    <label class="field" for="schedule">
      <span class="field-label">Horario <strong>*</strong></span>
      <select
        id="schedule"
        bind:value={form.schedule}
        aria-invalid={Boolean(errors.schedule)}
      >
        <option value="">Selecciona una opcion</option>
        {#each options.schedules as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.schedule}
        <span class="field-error">{errors.schedule}</span>
      {/if}
    </label>

    <label class="field field--wide" for="place_activities">
      <span class="field-label">Actividades en el lugar</span>
      <textarea
        id="place_activities"
        bind:value={form.place_activities}
        rows="2"
        maxlength="400"
        placeholder="Ej. casa habitada, oficina con trafico, local abierto..."
      ></textarea>
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
    gap: 0.85rem;
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
  textarea {
    width: 100%;
    border: 1.5px solid #d9e0ea;
    border-radius: 12px;
    background: #fff;
    color: #172033;
    font: inherit;
    font-size: 0.95rem;
    padding: 0.72rem 0.9rem;
  }

  select {
    min-height: 46px;
  }

  textarea {
    min-height: 70px;
    resize: none;
  }

  select:focus,
  textarea:focus {
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
