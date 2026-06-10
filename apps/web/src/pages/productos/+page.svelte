<script lang="ts">
  import ProductCard from "$lib/components/pages/ProductCard.svelte";
  import type { Measurement } from "$lib/components/pages/ProductCard.svelte";

  // Mock Schema Details based on the provided design image
  const products: {
    title: string;
    themeColor: string;
    measurements: Measurement[];
    description: string;
    coverage: string;
    finish: string;
    qualityYears: number;
    intensities: number[];
    imageSrc: string;
  }[] = [
    {
      title: "VIN J INTERIOR JR",
      themeColor: "#77b3aa", // Teal color
      description:
        "La pintura VIN J INTERIOR JR es una buena opción cuando se necesita economizar, ya que esta línea le ofrece un buen rendimiento para pintar interiores o dar mantenimiento a un bajo costo. Aun siendo la calidad mas sencilla de pinturas que manejamos, estamos convencidos de su excelente calidad a comparación de otros productos en el mercado. Los colores que ofrece esta calidad son colores blanco y tonos pastel. (Intensidad 1)",
      coverage: "4 a 5 M2 X LITRO",
      finish: "MATE",
      qualityYears: 2,
      intensities: [1],
      imageSrc: "/images/productos/J.png",
      measurements: [
        { label: "Litro", price: "N/A" },
        { label: "4 Lts", price: "N/A" },
        { label: "19 Lts", price: "$625.00" },
      ],
    },
    {
      title: "VIN I INTERIOR PRO",
      themeColor: "#E5D88F", // Yellow / Gold color
      description:
        "VIN I INTERIOR PRO es ideal para construcciones donde requiere un buen rendimiento, mayor poder cubriente y durabilidad a bajo costo. Esta calidad es recomendada para aplicarse en interior. Estamos convencidos de su excelente calidad a comparación de otros productos en el mercado. Los colores de esta calidad son Blanco y tonos pastel en Intensidad 1 y 2.",
      coverage: "4 a 5 M2 X LITRO",
      finish: "MATE",
      qualityYears: 3,
      intensities: [1, 2],
      imageSrc: "/images/productos/I.png",
      measurements: [
        { label: "Litro", price: "N/A" },
        { label: "4 Lts", price: "$200.00" },
        { label: "19 Lts", price: "$755.00" },
      ],
    },
    {
      title: "VIN M EXTERIOR",
      themeColor: "#A08365", // Bronze / Orange color
      description:
        "Pintura vinil-acrílica Vin M EXTERIOR muy buena calidad para interiores o exteriores, cuenta con un mayor rendimiento, poder cubriente y mas resistente comparado a nuestras lineas anteriores. Siendo nuestra primera calidad que se puede aplicar en exterior. La variedad de colores en el catalogo es mayor y cuenta con colores en intensidad 1, 2, 3, 4.",
      coverage: "5 a 6 M2 X LITRO",
      finish: "MATE",
      qualityYears: 5,
      intensities: [1, 2, 3, 4],
      imageSrc: "/images/productos/M.png",
      measurements: [
        { label: "Litro", price: "N/A" },
        { label: "4 Lts", price: "$260.00" },
        { label: "19 Lts", price: "$1030.00" },
      ],
    },
    {
      title: "VIN R EXTERIOR PRO",
      themeColor: "#F26522", // Orange color
      description:
        "Pintura Vinil-acrílica que reune las condiciones optimas de rendimiento, duracion y lavabilidad, permitiendo cuidar su economia. Recomendada para interiores y exteriores. Cuenta con una extensa variedad de los mejores colores, los cuales son firmes y resistentes a la interperie. Tonos disponibles intensidad 1, 2, 3, 4, 5, 6 y 7.",
      coverage: "7 M2 X LITRO",
      finish: "MATE",
      qualityYears: 7,
      intensities: [1, 2, 3, 4, 5, 6, 7],
      imageSrc: "/images/productos/R.png",
      measurements: [
        { label: "Litro", price: "$90.00" },
        { label: "4 Lts", price: "$325.00" },
        { label: "19 Lts", price: "$1310.00" },
      ],
    },
    {
      title: "VIN E PREMIUM MATE",
      themeColor: "#c44f46", // Red color
      description:
        "Pintura vinil-acrílica de alta calidad y resistencia, ideal para construcciones expuestas a severas condiciones ambientales. El optimo equilibrio en su formulacion permite obtener un magnifico rendimiento asi como mayor poder cubriente. Tonos disponibles intensidad 1, 2, 3, 4, 5, 6 y 7.",
      coverage: "8 M2 X LITRO",
      finish: "MATE",
      qualityYears: 10,
      intensities: [1, 2, 3, 4, 5, 6, 7],
      imageSrc: "/images/productos/E.png",
      measurements: [
        { label: "Litro", price: "$130.00" },
        { label: "4 Lts", price: "$450.00" },
        { label: "19 Lts", price: "$1,895.00" },
      ],
    },
    {
      title: "VIN E PREMIUM SATIN",
      themeColor: "#A8BF33", // Green color
      description:
        "Pintura vinil-acrílica de alta calidad y resistencia acabado satinado, ideal para construcciones expuestas a severas condiciones ambientales. El optimo equilibrio en su formulacion permite obtener un magnifico rendimiento asi como mayor poder cubriente. Tonos disponibles intensidad 1, 2, 3, 4, 5, 6 y 7.",
      coverage: "9 a 10 M2 X LITRO",
      finish: "SATINADO",
      qualityYears: 10,
      intensities: [1, 2, 3, 4, 5, 6, 7],
      imageSrc: "/images/productos/ES.png",
      measurements: [
        { label: "Litro", price: "$160.00" },
        { label: "4 Lts", price: "$620.00" },
        { label: "19 Lts", price: "$2,678.00" },
      ],
    },
  ];
</script>

<svelte:head>
  <title>Productos | SC-Servicios</title>
</svelte:head>

<section class="min-h-screen px-4 py-16 md:px-8">
  <div class="mx-auto max-w-7xl">
    <div class="mb-12 text-center">
      <h1
        class="text-4xl font-extrabold tracking-tight text-gray-900 sm:text-5xl"
      >
        Nuestro Catálogo
      </h1>
      <p class="mx-auto mt-4 max-w-2xl text-lg text-gray-600">
        Explora nuestra selección completa de pinturas de alta calidad,
        diseñadas para brindarte el mejor rendimiento, durabilidad y cobertura
        en todos tus proyectos.
      </p>
    </div>

    <!-- Product Grid / Stack Layout -->
    <div class="flex flex-col items-center gap-10">
      {#each products as pt}
        <ProductCard
          title={pt.title}
          themeColor={pt.themeColor}
          description={pt.description}
          coverage={pt.coverage}
          finish={pt.finish}
          qualityYears={pt.qualityYears}
          intensities={pt.intensities}
          imageSrc={pt.imageSrc}
          measurements={pt.measurements}
          class="transition-transform duration-300 hover:-translate-y-1 hover:shadow-lg"
        />
      {/each}
    </div>
  </div>
</section>
