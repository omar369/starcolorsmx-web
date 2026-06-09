<script lang="ts">
  import { onMount } from "svelte";
  import {
    getCurrentUser,
    getStoredUser,
    logoutUser,
    type AuthUser,
  } from "../../lib/auth";

  let user: AuthUser | null = null;
  let loading = true;

  const raffleEnabled = true;

  onMount(async () => {
    const storedUser = getStoredUser();

    if (storedUser) {
      user = storedUser;
    }

    try {
      const currentUser = await getCurrentUser();

      if (!currentUser) {
        window.location.href = "/inscribete?redirect=/hub";
        return;
      }

      user = currentUser;
    } catch {
      logoutUser();
      window.location.href = "/inscribete";
    } finally {
      loading = false;
    }
  });

  function goToRaffle() {
    window.location.href = "/tools/raffle";
  }

  function logout() {
    logoutUser();
    window.location.href = "/inscribete";
  }
</script>

<section class="hub">
  {#if loading}
    <p class="muted">Cargando tu espacio...</p>
  {:else if user}
    <header class="hub-header">
      <div>
        <p class="eyebrow">Portal de clientes</p>
        <h1>Hola, {user.full_name}</h1>
        <p class="muted">{user.email}</p>
      </div>

      <button class="ghost-button" type="button" on:click={logout}>
        Cerrar sesión
      </button>
    </header>

    <section class="hub-content">
      <article class="raffle-panel">
        <p class="card-label">Sorteo activo</p>
        <h2>Entra aquí para elegir tu número</h2>

        {#if raffleEnabled}
          <div class="instructions">
            <p>Puedes ingresar hasta 10 números a la vez.</p>
            <p>Cada boleto es igual a un número.</p>
            <p>
              Los números ocupados aparecen de color gris y no son
              seleccionables.
            </p>
            <p>Los números que elijas se verán de color verde.</p>
            <p>
              Una vez que confirmes tus números, los podrás consultar en esta
              página hasta que la promoción expire.
            </p>
          </div>

          <button class="primary-button" type="button" on:click={goToRaffle}>
            Elegir mi número
          </button>
        {:else}
          <p class="muted">Sin promociones por el momento.</p>
        {/if}
      </article>

      <aside class="side-panel">
        <p class="card-label">Próximamente</p>
        <h3>Mis herramientas</h3>
        <p>
          Aquí aparecerán tus cotizaciones, recompensas y promociones
          disponibles.
        </p>
      </aside>
    </section>
  {/if}
</section>

<style>
  .hub {
    width: min(100%, 1040px);
    margin: 0 auto;
    padding: 1.25rem 1rem 2rem;
    color: #ffffff;
  }

  .hub-header {
    display: grid;
    gap: 1rem;
    margin-bottom: 1.75rem;
  }

  .eyebrow,
  .card-label {
    margin: 0 0 0.5rem;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.65;
  }

  h1,
  h2,
  h3,
  p {
    margin: 0;
  }

  h1 {
    font-size: clamp(2rem, 8vw, 4rem);
    line-height: 1;
  }

  h2 {
    max-width: 11ch;
    margin-bottom: 1rem;
    font-size: clamp(2.1rem, 12vw, 5rem);
    line-height: 0.94;
  }

  h3 {
    margin-bottom: 0.55rem;
    font-size: 1.35rem;
    line-height: 1.1;
  }

  .muted {
    color: rgba(255, 255, 255, 0.65);
  }

  .hub-content {
    display: grid;
    gap: 1.35rem;
  }

  .raffle-panel,
  .side-panel {
    background: transparent;
  }

  .instructions {
    display: grid;
    gap: 0.6rem;
    max-width: 42rem;
    color: rgba(255, 255, 255, 0.76);
    font-size: 0.98rem;
    line-height: 1.55;
  }

  .instructions p {
    padding-left: 0.9rem;
    border-left: 2px solid rgba(255, 255, 255, 0.18);
  }

  .primary-button,
  .ghost-button {
    min-height: 44px;
    padding: 0 1.1rem;
    border-radius: 999px;
    font-weight: 800;
    cursor: pointer;
  }

  .primary-button {
    margin-top: 1.4rem;
    border: 0;
    background: #ffffff;
    color: #000000;
  }

  .ghost-button {
    width: max-content;
    border: 1px solid rgba(255, 255, 255, 0.18);
    background: transparent;
    color: #ffffff;
  }

  .side-panel {
    max-width: 26rem;
    color: rgba(255, 255, 255, 0.72);
  }

  @media (min-width: 720px) {
    .hub {
      padding: 3.5rem 1.5rem;
    }

    .hub-header {
      grid-template-columns: 1fr auto;
      align-items: start;
      margin-bottom: 3rem;
    }

    .hub-content {
      grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.5fr);
      align-items: start;
      gap: clamp(2rem, 6vw, 4rem);
    }

    .side-panel {
      padding-top: 2.25rem;
    }
  }
</style>
