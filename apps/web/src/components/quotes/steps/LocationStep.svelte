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
      Ubicación
    </p>
    <h2 class="m-0 text-[#101827] text-[clamp(1.4rem,6vw,2rem)] font-black leading-none tracking-tight">
      ¿Dónde se hará el trabajo?
    </h2>
    <p class="m-0 text-[#526070] text-[0.84rem] leading-snug">
      El estado se usa en el cálculo y el código postal ayuda a revisar la zona.
    </p>
  </div>

  <!-- Form -->
  <div class="grid gap-2.5">
    <!-- Estado (full width) -->
    <label class="grid gap-1.5 cursor-pointer" for="state">
      <span class="text-[#273549] text-[0.82rem] font-bold">
        Estado <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="state"
        bind:value={form.state}
        aria-invalid={Boolean(errors.state)}
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
        <option value="">Selecciona un estado</option>
        {#each options.states as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.state}
        <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.state}</span>
      {/if}
    </label>

    <!-- Ciudad + Código postal — 2 cols -->
    <div class="grid grid-cols-[1fr_120px] gap-2.5 items-start">
      <label class="grid gap-1.5 cursor-pointer min-w-0" for="city">
        <span class="text-[#273549] text-[0.82rem] font-bold">
          Ciudad / municipio <strong class="text-amber-600 font-black">*</strong>
        </span>
        <input
          id="city"
          type="text"
          placeholder="Ej. Querétaro"
          bind:value={form.city}
          autocomplete="address-level2"
          aria-invalid={Boolean(errors.city)}
          class="
            w-full min-h-[44px]
            border-[1.5px] border-[#d9e0ea] rounded-xl
            bg-white text-[#172033] text-[0.9rem]
            px-3 py-2.5 font-[inherit]
            transition-[border-color,box-shadow] duration-150
            focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
            aria-[invalid=true]:border-rose-500
          "
        />
        {#if errors.city}
          <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.city}</span>
        {/if}
      </label>

      <label class="grid gap-1.5 cursor-pointer min-w-0" for="postal_code">
        <span class="text-[#273549] text-[0.82rem] font-bold">
          C.P. <strong class="text-amber-600 font-black">*</strong>
        </span>
        <input
          id="postal_code"
          type="text"
          inputmode="numeric"
          placeholder="76000"
          maxlength="5"
          bind:value={form.postal_code}
          autocomplete="postal-code"
          aria-invalid={Boolean(errors.postal_code)}
          class="
            w-full min-h-[44px]
            border-[1.5px] border-[#d9e0ea] rounded-xl
            bg-white text-[#172033] text-[0.9rem]
            px-3 py-2.5 font-[inherit]
            transition-[border-color,box-shadow] duration-150
            focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
            aria-[invalid=true]:border-rose-500
          "
        />
        {#if errors.postal_code}
          <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.postal_code}</span>
        {/if}
      </label>
    </div>
  </div>
</section>
