<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};

  function togglePreparation(optionId: string) {
    if (form.preparation.includes(optionId)) {
      form.preparation = form.preparation.filter((id) => id !== optionId);
      return;
    }
    form.preparation = [...form.preparation, optionId];
  }

  function isPreparationSelected(optionId: string) {
    return form.preparation.includes(optionId);
  }
</script>

<section class="grid gap-3 min-h-0">
  <!-- Heading -->
  <div class="grid gap-1">
    <p class="m-0 text-[#8a6b00] text-[0.65rem] font-black tracking-[0.08em] uppercase">
      Superficie
    </p>
    <h2 class="m-0 text-[#101827] text-[clamp(1.3rem,5.5vw,1.9rem)] font-black leading-none tracking-tight">
      Estado del área
    </h2>
    <p class="m-0 text-[#526070] text-[0.82rem] leading-snug">
      Describe cómo está la superficie y qué preparación necesita antes de pintar.
    </p>
  </div>

  <!-- Form grid: 2 cols mobile -->
  <div class="grid grid-cols-2 gap-2.5 items-start">

    <!-- Estado de superficie -->
    <label class="grid gap-1 cursor-pointer min-w-0" for="surface_state">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Estado <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="surface_state"
        bind:value={form.surface_state}
        aria-invalid={Boolean(errors.surface_state)}
        class="
          w-full min-h-[42px] appearance-auto
          border-[1.5px] border-[#d9e0ea] rounded-xl
          bg-white text-[#172033] text-[0.84rem]
          px-2.5 py-2 font-[inherit] text-ellipsis
          transition-[border-color,box-shadow] duration-150
          focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
          aria-[invalid=true]:border-rose-500
        "
      >
        <option value="">Selecciona</option>
        {#each options.surface_states as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.surface_state}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.surface_state}</span>
      {/if}
    </label>

    <!-- Textura -->
    <label class="grid gap-1 cursor-pointer min-w-0" for="texture">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Textura <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="texture"
        bind:value={form.texture}
        aria-invalid={Boolean(errors.texture)}
        class="
          w-full min-h-[42px] appearance-auto
          border-[1.5px] border-[#d9e0ea] rounded-xl
          bg-white text-[#172033] text-[0.84rem]
          px-2.5 py-2 font-[inherit] text-ellipsis
          transition-[border-color,box-shadow] duration-150
          focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
          aria-[invalid=true]:border-rose-500
        "
      >
        <option value="">Selecciona</option>
        {#each options.textures as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.texture}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.texture}</span>
      {/if}
    </label>

    <!-- Protección del área — full width -->
    <label class="grid gap-1 cursor-pointer col-span-2" for="area_protection">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Protección del área <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="area_protection"
        bind:value={form.area_protection}
        aria-invalid={Boolean(errors.area_protection)}
        class="
          w-full min-h-[42px] appearance-auto
          border-[1.5px] border-[#d9e0ea] rounded-xl
          bg-white text-[#172033] text-[0.84rem]
          px-2.5 py-2 font-[inherit]
          transition-[border-color,box-shadow] duration-150
          focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
          aria-[invalid=true]:border-rose-500
        "
      >
        <option value="">Selecciona una opción</option>
        {#each options.area_protections as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.area_protection}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.area_protection}</span>
      {/if}
    </label>

    <!-- Preparación — full width, toggle buttons -->
    <div class="grid gap-1.5 col-span-2">
      <div class="flex items-baseline justify-between gap-3">
        <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
          Preparación de superficie
          <span class="text-[#64748b] font-normal text-[0.7rem]">(opcional)</span>
        </span>
        <span class="text-[#64748b] text-[0.68rem] font-semibold shrink-0">Puedes elegir más de una</span>
      </div>

      <div
        class="grid grid-cols-2 gap-1.5 sm:grid-cols-3"
        aria-invalid={Boolean(errors.preparation)}
      >
        {#each options.preparations as option}
          <button
            type="button"
            on:click={() => togglePreparation(option.id)}
            aria-pressed={isPreparationSelected(option.id)}
            class="
              flex items-center gap-2 min-h-[36px]
              border-[1.5px] rounded-xl
              text-[0.76rem] font-bold text-left
              px-2.5 py-2 cursor-pointer
              transition-[border-color,background] duration-150
              {isPreparationSelected(option.id)
                ? 'border-amber-400 bg-[#fff8dc] text-[#172033]'
                : 'border-[#d9e0ea] bg-white text-[#273549]'}
            "
          >
            <!-- Radio dot -->
            <span
              aria-hidden="true"
              class="
                inline-block w-3 h-3 shrink-0 rounded-full border-2 transition-all duration-150
                {isPreparationSelected(option.id)
                  ? 'border-[#172033] shadow-[inset_0_0_0_3px_#f5b700]'
                  : 'border-[#cbd5e1] bg-white'}
              "
            ></span>
            <span>{option.name}</span>
          </button>
        {/each}
      </div>

      {#if errors.preparation}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.preparation}</span>
      {/if}
    </div>
  </div>
</section>
