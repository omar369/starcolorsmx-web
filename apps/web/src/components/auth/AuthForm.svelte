<script lang="ts">
  import { loginUser, registerUser } from "../../lib/auth";

  let mode: "register" | "login" = "register";

  let fullName = "";
  let email = "";
  let password = "";
  let phone = "";

  let loading = false;
  let error = "";

  function setMode(nextMode: "register" | "login") {
    mode = nextMode;
    error = "";
  }

  async function handleSubmit() {
    loading = true;
    error = "";

    function getRedirectPath() {
      const params = new URLSearchParams(window.location.search);
      const redirect = params.get("redirect");

      if (!redirect || !redirect.startsWith("/") || redirect.startsWith("//")) {
        return "/hub";
      }

      return redirect;
    }

    try {
      if (mode === "register") {
        await registerUser({
          full_name: fullName.trim(),
          email: email.trim(),
          password,
          phone: phone.trim() || undefined,
        });
      } else {
        await loginUser({
          email: email.trim(),
          password,
        });
      }

      window.location.href = getRedirectPath();
    } catch (err) {
      error = err instanceof Error ? err.message : "Ocurrió un error.";
    } finally {
      loading = false;
    }
  }
</script>

<section
  class="auth-card"
  aria-label={mode === "register" ? "Crear cuenta" : "Iniciar sesión"}
>
  <header class="auth-card-header">
    <p class="auth-card-kicker">Cuenta</p>
    <h2>{mode === "register" ? "Crear cuenta" : "Iniciar sesión"}</h2>
  </header>

  <div class="auth-card-body">
    <div class="auth-tabs" role="tablist" aria-label="Modo de acceso">
      <button
        class:active={mode === "register"}
        type="button"
        aria-pressed={mode === "register"}
        on:click={() => setMode("register")}
      >
        Registrarme
      </button>

      <button
        class:active={mode === "login"}
        type="button"
        aria-pressed={mode === "login"}
        on:click={() => setMode("login")}
      >
        Entrar
      </button>
    </div>

    <form on:submit|preventDefault={handleSubmit}>
      {#if mode === "register"}
        <label>
          <span>Nombre completo</span>
          <input
            bind:value={fullName}
            autocomplete="name"
            maxlength="60"
            minlength="8"
            required
          />
        </label>
      {/if}

      <label>
        <span>Correo electrónico</span>
        <input bind:value={email} autocomplete="email" type="email" required />
      </label>

      <label>
        <span>Contraseña</span>
        <input
          bind:value={password}
          autocomplete={mode === "register"
            ? "new-password"
            : "current-password"}
          maxlength="128"
          minlength="8"
          type="password"
          required
        />
      </label>

      {#if mode === "register"}
        <label>
          <span>Teléfono opcional</span>
          <input
            bind:value={phone}
            autocomplete="tel"
            maxlength="10"
            minlength="7"
            type="tel"
          />
        </label>
      {/if}

      {#if error}
        <p class="error" role="alert">{error}</p>
      {/if}

      <button class="submit" type="submit" disabled={loading}>
        {loading
          ? "Procesando..."
          : mode === "register"
            ? "Crear cuenta"
            : "Entrar al hub"}
      </button>
    </form>
  </div>
</section>

<style>
  .auth-card {
    width: min(100%, 430px);
    margin: 0 auto;
    border: 1px solid #d8d8d4;
    border-radius: 8px;
    background: #ffffff;
    box-shadow: 0 18px 60px rgba(17, 17, 17, 0.12);
  }

  .auth-card-header {
    display: grid;
    gap: 0.35rem;
    border-bottom: 1px solid #e6e6e1;
    padding: 1rem 1rem 0.85rem;
  }

  .auth-card-kicker {
    margin: 0;
    color: #71716b;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    line-height: 1.1;
    text-transform: uppercase;
  }

  h2 {
    margin: 0;
    color: #111111;
    font-size: 1.35rem;
    font-weight: 820;
    line-height: 1.1;
  }

  .auth-card-body {
    display: grid;
    gap: 1.05rem;
    padding: 1rem;
  }

  .auth-tabs {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    border: 1px solid #d8d8d4;
    border-radius: 6px;
    overflow: hidden;
  }

  .auth-tabs button,
  .submit {
    min-height: 42px;
    border: 0;
    border-radius: 6px;
    padding: 0.68rem 0.85rem;
    font-size: 0.9rem;
    font-weight: 780;
    cursor: pointer;
  }

  .auth-tabs button {
    border-radius: 0;
    background: #ffffff;
    color: #61615b;
  }

  .auth-tabs button + button {
    border-left: 1px solid #d8d8d4;
  }

  .auth-tabs button.active {
    background: #111111;
    color: #ffffff;
  }

  form {
    display: grid;
    gap: 0.85rem;
  }

  label {
    display: grid;
    gap: 0.38rem;
    color: #111111;
    font-size: 0.82rem;
    font-weight: 760;
  }

  input {
    width: 100%;
    min-height: 43px;
    border: 1px solid #d8d8d4;
    border-radius: 6px;
    background: #ffffff;
    color: #111111;
    padding: 0.65rem 0.8rem;
    outline: none;
  }

  input:focus {
    border-color: #111111;
    box-shadow: 0 0 0 3px rgba(17, 17, 17, 0.08);
  }

  .submit {
    width: 100%;
    margin-top: 0.2rem;
    background: #111111;
    color: #ffffff;
  }

  .submit:disabled {
    cursor: not-allowed;
    opacity: 0.52;
  }

  .error {
    margin: 0;
    border: 1px solid #fecdd3;
    border-radius: 6px;
    background: #fff1f2;
    color: #9f1239;
    padding: 0.65rem 0.8rem;
    font-size: 0.8rem;
    font-weight: 750;
    line-height: 1.35;
  }

  @media (min-width: 760px) {
    .auth-card-header {
      padding: 1.15rem 1.2rem 0.95rem;
    }

    .auth-card-body {
      padding: 1.2rem;
    }
  }
</style>
