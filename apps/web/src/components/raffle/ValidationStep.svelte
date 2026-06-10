<script lang="ts">
  import type { RaffleBranch, TicketBatchValidation } from "../../lib/raffle";
  import { Button } from "$lib/components/ui/button/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { ChevronLeft, CheckCircle2, AlertTriangle } from "@lucide/svelte";

  // Svelte 5 props
  let {
    selectedBranch,
    validation,
    onBack,
    onContinue,
  }: {
    selectedBranch: RaffleBranch;
    validation: TicketBatchValidation;
    onBack: () => void;
    onContinue: () => void;
  } = $props();
</script>

<div class="w-full max-w-xl mx-auto space-y-4">
  <button
    type="button"
    onclick={onBack}
    class="inline-flex items-center gap-1.5 text-sm font-bold text-[#e67a25] hover:text-[#d96f20] transition-colors focus:outline-none"
  >
    <ChevronLeft class="h-4 w-4" />
    Volver a códigos
  </button>

  <Card.Root class="border-0 shadow-lg rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm">
    <div class="h-1.5 w-full bg-gradient-to-r from-[#e67a25] to-[#f59e0b]"></div>

    <Card.Header class="pb-4">
      <Card.Description class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1">
        Paso 3 de 6
      </Card.Description>
      <Card.Title class="text-2xl font-black text-[#111111] leading-tight">
        Resultado de validación
      </Card.Title>
      <p class="text-sm text-gray-500 font-medium">
        Revisando boletos de: <span class="font-black text-[#e67a25]">{selectedBranch.name}</span>
      </p>
    </Card.Header>

    <Card.Content class="space-y-6">
      <!-- Resumen aceptados / rechazados -->
      <div class="grid grid-cols-2 gap-4">
        <div class="p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-center">
          <p class="text-3xl font-black text-green-700">{validation.accepted_count}</p>
          <p class="text-[0.7rem] font-black uppercase tracking-widest text-green-600 mt-1">Aceptados</p>
        </div>
        <div class="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-center">
          <p class="text-3xl font-black text-red-700">{validation.rejected_count}</p>
          <p class="text-[0.7rem] font-black uppercase tracking-widest text-red-600 mt-1">Rechazados</p>
        </div>
      </div>

      <!-- Lista de validaciones -->
      <div class="space-y-2.5">
        <p class="text-xs font-black text-[#111111] uppercase tracking-wider">Detalle de boletos:</p>
        <ul class="space-y-2">
          {#each validation.results as result}
            {@const accepted = result.status === 'accepted'}
            <li class="flex items-center justify-between gap-4 px-4 py-3 rounded-xl border text-sm font-bold 
              {accepted 
                ? 'bg-green-500/5 text-green-800 border-green-200' 
                : 'bg-red-500/5 text-red-800 border-red-200'}">
              <div class="flex items-center gap-2.5">
                {#if accepted}
                  <CheckCircle2 class="h-4.5 w-4.5 text-green-600 shrink-0" />
                {:else}
                  <AlertTriangle class="h-4.5 w-4.5 text-red-600 shrink-0" />
                {/if}
                <span class="font-mono tracking-widest">•••• {result.code_last4}</span>
              </div>
              <span class="text-xs uppercase tracking-wider font-black">
                {accepted ? "✓ Aceptado" : (result.reason === "not_found" ? "No existe" : "Ya usado")}
              </span>
            </li>
          {/each}
        </ul>
      </div>

      {#if validation.accepted_count > 0}
        <Button
          type="button"
          onclick={onContinue}
          class="w-full h-12 rounded-xl bg-[#e67a25] hover:bg-[#d96f20] text-white font-black uppercase tracking-wider shadow-md hover:shadow-lg transition-all"
        >
          Elegir {validation.accepted_count} {validation.accepted_count === 1 ? "número" : "números"} →
        </Button>
      {:else}
        <Button
          type="button"
          variant="outline"
          onclick={onBack}
          class="w-full h-12 rounded-xl border-2 border-red-500/40 hover:border-red-600 text-red-700 font-black uppercase tracking-wider hover:bg-red-50 transition-all"
        >
          Intentar con otros códigos
        </Button>
      {/if}
    </Card.Content>
  </Card.Root>
</div>
