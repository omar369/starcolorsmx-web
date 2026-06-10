<script lang="ts">
  import { cn } from "$lib/lib/utils";

  export type Measurement = { label: string; price: string };

  let {
    title = "VIN J INTERIOR JR",
    themeColor = "#00A88F", // Default teal
    measurements = [
      { label: "Litro", price: "N/A" },
      { label: "4 Lts", price: "N/A" },
      { label: "19 Lts", price: "$625.00" },
    ],
    description = "La pintura VIN J INTERIOR JR es una buena opción cuando se necesita economizar, ya que esta línea le ofrece un buen rendimiento para pintar interiores o dar mantenimiento a un bajo costo. Aun siendo la calidad mas sencilla de pinturas que manejamos, estamos convencidos de su excelente calidad a comparación de otros productos en el mercado. Los colores que ofrece esta calidad son colores blanco y tonos pastel. (Intensidad 1)",
    coverage = "4 a 5 M2 X LITRO",
    finish = "MATE",
    qualityYears = 2,
    intensities = [1],
    imageSrc = "https://images.unsplash.com/photo-1562259929-b4e1fd3aef09?auto=format&fit=crop&q=80&w=300",
    class: className = "",
  } = $props<{
    title?: string;
    themeColor?: string;
    measurements?: Measurement[];
    description?: string;
    coverage?: string;
    finish?: string;
    qualityYears?: number | string;
    intensities?: number[];
    imageSrc?: string;
    class?: string;
  }>();
</script>

<div
  class={cn(
    "flex w-full max-w-[1100px] flex-col overflow-hidden rounded-2xl border bg-white shadow-sm lg:flex-row lg:rounded-none lg:rounded-tr-[4rem]",
    className,
  )}
  style="--tc: {themeColor}; border-color: var(--tc);"
>
  <!-- Mobile Image / Desktop Right Column -->
  <div
    class="flex w-full shrink-0 border-b lg:order-3 lg:w-[280px] lg:border-b-0 lg:border-l"
    style="border-color: var(--tc);"
  >
    <!-- Colored Section with Bucket -->
    <div
      class="relative flex flex-1 items-center justify-center overflow-hidden p-6 py-10 lg:py-6"
      style="background-color: var(--tc);"
    >
      <img
        src={imageSrc}
        alt={title}
        class="relative z-10 w-full max-w-[140px] object-contain drop-shadow-xl lg:max-w-[160px]"
      />
    </div>

    <!-- Quality Strip -->
    <div
      class="z-20 flex w-12 shrink-0 items-center justify-center bg-white lg:w-[3.25rem]"
    >
      <span
        class="rotate-180 transform text-[15px] font-medium tracking-[0.2em] whitespace-nowrap text-gray-700"
        style="writing-mode: vertical-rl;"
      >
        CALIDAD {qualityYears} AÑOS
      </span>
    </div>
  </div>

  <!-- Mobile Table / Desktop Left Column -->
  <div
    class="flex w-full flex-col border-b lg:order-1 lg:w-[25%] lg:border-r lg:border-b-0"
    style="border-color: var(--tc);"
  >
    <div
      class="flex min-h-[3rem] w-full items-center justify-center px-4 py-3 text-center text-[15px] font-semibold tracking-widest text-white lg:px-2 lg:py-0"
      style="background-color: var(--tc);"
    >
      {title}
    </div>
    <div class="flex w-full flex-col text-sm">
      <div
        class="flex w-full border-b bg-[#f7f9fa] font-medium text-gray-600"
        style="border-bottom-color: var(--tc);"
      >
        <div
          class="flex-1 border-r p-3 text-center tracking-wider"
          style="border-right-color: var(--tc);"
        >
          MEDIDA
        </div>
        <div class="flex-1 p-3 text-center tracking-wider">Precio</div>
      </div>
      {#each measurements as m}
        <div
          class="flex w-full border-b text-gray-800 last:border-b-0"
          style="border-bottom-color: var(--tc);"
        >
          <div
            class="flex-1 border-r bg-[#f2f7f7] p-3 text-center font-medium"
            style="border-right-color: var(--tc);"
          >
            {m.label}
          </div>
          <div class="flex-1 bg-white p-3 text-center font-medium">
            {m.price}
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Mobile Description / Desktop Middle Column -->
  <div
    class="relative flex flex-1 flex-col justify-between bg-white p-4 lg:order-2 lg:px-6"
  >
    <!-- Bordered Description Box -->
    <div
      class="relative flex flex-col rounded-2xl border-[1.5px] p-5"
      style="border-color: var(--tc);"
    >
      <h3
        class="mb-3 text-center text-[13px] font-medium tracking-widest uppercase"
        style="color: var(--tc);"
      >
        DESCRIPCIÓN
      </h3>
      <p class="text-[13px] leading-relaxed font-medium text-gray-700">
        {description}
      </p>
    </div>

    <!-- Stats area below -->
    <div
      class="mt-6 flex flex-col items-center justify-between gap-6 px-2 pb-2 sm:flex-row lg:items-end lg:gap-0 lg:px-4"
    >
      <div
        class="flex flex-col text-center text-[12px]"
        style="color: var(--tc);"
      >
        <span class="font-medium tracking-wide uppercase"
          >RENDIMIENTO TEÓRICO</span
        >
        <span class="mt-1 font-medium tracking-wide text-gray-800"
          >{coverage}</span
        >

        <span class="mt-4 font-medium tracking-wide uppercase">ACABADO</span>
        <span
          class="mt-1 flex justify-center font-bold tracking-widest text-gray-800"
          >{finish}</span
        >
      </div>

      <div class="flex w-full flex-col items-center pb-1 text-[12px] sm:w-auto">
        <span class="mb-3 text-center font-medium tracking-wide text-gray-800"
          >Intensidad de colores disponible.</span
        >
        <div class="flex flex-wrap justify-center gap-1">
          {#each Array(Math.max(5, intensities.length)) as _, idx}
            {@const active = idx < intensities.length}
            {@const val = active ? intensities[idx] : ""}
            <div
              class="flex h-8 w-10 items-center justify-center font-bold text-gray-700"
              style="background-color: {active
                ? `rgba(0,0,0,${idx * 0.15 + 0.08})`
                : '#f3f4f6'};"
            >
              {val}
            </div>
          {/each}
        </div>
      </div>
    </div>
  </div>
</div>
