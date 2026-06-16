<script lang="ts">
  import type {
    BasicOption,
    QuoteAdjustment,
    QuoteForm,
    QuoteOptions,
    QuoteResult,
  } from "../types";

  export let form: QuoteForm;
  export let options: QuoteOptions;
  export let quoteResult: QuoteResult;
  export let onDownloadPdf: () => void;
  export let onSendEmail: () => void;
  export let isSendingEmail: boolean;
  export let emailSuccess: string;
  export let emailError: string;

  function optionName(list: BasicOption[], id: string) {
    return list.find((option) => option.id === id)?.name ?? "No especificado";
  }

  function optionNames(list: BasicOption[], ids: string[]) {
    const names = ids.map((id) => optionName(list, id));
    return names.length > 0 ? names.join(", ") : "No especificado";
  }

  function val(value: string | boolean | undefined) {
    if (typeof value === "boolean") return value ? "Sí" : "No";
    return value && value.trim() !== "" ? value : "No especificado";
  }

  function money(value: number) {
    return new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN" }).format(value);
  }

  function contactMethodLabel(value: string) {
    if (value === "whatsapp") return "WhatsApp";
    if (value === "email") return "correo electrónico";
    return "medio seleccionado";
  }

  function getProjectDescription() {
    return [
      optionName(options.property_types, form.property_type),
      optionName(options.work_locations, form.work_location),
      optionName(options.service_types, form.service_type),
      optionName(options.paints, form.paint_product),
    ].join(" / ");
  }

  function getSurfaceSummary() {
    const importantAdjustments = quoteResult.adjustments
      .filter((a) => a.percentage !== 0)
      .map(formatAdjustment);

    if (importantAdjustments.length > 0) return importantAdjustments.join(", ");

    return [
      optionName(options.surface_states, form.surface_state),
      optionName(options.textures, form.texture),
      optionNames(options.preparations, form.preparation),
      optionName(options.area_protections, form.area_protection),
    ].join(", ");
  }

  function formatAdjustment(adjustment: QuoteAdjustment) {
    const category = adjustment.category.toLowerCase();
    if (category.includes("preparación")) return adjustment.option_name;
    if (category.includes("textura")) return `superficie ${adjustment.option_name.toLowerCase()}`;
    if (category.includes("altura")) return `trabajo en altura ${adjustment.option_name.toLowerCase()}`;
    return adjustment.option_name;
  }
</script>

<section class="grid gap-3 min-h-0">
  <!-- Success header -->
  <div class="grid gap-1">
    <p class="m-0 text-[#8a6b00] text-[0.65rem] font-black tracking-[0.08em] uppercase">
      Precotización generada
    </p>
    <h2 class="m-0 text-[#172033] text-[clamp(1.25rem,5vw,1.7rem)] font-black leading-tight tracking-tight">
      Gracias por usar la herramienta de pre-cotizaciones.
    </h2>
    <p class="m-0 text-[#475569] text-[0.8rem] leading-snug">
      Ya preparamos tu cotización. En el futuro también podrás recibirla por
      <strong class="text-[#172033]">{contactMethodLabel(form.contact_method)}</strong>.
    </p>
  </div>

  <!-- Quote document card -->
  <article class="grid gap-2 border-[1.5px] border-[#e2e8f0] rounded-2xl bg-white p-3" aria-live="polite">
    <!-- Document header -->
    <header class="grid grid-cols-[1fr_auto] gap-2 items-start border-b border-[#e2e8f0] pb-2">
      <div>
        <p class="m-0 text-[#8a6b00] text-[0.62rem] font-black tracking-widest uppercase">StarColors</p>
        <h3 class="m-0 text-[#172033] text-[clamp(0.9rem,3.5vw,1.15rem)] font-black leading-tight">
          Precotización de servicio de pintura
        </h3>
      </div>
      <div class="grid gap-0.5 rounded-xl bg-[#f8fafc] px-2.5 py-2 text-right min-w-[110px]">
        <span class="text-[#64748b] text-[0.6rem] font-black uppercase tracking-wide">Cliente</span>
        <strong class="text-[#172033] text-[0.74rem] leading-tight">{val(form.customer_name)}</strong>
        <small class="text-[#64748b] text-[0.62rem] leading-tight">
          {contactMethodLabel(form.contact_method)}: {val(form.contact_value)}
        </small>
      </div>
    </header>

    <!-- Meta grid: ubicación + proyecto -->
    <div class="grid grid-cols-2 gap-1.5">
      <div class="grid gap-0.5 rounded-xl bg-[#f8fafc] px-2.5 py-2">
        <span class="text-[#64748b] text-[0.6rem] font-black uppercase tracking-wide">Ubicación</span>
        <strong class="text-[#172033] text-[0.74rem] leading-tight">
          {optionName(options.states, form.state)}, {val(form.city)}
        </strong>
        <small class="text-[#64748b] text-[0.62rem]">CP {val(form.postal_code)}</small>
      </div>
      <div class="grid gap-0.5 rounded-xl bg-[#f8fafc] px-2.5 py-2">
        <span class="text-[#64748b] text-[0.6rem] font-black uppercase tracking-wide">Proyecto</span>
        <strong class="text-[#172033] text-[0.74rem] leading-tight">{getProjectDescription()}</strong>
      </div>
    </div>

    <!-- Quote table -->
    <div class="grid overflow-hidden border border-[#e2e8f0] rounded-xl" role="table" aria-label="Resumen de cotización">
      <!-- Head -->
      <div class="grid grid-cols-[0.5fr_1.4fr_0.9fr] bg-[#172033]" role="row">
        <span class="px-2 py-1.5 text-white text-[0.56rem] font-black uppercase tracking-wider" role="columnheader">Cant.</span>
        <span class="px-2 py-1.5 text-white text-[0.56rem] font-black uppercase tracking-wider border-l border-white/10" role="columnheader">Servicio</span>
        <span class="px-2 py-1.5 text-white text-[0.56rem] font-black uppercase tracking-wider border-l border-white/10 text-right" role="columnheader">Importe</span>
      </div>
      <!-- Row -->
      <div class="grid grid-cols-[0.5fr_1.4fr_0.9fr]" role="row">
        <div class="px-2 py-2 grid gap-0 border-r border-[#e2e8f0]" role="cell">
          <strong class="text-[#172033] text-[0.95rem] font-black leading-none">{quoteResult.square_meters}</strong>
          <span class="text-[#64748b] text-[0.64rem] font-black">m²</span>
        </div>
        <div class="px-2 py-2 grid gap-0.5 border-r border-[#e2e8f0]" role="cell">
          <strong class="text-[#172033] text-[0.74rem] leading-tight">{quoteResult.paint_product_name}</strong>
          <p class="m-0 text-[#475569] text-[0.64rem] leading-snug">{getSurfaceSummary()}</p>
        </div>
        <div class="px-2 py-2 flex items-center justify-end" role="cell">
          <strong class="text-emerald-800 text-[clamp(0.9rem,3.5vw,1.1rem)] font-black leading-none text-right">
            {money(quoteResult.estimated_price)}
          </strong>
        </div>
      </div>
    </div>

    <!-- Note -->
    <div class="rounded-xl bg-[#fffbeb] text-[#78350f] text-[0.68rem] leading-snug px-2.5 py-2">
      <strong>Importante:</strong> Este resultado es una pre-cotización generada con los datos capturados.
      El importe final puede cambiar después de una revisión técnica o validación presencial.
    </div>
  </article>

  <!-- PDF download -->
  <div class="grid gap-2 border-[1.5px] border-[#e2e8f0] rounded-2xl bg-[#f8fafc] p-3">
    <p class="m-0 text-[#475569] text-[0.76rem] font-bold">Descarga tu cotización</p>
    <div class="grid grid-cols-2 gap-2">
      <button
        type="button"
        on:click={onDownloadPdf}
        class="
          flex items-center justify-center min-h-[36px]
          border border-dashed border-[#f5b700] rounded-full
          bg-white text-[#172033] text-[0.7rem] font-bold
          px-3 cursor-pointer
          hover:bg-[#fffbeb] transition-colors duration-150
        "
      >
        PDF de cotización
      </button>
      <button
        type="button"
        on:click={onSendEmail}
        disabled={isSendingEmail}
        class="
          flex items-center justify-center min-h-[36px]
          border border-dashed border-[#e67a25] rounded-full
          bg-white text-[#e67a25] text-[0.7rem] font-bold
          px-3 cursor-pointer
          hover:bg-[#fff7ed] transition-colors duration-150
          disabled:opacity-40 disabled:cursor-not-allowed
        "
      >
        {isSendingEmail ? "Enviando..." : "Enviar por correo"}
      </button>
    </div>
    
    {#if emailSuccess}
      <p class="m-0 text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-xl text-[0.7rem] font-bold px-3 py-2 text-center mt-2">
        {emailSuccess}
      </p>
    {/if}
    {#if emailError}
      <p class="m-0 text-red-700 bg-red-50 border border-red-200 rounded-xl text-[0.7rem] font-bold px-3 py-2 text-center mt-2">
        {emailError}
      </p>
    {/if}
  </div>
</section>
