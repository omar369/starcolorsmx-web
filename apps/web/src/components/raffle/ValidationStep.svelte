<script lang="ts">
  import type { RaffleBranch, TicketBatchValidation } from "../../lib/raffle";

  export let selectedBranch: RaffleBranch;
  export let validation: TicketBatchValidation;
  export let onBack: () => void;
  export let onContinue: () => void;
</script>

<article class="card">
  <button class="back-button" type="button" on:click={onBack}>
    Editar códigos
  </button>

  <p class="eyebrow">Paso 3</p>
  <h2>Resultado de tus boletos</h2>

  <p class="muted">
    Revisamos tus códigos para la sucursal {selectedBranch.name}.
  </p>

  <section class="summary-grid">
    <div>
      <strong>{validation.accepted_count}</strong>
      <span>Aceptados</span>
    </div>

    <div>
      <strong>{validation.rejected_count}</strong>
      <span>Rechazados</span>
    </div>
  </section>

  <ul class="validation-list">
    {#each validation.results as result}
      <li class:accepted={result.status === "accepted"}>
        <span>•••• {result.code_last4}</span>
        <strong
          >{result.status === "accepted" ? "Aceptado" : result.reason}</strong
        >
      </li>
    {/each}
  </ul>

  {#if validation.accepted_count > 0}
    <button class="primary-button" type="button" on:click={onContinue}>
      Elegir {validation.accepted_count}
      {validation.accepted_count === 1 ? " número" : " números"}
    </button>
  {:else}
    <button class="primary-button" type="button" on:click={onBack}>
      Intentar con otros códigos
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

  .summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-top: 1.25rem;
  }

  .summary-grid div {
    display: grid;
    gap: 0.25rem;
    padding: 1rem;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.08);
  }

  .summary-grid strong {
    font-size: 2rem;
    line-height: 1;
  }

  .summary-grid span {
    color: rgba(255, 255, 255, 0.65);
    font-size: 0.85rem;
    font-weight: 800;
  }

  .validation-list {
    display: grid;
    gap: 0.6rem;
    margin: 1.25rem 0 0;
    padding: 0;
    list-style: none;
  }

  .validation-list li {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.85rem;
    border-radius: 14px;
    background: rgba(255, 115, 115, 0.12);
    color: #ffb0b0;
  }

  .validation-list li.accepted {
    background: rgba(159, 255, 194, 0.12);
    color: #9fffc2;
  }

  .primary-button {
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
</style>
