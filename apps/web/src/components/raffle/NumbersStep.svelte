<script lang="ts">
  import type { RaffleNumber, TicketValidationResult } from "../../lib/raffle";

  export let numbers: RaffleNumber[] = [];
  export let acceptedTickets: TicketValidationResult[] = [];
  export let selectedNumberIds: number[] = [];
  export let loading = false;
  export let error = "";
  export let onBack: () => void;
  export let onContinue: () => void;

  function toggleNumber(numberId: number) {
    const numberIsSelected = selectedNumberIds.includes(numberId);

    if (numberIsSelected) {
      selectedNumberIds = selectedNumberIds.filter((id) => id !== numberId);
      return;
    }

    if (selectedNumberIds.length >= acceptedTickets.length) {
      return;
    }

    selectedNumberIds = [...selectedNumberIds, numberId];
  }

  function numberLabel(numberId: number) {
    const number = numbers.find((item) => item.id === numberId);
    return number?.number ?? numberId;
  }
</script>

<article class="card">
  <button class="back-button" type="button" on:click={onBack}>
    Volver al resultado
  </button>

  <p class="eyebrow">Paso 4</p>
  <h2>Elige tus números</h2>

  <p class="muted">
    Puedes elegir {acceptedTickets.length}
    {acceptedTickets.length === 1 ? " número" : " números"}.
  </p>

  <p class="counter">
    Seleccionados: {selectedNumberIds.length} / {acceptedTickets.length}
  </p>

  {#if loading}
    <p class="muted">Cargando números...</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else}
    <div class="number-grid" aria-label="Tablero de números">
      {#each numbers as item}
        {@const selected = selectedNumberIds.includes(item.id)}
        {@const taken = item.status !== "available"}

        <button
          class:selected
          class:taken
          type="button"
          disabled={taken}
          on:click={() => toggleNumber(item.id)}
        >
          {item.number}
        </button>
      {/each}
    </div>

    {#if selectedNumberIds.length > 0}
      <p class="selected-list">
        Elegidos: {selectedNumberIds.map(numberLabel).join(", ")}
      </p>
    {/if}

    <button
      class="primary-button"
      type="button"
      disabled={selectedNumberIds.length !== acceptedTickets.length}
      on:click={onContinue}
    >
      Revisar selección
    </button>
  {/if}
</article>

<style>
  .card {
    width: 100%;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.05);
    color: inherit;
  }

  .back-button {
    width: fit-content;
    margin-bottom: 1rem;
    border: 0;
    background: transparent;
    color: rgba(255, 255, 255, 0.72);
    font-weight: 800;
    cursor: pointer;
  }

  .eyebrow {
    margin: 0 0 0.5rem;
    font-size: 0.75rem;
    font-weight: 850;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.65;
  }

  h2,
  p {
    margin: 0;
  }

  h2 {
    margin-bottom: 0.75rem;
  }

  .muted {
    color: rgba(255, 255, 255, 0.68);
  }

  .error {
    color: #ff7373;
  }

  .counter,
  .selected-list {
    margin-top: 1rem;
    color: rgba(255, 255, 255, 0.72);
    font-weight: 800;
  }

  .number-grid {
    display: grid;
    grid-template-columns: repeat(11, minmax(0, 1fr));
    gap: 0.28rem;
    margin-top: 1rem;
  }

  .number-grid button {
    min-width: 0;
    min-height: 32px;
    padding: 0;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 9px;
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
    font-size: 0.72rem;
    font-weight: 850;
    cursor: pointer;
  }

  .number-grid button.selected {
    border-color: #ffffff;
    background: #ffffff;
    color: #000000;
  }

  .number-grid button.taken {
    opacity: 0.25;
    cursor: not-allowed;
  }

  .primary-button {
    width: 100%;
    min-height: 44px;
    margin-top: 1rem;
    padding: 0 1.1rem;
    border: 0;
    border-radius: 999px;
    background: #ffffff;
    color: #000000;
    font-weight: 850;
    cursor: pointer;
  }

  .primary-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
</style>
