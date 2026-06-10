<script lang="ts">
  export let currentStep: number;
  export let totalSteps = 6;
</script>

<div class="mb-6" aria-label="Progreso del registro">
  <p class="mb-2 text-[0.75rem] font-black uppercase tracking-[0.12em] text-[#e67a25]">
    Paso {currentStep} de {totalSteps}
  </p>
  <div class="grid gap-1.5" style="grid-template-columns: repeat({totalSteps}, 1fr)">
    {#each Array(totalSteps) as _, index}
      <span
        class="h-1.5 rounded-full transition-all duration-300 {index + 1 <= currentStep ? 'bg-[#e67a25]' : 'bg-[#e67a25]/20'}"
      ></span>
    {/each}
  </div>
</div>
