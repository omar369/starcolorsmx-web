<script lang="ts">
  import { fade, fly } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { onMount } from "svelte";

  export type Testimonial = {
    quote?: string;
    name: string;
    designation?: string;
    src: string;
    details?: string[];
  };

  let {
    testimonials,
    autoplay = false,
    interval = 5000,
    class: className = "",
  } = $props<{
    testimonials: Testimonial[];
    autoplay?: boolean;
    interval?: number;
    class?: string;
  }>();

  let activeIndex = $state(0);
  let rotations = $state<number[]>([]);

  // Pre-calculate random rotations for each card to keep them stable
  onMount(() => {
    rotations = testimonials.map(() => Math.floor(Math.random() * 21) - 10);

    let timer: ReturnType<typeof setInterval>;
    if (autoplay) {
      timer = setInterval(handleNext, interval);
    }
    return () => clearInterval(timer);
  });

  function handleNext() {
    activeIndex = (activeIndex + 1) % testimonials.length;
  }

  function handlePrev() {
    activeIndex = (activeIndex - 1 + testimonials.length) % testimonials.length;
  }

  // Calculate if a card is the active one, or its relative position
  function isActive(index: number) {
    return index === activeIndex;
  }
</script>

<div
  class="mx-auto flex w-full max-w-5xl flex-col items-center gap-12 px-4 py-8 md:flex-row md:gap-20 {className}"
>
  <!-- Left Side: Image Stack -->
  <div class="relative mx-auto aspect-square w-full max-w-md md:w-1/2">
    <!-- We iterate backwards so the first item naturally overlaps in DOM, but we control via z-index anyway -->
    {#each testimonials as testimonial, i}
      {@const active = isActive(i)}
      {@const zIndex = active ? 20 : testimonials.length - i}
      {@const randomRotate = rotations[i] ?? 0}

      <div
        class="absolute inset-0 flex origin-bottom items-center justify-center p-4 transition-all duration-500 ease-out"
        style="
					z-index: {zIndex};
					transform: scale({active ? 1 : 0.9 + i * 0.02}) rotate({active
          ? 0
          : randomRotate}deg);
					opacity: {active ? 1 : 0.7 - i * 0.15};
				"
      >
        <div
          class="relative h-full w-full overflow-hidden rounded-3xl border-4 border-white bg-white shadow-xl dark:border-gray-800"
        >
          <img
            src={testimonial.src}
            alt={testimonial.name}
            class="h-full w-full object-cover"
          />
        </div>
      </div>
    {/each}
  </div>

  <!-- Right Side: Text & Controls -->
  <div
    class="relative flex min-h-[350px] w-full flex-col justify-between py-4 md:h-full md:w-1/2"
  >
    <!-- We use #key to force re-render and trigger transitions when activeIndex changes -->
    <div class="relative flex-grow">
      {#key activeIndex}
        <div
          class="absolute inset-x-0 top-0 flex flex-col justify-start"
          in:fly={{ y: 20, duration: 400, delay: 150, easing: cubicOut }}
          out:fade={{ duration: 150 }}
        >
          <h3 class="mb-2 text-3xl font-bold text-gray-900">
            {testimonials[activeIndex].name}
          </h3>
          {#if testimonials[activeIndex].designation}
            <p class="mb-4 text-base font-medium text-gray-500">
              {testimonials[activeIndex].designation}
            </p>
          {/if}
          {#if testimonials[activeIndex].quote}
            <p class="mb-6 text-lg leading-relaxed text-gray-700 md:text-xl">
              "{testimonials[activeIndex].quote}"
            </p>
          {/if}
          {#if testimonials[activeIndex].details}
            <div
              class="mt-2 flex flex-col gap-3 text-[15px] text-gray-700 md:text-base"
            >
              {#each testimonials[activeIndex].details as detail}
                <p>{@html detail}</p>
              {/each}
            </div>
          {/if}
        </div>
      {/key}
    </div>

    <!-- Navigation Arrows positioned at the bottom naturally -->
    <div class="z-30 mt-auto flex gap-4 pt-12 md:pt-16">
      <button
        aria-label="Testimonio Anterior"
        onclick={handlePrev}
        class="flex h-12 w-12 items-center justify-center rounded-full bg-gray-100 text-gray-800 transition-colors hover:bg-gray-200"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-6 w-6"><path d="m15 18-6-6 6-6" /></svg
        >
      </button>
      <button
        aria-label="Siguiente Testimonio"
        onclick={handleNext}
        class="flex h-12 w-12 items-center justify-center rounded-full bg-gray-100 text-gray-800 transition-colors hover:bg-gray-200"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="h-6 w-6"><path d="m9 18 6-6-6-6" /></svg
        >
      </button>
    </div>
  </div>
</div>
