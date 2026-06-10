<script lang="ts">
  import type { RaffleBranch, RaffleStatus } from "../../lib/raffle";
  import * as Card from "$lib/components/ui/card/index.js";

  // Svelte 5 props
  let { raffle, onSelect }: { raffle: RaffleStatus; onSelect: (branch: RaffleBranch) => void } = $props();
</script>

<header class="mb-8 text-center sm:text-left">
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

<div class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
  {#each raffle.branches as branch}
    <button
      type="button"
      onclick={() => onSelect(branch)}
      class="group text-left cursor-pointer w-full focus:outline-none focus-visible:ring-2 focus-visible:ring-[#e67a25] focus-visible:ring-offset-2 rounded-2xl"
    >
      <Card.Root class="h-full border-0 shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm group-hover:ring-2 group-hover:ring-[#e67a25]/50 flex flex-col">
        <!-- Contenedor de la Imagen con zoom -->
        <div class="relative w-full h-48 sm:h-44 md:h-48 overflow-hidden bg-gray-100 flex-shrink-0">
          {#if branch.image_url}
            <img 
              src={branch.image_url} 
              alt={branch.name} 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out" 
            />
          {:else}
            <!-- Fallback de iniciales si no hay imagen -->
            <div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-[#e67a25]/10 to-[#f59e0b]/10 text-[#e67a25] text-4xl font-black">
              {branch.name.slice(0, 2).toUpperCase()}
            </div>
          {/if}
          <!-- Overlay sutil -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/10 via-transparent to-transparent"></div>
        </div>

        <Card.Content class="p-5 flex-1 flex flex-col justify-between gap-5">
          <div class="space-y-1.5">
            <h3 class="text-xl font-black text-[#111111] group-hover:text-[#e67a25] transition-colors leading-tight">
              {branch.name}
            </h3>
            <p class="text-xs text-gray-500 font-bold uppercase tracking-wider flex items-center gap-2">
              <span class="inline-block w-2.5 h-2.5 rounded-full bg-[#006b3f] shadow-sm animate-pulse"></span>
              Números {branch.number_start} al {branch.number_end}
            </p>
          </div>

          <!-- Botón simulado -->
          <div class="w-full py-3 px-4 rounded-xl text-center text-xs font-black uppercase tracking-wider border-2 border-gray-100 group-hover:border-[#e67a25] group-hover:bg-[#e67a25] group-hover:text-white text-[#111] transition-all duration-300">
            Seleccionar Sucursal
          </div>
        </Card.Content>
      </Card.Root>
    </button>
  {/each}
</div>
