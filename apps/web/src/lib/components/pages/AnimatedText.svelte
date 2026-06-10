<script lang="ts">
	import { onMount } from 'svelte';

	let {
		text = '',
		class: className = '',
		delayOffset = 0
	} = $props<{
		text?: string;
		class?: string;
		delayOffset?: number;
	}>();

	let animate = $state(false);

	onMount(() => {
		// Small delay to ensure CSS is ready
		setTimeout(() => {
			animate = true;
		}, 50);
	});
</script>

<span class={className}>
	{#each text.split('') as char, i}
		<span
			class="inline-block transition-all duration-[1200ms] ease-out"
			class:opacity-0={!animate}
			class:opacity-100={animate}
			class:blur-md={!animate}
			class:blur-none={animate}
			style="transition-delay: {delayOffset + Math.random() * 0.8}s;"
		>
			{#if char === ' '}
				&nbsp;
			{:else}
				{char}
			{/if}
		</span>
	{/each}
</span>
