from app.api.v1.quotes.catalog import AdjustmentOption, PriceOption, find_option
from app.api.v1.quotes.schemas import QuoteAdjustment, QuoteCreate

TECHNICAL_ADJUSTMENT_FIELDS = [
    ("service_type", "Tipo de servicio"),
    ("color_intensity", "Color"),
    ("surface_state", "Estado de superficie"),
    ("texture", "Textura"),
    ("advance_difficulty", "Dificultad de avance"),
    ("occupancy", "Ocupación del inmueble"),
    ("height_risk", "Altura y riesgo"),
    ("area_protection", "Protección del área"),
    ("schedule", "Horarios"),
]

LOGISTICS_ADJUSTMENT_FIELDS = [
    ("state", "Estado"),
]

ADJUSTMENT_FIELDS = TECHNICAL_ADJUSTMENT_FIELDS + LOGISTICS_ADJUSTMENT_FIELDS


def get_paint_product(paint_product_id: str) -> PriceOption:
    option = find_option("paint_product", paint_product_id)

    if not isinstance(option, PriceOption):
        raise TypeError("paint product catalog returned an invalid option")

    return option


def get_adjustment(catalog_name: str, option_id: str) -> AdjustmentOption:
    option = find_option(catalog_name, option_id)

    if not isinstance(option, AdjustmentOption):
        raise TypeError(f"{catalog_name} catalog returned an invalid option")

    return option


def build_adjustments(
    payload: QuoteCreate,
    subtotal: float,
    fields: list[tuple[str, str]] | None = None,
) -> list[QuoteAdjustment]:
    adjustment_fields = fields or ADJUSTMENT_FIELDS
    adjustments: list[QuoteAdjustment] = []

    for field_name, label in adjustment_fields:
        option_id = getattr(payload, field_name)
        option = get_adjustment(field_name, option_id)
        amount = subtotal * option.percentage

        adjustments.append(
            QuoteAdjustment(
                category=label,
                option_id=option.id,
                option_name=option.name,
                percentage=round(option.percentage, 4),
                amount=round(amount, 2),
            )
        )

    for option_id in payload.preparation:
        option = get_adjustment("preparation", option_id)
        amount = subtotal * option.percentage

        adjustments.append(
            QuoteAdjustment(
                category="Preparación",
                option_id=option.id,
                option_name=option.name,
                percentage=round(option.percentage, 4),
                amount=round(amount, 2)
            )
        )

    return adjustments


def calculate_total_adjustment_percentage(
    adjustments: list[QuoteAdjustment],
) -> float:
    return sum(adjustment.percentage for adjustment in adjustments)


def calculate_adjusted_price_per_m2(
    base_price_per_m2: float,
    total_adjustment_percentage: float,
) -> float:
    return base_price_per_m2 * (1 + total_adjustment_percentage)


def calculate_estimated_price(
    square_meters: float,
    adjusted_price_per_m2: float,
) -> float:
    return square_meters * adjusted_price_per_m2
