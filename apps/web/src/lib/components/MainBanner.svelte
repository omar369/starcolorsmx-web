<script lang="ts">
  import Button from "$lib/components/ui/button/button.svelte";
</script>

<div class="main-banner-wrapper">
  <div class="banner-card">
    <div class="pattern-layer" aria-hidden="true"></div>

    <div class="banner-content">
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

      <div class="images-container">
        <div class="image image-one">
          <span>Balón</span>
        </div>

        <div class="image image-two">
          <span>Pantalla</span>
        </div>

        <div class="image image-three">
          <span>Premio</span>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  /* ANIMACIONES SUTILES */
  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes fade-in-pattern {
    from { opacity: 0; }
    to { opacity: 0.38; }
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
  }

  .banner-card {
    position: relative;
    min-height: 440px;
    overflow: hidden;
    border-radius: 2.5rem;
    background: #006b3f;
    box-shadow: 0 24px 50px rgba(0, 107, 63, 0.25);
    
    opacity: 0;
    animation: fade-in 0.8s ease-out forwards;
  }

  .pattern-layer {
    position: absolute;
    inset: 0;
    background:
      linear-gradient(90deg, transparent 0 18px, rgba(77, 185, 79, 0.8) 18px 28px, transparent 28px 46px),
      repeating-linear-gradient(135deg, transparent 0 18px, rgba(77, 185, 79, 0.55) 18px 26px, transparent 26px 52px),
      #006b3f;
      
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
    padding: 3rem 2rem;
    gap: 4rem;
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
    font-size: clamp(3.8rem, 14vw, 7.5rem);
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
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
    transition: transform 0.2s ease !important;
  }

  :global(.raffle-btn:hover) {
    transform: scale(1.05) !important;
    background-color: #f8fafc !important;
  }

  .images-container {
    position: relative;
    width: 100%;
    max-width: 400px;
    height: 220px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .image {
    position: absolute;
    display: grid;
    place-items: center;
    border: 5px solid rgba(255, 255, 255, 0.85);
    background: white;
    color: #006b3f;
    font-size: 0.9rem;
    font-weight: 900;
    box-shadow: 0 18px 30px rgba(0, 0, 0, 0.22);
    
    opacity: 0;
  }

  .image-one,
  .image-three {
    width: 90px;
    aspect-ratio: 1;
    border-radius: 999px;
    z-index: 2;
  }

  .image-one {
    left: 0;
    bottom: 10px;
    animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.8s forwards;
  }

  .image-two {
    width: 150px;
    height: 100px;
    rotate: 7deg;
    border-radius: 1rem;
    z-index: 1;
    animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 1.0s forwards;
  }

  .image-three {
    right: 0;
    top: 10px;
    animation: pop-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 1.2s forwards;
  }

  @media (min-width: 860px) {
    .banner-content {
      flex-direction: row;
      justify-content: space-around;
      padding: 4rem 5rem;
    }

    .hero-copy {
      text-align: left;
      align-items: flex-start;
    }

    .images-container {
      width: 480px;
      height: 300px;
    }

    .image-one,
    .image-three {
      width: 110px;
    }

    .image-two {
      width: 200px;
      height: 125px;
    }
  }
</style>
