<script lang="ts">
  export let currentStep: number;
  export let totalSteps = 6;
</script>

<div class="steps" aria-label="Progreso del registro">
  <p>Paso {currentStep} de {totalSteps}</p>

  <div class="dots">
    {#each Array(totalSteps) as _, index}
      <span class:active={index + 1 <= currentStep}></span>
    {/each}
  </div>
</div>

<style>
  .steps {
    display: grid;
    gap: 0.55rem;
    margin-bottom: 1.5rem;
  }

  .steps p {
    margin: 0;
    color: rgba(255, 255, 255, 0.62);
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .dots {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.4rem;
  }

  .dots span {
    height: 6px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.16);
  }

  .dots span.active {
    background: #ffffff;
  }
</style>
