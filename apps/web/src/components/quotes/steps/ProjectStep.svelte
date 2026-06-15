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
      Proyecto
    </p>
    <h2 class="m-0 text-[#101827] text-[clamp(1.4rem,6vw,2rem)] font-black leading-none tracking-tight">
      ¿Qué espacio se va a pintar?
    </h2>
    <p class="m-0 text-[#526070] text-[0.84rem] leading-snug">
      Indica el inmueble, la zona del trabajo y el área aproximada.
    </p>
  </div>

  <!-- Form -->
  <div class="grid gap-3">
    <!-- Tipo de inmueble -->
    <label class="grid gap-1.5 cursor-pointer" for="property_type">
      <span class="text-[#273549] text-[0.82rem] font-bold leading-tight">
        Tipo de inmueble <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="property_type"
        bind:value={form.property_type}
        aria-invalid={Boolean(errors.property_type)}
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
        {#each options.property_types as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.property_type}
        <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.property_type}</span>
      {/if}
    </label>

    <!-- Ubicación del trabajo -->
    <label class="grid gap-1.5 cursor-pointer" for="work_location">
      <span class="text-[#273549] text-[0.82rem] font-bold leading-tight">
        Ubicación del trabajo <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="work_location"
        bind:value={form.work_location}
        aria-invalid={Boolean(errors.work_location)}
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
        {#each options.work_locations as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.work_location}
        <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.work_location}</span>
      {/if}
    </label>

    <!-- Servicio + Metros — 2 cols en mobile -->
    <div class="grid grid-cols-[1fr_110px] gap-2.5 items-start sm:grid-cols-[1fr_140px]">
      <!-- Tipo de servicio -->
      <label class="grid gap-1.5 cursor-pointer min-w-0" for="service_type">
        <span class="text-[#273549] text-[0.82rem] font-bold leading-tight">
          Tipo de servicio <strong class="text-amber-600 font-black">*</strong>
        </span>
        <select
          id="service_type"
          bind:value={form.service_type}
          aria-invalid={Boolean(errors.service_type)}
          class="
            w-full min-h-[44px] appearance-auto
            border-[1.5px] border-[#d9e0ea] rounded-xl
            bg-white text-[#172033] text-[0.88rem]
            px-3 py-2.5 font-[inherit] text-ellipsis
            transition-[border-color,box-shadow] duration-150
            focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
            aria-[invalid=true]:border-rose-500
          "
        >
          <option value="">Selecciona</option>
          {#each options.service_types as option}
            <option value={option.id}>{option.name}</option>
          {/each}
        </select>
        {#if errors.service_type}
          <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.service_type}</span>
        {/if}
      </label>

      <!-- Área m² -->
      <label class="grid gap-1.5 cursor-pointer min-w-0" for="square_meters">
        <span class="text-[#273549] text-[0.82rem] font-bold leading-tight">
          Área <strong class="text-amber-600 font-black">*</strong>
        </span>
        <div class="relative">
          <input
            id="square_meters"
            bind:value={form.square_meters}
            type="number"
            min="1"
            step="0.01"
            placeholder="40"
            aria-invalid={Boolean(errors.square_meters)}
            class="
              w-full min-h-[44px]
              border-[1.5px] border-[#d9e0ea] rounded-xl
              bg-white text-[#172033] text-[0.9rem]
              pl-3 pr-8 py-2.5 font-[inherit]
              transition-[border-color,box-shadow] duration-150
              focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
              aria-[invalid=true]:border-rose-500
            "
          />
          <span
            class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#64748b] text-[0.72rem] font-black pointer-events-none"
            aria-hidden="true"
          >m²</span>
        </div>
        {#if errors.square_meters}
          <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.square_meters}</span>
        {/if}
      </label>
    </div>
  </div>
</section>
