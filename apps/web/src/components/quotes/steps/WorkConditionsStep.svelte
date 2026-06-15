<script lang="ts">
  import type { QuoteForm, QuoteOptions } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let errors: Record<string, string> = {};
</script>

<!-- Common select class — shared across all selects in this step -->
<section class="grid gap-3.5 min-h-0">
  <!-- Heading -->
  <div class="grid gap-1">
    <p class="m-0 text-[#8a6b00] text-[0.68rem] font-black tracking-[0.08em] uppercase">
      Condiciones
    </p>
    <h2 class="m-0 text-[#101827] text-[clamp(1.4rem,6vw,2rem)] font-black leading-none tracking-tight">
      Cómo se puede trabajar ahí
    </h2>
    <p class="m-0 text-[#526070] text-[0.84rem] leading-snug">
      Estos datos ayudan a estimar complejidad, acceso, horario y riesgo.
    </p>
  </div>

  <!-- Form: 2 cols on mobile for compact display -->
  <div class="grid grid-cols-2 gap-2.5 items-start">

    <!-- Dificultad de avance -->
    <label class="grid gap-1 cursor-pointer min-w-0" for="advance_difficulty">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Dificultad <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="advance_difficulty"
        bind:value={form.advance_difficulty}
        aria-invalid={Boolean(errors.advance_difficulty)}
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
        {#each options.advance_difficulties as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.advance_difficulty}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.advance_difficulty}</span>
      {/if}
    </label>

    <!-- Ocupación del inmueble -->
    <label class="grid gap-1 cursor-pointer min-w-0" for="occupancy">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Ocupación <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="occupancy"
        bind:value={form.occupancy}
        aria-invalid={Boolean(errors.occupancy)}
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
        {#each options.occupancies as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.occupancy}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.occupancy}</span>
      {/if}
    </label>

    <!-- Altura y riesgo -->
    <label class="grid gap-1 cursor-pointer min-w-0" for="height_risk">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Altura y riesgo <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="height_risk"
        bind:value={form.height_risk}
        aria-invalid={Boolean(errors.height_risk)}
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
        {#each options.height_risks as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.height_risk}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.height_risk}</span>
      {/if}
    </label>

    <!-- Horario -->
    <label class="grid gap-1 cursor-pointer min-w-0" for="schedule">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Horario <strong class="text-amber-600 font-black">*</strong>
      </span>
      <select
        id="schedule"
        bind:value={form.schedule}
        aria-invalid={Boolean(errors.schedule)}
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
        {#each options.schedules as option}
          <option value={option.id}>{option.name}</option>
        {/each}
      </select>
      {#if errors.schedule}
        <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.schedule}</span>
      {/if}
    </label>

    <!-- Actividades (full width, optional) -->
    <label class="grid gap-1 cursor-pointer col-span-2" for="place_activities">
      <span class="text-[#273549] text-[0.78rem] font-bold leading-tight">
        Actividades en el lugar <span class="text-[#64748b] font-normal">(opcional)</span>
      </span>
      <textarea
        id="place_activities"
        bind:value={form.place_activities}
        rows="2"
        maxlength="400"
        placeholder="Ej. casa habitada, oficina con tráfico, local abierto..."
        class="
          w-full min-h-[62px] resize-none
          border-[1.5px] border-[#d9e0ea] rounded-xl
          bg-white text-[#172033] text-[0.84rem]
          px-2.5 py-2 font-[inherit]
          transition-[border-color,box-shadow] duration-150
          focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
        "
      ></textarea>
    </label>
  </div>
</section>
