import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import anyio

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_quote_email_sync(
    email_to: str,
    customer_name: str,
    pdf_bytes: bytes,
    filename: str = "precotizacion-starcolors.pdf"
) -> bool:
    if not settings.smtp_host:
        logger.warning("SMTP_HOST no configurado. No se enviará el correo de la cotización.")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = settings.smtp_from
        msg["To"] = email_to
        msg["Subject"] = f"Precotización StarColors - {customer_name}"

        # HTML Body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #172033; line-height: 1.6;">
            <h2 style="color: #e67a25;">¡Hola, {customer_name}!</h2>
            <p>Agradecemos tu interés en los servicios de Pinturas StarColors MX.</p>
            <p>Adjunto a este correo encontrarás el archivo PDF con la precotización estimada que solicitaste en nuestra plataforma web.</p>
            <p>Recuerda que este presupuesto tiene una vigencia estimada de 10 días naturales y los precios presentados no incluyen I.V.A.</p>
            <br/>
            <hr style="border: 0; border-top: 1px solid #eee;"/>
            <p style="font-size: 0.8em; color: #666;">
                Este es un correo automático enviado desde nuestro portal. Por favor, no respondas a este mensaje.<br/>
                Si deseas una cotización formal o agendar una visita técnica en sitio, puedes contactarnos directamente vía WhatsApp.
            </p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, "html", "utf-8"))

        # Attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(pdf_bytes)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        msg.attach(part)

        # SMTP Connection
        server = smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10)
        server.starttls()
        if settings.smtp_username and settings.smtp_password:
            server.login(settings.smtp_username, settings.smtp_password)
        
        server.sendmail(settings.smtp_from, email_to, msg.as_string())
        server.quit()
        logger.info(f"Correo de cotización enviado exitosamente a {email_to}")
        return True
    except Exception as e:
        logger.error(f"Error al enviar correo SMTP: {str(e)}")
        return False


async def send_quote_email(
    email_to: str,
    customer_name: str,
    pdf_bytes: bytes,
    filename: str = "precotizacion-starcolors.pdf"
) -> bool:
    return await anyio.to_thread.run_sync(
        send_quote_email_sync,
        email_to,
        customer_name,
        pdf_bytes,
        filename
    )
