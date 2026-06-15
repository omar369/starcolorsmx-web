from pydantic import BaseModel, Field, field_validator, model_validator

from app.api.v1.quotes.catalog import has_option


class QuoteCreate(BaseModel):
    property_type: str = Field(min_length=2, max_length=80)
    work_location: str = Field(min_length=2, max_length=80)
    square_meters: float = Field(gt=0, le=100_000)

    service_type: str = Field(min_length=2, max_length=80)
    paint_product: str = Field(min_length=2, max_length=80)
    color_intensity: str = Field(min_length=2, max_length=80)

    surface_state: str = Field(min_length=2, max_length=80)
    texture: str = Field(min_length=2, max_length=80)
    advance_difficulty: str = Field(min_length=2, max_length=80)
    occupancy: str = Field(min_length=2, max_length=80)
    height_risk: str = Field(min_length=2, max_length=80)
    area_protection: str = Field(min_length=2, max_length=80)
    preparation: list[str] = Field(min_length=1, max_length=20)
    schedule: str = Field(min_length=2, max_length=80)
    place_activities: str | None = Field(default=None, max_length=400)

    state: str = Field(min_length=2, max_length=80)
    city: str = Field(min_length=2, max_length=100)
    postal_code: str = Field(min_length=5, max_length=5)

    customer_name: str = Field(min_length=2, max_length=100)
    contact_method: str = Field(min_length=2, max_length=20)
    contact_value: str = Field(min_length=5, max_length=120)
    wants_offers: bool = False

    @field_validator("property_type")
    @classmethod
    def validate_property_type(cls, value: str) -> str:
        return validate_catalog_option("property_type", value)

    @field_validator("work_location")
    @classmethod
    def validate_work_location(cls, value: str) -> str:
        return validate_catalog_option("work_location", value)

    @field_validator("service_type")
    @classmethod
    def validate_service_type(cls, value: str) -> str:
        return validate_catalog_option("service_type", value)

    @field_validator("paint_product")
    @classmethod
    def validate_paint_product(cls, value: str) -> str:
        return validate_catalog_option("paint_product", value)

    @field_validator("color_intensity")
    @classmethod
    def validate_color_intensity(cls, value: str) -> str:
        return validate_catalog_option("color_intensity", value)

    @field_validator("surface_state")
    @classmethod
    def validate_surface_state(cls, value: str) -> str:
        return validate_catalog_option("surface_state", value)

    @field_validator("texture")
    @classmethod
    def validate_texture(cls, value: str) -> str:
        return validate_catalog_option("texture", value)

    @field_validator("advance_difficulty")
    @classmethod
    def validate_advance_difficulty(cls, value: str) -> str:
        return validate_catalog_option("advance_difficulty", value)

    @field_validator("occupancy")
    @classmethod
    def validate_occupancy(cls, value: str) -> str:
        return validate_catalog_option("occupancy", value)

    @field_validator("height_risk")
    @classmethod
    def validate_height_risk(cls, value: str) -> str:
        return validate_catalog_option("height_risk", value)

    @field_validator("area_protection")
    @classmethod
    def validate_area_protection(cls, value: str) -> str:
        return validate_catalog_option("area_protection", value)

    @field_validator("preparation")
    @classmethod
    def validate_preparation(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("Debes de elegir al menos una preparación")

        unique_values = list(dict.fromkeys(value))

        for option_id in unique_values:
            validate_catalog_option("preparation", option_id)

        return unique_values

    @field_validator("schedule")
    @classmethod
    def validate_schedule(cls, value: str) -> str:
        return validate_catalog_option("schedule", value)

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        return validate_catalog_option("state", value)

    @field_validator("contact_method")
    @classmethod
    def validate_contact_method(cls, value: str) -> str:
        if value not in {"whatsapp", "email"}:
            raise ValueError("invalid contact method")
        return value

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("postal code must contain only digits")
        return value

    @model_validator(mode="after")
    def validate_contact_value(self) -> "QuoteCreate":
        if self.contact_method == "email" and "@" not in self.contact_value:
            raise ValueError("valid email contact is required")

        if self.contact_method == "whatsapp":
            digits = "".join(char for char in self.contact_value if char.isdigit())
            if len(digits) < 10:
                raise ValueError("valid WhatsApp number is required")

        return self


class BasicOption(BaseModel):
    id: str
    name: str


class QuoteOptions(BaseModel):
    property_types: list[BasicOption]
    work_locations: list[BasicOption]
    service_types: list[BasicOption]
    paints: list[BasicOption]
    color_intensities: list[BasicOption]
    surface_states: list[BasicOption]
    textures: list[BasicOption]
    advance_difficulties: list[BasicOption]
    occupancies: list[BasicOption]
    height_risks: list[BasicOption]
    area_protections: list[BasicOption]
    preparations: list[BasicOption]
    schedules: list[BasicOption]
    states: list[BasicOption]


class QuoteAdjustment(BaseModel):
    category: str
    option_id: str
    option_name: str
    percentage: float
    amount: float


class QuoteResult(BaseModel):
    id: int | None = None
    customer_name: str
    paint_product: str
    paint_product_name: str
    base_price_per_m2: float
    total_adjustment_percentage: float
    adjusted_price_per_m2: float
    square_meters: float
    subtotal: float
    adjustments: list[QuoteAdjustment]
    estimated_price: float
    created_at: str | None = None
    is_expired: bool = False



def validate_catalog_option(catalog_name: str, value: str) -> str:
    if not has_option(catalog_name, value):
        raise ValueError(f"invalid {catalog_name}")
    return value
