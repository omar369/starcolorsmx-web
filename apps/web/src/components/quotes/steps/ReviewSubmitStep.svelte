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
    return list.find((option) => option.id === id)?.name ?? "No especificado";
  }

  function optionNames(list: BasicOption[], ids: string[]) {
    if (!Array.isArray(ids) || ids.length === 0) return "No especificado";
    return ids.map((id) => optionName(list, id)).join(", ");
  }

  function val(value: unknown) {
    if (Array.isArray(value)) return value.length > 0 ? value.join(", ") : "No especificado";
    if (typeof value === "boolean") return value ? "Sí" : "No";
    if (typeof value === "number") return String(value);
    if (typeof value === "string") return value.trim() !== "" ? value : "No especificado";
    return "No especificado";
  }

  function money(value: number) {
    return new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN" }).format(value);
  }
</script>

<section class="grid gap-3 min-h-0">
  <!-- Heading -->
  <div class="grid gap-0.5">
    <h2 class="m-0 text-[#101827] text-[clamp(1.4rem,6vw,2rem)] font-black leading-tight tracking-tight">
      Confirmar y enviar
    </h2>
    <p class="m-0 text-[#526070] text-[0.84rem] leading-snug">
      Revisa el resumen antes de enviar. Puedes regresar si necesitas corregir.
    </p>
  </div>

  <!-- Summary card -->
  <dl class="m-0 grid gap-0 border-[1.5px] border-[#e2e8f0] rounded-2xl bg-[#f8fafc] overflow-hidden">
    {#each [
      { label: "Proyecto", value: `${optionName(options.property_types, form.property_type)} / ${optionName(options.work_locations, form.work_location)} / ${optionName(options.service_types, form.service_type)}` },
      { label: "Área", value: `${val(form.square_meters)} m²` },
      { label: "Pintura", value: `${optionName(options.paints, form.paint_product)} / ${optionName(options.color_intensities, form.color_intensity)}` },
      { label: "Superficie", value: `${optionName(options.surface_states, form.surface_state)} / ${optionName(options.textures, form.texture)} / ${optionNames(options.preparations, form.preparation)}` },
      { label: "Trabajo", value: `${optionName(options.advance_difficulties, form.advance_difficulty)} / ${optionName(options.height_risks, form.height_risk)} / ${optionName(options.schedules, form.schedule)}` },
      { label: "Ubicación", value: `${optionName(options.states, form.state)} / ${val(form.city)} / CP ${val(form.postal_code)}` },
      { label: "Contacto", value: `${val(form.customer_name)} / ${form.contact_method === "whatsapp" ? "WhatsApp" : "Email"}` },
    ] as row, i}
      <div class="flex justify-between gap-3 px-3.5 py-2.5 {i > 0 ? 'border-t border-[#e2e8f0]' : ''}">
        <dt class="text-[#64748b] text-[0.74rem] font-bold uppercase tracking-wide shrink-0 pt-px">{row.label}</dt>
        <dd class="m-0 text-[#172033] text-[0.8rem] font-semibold text-right leading-snug">{row.value}</dd>
      </div>
    {/each}
  </dl>

  <!-- Result card (shown after API responds) -->
  {#if quoteResult}
    <article class="grid gap-1.5 border-[1.5px] border-emerald-200 rounded-2xl bg-[#f0fdf4] px-3.5 py-3" aria-live="polite">
      <p class="m-0 text-emerald-700 text-[0.76rem] font-black uppercase tracking-wide">Precotización estimada</p>
      <strong class="block text-emerald-900 text-[clamp(1.8rem,8vw,2.8rem)] font-black leading-none">
        {money(quoteResult.estimated_price)}
      </strong>
      <p class="m-0 border-t border-emerald-200 text-emerald-700 text-[0.8rem] leading-snug pt-2">
        El cálculo ya incluye las condiciones seleccionadas. Un asesor puede confirmar el precio final si el trabajo requiere visita técnica.
      </p>
    </article>
  {/if}
</section>
