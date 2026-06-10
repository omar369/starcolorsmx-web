<script lang="ts">
  import type { RaffleBranch } from "../../lib/raffle";
  import { Button } from "$lib/components/ui/button/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { ChevronLeft } from "@lucide/svelte";

  // Svelte 5 props with bindable codesText
  let {
    selectedBranch,
    codesText = $bindable(),
    loading = false,
    error = "",
    onBack,
    onValidate,
  }: {
    selectedBranch: RaffleBranch;
    codesText: string;
    loading: boolean;
    error: string;
    onBack: () => void;
    onValidate: (codesText: string) => void;
  } = $props();
</script>

<div class="w-full max-w-xl mx-auto space-y-4">
  <button
    type="button"
    onclick={onBack}
    class="inline-flex items-center gap-1.5 text-sm font-bold text-[#e67a25] hover:text-[#d96f20] transition-colors focus:outline-none"
  >
    <ChevronLeft class="h-4 w-4" />
    Cambiar sucursal
  </button>

  <Card.Root class="border-0 shadow-lg rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm">
    <div class="h-1.5 w-full bg-gradient-to-r from-[#e67a25] to-[#f59e0b]"></div>
    
    <Card.Header class="pb-4">
      <Card.Description class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1">
        Paso 2 de 6
      </Card.Description>
      <Card.Title class="text-2xl font-black text-[#111111] leading-tight">
        Registra tus boletos
      </Card.Title>
      <p class="text-sm text-gray-500 font-medium">
        Sucursal seleccionada: <span class="font-black text-[#e67a25]">{selectedBranch.name}</span>
      </p>
    </Card.Header>

    <Card.Content class="space-y-6">
      <div class="space-y-2">
        <Label for="codesInput" class="text-sm font-bold text-[#111111]">
          Códigos de boleto físico
        </Label>
        <textarea
          id="codesInput"
          bind:value={codesText}
          placeholder={"A7K2P9\nM4X8Q1\nZ9T3L6"}
          rows={6}
          class="w-full px-4 py-3 rounded-xl border-2 border-gray-200 bg-gray-50/50 text-[#111] font-mono text-sm focus:outline-none focus:border-[#e67a25] focus:ring-4 focus:ring-[#e67a25]/10 resize-y transition-all placeholder:text-gray-300"
        ></textarea>
        <div class="flex items-center justify-between text-[0.75rem] text-gray-400 font-bold uppercase tracking-wider">
          <span>Escribe un código por línea</span>
          <span>Máx. 10 boletos</span>
        </div>
      </div>

      {#if error}
        <div class="p-3.5 rounded-xl bg-red-50 border border-red-100 text-red-700 text-sm font-bold animate-in fade-in zoom-in-95 duration-200" role="alert">
          {error}
        </div>
      {/if}

      <Button
        type="button"
        disabled={loading || !codesText.trim()}
        onclick={() => onValidate(codesText)}
        class="w-full h-12 rounded-xl bg-[#e67a25] hover:bg-[#d96f20] text-white font-black uppercase tracking-wider shadow-md hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {#if loading}
          <div class="h-5 w-5 animate-spin rounded-full border-2 border-white/20 border-t-white"></div>
        {:else}
          Validar boletos →
        {/if}
      </Button>
    </Card.Content>
  </Card.Root>
</div>
