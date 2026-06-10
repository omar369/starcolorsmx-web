<script lang="ts">
  import { cn } from "$lib/lib/utils";

  let {
    title = "SERVICIO",
    themeColor = "#00A88F",
    description = "Descripción del servicio.",
    qualityYears = 2,
    imageSrc = "",
    stockImageSrc = "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&q=80&w=600",
    class: className = "",
  } = $props<{
    title?: string;
    themeColor?: string;
    description?: string;
    qualityYears?: number | string;
    imageSrc?: string;
    stockImageSrc?: string;
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
      {#if imageSrc}
        <img
          src={imageSrc}
          alt={title}
          class="relative z-10 w-full max-w-[140px] object-contain drop-shadow-xl lg:max-w-[160px]"
        />
      {/if}
    </div>

    {#if qualityYears && qualityYears !== 0}
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
    {/if}
  </div>

  <!-- Mobile Table (Stock Image) / Desktop Left Column -->
  <div
    class="flex w-full flex-col border-b lg:order-1 lg:w-[30%] lg:border-r lg:border-b-0"
    style="border-color: var(--tc);"
  >
    <div
      class="flex min-h-[3rem] w-full items-center justify-center px-4 py-3 text-center text-[15px] font-semibold tracking-widest text-white lg:px-2 lg:py-0"
      style="background-color: var(--tc);"
    >
      {title}
    </div>
    <div
      class="relative min-h-[15rem] w-full flex-1 overflow-hidden bg-gray-100 lg:min-h-0"
    >
      <img
        src={stockImageSrc}
        alt="Servicio {title}"
        class="absolute inset-0 h-full w-full object-cover"
      />
    </div>
  </div>

  <!-- Mobile Description / Desktop Middle Column -->
  <div
    class="relative flex flex-1 flex-col justify-between bg-white p-4 lg:order-2 lg:px-6"
  >
    <!-- Bordered Description Box -->
    <div
      class="relative flex h-full flex-col rounded-2xl border-[1.5px] p-5 lg:h-auto"
      style="border-color: var(--tc);"
    >
      <h3
        class="mb-3 text-center text-[13px] font-medium tracking-widest uppercase"
        style="color: var(--tc);"
      >
        DESCRIPCIÓN
      </h3>
      <p
        class="text-[13px] leading-relaxed font-medium whitespace-pre-line text-gray-700"
      >
        {description}
      </p>
    </div>
  </div>
</div>
