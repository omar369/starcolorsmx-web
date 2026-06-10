<script lang="ts">
  import type { RaffleNumber, TicketValidationResult } from "../../lib/raffle";
  import { Button } from "$lib/components/ui/button/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { ChevronLeft, HelpCircle } from "@lucide/svelte";

  // Svelte 5 props with bindable selectedNumberIds
  let {
    numbers = [],
    acceptedTickets = [],
    selectedNumberIds = $bindable([]),
    loading = false,
    error = "",
    onBack,
    onContinue,
  }: {
    numbers: RaffleNumber[];
    acceptedTickets: TicketValidationResult[];
    selectedNumberIds: number[];
    loading: boolean;
    error: string;
    onBack: () => void;
    onContinue: () => void;
  } = $props();

  function toggleNumber(numberId: number) {
    const isSelected = selectedNumberIds.includes(numberId);
    if (isSelected) {
      selectedNumberIds = selectedNumberIds.filter((id) => id !== numberId);
      return;
    }
    if (selectedNumberIds.length >= acceptedTickets.length) return;
    selectedNumberIds = [...selectedNumberIds, numberId];
  }

  function numberLabel(numberId: number) {
    return numbers.find((n) => n.id === numberId)?.number ?? numberId;
  }
</script>

<div class="w-full max-w-2xl mx-auto space-y-4">
  <button
    type="button"
    onclick={onBack}
    class="inline-flex items-center gap-1.5 text-sm font-bold text-[#e67a25] hover:text-[#d96f20] transition-colors focus:outline-none"
  >
    <ChevronLeft class="h-4 w-4" />
    Volver al resultado
  </button>

  <Card.Root class="border-0 shadow-lg rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm">
    <div class="h-1.5 w-full bg-gradient-to-r from-[#e67a25] to-[#f59e0b]"></div>

    <Card.Header class="pb-4">
      <Card.Description class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1">
        Paso 4 de 6
      </Card.Description>
      <Card.Title class="text-2xl font-black text-[#111111] leading-tight">
        Elige tus números
      </Card.Title>
      <p class="text-sm text-gray-500 font-medium">
        Tienes <span class="font-black text-[#e67a25]">{acceptedTickets.length}</span> {acceptedTickets.length === 1 ? "número disponible" : "números disponibles"} para elegir.
      </p>
    </Card.Header>

    <Card.Content class="space-y-6">
      <!-- Contador e Info -->
      <div class="flex items-center justify-between flex-wrap gap-3 p-3 bg-[#e67a25]/5 border border-[#e67a25]/10 rounded-xl">
        <div class="inline-flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-[#e67a25] animate-pulse"></span>
          <p class="text-sm font-black text-[#e67a25]">
            Seleccionados: {selectedNumberIds.length} de {acceptedTickets.length}
          </p>
        </div>
        
        <div class="flex items-center gap-1 text-xs text-gray-400 font-bold">
          <HelpCircle class="h-3.5 w-3.5" />
          <span>Haz clic en un número libre</span>
        </div>
      </div>

      {#if loading}
        <div class="py-12 text-center">
          <div class="h-8 w-8 animate-spin rounded-full border-4 border-[#e67a25]/20 border-t-[#e67a25] mx-auto mb-2"></div>
          <p class="text-sm text-gray-400 font-bold">Cargando tablero...</p>
        </div>
      {:else if error}
        <div class="p-3.5 rounded-xl bg-red-50 border border-red-100 text-red-700 text-sm font-bold" role="alert">
          {error}
        </div>
      {:else}
        <!-- Tablero de números -->
        <div class="space-y-3">
          <p class="text-xs font-black text-[#111111] uppercase tracking-wider">Tablero de números:</p>
          
          <div
            class="grid gap-2"
            style="grid-template-columns: repeat(auto-fill, minmax(46px, 1fr))"
            aria-label="Tablero de números"
          >
            {#each numbers as item}
              {@const selected = selectedNumberIds.includes(item.id)}
              {@const taken = item.status !== "available"}
              <button
                type="button"
                disabled={taken}
                onclick={() => toggleNumber(item.id)}
                class="h-11 w-full min-w-0 rounded-xl text-xs font-black transition-all duration-200 border-2
                  {taken
                    ? 'bg-gray-50 text-gray-300 cursor-not-allowed border-gray-100'
                    : selected
                      ? 'bg-[#e67a25] text-white shadow-md scale-105 border-[#e67a25]'
                      : 'bg-white text-[#111] border-gray-200 hover:border-[#e67a25] hover:text-[#e67a25] hover:bg-[#e67a25]/5 cursor-pointer'}"
              >
                {item.number}
              </button>
            {/each}
          </div>
        </div>

        <!-- Resumen de selección -->
        {#if selectedNumberIds.length > 0}
          <div class="p-4 bg-gray-50 rounded-xl border border-gray-100 space-y-1 animate-in fade-in slide-in-from-bottom-2 duration-200">
            <p class="text-[0.7rem] font-black uppercase tracking-wider text-gray-400">Números elegidos:</p>
            <p class="text-[1.1rem] font-black text-[#e67a25] tracking-wider leading-none">
              #{selectedNumberIds.map(numberLabel).join(", #")}
            </p>
          </div>
        {/if}

        <Button
          type="button"
          disabled={selectedNumberIds.length !== acceptedTickets.length}
          onclick={onContinue}
          class="w-full h-12 rounded-xl bg-[#e67a25] hover:bg-[#d96f20] text-white font-black uppercase tracking-wider shadow-md hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Revisar selección →
        </Button>
      {/if}
    </Card.Content>
  </Card.Root>
</div>
