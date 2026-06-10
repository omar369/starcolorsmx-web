<script lang="ts">
  import { loginUser, registerUser } from "../../lib/auth";
  import * as Tabs from "$lib/components/ui/tabs/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Button } from "$lib/components/ui/button/index.js";

  // Use string mode to easily bind to Tabs
  let mode = $state("register");

  let fullName = $state("");
  let email = $state("");
  let password = $state("");
  let phone = $state("");

  let loading = $state(false);
  let error = $state("");

  async function handleSubmit(e: Event) {
    e.preventDefault();
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

<div class="w-full max-w-[440px] animate-in fade-in zoom-in-95 duration-500">
  <Card.Root class="border-0 shadow-2xl rounded-2xl overflow-hidden bg-white/95 backdrop-blur-sm">
    <Card.Header class="pb-6 border-b border-gray-100 bg-white">
      <Card.Description class="font-black text-[#e67a25] tracking-widest uppercase text-[0.7rem] mb-1">
        Cuenta
      </Card.Description>
      <Card.Title class="text-[1.6rem] font-bold text-[#111111]">
        {mode === "register" ? "Crear cuenta" : "Iniciar sesión"}
      </Card.Title>
    </Card.Header>
    <Card.Content class="pt-6 px-6 sm:px-8">
      <Tabs.Root bind:value={mode} class="w-full">
        <Tabs.List class="grid w-full grid-cols-2 mb-8 bg-gray-100/80 p-1 rounded-xl">
          <Tabs.Trigger value="register" class="rounded-lg font-bold data-[state=active]:bg-white data-[state=active]:text-[#111111] data-[state=active]:shadow-sm transition-all">
            Registrarme
          </Tabs.Trigger>
          <Tabs.Trigger value="login" class="rounded-lg font-bold data-[state=active]:bg-white data-[state=active]:text-[#111111] data-[state=active]:shadow-sm transition-all">
            Entrar
          </Tabs.Trigger>
        </Tabs.List>
        
        <form onsubmit={handleSubmit} class="grid gap-5">
          {#if mode === "register"}
            <div class="grid gap-2">
              <Label for="fullName" class="text-sm font-bold text-[#111111]">Nombre completo</Label>
              <Input
                id="fullName"
                bind:value={fullName}
                autocomplete="name"
                maxlength={60}
                minlength={8}
                required
                class="h-12 px-4 rounded-xl border-gray-200 bg-gray-50/50 focus-visible:ring-[#e67a25] focus-visible:border-[#e67a25] transition-all"
              />
            </div>
          {/if}

          <div class="grid gap-2">
            <Label for="email" class="text-sm font-bold text-[#111111]">Correo electrónico</Label>
            <Input 
              id="email" 
              bind:value={email} 
              autocomplete="email" 
              type="email" 
              required 
              class="h-12 px-4 rounded-xl border-gray-200 bg-gray-50/50 focus-visible:ring-[#e67a25] focus-visible:border-[#e67a25] transition-all"
            />
          </div>

          <div class="grid gap-2">
            <Label for="password" class="text-sm font-bold text-[#111111]">Contraseña</Label>
            <Input
              id="password"
              bind:value={password}
              autocomplete={mode === "register" ? "new-password" : "current-password"}
              maxlength={128}
              minlength={8}
              type="password"
              required
              class="h-12 px-4 rounded-xl border-gray-200 bg-gray-50/50 focus-visible:ring-[#e67a25] focus-visible:border-[#e67a25] transition-all"
            />
          </div>

          {#if mode === "register"}
            <div class="grid gap-2">
              <Label for="phone" class="text-sm font-bold text-[#111111]">Teléfono <span class="text-gray-400 font-normal ml-1">(opcional)</span></Label>
              <Input
                id="phone"
                bind:value={phone}
                autocomplete="tel"
                maxlength={10}
                minlength={7}
                type="tel"
                class="h-12 px-4 rounded-xl border-gray-200 bg-gray-50/50 focus-visible:ring-[#e67a25] focus-visible:border-[#e67a25] transition-all"
              />
            </div>
          {/if}

          {#if error}
            <div class="text-[0.85rem] font-bold text-red-700 bg-red-50 p-3.5 rounded-xl border border-red-200 mt-1" role="alert">
              {error}
            </div>
          {/if}

          <Button type="submit" disabled={loading} class="h-14 mt-4 w-full rounded-xl bg-[#111111] hover:bg-[#e67a25] text-white text-[1rem] font-black uppercase tracking-wider transition-all shadow-md hover:shadow-xl hover:-translate-y-0.5">
            {#if loading}
              Procesando...
            {:else if mode === "register"}
              Crear cuenta
            {:else}
              Entrar al hub
            {/if}
          </Button>
        </form>
      </Tabs.Root>
    </Card.Content>
  </Card.Root>
</div>
