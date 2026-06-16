<script lang="ts">
  import * as NavigationMenu from "$lib/components/ui/navigation-menu/index.js";
  import Button from "$lib/components/ui/button/button.svelte";
  import { Menu, X, User } from "@lucide/svelte";
  import { onMount } from "svelte";
  import { getStoredUser } from "$lib/auth";

  const links = [
    { href: "/", label: "Inicio" },
    { href: "/servicios", label: "Servicios" },
    { href: "/productos", label: "Productos" },
    { href: "/sobre-nosotros", label: "Sobre nosotros" },
    { href: "/contacto", label: "Contacto" },
  ];

  let menuOpen = $state(false);

  // Read stored user from session on mount
  let user = $state<{
    name: string;
    email?: string;
    avatarUrl?: string;
  } | null>(null);

  onMount(() => {
    const storedUser = getStoredUser();
    if (storedUser) {
      user = {
        name: storedUser.full_name,
        email: storedUser.email,
      };
    }
  });

  function getInitials(name: string) {
    if (!name) return "";
    const parts = name.trim().split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return parts[0].slice(0, 2).toUpperCase();
  }
</script>

<header
  class="sticky top-0 z-50 w-full border-b border-[#d96f20] bg-[#f3eadb] shadow-sm overflow-hidden"
>
  <!-- Orange wave SVG - Now moved outside the max-w container so it extends to the very edges -->
  <svg
    class="pointer-events-none absolute inset-0 hidden h-full w-full md:block"
    viewBox="0 0 1200 76"
    preserveAspectRatio="none"
    aria-hidden="true"
  >
    <path
      d="M0 64 H310 C430 64 470 30 610 24 C770 16 960 14 1200 14 V76 H0 Z"
      fill="#e67a25"
    />
    <path
      d="M0 58 H315 C430 58 465 25 610 19 C780 11 955 9 1200 9"
      fill="none"
      stroke="#ffffff"
      stroke-width="3"
    />
    <path
      d="M0 68 H320 C430 68 470 35 615 29 C790 21 965 19 1200 19"
      fill="none"
      stroke="#ffffff"
      stroke-width="2"
      opacity="0.8"
    />
  </svg>

  <div
    class="relative mx-auto flex h-[76px] max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8"
  >
    <!-- Logo -->
    <a
      href="/"
      class="relative z-10 flex items-center"
      aria-label="Ir al inicio"
    >
      <img
        src="/sc_logo.svg"
        alt="StarColors"
        class="h-11 w-auto sm:h-12 md:h-14"
      />
    </a>

    <!-- Desktop nav — shifted 30% right (extra 10%) so it sits well above the orange area -->
    <NavigationMenu.Root
      class="relative z-10 hidden md:flex"
      style="margin-left: 30%;"
    >
      <NavigationMenu.List class="flex items-center gap-0.5 mt-4">
        {#each links as link}
          <NavigationMenu.Item>
            <!-- Added !text-white to ensure shadcn defaults don't override the color -->
            <NavigationMenu.Link
              href={link.href}
              class="rounded-full px-2 py-2 text-[0.95rem] font-normal tracking-wide text-white! no-underline transition-colors hover:bg-white/20 hover:text-white!"
            >
              {link.label}
            </NavigationMenu.Link>
          </NavigationMenu.Item>
        {/each}
      </NavigationMenu.List>
    </NavigationMenu.Root>

    <!-- Desktop CTA: Portal clientes button + avatar slot -->
    <div class="relative z-10 hidden items-center gap-2 md:flex">
      {#if user}
        <!-- Logged-in state: avatar button with initials -->
        <button
          class="flex h-10 w-10 mt-4 items-center justify-center overflow-hidden rounded-full border-2 border-white bg-[#f3eadb] shadow-md transition-all duration-300 hover:scale-105 hover:border-[#e67a25] hover:shadow-lg focus:outline-none"
          aria-label="Mi perfil"
          onclick={() => (window.location.href = "/hub")}
        >
          {#if user.avatarUrl}
            <img
              src={user.avatarUrl}
              alt={user.name}
              class="h-full w-full object-cover"
            />
          {:else}
            <!-- Initials fallback -->
            <span
              class="text-xs font-black text-[#e67a25] uppercase tracking-wider leading-none"
            >
              {getInitials(user.name)}
            </span>
          {/if}
        </button>
      {:else}
        <!-- Logged-out state: compact "Portal clientes" button -->
        <Button
          href="/hub"
          variant="outline"
          size="sm"
          class="rounded-full mt-4 border-white/70 bg-white/10 px-4 text-[0.8rem] font-black uppercase tracking-wider text-white! backdrop-blur-sm hover:bg-white hover:!text-[#e67a25] transition-all"
        >
          <User class="mr-1.5 h-3.5 w-3.5" />
          Portal clientes
        </Button>
      {/if}
    </div>

    <!-- Mobile hamburger -->
    <button
      class="relative z-10 inline-flex h-11 w-11 items-center justify-center rounded-full bg-white text-[#111111] shadow-sm md:hidden"
      aria-label={menuOpen ? "Cerrar menú" : "Abrir menú"}
      onclick={() => (menuOpen = !menuOpen)}
    >
      {#if menuOpen}
        <X class="h-6 w-6" />
      {:else}
        <Menu class="h-6 w-6" />
      {/if}
    </button>
  </div>

  <!-- Mobile menu -->
  {#if menuOpen}
    <nav
      class="relative z-10 grid gap-1 border-t border-[#e1cdb8] bg-[#f3eadb] px-4 py-4 md:hidden"
    >
      {#each links as link}
        <a
          href={link.href}
          class="rounded-xl px-3 py-3 text-base font-bold text-[#172033] no-underline hover:bg-white hover:no-underline"
          onclick={() => (menuOpen = false)}
        >
          {link.label}
        </a>
      {/each}

      {#if user}
        <div class="mt-2 flex flex-col gap-2 border-t border-[#e1cdb8]/60 pt-3">
          <div class="flex items-center gap-3 px-3 py-1.5">
            <div
              class="flex h-10 w-10 items-center justify-center rounded-full bg-[#e67a25] text-white font-black text-xs uppercase shadow-sm"
            >
              {getInitials(user.name)}
            </div>
            <div class="flex-1 min-w-0">
              <p
                class="text-sm font-black text-[#172033] truncate leading-none mb-1"
              >
                {user.name}
              </p>
              <p
                class="text-[0.75rem] text-gray-500 font-bold truncate leading-none"
              >
                {user.email ?? ""}
              </p>
            </div>
          </div>
          <a
            href="/hub"
            class="flex items-center justify-center gap-2 rounded-xl bg-[#e67a25] px-3 py-3 text-center text-base font-black uppercase text-white no-underline hover:no-underline hover:bg-[#d96f20] transition-colors"
            onclick={() => (menuOpen = false)}
          >
            Portal cliente
          </a>
        </div>
      {:else}
        <a
          href="/hub"
          class="mt-2 flex items-center justify-center gap-2 rounded-xl bg-[#e67a25] px-3 py-3 text-center text-base font-black uppercase text-white no-underline hover:no-underline hover:bg-[#d96f20] transition-colors"
          onclick={() => (menuOpen = false)}
        >
          <User class="h-4 w-4" />
          Portal clientes
        </a>
      {/if}
    </nav>
  {/if}
</header>
