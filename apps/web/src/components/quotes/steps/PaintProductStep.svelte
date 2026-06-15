<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};
</script>

<section class="grid gap-3.5 min-h-0">
  <!-- Heading -->
  <div class="grid gap-1">
    <p class="m-0 text-[#8a6b00] text-[0.68rem] font-black tracking-[0.08em] uppercase">
      Pintura
    </p>
    <h2 class="m-0 text-[#101827] text-[clamp(1.4rem,6vw,2rem)] font-black leading-none tracking-tight">
      Producto y color
    </h2>
    <p class="m-0 text-[#526070] text-[0.84rem] leading-snug">
      Elige la pintura vinílica y la intensidad del color. El cálculo interno
      aplica el costo correspondiente.
    </p>
  </div>

  <!-- Form -->
  <div class="grid gap-3">
    <!-- Pintura -->
    <label class="grid gap-1.5 cursor-pointer" for="paint_product">
      <span class="text-[#273549] text-[0.82rem] font-bold">
        Pintura vinílica <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="paint_product"
        bind:value={form.paint_product}
        aria-invalid={Boolean(errors.paint_product)}
        class="
          w-full min-h-[44px] appearance-auto
          border-[1.5px] border-[#d9e0ea] rounded-xl
          bg-white text-[#172033] text-[0.9rem]
          px-3 py-2.5 font-[inherit]
          transition-[border-color,box-shadow] duration-150
          focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
          aria-[invalid=true]:border-rose-500
        "
      >
        <option value="">Selecciona una pintura</option>
        {#each options.paints as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.paint_product}
        <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.paint_product}</span>
      {/if}
    </label>

    <!-- Intensidad del color -->
    <label class="grid gap-1.5 cursor-pointer" for="color_intensity">
      <span class="text-[#273549] text-[0.82rem] font-bold">
        Intensidad del color <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="color_intensity"
        bind:value={form.color_intensity}
        aria-invalid={Boolean(errors.color_intensity)}
        class="
          w-full min-h-[44px] appearance-auto
          border-[1.5px] border-[#d9e0ea] rounded-xl
          bg-white text-[#172033] text-[0.9rem]
          px-3 py-2.5 font-[inherit]
          transition-[border-color,box-shadow] duration-150
          focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
          aria-[invalid=true]:border-rose-500
        "
      >
        <option value="">Selecciona una opción</option>
        {#each options.color_intensities as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.color_intensity}
        <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.color_intensity}</span>
      {/if}
    </label>
  </div>
</section>
