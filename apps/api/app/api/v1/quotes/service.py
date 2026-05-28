from collections.abc import Sequence

from app.api.v1.quotes import catalog
from app.api.v1.quotes.pricing import (
    build_adjustments,
    calculate_adjusted_price_per_m2,
    calculate_estimated_price,
    calculate_total_adjustment_percentage,
    get_paint_product,
)
from app.api.v1.quotes.schemas import (
    BasicOption,
    QuoteCreate,
    QuoteOptions,
    QuoteResult,
)


def calculate_quote(payload: QuoteCreate) -> QuoteResult:
    paint_product = get_paint_product(payload.paint_product)

    base_price_per_m2 = paint_product.price_per_m2
    subtotal = payload.square_meters * base_price_per_m2

    adjustments = build_adjustments(payload, subtotal)

    total_adjustment_percentage = calculate_total_adjustment_percentage(
        adjustments
    )

    adjusted_price_per_m2 = calculate_adjusted_price_per_m2(
        base_price_per_m2=base_price_per_m2,
        total_adjustment_percentage=total_adjustment_percentage,
    )

    estimated_price = calculate_estimated_price(
        square_meters=payload.square_meters,
        adjusted_price_per_m2=adjusted_price_per_m2,
    )

    return QuoteResult(
        customer_name=payload.customer_name,
        paint_product=paint_product.id,
        paint_product_name=paint_product.name,
        base_price_per_m2=round(base_price_per_m2, 2),
        total_adjustment_percentage=round(total_adjustment_percentage, 4),
        adjusted_price_per_m2=round(adjusted_price_per_m2, 2),
        square_meters=payload.square_meters,
        subtotal=round(subtotal, 2),
        adjustments=adjustments,
        estimated_price=round(estimated_price, 2),
    )


def get_quote_options() -> QuoteOptions:
    return QuoteOptions(
        property_types=to_basic_options(catalog.PROPERTY_TYPES),
        work_locations=to_basic_options(catalog.WORK_LOCATIONS),
        service_types=to_basic_options(catalog.SERVICE_TYPES),
        paints=to_basic_options(catalog.PAINT_PRODUCTS),
        color_intensities=to_basic_options(catalog.COLOR_INTENSITIES),
        surface_states=to_basic_options(catalog.SURFACE_STATES),
        textures=to_basic_options(catalog.TEXTURES),
        advance_difficulties=to_basic_options(catalog.ADVANCE_DIFFICULTIES),
        occupancies=to_basic_options(catalog.OCCUPANCIES),
        height_risks=to_basic_options(catalog.HEIGHT_RISKS),
        area_protections=to_basic_options(catalog.AREA_PROTECTIONS),
        preparations=to_basic_options(catalog.PREPARATIONS),
        schedules=to_basic_options(catalog.SCHEDULES),
        states=to_basic_options(catalog.STATES),
    )


def to_basic_options(options: Sequence[catalog.Option]) -> list[BasicOption]:
    return [BasicOption(id=option.id, name=option.name) for option in options]
