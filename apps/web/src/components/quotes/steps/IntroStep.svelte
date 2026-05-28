<section class="step">
  <h2>Antes de comenzar</h2>

  <p>
    Esta precotizacion usa precios base por metro cuadrado y ajustes por
    condiciones del trabajo: superficie, textura, preparacion, horario, altura,
    proteccion del area y estado.
  </p>

  <p>
    El resultado es una guia inicial. Si el proyecto requiere visita tecnica,
    fotos o ajustes manuales, el precio final puede cambiar.
  </p>

  <div class="notice">
    Los campos del cotizador vienen desde la API. Por ahora son datos mock; mas
    adelante se moveran a la base de datos.
  </div>
</section>

<style>
  .step {
    display: grid;
    gap: 1rem;
  }

  h2 {
    margin: 0;
    color: #172033;
    font-size: clamp(1.8rem, 8vw, 3rem);
    line-height: 1;
  }

  p {
    margin: 0;
    color: #475569;
    line-height: 1.7;
  }

  .notice {
    border-radius: 14px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    color: #334155;
    line-height: 1.6;
    padding: 1rem;
  }
</style>
