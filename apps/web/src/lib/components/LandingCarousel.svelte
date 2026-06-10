<script lang="ts">
	import * as Carousel from '$lib/components/ui/carousel/index.js';

	const sections = [
		{
			id: 'productos',
			title: 'Productos',
			description: 'Catálogo completo de soluciones para tu espacio.',
			video: '/videos/servicio_pintura.mp4',
			link: '/productos'
		},
		{
			id: 'servicios',
			title: 'Servicios',
			description: 'Aplicación profesional y certificada en cada proyecto.',
			video: '/videos/servicios_imper.mp4',
			link: '/servicios'
		},
		{
			id: 'sobre-nosotros',
			title: 'Sobre Nosotros',
			description: 'Conoce sobre nuestra misión, visión y compromiso social.',
			video: '/videos/servicio_pintura2.mp4',
			link: '/sobre-nosotros'
		},
		{
			id: 'contacto',
			title: 'Contacto',
			description:
				'Comunícate con nosotros por cualquier medio, te brindamos atención personalizada.',
			image:
				'https://images.unsplash.com/photo-1423666639041-f56000c27a9a?auto=format&fit=crop&q=80&w=1200',
			link: '/contacto'
		}
	];
</script>

<section
	class="relative m-0 flex w-full flex-col justify-center overflow-hidden bg-transparent py-10 px-4 md:px-8"
>
	<div class="relative z-10 mx-auto flex h-full w-full max-w-[1200px] flex-col gap-6">
		<div class="h-full w-full">
			<Carousel.Root
				opts={{
					align: 'start',
					dragFree: true,
					loop: true
				}}
				class="group/carousel w-full cursor-grab active:cursor-grabbing"
			>
				<Carousel.Content class="-ml-4 md:-ml-6">
					{#each sections as section (section.id)}
						<Carousel.Item class="basis-full pl-4 md:basis-1/2 md:pl-6 lg:basis-1/3">
							<a
								href={section.link}
								class="group relative block h-[48vh] max-h-[600px] min-h-[380px] w-full overflow-hidden bg-[#050a14] rounded-3xl shadow-lg border border-white/10 transition-all duration-500 hover:shadow-2xl hover:-translate-y-1"
							>
								<!-- Background logic -->
								{#if section.video}
									<video
										src={section.video}
										autoplay
										loop
										muted
										playsinline
										class="absolute inset-0 h-full w-full scale-100 transform object-cover opacity-60 transition-transform duration-700 ease-in-out group-hover:scale-105 group-hover:opacity-40"
									></video>
									<!-- Warm Glassmorphism Overlay for text readability -->
									<div
										class="absolute inset-0 bg-[#f3eadb]/20 transition-colors duration-500 group-hover:bg-[#f3eadb]/45"
									></div>
								{:else}
									<img
										src={section.image}
										alt={section.title}
										class="absolute inset-0 h-full w-full scale-100 transform object-cover transition-transform duration-700 ease-in-out group-hover:scale-105 group-hover:opacity-40"
									/>
									<div
										class="absolute inset-0 bg-[#f3eadb]/20 transition-colors duration-500 group-hover:bg-[#f3eadb]/45"
									></div>
								{/if}

								<!-- Minimal Overlay Box -->
								<div
									class="absolute inset-6 z-20 flex flex-col items-center justify-center border border-white/20 bg-white/50 text-center rounded-2xl backdrop-blur-[3px] transition-all duration-500 group-hover:border-[#e67a25]/30 group-hover:bg-white/80 p-6 shadow-sm"
								>
									<h2
										class="mb-3 text-3xl font-black tracking-tight text-[#111111] group-hover:text-[#e67a25] transition-colors md:text-4xl"
									>
										{section.title}
									</h2>
									<p class="mx-auto max-w-[90%] text-sm font-bold text-gray-700 leading-relaxed">
										{section.description}
									</p>
								</div>
							</a>
						</Carousel.Item>
					{/each}
				</Carousel.Content>

				<!-- Custom Navigation Placed at Bottom Center -->
				<div class="mt-8 flex w-full items-center justify-center gap-6 px-4 text-[#e67a25] md:px-8">
					<Carousel.Previous
						class="static h-11 w-11 translate-y-0 rounded-full border border-[#e67a25]/20 bg-[#e67a25]/10 text-[#e67a25] shadow-none backdrop-blur-sm transition-all hover:bg-[#e67a25]/20 hover:text-[#e67a25]"
					/>
					<span class="text-xs font-black tracking-[0.2em] text-[#e67a25]/60 uppercase animate-pulse">
						desliza hacia los lados
					</span>
					<Carousel.Next
						class="static h-11 w-11 translate-y-0 rounded-full border border-[#e67a25]/20 bg-[#e67a25]/10 text-[#e67a25] shadow-none backdrop-blur-sm transition-all hover:bg-[#e67a25]/20 hover:text-[#e67a25]"
					/>
				</div>
			</Carousel.Root>
		</div>
	</div>
</section>
