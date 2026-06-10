<script lang="ts">
	import AnimatedTestimonials from '$lib/components/pages/AnimatedTestimonials.svelte';

	// Sucursales Data
	const locationsData = [
		{
			name: 'Pinturas Star Colors - Burócrata',
			src: '/images/contacto/burocrata.jpg',
			details: [
				'<strong>Dirección:</strong> Av. Luis Pasteur Sur 210, zona dos extendida, Corregidora, 76070 Santiago de Querétaro, Qro.',
				'<strong>Áreas de servicio:</strong> Santiago de Querétaro',
				'<strong>Horario:</strong> Abre a las 9 a.m. del mar',
				'<strong>Teléfono:</strong> 442 187 8771',
				'<strong>Opciones de servicio:</strong> Ofrece entrega el mismo día'
			]
		},
		{
			name: 'Pinturas Star Colors - El Pueblito',
			src: '/images/contacto/pueblito.jpg',
			details: [
				'<strong>Dirección:</strong> Miguel Hidalgo 47, El Pueblito, 76900 Santiago de Querétaro, Qro.',
				'<strong>Horario:</strong> Abre a las 9 a.m. del mar',
				'<strong>Teléfono:</strong> 442 225 1825',
				'<strong>Opciones de servicio:</strong> Ofrece entrega el mismo día'
			]
		},
		{
			name: 'Pinturas Star Colors - Constituyentes',
			src: '/images/contacto/constituyentes.jpg',
			details: [
				'<strong>Dirección:</strong> Carretera Libre a celaya Kilometro 6.5, El Pueblito, 76900 Santiago de Querétaro, Qro.',
				'<strong>Horario:</strong> Abre a las 8 a.m. del mar',
				'<strong>Teléfono:</strong> 442 447 3785',
				'<strong>Opciones de servicio:</strong> Ofrece entrega el mismo día'
			]
		}
	];
</script>

<svelte:head>
	<title>Contacto | SC-Servicios</title>
</svelte:head>

<section
	class="flex min-h-[calc(100vh-80px)] flex-col items-center justify-center bg-transparent px-4 py-8 md:px-8"
>
	<div class="mx-auto flex w-full max-w-5xl flex-col items-center">
		<h2 class="mb-12 text-center text-3xl font-semibold tracking-widest text-gray-800 md:text-4xl">
			NUESTRAS SUCURSALES
		</h2>

		<AnimatedTestimonials testimonials={locationsData} autoplay={true} interval={6000} />
	</div>
</section>
