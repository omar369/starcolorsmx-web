<script lang="ts">
	import AnimatedText from '$lib/components/pages/AnimatedText.svelte';
	import { onMount } from 'svelte';

	let imgLoaded = $state(false);

	onMount(() => {
		// Small delay to trigger the ink animation smoothly
		setTimeout(() => {
			imgLoaded = true;
		}, 100);
	});
</script>

<svelte:head>
	<title>Sobre nosotros | SC-Servicios</title>
</svelte:head>

<section
	class="flex min-h-[calc(100vh-80px)] flex-col items-center justify-center bg-transparent px-4 py-8 md:px-8"
>
	<div class="mx-auto flex w-full max-w-4xl flex-col items-center">
		<!-- Hero Illustration with Ink Reveal Animation -->
		<div class="mb-12 flex w-full justify-center lg:mb-16">
			<div class="relative w-full max-w-2xl overflow-hidden drop-shadow-md">
				<img
					src="/images/nosotros/fondo_img.svg"
					alt="Tienda de Pinturas Star Colors"
					class="w-full object-contain transition-all duration-[2000ms] ease-out"
					class:ink-hidden={!imgLoaded}
					class:ink-revealed={imgLoaded}
				/>
			</div>
		</div>

		<!-- Slogan / Heading -->
		<h1
			class="mb-12 text-center text-3xl font-normal tracking-tight text-gray-900 md:text-4xl lg:text-[42px]"
		>
			<AnimatedText text="Refleja tu Imaginación" delayOffset={0.2} />
		</h1>

		<!-- Mission Text -->
		<div
			class="mx-auto flex max-w-2xl flex-col gap-6 text-center text-[13px] leading-relaxed font-medium text-gray-800 md:text-base"
		>
			<p>
				<AnimatedText
					text="Los espacios hablan, incluso antes de que alguien los habite."
					delayOffset={0.6}
				/><br />
				<AnimatedText
					text="Hablan a través de su color, su textura y su presencia."
					delayOffset={0.8}
				/>
			</p>

			<p>
				<AnimatedText
					text="Desde 1994 hemos trabajado para que cada superficie no solo esté cubierta, sino respaldada."
					delayOffset={1.2}
				/>
				<AnimatedText
					text="Entendimos que la verdadera calidad no termina en la fabricación; por eso en 2012 integramos"
					delayOffset={1.6}
				/>
				<AnimatedText
					text="la aplicación especializada, asegurando coherencia entre lo que se formula y lo que"
					delayOffset={2.0}
				/>
				<AnimatedText text="finalmente se ve." delayOffset={2.4} />
			</p>

			<p>
				<AnimatedText
					text="Creemos en la fuerza de los procesos bien hechos y en la responsabilidad detrás de cada"
					delayOffset={2.8}
				/>
				<AnimatedText
					text="resultado. Porque un recubrimiento no solo protege del clima o del desgaste; protege la"
					delayOffset={3.2}
				/>
				<AnimatedText text="intención con la que fue creado el espacio." delayOffset={3.6} />
			</p>

			<p class="mt-2 text-[12px] md:text-[15px]">
				<AnimatedText
					text="&quot;Refleja tu imaginación&quot; esta en cada proyecto que pueda trascender lo ordinario en"
					delayOffset={4.0}
				/>
				<br class="hidden md:block" />
				<AnimatedText text="algo unico." delayOffset={4.4} />
			</p>
		</div>
	</div>
</section>

<style>
	/* Ink reveal animation styles for the SVG */
	.ink-hidden {
		opacity: 0;
		filter: blur(10px) grayscale(100%);
		clip-path: circle(0% at 50% 50%);
		transform: scale(0.95);
	}
	.ink-revealed {
		opacity: 1;
		filter: blur(0px) grayscale(0%);
		clip-path: circle(150% at 50% 50%);
		transform: scale(1);
	}
</style>
