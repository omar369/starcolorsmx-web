<script lang="ts">
  import type { RaffleEntry } from "../../lib/raffle";
  import { Button } from "$lib/components/ui/button/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { CheckCircle2, Ticket, Home } from "@lucide/svelte";

  // Svelte 5 props
  let {
    entries = [],
    onRestart,
  }: {
    entries: RaffleEntry[];
    onRestart: () => void;
  } = $props();
</script>

<div class="w-full max-w-xl mx-auto">
  <Card.Root class="border-0 shadow-xl rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm text-center">
    <div class="h-1.5 w-full bg-gradient-to-r from-green-500 to-emerald-400"></div>

    <Card.Content class="p-6 sm:p-8 space-y-6">
      <!-- Icono de éxito con animación de escala -->
      <div class="flex items-center justify-center w-20 h-20 mx-auto rounded-full bg-green-100 border-4 border-green-300 text-green-600 animate-in zoom-in-50 duration-300">
        <CheckCircle2 class="h-10 w-10" />
      </div>

      <div>
        <p class="text-[0.75rem] font-black uppercase tracking-[0.14em] text-green-600 mb-2">¡Operación Exitosa!</p>
        <h2 class="text-2xl sm:text-3xl font-black text-[#111111] mb-2 leading-tight">Tus números han sido registrados</h2>
        <p class="text-sm text-gray-500 leading-relaxed max-w-sm mx-auto">
          Los números de tu boleto ya están asignados a tu cuenta. Puedes consultarlos en cualquier momento desde tu Hub de cliente.
        </p>
      </div>

      <!-- Números registrados -->
      <div class="space-y-2.5 text-left">
        <p class="text-xs font-black text-[#111111] uppercase tracking-wider">Tus números asignados:</p>
        <ul class="space-y-2">
          {#each entries as entry}
            <li class="flex items-center justify-between px-5 py-3 rounded-xl bg-green-500/5 border border-green-200">
              <span class="text-sm font-bold text-green-800 flex items-center gap-2">
                <Ticket class="h-4.5 w-4.5 text-green-600" />
                Número registrado:
              </span>
              <strong class="text-2xl font-black text-green-700">#{entry.selected_number}</strong>
            </li>
          {/each}
        </ul>
      </div>

      <!-- Acciones -->
      <div class="grid gap-3 pt-2">
        <Button
          type="button"
          onclick={onRestart}
          class="w-full h-12 rounded-xl bg-[#e67a25] hover:bg-[#d96f20] text-white font-black uppercase tracking-wider shadow-md hover:shadow-lg transition-all"
        >
          Registrar más boletos
        </Button>

        <Button
          href="/hub"
          variant="outline"
          class="w-full h-12 rounded-xl border-2 border-gray-200 text-gray-700 font-bold hover:bg-gray-50 transition-all flex items-center justify-center gap-2"
        >
          <Home class="h-4.5 w-4.5" />
          Volver a mi Hub
        </Button>
      </div>
    </Card.Content>
  </Card.Root>
</div>
