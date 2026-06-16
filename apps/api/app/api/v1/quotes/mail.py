import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import anyio

from app.core.config import settings

logger = logging.getLogger(__name__)


def _build_email_html(customer_name: str, filename: str) -> str:
    """
    Construye el cuerpo HTML del correo de cotización.
    Diseño simple pero profesional, compatible con la mayoría de clientes de correo.
    Usa tablas para máxima compatibilidad (Gmail, Outlook, Apple Mail).
    """
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Precotización StarColors</title>
</head>
<body style="margin:0;padding:0;background-color:#f1f5f9;font-family:Arial,Helvetica,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f5f9;padding:32px 16px;">
    <tr>
      <td align="center">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0"
          style="max-width:560px;background-color:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

          <!-- Header con color de marca -->
          <tr>
            <td style="background:linear-gradient(135deg,#172033 0%,#243047 100%);padding:28px 32px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td>
                    <p style="margin:0;color:#f5b700;font-size:11px;font-weight:900;letter-spacing:2px;text-transform:uppercase;">
                      StarColors MX
                    </p>
                    <h1 style="margin:6px 0 0;color:#ffffff;font-size:22px;font-weight:900;line-height:1.2;">
                      Tu precotización está lista
                    </h1>
                  </td>
                  <td align="right" style="vertical-align:top;">
                    <div style="width:44px;height:44px;border-radius:12px;background-color:rgba(245,183,0,0.15);display:flex;align-items:center;justify-content:center;">
                      <span style="font-size:22px;">📋</span>
                    </div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:28px 32px;">

              <p style="margin:0 0 8px;color:#172033;font-size:16px;font-weight:700;">
                ¡Hola, {customer_name}!
              </p>

              <p style="margin:0 0 20px;color:#475569;font-size:14px;line-height:1.65;">
                Gracias por usar nuestra herramienta de pre-cotización.
                Adjunto a este correo encontrarás el archivo
                <strong style="color:#172033;">{filename}</strong>
                con el resumen de tu presupuesto estimado.
              </p>

              <!-- Info box -->
              <table width="100%" cellpadding="0" cellspacing="0"
                style="background-color:#fffbeb;border:1.5px solid #fde68a;border-radius:12px;margin-bottom:24px;">
                <tr>
                  <td style="padding:14px 16px;">
                    <p style="margin:0 0 4px;color:#92400e;font-size:11px;font-weight:900;letter-spacing:1px;text-transform:uppercase;">
                      Importante
                    </p>
                    <p style="margin:0;color:#78350f;font-size:13px;line-height:1.55;">
                      Esta pre-cotización es una <strong>estimación inicial</strong> basada en los datos que proporcionaste.
                      El precio final puede variar después de una visita técnica o revisión presencial.
                      Los precios <strong>no incluyen I.V.A.</strong>
                    </p>
                  </td>
                </tr>
              </table>

              <p style="margin:0 0 20px;color:#475569;font-size:14px;line-height:1.65;">
                Si deseas agendar una visita técnica, obtener una cotización formal o tienes alguna pregunta,
                no dudes en contactarnos directamente.
              </p>

              <!-- CTA Button -->
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                <tr>
                  <td align="center">
                    <a href="https://starcolorsmx.com"
                      style="display:inline-block;background-color:#f5b700;color:#172033;font-size:14px;font-weight:900;text-decoration:none;padding:12px 28px;border-radius:999px;">
                      Visita nuestro sitio web →
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="border-top:1px solid #e2e8f0;padding:20px 32px;background-color:#f8fafc;">
              <p style="margin:0;color:#94a3b8;font-size:11px;line-height:1.55;text-align:center;">
                Este correo fue generado automáticamente desde el portal de StarColors MX.<br/>
                Por favor no respondas a este mensaje directamente.<br/>
                <strong style="color:#64748b;">StarColors MX</strong> · starcolorsmx.com
              </p>
            </td>
          </tr>

        </table>
        <!-- /Card -->

      </td>
    </tr>
  </table>
  <!-- /Wrapper -->

</body>
</html>"""


def send_quote_email_sync(
    email_to: str,
    customer_name: str,
    pdf_bytes: bytes,
    filename: str = "precotizacion-starcolors.pdf"
) -> bool:
    """
    Envía el PDF de cotización por correo usando SMTP.
    Funciona con cualquier proveedor SMTP estándar (Resend, Gmail, Brevo, etc.)
    Lanza una excepción con mensaje descriptivo si algo falla.
    """
    if not settings.smtp_host:
        raise RuntimeError(
            "SMTP_HOST no está configurado en las variables de entorno del servidor."
        )

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f"StarColors MX <{settings.smtp_from}>"
        msg["To"] = email_to
        msg["Subject"] = "Tu precotización de pintura — StarColors MX"
        msg["Reply-To"] = settings.smtp_from

        # Texto plano (fallback para clientes que no soportan HTML)
        plain_text = (
            f"Hola {customer_name},\n\n"
            "Adjunto encontrarás el PDF con tu precotización de pintura.\n\n"
            "Recuerda que este es un estimado inicial. El precio final puede variar\n"
            "después de una visita técnica.\n\n"
            "Gracias por contactar a StarColors MX.\n"
            "starcolorsmx.com"
        )
        msg.attach(MIMEText(plain_text, "plain", "utf-8"))
        msg.attach(MIMEText(_build_email_html(customer_name, filename), "html", "utf-8"))

        # Adjunto PDF
        full_msg = MIMEMultipart("mixed")
        full_msg["From"] = msg["From"]
        full_msg["To"] = msg["To"]
        full_msg["Subject"] = msg["Subject"]
        full_msg["Reply-To"] = msg["Reply-To"]
        full_msg.attach(msg)

        part = MIMEBase("application", "pdf")
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{filename}"',
        )
        full_msg.attach(part)

        # Conexión SMTP con TLS
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            if settings.smtp_username and settings.smtp_password:
                server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.smtp_from, email_to, full_msg.as_string())

        logger.info(f"Correo de cotización enviado exitosamente a {email_to}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        msg = f"Error de autenticación SMTP — verifica SMTP_USERNAME y SMTP_PASSWORD en Railway. Detalle: {e}"
        logger.error(msg)
        raise RuntimeError(msg) from e
    except smtplib.SMTPConnectError as e:
        msg = f"No se pudo conectar al servidor SMTP {settings.smtp_host}:{settings.smtp_port}. Detalle: {e}"
        logger.error(msg)
        raise RuntimeError(msg) from e
    except smtplib.SMTPRecipientsRefused as e:
        msg = f"El destinatario fue rechazado por el servidor: {email_to}. Detalle: {e}"
        logger.error(msg)
        raise RuntimeError(msg) from e
    except smtplib.SMTPSenderRefused as e:
        msg = f"El remitente fue rechazado: {settings.smtp_from}. Verifica que el dominio esté verificado en Resend. Detalle: {e}"
        logger.error(msg)
        raise RuntimeError(msg) from e
    except Exception as e:
        msg = f"Error inesperado al enviar correo SMTP: {type(e).__name__}: {e}"
        logger.error(msg)
        raise RuntimeError(msg) from e


async def send_quote_email(
    email_to: str,
    customer_name: str,
    pdf_bytes: bytes,
    filename: str = "precotizacion-starcolors.pdf"
) -> bool:
    """
    Wrapper async — ejecuta el envío SMTP en un thread separado
    para no bloquear el event loop de FastAPI.
    Deja que las excepciones de send_quote_email_sync se propaguen.
    """
    return await anyio.to_thread.run_sync(
        lambda: send_quote_email_sync(email_to, customer_name, pdf_bytes, filename)
    )
