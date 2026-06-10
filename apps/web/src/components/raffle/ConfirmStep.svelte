<script lang="ts">
  import type { RaffleNumber, TicketValidationResult } from "../../lib/raffle";
  import { Button } from "$lib/components/ui/button/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { ChevronLeft, CheckCircle2 } from "@lucide/svelte";

  // Svelte 5 props
  let {
    acceptedTickets = [],
    numbers = [],
    selectedNumberIds = [],
    loading = false,
    error = "",
    onBack,
    onConfirm,
  }: {
    acceptedTickets: TicketValidationResult[];
    numbers: RaffleNumber[];
    selectedNumberIds: number[];
    loading: boolean;
    error: string;
    onBack: () => void;
    onConfirm: () => void;
  } = $props();

  function findNumber(numberId: number) {
    return numbers.find((item) => item.id === numberId);
  }
</script>

<div class="w-full max-w-xl mx-auto space-y-4">
  <button
    type="button"
    onclick={onBack}
    class="inline-flex items-center gap-1.5 text-sm font-bold text-[#e67a25] hover:text-[#d96f20] transition-colors focus:outline-none"
  >
    <ChevronLeft class="h-4 w-4" />
    Cambiar números
  </button>

  <Card.Root class="border-0 shadow-lg rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm">
    <div class="h-1.5 w-full bg-gradient-to-r from-[#e67a25] to-[#f59e0b]"></div>

    <Card.Header class="pb-4">
      <Card.Description class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1">
        Paso 5 de 6
      </Card.Description>
      <Card.Title class="text-2xl font-black text-[#111111] leading-tight">
        Confirma tus números
      </Card.Title>
      <p class="text-sm text-gray-500 font-medium">Revisa tu asignación antes de realizar el registro definitivo.</p>
    </Card.Header>

    <Card.Content class="space-y-6">
      <!-- Lista de confirmación -->
      <div class="space-y-3">
        <p class="text-xs font-black text-[#111111] uppercase tracking-wider">Asignación final:</p>
        <ul class="space-y-2.5">
          {#each acceptedTickets as ticket, index}
            {@const number = findNumber(selectedNumberIds[index])}
            <li class="flex items-center justify-between gap-4 px-4 py-3.5 rounded-xl bg-[#e67a25]/5 border border-[#e67a25]/10 font-bold">
              <span class="text-sm text-[#444] font-mono tracking-widest">Boleto •••• {ticket.code_last4}</span>
              <div class="flex items-center gap-2">
                <span class="text-xs text-gray-400 font-medium">Asignado:</span>
                <strong class="text-[#e67a25] font-black text-xl">#{number?.number}</strong>
              </div>
            </li>
          {/each}
        </ul>
      </div>

      {#if error}
        <div class="p-3.5 rounded-xl bg-red-50 border border-red-100 text-red-700 text-sm font-bold" role="alert">
          {error}
        </div>
      {/if}

      <Button
        type="button"
        disabled={loading}
        onclick={onConfirm}
        class="w-full h-12 rounded-xl bg-[#111111] hover:bg-[#e67a25] text-white font-black uppercase tracking-wider shadow-md hover:shadow-lg transition-all disabled:opacity-60 flex items-center justify-center gap-2"
      >
        {#if loading}
          <div class="h-5 w-5 animate-spin rounded-full border-2 border-white/20 border-t-white"></div>
        {:else}
          <CheckCircle2 class="h-4.5 w-4.5" />
          Confirmar mis números ✓
        {/if}
      </Button>
    </Card.Content>
  </Card.Root>
</div>
