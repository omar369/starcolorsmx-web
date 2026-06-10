<script lang="ts">
	import ServiceCard from '$lib/components/pages/ServiceCard.svelte';

	// Mock Schema Details based on the provided design image
	const services = [
		{
			title: 'AP Vin R',
			themeColor: '#F26522', // Red/Orange
			description:
				'SERVICIO BÁSICO INCLUYE:\n- LIMPIEZA EN MUROS (POLVO Y PINTURA EN MAL ESTADO).\n- RESANE EN GRIETAS Y CLAVOS.\n- PRIMERA Y SEGUNDA MANO DEL PRODUCTO (3RA DE SER NECESARIO)\n- LIMPIEZA DEL AREA DE TRABAJO.\n\nSERVICIO CON COSTO ADICIONAL:\n- ALTURA MAYOR A 6 MTS\n- ANDAMIOS\n- HAMACA\n- GRUA\n- RESANE MAYOR\n- PINTURA EN MOLDURAS\n- DISTANCIA MAYOR A 25 KM DEL PV\n- SELLADO DE MURO\n- FONDEO BLANCO\n- LIJADO',
			qualityYears: 7,
			imageSrc: '/images/productos/R.png',
			stockImageSrc: '/images/servicios/1.png'
		},
		{
			title: 'AP Vin E',
			themeColor: '#c44f46', // Cardinal Red
			description:
				'SERVICIO BÁSICO INCLUYE:\n- LIMPIEZA EN MUROS (POLVO Y PINTURA EN MAL ESTADO).\n- RESANE EN GRIETAS Y CLAVOS.\n- PRIMERA Y SEGUNDA MANO DEL PRODUCTO (3RA DE SER NECESARIO)\n- LIMPIEZA DEL AREA DE TRABAJO.\n\nSERVICIO CON COSTO ADICIONAL:\n- ALTURA MAYOR A 6 MTS\n- ANDAMIOS\n- HAMACA\n- GRUA\n- RESANE MAYOR\n- PINTURA EN MOLDURAS\n- DISTANCIA MAYOR A 25 KM DEL PV\n- SELLADO DE MURO\n- FONDEO BLANCO\n- LIJADO',
			qualityYears: 10,
			imageSrc: '/images/productos/E.png',
			stockImageSrc: '/images/servicios/2.png'
		},
		{
			title: 'AP Vin Es',
			themeColor: '#A8BF33', // Green
			description:
				'SERVICIO BÁSICO INCLUYE:\n- LIMPIEZA EN MUROS (POLVO Y PINTURA EN MAL ESTADO).\n- RESANE EN GRIETAS Y CLAVOS.\n- PRIMERA Y SEGUNDA MANO DEL PRODUCTO (3RA DE SER NECESARIO)\n- LIMPIEZA DEL AREA DE TRABAJO.\n\nSERVICIO CON COSTO ADICIONAL:\n- ALTURA MAYOR A 6 MTS\n- ANDAMIOS\n- HAMACA\n- GRUA\n- RESANE MAYOR\n- PINTURA EN MOLDURAS\n- DISTANCIA MAYOR A 25 KM DEL PV\n- SELLADO DE MURO\n- FONDEO BLANCO\n- LIJADO',
			qualityYears: 10,
			imageSrc: '/images/productos/ES.png',
			stockImageSrc: '/images/servicios/3.png'
		},
		{
			title: 'AP Vin Pro',
			themeColor: '#0F7F8C', // Teal/Cyan
			description:
				'SERVICIO BÁSICO INCLUYE:\n- LIMPIEZA EN MUROS (POLVO Y PINTURA EN MAL ESTADO).\n- RESANE EN GRIETAS Y CLAVOS.\n- PRIMERA Y SEGUNDA MANO DEL PRODUCTO (3RA DE SER NECESARIO)\n- LIMPIEZA DEL AREA DE TRABAJO.\n\nSERVICIO CON COSTO ADICIONAL:\n- ALTURA MAYOR A 6 MTS\n- ANDAMIOS\n- HAMACA\n- GRUA\n- RESANE MAYOR\n- PINTURA EN MOLDURAS\n- DISTANCIA MAYOR A 25 KM DEL PV\n- SELLADO DE MURO\n- FONDEO BLANCO\n- LIJADO',
			qualityYears: 12,
			imageSrc: '', // Fallback
			stockImageSrc: '/images/servicios/4.png'
		}
	];

	const impermeabilizantes = [
		{
			title: 'AP Acristar 4 años',
			themeColor: '#00908F', // Teal color from image
			description:
				'SERVICIO BÁSICO INCLUYE:\n- LIMPIEZA EN MUROS (POLVO).\n- CALEFATEO DE GRIETAS CON SILICÓN POLIURETANO.\n- SELLADO CON ACRISTAR 5 X 1\n- 3 MANOS DEL PRODUCTO\n- LIMPIEZA DE AREA DE TRABAJO.\n- ENTREGA HOJA DE GARANTIA.\n\nSERVICIO CON COSTO ADICIONAL:\n- GRUA\n- RESANE MAYOR\n- MAS DE 2DO NIVEL\n- COLOR ESPECIAL\n- LECHAREADA EN SUPERFICIE\n- DISTANCIA MAYOR A 25 KM DEL PV\n- NIVELACION\n- RETIRO DE MATERIAL ANTERIOR',
			qualityYears: 4,
			imageSrc: '', // Pending bucket image
			stockImageSrc: '/images/servicios/9.png'
		},
		{
			title: 'AP Acristar 6 años',
			themeColor: '#00908F', // Same teal
			description:
				'SERVICIO BÁSICO INCLUYE:\n- LIMPIEZA EN MUROS (POLVO).\n- CALEFATEO DE GRIETAS CON SILICÓN POLIURETANO.\n- SELLADO CON ACRISTAR 5 X 1\n- 3 MANOS DEL PRODUCTO\n- LIMPIEZA DE AREA DE TRABAJO.\n- ENTREGA HOJA DE GARANTIA.\n\nSERVICIO CON COSTO ADICIONAL:\n- GRUA\n- RESANE MAYOR\n- MAS DE 2DO NIVEL\n- COLOR ESPECIAL\n- LECHAREADA EN SUPERFICIE\n- DISTANCIA MAYOR A 25 KM DEL PV\n- NIVELACION\n- RETIRO DE MATERIAL ANTERIOR',
			qualityYears: 6,
			imageSrc: '',
			stockImageSrc: '/images/servicios/12.png'
		},
		{
			title: 'AP Acristar 8 años',
			themeColor: '#00908F',
			description:
				'SERVICIO BÁSICO INCLUYE:\n- LIMPIEZA EN MUROS (POLVO).\n- CALEFATEO DE GRIETAS CON SILICÓN POLIURETANO.\n- SELLADO CON ACRISTAR 5 X 1\n- 3 MANOS DEL PRODUCTO\n- LIMPIEZA DE AREA DE TRABAJO.\n- ENTREGA HOJA DE GARANTIA.\n\nSERVICIO CON COSTO ADICIONAL:\n- GRUA\n- RESANE MAYOR\n- MAS DE 2DO NIVEL\n- COLOR ESPECIAL\n- LECHAREADA EN SUPERFICIE\n- DISTANCIA MAYOR A 25 KM DEL PV\n- NIVELACION\n- RETIRO DE MATERIAL ANTERIOR',
			qualityYears: 8,
			imageSrc: '',
			stockImageSrc: '/images/servicios/11.png'
		}
	];
</script>

<svelte:head>
	<title>Servicios | SC-Servicios</title>
</svelte:head>

<section class="min-h-screen px-4 py-16 md:px-8">
	<div class="mx-auto max-w-7xl">
		<div class="mb-12 text-center">
			<h1 class="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl">
				Nuestros Servicios
			</h1>
			<p class="mx-auto mt-4 max-w-2xl text-lg text-gray-600">
				Explora nuestra selección completa de pinturas de alta calidad, diseñadas para brindarte el
				mejor rendimiento, durabilidad y cobertura en todos tus proyectos.
			</p>
		</div>

		<!-- Product Grid / Stack Layout - Pintura Vinílica -->
		<div class="mb-16">
			<h2 class="mb-8 text-center text-3xl font-bold tracking-widest text-gray-800 uppercase">
				Pintura Vinílica
			</h2>
			<div class="flex flex-col items-center gap-10">
				{#each services as pt}
					<ServiceCard
						title={pt.title}
						themeColor={pt.themeColor}
						description={pt.description}
						qualityYears={pt.qualityYears}
						imageSrc={pt.imageSrc}
						stockImageSrc={pt.stockImageSrc}
						class="transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg"
					/>
				{/each}
			</div>
		</div>

		<!-- Product Grid / Stack Layout - Impermeabilizante -->
		<div>
			<h2 class="mb-8 text-center text-3xl font-bold tracking-widest text-gray-800 uppercase">
				Impermeabilizante
			</h2>
			<div class="flex flex-col items-center gap-10">
				{#each impermeabilizantes as pt}
					<ServiceCard
						title={pt.title}
						themeColor={pt.themeColor}
						description={pt.description}
						qualityYears={pt.qualityYears}
						imageSrc={pt.imageSrc}
						stockImageSrc={pt.stockImageSrc}
						class="transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg"
					/>
				{/each}
			</div>

			<div class="mt-8 text-center text-lg font-bold tracking-widest text-gray-600">
				PRECIOS MAS I.V.A.
			</div>
		</div>
	</div>
</section>
