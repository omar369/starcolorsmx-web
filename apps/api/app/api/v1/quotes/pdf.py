from datetime import date
from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.api.v1.quotes.schemas import QuoteCreate, QuoteResult

BASE_DIR = Path(__file__).resolve().parents[4]
STATIC_PDF_DIR = BASE_DIR / "static" / "pdf"

LOGO_PATH = STATIC_PDF_DIR / "starcolors-logo.png"
FOOTER_IMAGE_PATH = STATIC_PDF_DIR / "pdf-footer-wave.png"

ORANGE = colors.HexColor("#f28c00")
DARK = colors.HexColor("#1f2933")
DARKGRAY = colors.HexColor("#696969")
LIGHT_GRAY = colors.HexColor("#f2f2f2")
MID_GRAY = colors.HexColor("#d9d9d9")
WHITE = colors.white


def build_quote_pdf(payload: QuoteCreate, quote: QuoteResult) -> bytes:
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=0.45 * inch,
        leftMargin=0.45 * inch,
        topMargin=0.35 * inch,
        bottomMargin=0.35 * inch,
        title="Precotizacion StarColors",
    )

    styles = build_styles()
    story = []

    story.extend(build_header(styles))
    story.append(Spacer(1, 14))

    story.append(build_service_table(payload, styles))
    story.append(Spacer(1, 8))

    story.append(build_quote_table(payload, quote, styles))
    story.append(Spacer(1, 8))

    story.append(build_total_table(quote, styles))
    story.append(Spacer(1, 12))

    story.append(build_note(styles))
    story.append(Spacer(1, 18))

    story.extend(build_footer(styles))

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def build_styles() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle(
            name="Title",
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=ORANGE,
            alignment=0,
        ),
        "website": ParagraphStyle(
            name="Website",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=DARK,
            alignment=0,
        ),
        "body": ParagraphStyle(
            name="Body",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=DARK,
        ),
        "body_bold": ParagraphStyle(
            name="BodyBold",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=WHITE,
        ),
        "note": ParagraphStyle(
            name="Note",
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=DARKGRAY,
        ),
        "footer": ParagraphStyle(
            name="Footer",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=WHITE,
            alignment=1,
        ),
    }


def build_header(styles: dict[str, ParagraphStyle]) -> list:
    left_content = [
        Paragraph("www.starcolorsmx.com", styles["website"]),
        Spacer(1, 10),
        Paragraph("Pre - Cotizacion", styles["title"]),
    ]

    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH))
        logo.drawHeight = 0.7 * inch
        logo.drawWidth = 2.0 * inch
        right_content = logo
    else:
        right_content = Paragraph("StarColors", styles["title"])

    header = Table(
        [[left_content, right_content]],
        colWidths=[4.6 * inch, 2.0 * inch],
    )

    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    return [header]


def build_service_table(payload: QuoteCreate, styles: dict[str, ParagraphStyle]) -> Table:
    today = date.today().strftime("%d/%m/%Y")

    data = [
        ["SERVICIO", "DATOS GENERALES", "FECHA"],
        [
            "Pintura residencial",
            f"Cliente: {payload.customer_name}<br/>"
            f"Contacto: {payload.contact_method} - {payload.contact_value}<br/>"
            f"Ubicacion: {payload.city}, {payload.state}, CP {payload.postal_code}",
            today,
        ],
    ]

    table = Table(
        [
            [Paragraph(cell, styles["body_bold"]) for cell in data[0]],
            [
                Paragraph(data[1][0], styles["note"]),
                Paragraph(data[1][1], styles["note"]),
                Paragraph(data[1][2], styles["note"]),
            ],
        ],
        colWidths=[1.7 * inch, 3.6 * inch, 1.3 * inch],
    )

    apply_table_style(table)

    return table


def build_quote_table(
    payload: QuoteCreate,
    quote: QuoteResult,
    styles: dict[str, ParagraphStyle],
) -> Table:
    description = build_service_description(payload, quote)

    data = [
        ["CANT.", "MEDIDA", "DESCRIPCIÓN", "PRECIO UNITARIO", "IMPORTE"],
        [
            format_number(quote.square_meters),
            "m2",
            description,
            "",
            format_money(quote.estimated_price),
        ],
    ]

    table = Table(
        [
            [Paragraph(cell, styles["body_bold"]) for cell in data[0]],
            [
                Paragraph(data[1][0], styles["note"]),
                Paragraph(data[1][1], styles["note"]),
                Paragraph(data[1][2], styles["note"]),
                Paragraph(data[1][3], styles["note"]),
                Paragraph(data[1][4], styles["note"]),
            ],
        ],
        colWidths=[0.75 * inch, 0.85 * inch, 3.1 * inch, 1.05 * inch, 0.85 * inch],
    )

    apply_table_style(table)

    return table


def build_total_table(quote: QuoteResult, styles: dict[str, ParagraphStyle]) -> Table:
    table = Table(
        [
            [
                "",
                Paragraph("IMPORTE", styles["body_bold"]),
                Paragraph(format_money(quote.estimated_price), styles["note"]),
            ]
        ],
        colWidths=[4.7 * inch, 1.05 * inch, 0.85 * inch],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (1, 0), (1, 0), ORANGE),
                ("BACKGROUND", (2, 0), (2, 0), LIGHT_GRAY),
                ("TEXTCOLOR", (1, 0), (1, 0), DARK),
                ("GRID", (1, 0), (2, 0), 0.5, DARK),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (2, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    return table


def build_note(styles: dict[str, ParagraphStyle]) -> Paragraph:
    text = (
        "<b>Nota:</b> La presente es una precotizacion estimada, elaborada con base "
        "en la informacion proporcionada por el cliente. Los precios, cantidades y "
        "alcances pueden variar despues de realizar una visita ocular o revision "
        "tecnica en sitio. La cotizacion final se ajustara conforme a las condiciones "
        "reales del trabajo, materiales requeridos y maniobras necesarias. "
        "<b>Vigencia: 10 dias naturales. PRECIOS MAS I.V.A.</b>"
    )

    return Paragraph(text, styles["note"])


def build_footer(styles: dict[str, ParagraphStyle]) -> list:
    if FOOTER_IMAGE_PATH.exists():
        footer = Image(str(FOOTER_IMAGE_PATH))
        footer.drawWidth = 6.6 * inch
        footer.drawHeight = 0.75 * inch
        return [footer]

    footer_table = Table(
        [[Paragraph("www.starcolorsmx.com", styles["footer"])]],
        colWidths=[6.6 * inch],
        rowHeights=[0.55 * inch],
    )

    footer_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ORANGE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    return [footer_table]


def apply_table_style(table: Table) -> None:
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), ORANGE),
                ("TEXTCOLOR", (0, 0), (-1, 0), DARK),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_GRAY),
                ("GRID", (0, 0), (-1, -1), 0.5, DARK),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )


def build_service_description(payload: QuoteCreate, quote: QuoteResult) -> str:
    features = [
        adjustment.option_name
        for adjustment in quote.adjustments
        if adjustment.percentage != 0
    ]

    if not features:
        features = ["Sin ajustes adicionales relevantes"]

    features_text = ", ".join(features)

    return (
        f"{quote.paint_product_name}<br/>"
        f"Servicio de pintura en {format_number(quote.square_meters)} m2.<br/>"
        f"Caracteristicas: {features_text}.<br/>"
        f"Actividades del lugar: {payload.place_activities or 'No especificado'}."
    )


def format_money(value: float) -> str:
    return f"${value:,.2f}"


def format_number(value: float) -> str:
    if value.is_integer():
        return str(int(value))

    return f"{value:,.2f}"
