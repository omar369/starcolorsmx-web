<script lang="ts">
  import type { QuoteForm } from "../types";

  export let form: QuoteForm;
  export let errors: Record<string, string> = {};

  $: contactLabel =
    form.contact_method === "whatsapp"
      ? "Número de WhatsApp"
      : form.contact_method === "email"
        ? "Correo electrónico"
        : "Dato de contacto";

  $: contactPlaceholder =
    form.contact_method === "whatsapp"
      ? "Ej. 4421234567"
      : form.contact_method === "email"
        ? "ejemplo@correo.com"
        : "Selecciona primero un método";

  $: contactType =
    form.contact_method === "whatsapp"
      ? "tel"
      : form.contact_method === "email"
        ? "email"
        : "text";
</script>

<section class="grid gap-3.5 min-h-0">
  <!-- Heading -->
  <div class="grid gap-1">
    <p class="m-0 text-[#8a6b00] text-[0.68rem] font-black tracking-[0.08em] uppercase">
      Contacto
    </p>
    <h2 class="m-0 text-[#101827] text-[clamp(1.4rem,6vw,2rem)] font-black leading-none tracking-tight">
      ¿A dónde enviamos la precotización?
    </h2>
    <p class="m-0 text-[#526070] text-[0.84rem] leading-snug">
      No necesitas crear cuenta para recibir la primera estimación.
    </p>
  </div>

  <!-- Form -->
  <div class="grid gap-2.5">
    <!-- Nombre -->
    <label class="grid gap-1.5 cursor-pointer" for="customer_name">
      <span class="text-[#273549] text-[0.82rem] font-bold">
        Nombre del cliente <strong class="text-amber-600 font-black">*</strong>
      </span>
      <input
        id="customer_name"
        type="text"
        placeholder="Ej. Omar Castillo"
        bind:value={form.customer_name}
        autocomplete="name"
        aria-invalid={Boolean(errors.customer_name)}
        class="
          w-full min-h-[44px]
          border-[1.5px] border-[#d9e0ea] rounded-xl
          bg-white text-[#172033] text-[0.9rem]
          px-3 py-2.5 font-[inherit]
          transition-[border-color,box-shadow] duration-150
          focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
          aria-[invalid=true]:border-rose-500
        "
      />
      {#if errors.customer_name}
        <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.customer_name}</span>
      {/if}
    </label>

    <!-- Método + dato de contacto — 2 cols -->
    <div class="grid grid-cols-[120px_1fr] gap-2.5 items-start">
      <label class="grid gap-1.5 cursor-pointer min-w-0" for="contact_method">
        <span class="text-[#273549] text-[0.82rem] font-bold">
          Vía <strong class="text-amber-600 font-black">*</strong>
        </span>
        <select
          id="contact_method"
          bind:value={form.contact_method}
          aria-invalid={Boolean(errors.contact_method)}
          class="
            w-full min-h-[44px] appearance-auto
            border-[1.5px] border-[#d9e0ea] rounded-xl
            bg-white text-[#172033] text-[0.88rem]
            px-2.5 py-2.5 font-[inherit]
            transition-[border-color,box-shadow] duration-150
            focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
            aria-[invalid=true]:border-rose-500
          "
        >
          <option value="">Elige</option>
          <option value="whatsapp">WhatsApp</option>
          <option value="email">Email</option>
        </select>
        {#if errors.contact_method}
          <span class="text-rose-700 text-[0.68rem] font-semibold">{errors.contact_method}</span>
        {/if}
      </label>

      <label class="grid gap-1.5 cursor-pointer min-w-0" for="contact_value">
        <span class="text-[#273549] text-[0.82rem] font-bold truncate">
          {contactLabel} <strong class="text-amber-600 font-black">*</strong>
        </span>
        <input
          id="contact_value"
          type={contactType}
          placeholder={contactPlaceholder}
          bind:value={form.contact_value}
          disabled={!form.contact_method}
          autocomplete={form.contact_method === "email" ? "email" : "tel"}
          aria-invalid={Boolean(errors.contact_value)}
          class="
            w-full min-h-[44px]
            border-[1.5px] border-[#d9e0ea] rounded-xl
            bg-white text-[#172033] text-[0.9rem]
            px-3 py-2.5 font-[inherit]
            transition-[border-color,box-shadow] duration-150
            focus:outline-none focus:border-amber-400 focus:shadow-[0_0_0_3px_rgba(245,183,0,0.18)]
            aria-[invalid=true]:border-rose-500
            disabled:bg-[#f1f5f9] disabled:text-[#94a3b8] disabled:cursor-not-allowed
          "
        />
        {#if errors.contact_value}
          <span class="text-rose-700 text-[0.7rem] font-semibold">{errors.contact_value}</span>
        {/if}
      </label>
    </div>

    <!-- Checkbox -->
    <label class="flex items-start gap-3 cursor-pointer mt-1">
      <input
        type="checkbox"
        bind:checked={form.wants_offers}
        class="mt-0.5 w-4 h-4 shrink-0 cursor-pointer accent-amber-400"
      />
      <span class="text-[#526070] text-[0.84rem] leading-snug">
        Quiero recibir ofertas y recomendaciones de pintura.
      </span>
    </label>
  </div>
</section>
