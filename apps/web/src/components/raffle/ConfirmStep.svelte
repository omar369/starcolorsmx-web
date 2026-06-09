<script lang="ts">
  import type { RaffleNumber, TicketValidationResult } from "../../lib/raffle";

  export let acceptedTickets: TicketValidationResult[] = [];
  export let numbers: RaffleNumber[] = [];
  export let selectedNumberIds: number[] = [];
  export let loading = false;
  export let error = "";
  export let onBack: () => void;
  export let onConfirm: () => void;

  function findNumber(numberId: number) {
    return numbers.find((item) => item.id === numberId);
  }
</script>

<article class="card">
  <button class="back-button" type="button" on:click={onBack}>
    Cambiar números
  </button>

  <p class="eyebrow">Paso 5</p>
  <h2>Confirma tu selección</h2>

  <p class="muted">
    Revisa que tus números estén correctos antes de confirmar.
  </p>

  <ul class="confirm-list">
    {#each acceptedTickets as ticket, index}
      {@const number = findNumber(selectedNumberIds[index])}

      <li>
        <span>Boleto •••• {ticket.code_last4}</span>
        <strong>Número {number?.number}</strong>
      </li>
    {/each}
  </ul>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <button
    class="primary-button"
    type="button"
    disabled={loading}
    on:click={onConfirm}
  >
    {loading ? "Confirmando..." : "Confirmar mis números"}
  </button>
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

  .confirm-list {
    display: grid;
    gap: 0.65rem;
    margin: 1.25rem 0 0;
    padding: 0;
    list-style: none;
  }

  .confirm-list li {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.9rem;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.08);
  }

  .error {
    margin-top: 1rem;
    color: #ff7373;
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
