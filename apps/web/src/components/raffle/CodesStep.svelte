<script lang="ts">
  import type { RaffleBranch } from "../../lib/raffle";

  export let selectedBranch: RaffleBranch;
  export let codesText: string;
  export let loading = false;
  export let error = "";
  export let onBack: () => void;
  export let onValidate: (codesText: string) => void;
</script>

<article class="card">
  <button class="back-button" type="button" on:click={onBack}>
    Cambiar sucursal
  </button>

  <p class="eyebrow">Paso 2</p>
  <h2>Registra tus códigos de boleto</h2>

  <p class="muted">
    Sucursal: {selectedBranch.name}. Puedes cargar hasta 10 códigos por vez.
  </p>

  <label class="code-field">
    Códigos de boleto
    <textarea
      bind:value={codesText}
      placeholder="A7K2P9&#10;M4X8Q1&#10;Z9T3L6"
      rows="8"
    ></textarea>
  </label>

  <p class="helper">Escribe un código por línea o sepáralos con coma.</p>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <button
    class="primary-button"
    type="button"
    disabled={loading}
    on:click={() => onValidate(codesText)}
  >
    {loading ? "Validando..." : "Validar boletos"}
  </button>
</article>

<style>
  .card {
    width: 100%;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.05);
    color: inherit;
  }

  .back-button {
    width: fit-content;
    margin-bottom: 1rem;
    border: 0;
    background: transparent;
    color: rgba(255, 255, 255, 0.72);
    font-weight: 800;
    cursor: pointer;
  }

  .eyebrow {
    margin: 0 0 0.5rem;
    font-size: 0.75rem;
    font-weight: 850;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.65;
  }

  h2,
  p {
    margin: 0;
  }

  h2 {
    margin-bottom: 0.75rem;
  }

  .muted {
    color: rgba(255, 255, 255, 0.68);
  }

  .code-field {
    display: grid;
    gap: 0.5rem;
    margin-top: 1.25rem;
    font-weight: 800;
  }

  textarea {
    width: 100%;
    padding: 0.9rem;
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.24);
    color: inherit;
    font: inherit;
    resize: vertical;
  }

  .helper {
    margin-top: 0.5rem;
    color: rgba(255, 255, 255, 0.56);
    font-size: 0.9rem;
  }

  .error {
    margin-top: 0.75rem;
    color: #ff7373;
  }

  .primary-button {
    min-height: 44px;
    margin-top: 1rem;
    padding: 0 1.1rem;
    border: 0;
    border-radius: 999px;
    background: #ffffff;
    color: #000000;
    font-weight: 850;
    cursor: pointer;
  }

  .primary-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
</style>
