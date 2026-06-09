<script lang="ts">
  import type { RaffleBranch, RaffleStatus } from "../../lib/raffle";

  export let raffle: RaffleStatus;
  export let onSelect: (branch: RaffleBranch) => void;
</script>

<header class="header">
  <p class="eyebrow">Sorteo de temporada</p>
  <h1>{raffle.prize_title ?? raffle.title}</h1>
  <p class="muted">Paso 1: Elige la sucursal donde realizaste tu compra.</p>
</header>

<div class="branch-grid">
  {#each raffle.branches as branch}
    <button class="branch-card" type="button" on:click={() => onSelect(branch)}>
      <div class="branch-image">
        {#if branch.image_url}
          <img src={branch.image_url} alt={branch.name} />
        {:else}
          <span>{branch.name.slice(0, 1)}</span>
        {/if}
      </div>

      <div>
        <h2>{branch.name}</h2>
        <p>Números {branch.number_start}–{branch.number_end}</p>
      </div>
    </button>
  {/each}
</div>

<style>
  .header {
    display: grid;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .eyebrow {
    margin: 0;
    font-size: 0.75rem;
    font-weight: 850;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.65;
  }

  h1,
  h2,
  p {
    margin: 0;
  }

  h1 {
    font-size: clamp(2.25rem, 10vw, 4.5rem);
    line-height: 0.95;
  }

  .muted {
    color: rgba(255, 255, 255, 0.68);
  }

  .branch-grid {
    display: grid;
    gap: 1rem;
  }

  .branch-card {
    display: grid;
    grid-template-columns: 84px 1fr;
    gap: 1rem;
    width: 100%;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.05);
    color: inherit;
    text-align: left;
    cursor: pointer;
  }

  .branch-image {
    display: grid;
    place-items: center;
    width: 84px;
    aspect-ratio: 1;
    overflow: hidden;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.1);
    font-size: 2rem;
    font-weight: 900;
  }

  .branch-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .branch-card h2 {
    margin-bottom: 0.35rem;
  }

  @media (min-width: 760px) {
    .branch-grid {
      grid-template-columns: repeat(3, 1fr);
    }

    .branch-card {
      grid-template-columns: 1fr;
    }

    .branch-image {
      width: 100%;
    }
  }
</style>
