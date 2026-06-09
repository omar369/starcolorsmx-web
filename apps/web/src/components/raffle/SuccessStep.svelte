<script lang="ts">
  import type { RaffleEntry } from "../../lib/raffle";

  export let entries: RaffleEntry[] = [];
  export let onRestart: () => void;
</script>

<article class="card success-card">
  <p class="eyebrow">Paso 6</p>
  <h2>¡Tus números quedaron registrados!</h2>

  <p class="muted">
    Guarda esta información. También podrás ver tus números en tu espacio de cliente.
  </p>

  <ul class="number-list">
    {#each entries as entry}
      <li>Número {entry.selected_number}</li>
    {/each}
  </ul>

  <div class="actions">
    <button class="primary-button" type="button" on:click={onRestart}>
      Registrar más boletos
    </button>

    <a class="secondary-button" href="/hub">Volver al hub</a>
  </div>
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

  .success-card {
    text-align: center;
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

  .number-list {
    display: grid;
    gap: 0.5rem;
    margin: 1.25rem 0 0;
    padding: 0;
    list-style: none;
  }

  .number-list li {
    padding: 0.9rem;
    border-radius: 16px;
    background: rgba(159, 255, 194, 0.12);
    color: #9fffc2;
    font-size: 1.2rem;
    font-weight: 900;
  }

  .actions {
    display: grid;
    gap: 0.75rem;
    margin-top: 1.25rem;
  }

  .primary-button,
  .secondary-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 44px;
    padding: 0 1.1rem;
    border-radius: 999px;
    font-weight: 850;
    text-decoration: none;
    cursor: pointer;
  }

  .primary-button {
    border: 0;
    background: #ffffff;
    color: #000000;
  }

  .secondary-button {
    border: 1px solid rgba(255, 255, 255, 0.16);
    background: transparent;
    color: #ffffff;
  }
</style>
