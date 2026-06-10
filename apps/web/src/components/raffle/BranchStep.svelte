<script lang="ts">
  import type { RaffleBranch, RaffleStatus } from "../../lib/raffle";
  import * as Card from "$lib/components/ui/card/index.js";

  // Svelte 5 props
  let { raffle, onSelect }: { raffle: RaffleStatus; onSelect: (branch: RaffleBranch) => void } = $props();
</script>

<header class="mb-8">
  <p class="mb-2 text-[0.75rem] font-black uppercase tracking-[0.14em] text-[#e67a25]">
    Sorteo de temporada
  </p>
  <h2 class="text-3xl md:text-4xl font-black text-[#111111] leading-tight mb-3">
    {raffle.prize_title ?? raffle.title}
  </h2>
  <p class="text-[0.95rem] text-gray-500 font-medium">
    Paso 1: Selecciona la sucursal donde realizaste tu compra para validar tus boletos.
  </p>
</header>

<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
  {#each raffle.branches as branch}
    <button
      type="button"
      onclick={() => onSelect(branch)}
      class="group text-left cursor-pointer w-full focus:outline-none"
    >
      <Card.Root class="h-full border-0 shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm group-hover:ring-2 group-hover:ring-[#e67a25]/50">
        <Card.Content class="p-6 flex flex-col gap-4">
          <!-- Imagen / inicial -->
          <div class="flex items-center justify-center w-14 h-14 rounded-xl bg-[#e67a25]/10 text-[#e67a25] text-2xl font-black overflow-hidden shadow-inner group-hover:scale-105 transition-transform duration-300">
            {#if branch.image_url}
              <img src={branch.image_url} alt={branch.name} class="w-full h-full object-cover" />
            {:else}
              {branch.name.slice(9, 11) || branch.name.slice(0, 1)}
            {/if}
          </div>

          <div>
            <h3 class="text-lg font-black text-[#111111] group-hover:text-[#e67a25] transition-colors leading-tight mb-1">
              {branch.name}
            </h3>
            <p class="text-[0.8rem] text-gray-400 font-bold uppercase tracking-wider">
              Números {branch.number_start}–{branch.number_end}
            </p>
          </div>
        </Card.Content>
      </Card.Root>
    </button>
  {/each}
</div>
