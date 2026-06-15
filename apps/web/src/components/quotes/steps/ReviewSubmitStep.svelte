<script lang="ts">
  import type {
    BasicOption,
    QuoteForm,
    QuoteOptions,
    QuoteResult,
  } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let quoteResult: QuoteResult | null = null;

  function optionName(list: BasicOption[], id: string) {
    return list.find((o) => o.id === id)?.name ?? "No especificado";
  }

  function optionNameList(list: BasicOption[], ids: string[]): string[] {
    if (!Array.isArray(ids) || ids.length === 0) return [];
    return ids.map((id) => list.find((o) => o.id === id)?.name ?? id);
  }

  function val(value: unknown) {
    if (Array.isArray(value))
      return value.length > 0 ? value.join(", ") : "No especificado";
    if (typeof value === "boolean") return value ? "Sí" : "No";
    if (typeof value === "number") return String(value);
    if (typeof value === "string")
      return value.trim() !== "" ? value : "No especificado";
    return "No especificado";
  }

  function money(value: number) {
    return new Intl.NumberFormat("es-MX", {
      style: "currency",
      currency: "MXN",
    }).format(value);
  }

  // Computed lists
  $: preparationNames = optionNameList(options.preparations, form.preparation);
</script>

<!--
  Este step tiene scroll propio para que en cualquier tamaño de celular
  el usuario pueda revisar toda la información antes de enviar.
-->
<section
  class="flex flex-col gap-3 min-h-0 h-full overflow-y-auto overflow-x-hidden pr-0.5 -mr-0.5"
>
  <!-- Heading -->
  <div class="grid gap-0.5 shrink-0">
    <h2
      class="m-0 text-[#101827] text-[clamp(1.3rem,5.5vw,1.8rem)] font-black leading-tight tracking-tight"
    >
      Confirmar y enviar
    </h2>
    <p class="m-0 text-[#526070] text-[0.84rem] leading-snug">
      Revisa todos los datos antes de enviar. Puedes regresar a corregir
      cualquier campo.
    </p>
  </div>

  <!-- ── Summary card ── -->
  <div
    class="grid gap-0 border-[1.5px] border-[#e2e8f0] rounded-2xl bg-[#f8fafc] overflow-hidden shrink-0"
  >
    <!-- Sección: Proyecto -->
    <div class="px-3.5 py-2.5 grid gap-1">
      <span
        class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
        >Proyecto</span
      >
      <div class="grid gap-0.5">
        <span class="text-[#172033] text-[0.8rem] font-semibold leading-snug">
          {optionName(options.property_types, form.property_type)}
        </span>
        <span class="text-[#475569] text-[0.76rem]">
          {optionName(options.work_locations, form.work_location)} ·
          {optionName(options.service_types, form.service_type)}
        </span>
      </div>
    </div>

    <div class="border-t border-[#e2e8f0]"></div>

    <!-- Sección: Área + Pintura (2 cols) -->
    <div class="grid grid-cols-2 divide-x divide-[#e2e8f0]">
      <div class="px-3.5 py-2.5 grid gap-0.5">
        <span
          class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
          >Área</span
        >
        <span class="text-[#172033] text-[0.88rem] font-black leading-tight">
          {val(form.square_meters)}
          <span class="text-[0.72rem] font-semibold text-[#64748b]">m²</span>
        </span>
      </div>
      <div class="px-3.5 py-2.5 grid gap-0.5">
        <span
          class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
          >Pintura</span
        >
        <span class="text-[#172033] text-[0.8rem] font-semibold leading-snug">
          {optionName(options.paints, form.paint_product)}
        </span>
        <span class="text-[#475569] text-[0.74rem]">
          {optionName(options.color_intensities, form.color_intensity)}
        </span>
      </div>
    </div>

    <div class="border-t border-[#e2e8f0]"></div>

    <!-- Sección: Superficie (estado + textura) -->
    <div class="grid grid-cols-2 divide-x divide-[#e2e8f0]">
      <div class="px-3.5 py-2.5 grid gap-0.5">
        <span
          class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
          >Estado</span
        >
        <span class="text-[#172033] text-[0.8rem] font-semibold leading-snug">
          {optionName(options.surface_states, form.surface_state)}
        </span>
      </div>
      <div class="px-3.5 py-2.5 grid gap-0.5">
        <span
          class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
          >Textura</span
        >
        <span class="text-[#172033] text-[0.8rem] font-semibold leading-snug">
          {optionName(options.textures, form.texture)}
        </span>
      </div>
    </div>

    <div class="border-t border-[#e2e8f0]"></div>

    <!-- Sección: Preparación de superficie — multi-valor con chips -->
    <div class="px-3.5 py-2.5 grid gap-1.5">
      <span
        class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
      >
        Preparación de superficie
      </span>
      {#if preparationNames.length > 0}
        <div class="flex flex-wrap gap-1.5">
          {#each preparationNames as name}
            <span
              class="inline-flex items-center px-2.5 py-0.5 rounded-full border border-amber-300 bg-amber-50 text-amber-900 text-[0.72rem] font-bold"
            >
              {name}
            </span>
          {/each}
        </div>
      {:else}
        <span class="text-[#64748b] text-[0.78rem]">Sin preparación adicional <span class="text-[#94a3b8]">· sin ajuste de costo</span></span>
      {/if}
    </div>

    <div class="border-t border-[#e2e8f0]"></div>

    <!-- Sección: Protección del área -->
    <div class="px-3.5 py-2.5 grid gap-0.5">
      <span
        class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
        >Protección del área</span
      >
      <span class="text-[#172033] text-[0.8rem] font-semibold leading-snug">
        {optionName(options.area_protections, form.area_protection)}
      </span>
    </div>

    <div class="border-t border-[#e2e8f0]"></div>

    <!-- Sección: Condiciones de trabajo -->
    <div class="px-3.5 py-2.5 grid gap-1">
      <span
        class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
        >Condiciones de trabajo</span
      >
      <div class="grid grid-cols-3 gap-2">
        <div class="grid gap-0.5">
          <span class="text-[#94a3b8] text-[0.62rem] font-bold uppercase"
            >Dificultad</span
          >
          <span
            class="text-[#172033] text-[0.76rem] font-semibold leading-tight"
          >
            {optionName(options.advance_difficulties, form.advance_difficulty)}
          </span>
        </div>
        <div class="grid gap-0.5">
          <span class="text-[#94a3b8] text-[0.62rem] font-bold uppercase"
            >Altura</span
          >
          <span
            class="text-[#172033] text-[0.76rem] font-semibold leading-tight"
          >
            {optionName(options.height_risks, form.height_risk)}
          </span>
        </div>
        <div class="grid gap-0.5">
          <span class="text-[#94a3b8] text-[0.62rem] font-bold uppercase"
            >Horario</span
          >
          <span
            class="text-[#172033] text-[0.76rem] font-semibold leading-tight"
          >
            {optionName(options.schedules, form.schedule)}
          </span>
        </div>
      </div>
    </div>

    <div class="border-t border-[#e2e8f0]"></div>

    <!-- Sección: Ubicación -->
    <div class="px-3.5 py-2.5 grid gap-0.5">
      <span
        class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
        >Ubicación</span
      >
      <span class="text-[#172033] text-[0.8rem] font-semibold leading-snug">
        {optionName(options.states, form.state)}, {val(form.city)}
      </span>
      <span class="text-[#475569] text-[0.74rem]"
        >CP {val(form.postal_code)}</span
      >
    </div>

    <div class="border-t border-[#e2e8f0]"></div>

    <!-- Sección: Contacto -->
    <div class="px-3.5 py-2.5 grid gap-0.5">
      <span
        class="text-[#64748b] text-[0.66rem] font-black uppercase tracking-wider"
        >Contacto</span
      >
      <span class="text-[#172033] text-[0.8rem] font-semibold leading-snug">
        {val(form.customer_name)}
      </span>
      <span class="text-[#475569] text-[0.74rem]">
        {form.contact_method === "whatsapp" ? "WhatsApp" : "Email"}: {val(
          form.contact_value,
        )}
      </span>
    </div>
  </div>

  <!-- ── Result card (visible después del cálculo) ── -->
  {#if quoteResult}
    <article
      class="grid gap-1.5 border-[1.5px] border-emerald-200 rounded-2xl bg-[#f0fdf4] px-3.5 py-3 shrink-0"
      aria-live="polite"
    >
      <p
        class="m-0 text-emerald-700 text-[0.76rem] font-black uppercase tracking-wide"
      >
        Precotización estimada
      </p>
      <strong
        class="block text-emerald-900 text-[clamp(1.8rem,8vw,2.8rem)] font-black leading-none"
      >
        {money(quoteResult.estimated_price)}
      </strong>
      <p
        class="m-0 border-t border-emerald-200 text-emerald-700 text-[0.8rem] leading-snug pt-2"
      >
        El cálculo ya incluye las condiciones seleccionadas. Un asesor puede
        confirmar el precio final si el trabajo requiere visita técnica.
      </p>
    </article>
  {/if}
</section>
