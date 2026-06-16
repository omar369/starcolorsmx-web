<script lang="ts">
  import Button from "$lib/components/ui/button/button.svelte";
</script>

<div class="main-banner-wrapper">
  <div class="banner-card">
    <!-- Capa de fondo con el patrón verde cool -->
    <div class="pattern-layer" aria-hidden="true"></div>

    <div class="banner-content">
      <!-- Contenedor de imágenes de premios flotantes -->
      <div class="images-container">
        <!-- Balón Principal -->
        <div class="image image-one">
          <img
            src="/images/balon.webp"
            alt="Balón de fútbol StarColors"
            class="prize-img"
          />
        </div>

        <!-- Balón Secundario (Duplicado) -->
        <div class="image image-three">
          <img
            src="/images/balon.webp"
            alt="Balón secundario"
            class="prize-img"
          />
        </div>

        <!-- Balón Terciario (Nuevo) -->
        <div class="image image-four">
          <img
            src="/images/balon.webp"
            alt="Balón terciario"
            class="prize-img"
          />
        </div>

        <!-- Pantalla de Sorteo centrado (Grande y puede desbordar) -->
        <div class="image image-two">
          <img
            src="/images/pantalla.webp"
            alt="Pantalla de 49 pulgadas"
            class="prize-img"
          />
        </div>
      </div>

      <!-- Divisor punteado estilo ticket troquelado -->
      <div class="ticket-divider" aria-hidden="true"></div>

      <div class="hero-copy">
        <p class="eyebrow">Sorteo de temporada</p>
        <h1>
          Pinta,<br />
          Compra<br />
          y Gana!
        </h1>

        <div class="cta-container">
          <Button href="/hub" size="lg" class="raffle-btn">
            ¡Entrar al sorteo!
          </Button>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  /* ANIMACIONES */
  @keyframes fade-in {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes fade-in-pattern {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes slide-up {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes pop-in {
    0% {
      opacity: 0;
      transform: scale(0.5);
    }
    70% {
      opacity: 1;
      transform: scale(1.08);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }

  .main-banner-wrapper {
    width: min(100% - 2rem, 1200px);
    margin: 3rem auto 4rem;
    padding-top: 5vh;
  }

  .banner-card {
    position: relative;
    min-height: 440px;
    border-radius: 2.5rem;
    background: #006b3f;
    /* box-shadow: 0 24px 50px rgba(0, 107, 63, 0.25); */
    opacity: 0;
    animation: fade-in 0.8s ease-out forwards;
  }

  /* Notchas / recortes de ticket circulares en los bordes */
  .banner-card::before,
  .banner-card::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background-color: #f3eadb; /* Mezcla con el nuevo fondo de index.astro */
    z-index: 10;
    transform: translateY(-50%);
  }

  .banner-card::before {
    left: -22px;
  }

  .banner-card::after {
    right: -22px;
  }

  .pattern-layer {
    position: absolute;
    inset: 0;
    border-radius: 2.5rem;
    background: url("/images/bannerBG.webp") no-repeat center center / cover;

    opacity: 0;
    animation: fade-in-pattern 1.2s ease-in-out 0.2s forwards;
  }

  .banner-content {
    position: relative;
    z-index: 1;
    min-height: 440px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3.3rem 2.75rem;
    gap: 3rem;
  }

  .hero-copy {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .eyebrow {
    margin: 0;
    color: #b4f0b0;
    font-size: 0.9rem;
    font-weight: 900;
    letter-spacing: 0.15em;
    text-transform: uppercase;

    opacity: 0;
    animation: slide-up 0.6s ease-out 0.3s forwards;
  }

  h1 {
    margin: 0;
    color: white;
    font-family: Georgia, "Times New Roman", serif;
    font-size: clamp(3.5rem, 12vw, 7rem);
    line-height: 0.92;
    text-shadow: 0 4px 0 rgba(0, 0, 0, 0.18);

    opacity: 0;
    animation: slide-up 0.8s ease-out 0.5s forwards;
  }

  .cta-container {
    margin-top: 1.5rem;

    opacity: 0;
    animation: slide-up 0.8s ease-out 0.7s forwards;
  }

  :global(.raffle-btn) {
    background-color: white !important;
    color: #006b3f !important;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.35rem !important;
    font-weight: 900 !important;
    padding: 1.75rem 3.5rem !important;
    border-radius: 999px !important;
    height: auto !important;
    text-transform: uppercase;
    /* box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important; */
    transition: transform 0.2s ease !important;
  }

  :global(.raffle-btn:hover) {
    transform: scale(1.05) !important;
    background-color: #f8fafc !important;
  }

  .ticket-divider {
    display: none;
  }

  .images-container {
    position: relative;
    width: 100%;
    max-width: 400px;
    height: 280px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: visible;
  }

  /* Contenedores de imagen transparentes sin bordes ni fondos blancos */
  .image {
    position: absolute;
    display: grid;
    place-items: center;
    background: transparent;
    border: none;
    box-shadow: none;
    /* Sombras 3D aplicadas al recorte de la silueta del PNG transparente */
    /* filter: drop-shadow(0 15px 25px rgba(0, 0, 0, 0.35)); */
    overflow: visible;
    opacity: 0;
  }

  .prize-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  /* Balón Principal - Grande */
  .image-one {
    width: 160px;
    height: 160px;
    z-index: 4;
    left: 120px;
    bottom: -15px;
    animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.8s forwards;
  }

  /* Balón Secundario (Duplicado) - Mediano y flotando detrás */
  .image-three {
    width: 100px;
    height: 100px;
    z-index: 3;
    left: 130px;
    bottom: 215px;
    rotate: -18deg;
    animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 1.2s forwards;
  }

  /* Balón Terciario (Nuevo) - Pequeño y flotando abajo/derecha */
  .image-four {
    width: 80px;
    height: 80px;
    z-index: 5;
    left: -35px;
    bottom: -20px;
    rotate: 25deg;
    animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 1.4s forwards;
  }

  /* Pantalla de Sorteo (Grande y puede sobresalir) */
  .image-two {
    width: 320px;
    height: 220px;
    rotate: 6deg;
    z-index: 1;
    right: -35px;
    top: -20px;
    animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 1s forwards;
  }

  @media (min-width: 860px) {
    .banner-content {
      flex-direction: row;
      justify-content: space-between;
      padding: 4.4rem 5.5rem;
      gap: 2rem;
    }

    .hero-copy {
      text-align: left;
      align-items: flex-start;
      margin-right: 10%;
    }

    .ticket-divider {
      display: block;
      width: 0;
      border-left: 3px dashed rgba(255, 255, 255, 0.35);
      height: 280px;
      margin: 0 1.5rem;
      align-self: center;
    }

    .images-container {
      width: 480px;
      height: 340px;
      margin-left: 10%;
    }

    /* Tamaños 2x Grandes en Escritorio y distribuidos 5% más separados */
    .image-one {
      width: 220px;
      height: 220px;
      left: 200px;
      bottom: -65px;
    }

    .image-three {
      width: 130px;
      height: 130px;
      left: 171px;
      bottom: 285px;
    }

    .image-four {
      width: 110px;
      height: 110px;
      left: 45px;
      bottom: 20px;
    }

    .image-two {
      width: 450px;
      height: 310px;
      right: -85px;
      top: -50px;
    }
  }
</style>
