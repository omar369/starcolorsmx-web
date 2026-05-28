from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    id: str
    name: str


@dataclass(frozen=True)
class PriceOption(Option):
    price_per_m2: float


@dataclass(frozen=True)
class AdjustmentOption(Option):
    percentage: float


PROPERTY_TYPES = [
    Option("casa", "Casa"),
    Option("departamento", "Departamento"),
    Option("oficina", "Oficina"),
    Option("local-comercial", "Local comercial"),
    Option("bodega", "Bodega"),
    Option("otro", "Otro"),
]

WORK_LOCATIONS = [
    Option("interior", "Interior"),
    Option("exterior", "Exterior"),
    Option("interior-exterior", "Interior y exterior"),
]

PAINT_PRODUCTS = [
    PriceOption("vin-r", "VIN R", 55.00),
    PriceOption("vin-e", "VIN E", 60.00),
    PriceOption("vin-es", "VIN ES", 65.00),
    PriceOption("vin-pro", "VIN PRO", 70.00),
    PriceOption("pro1000", "PRO1000", 70.00),
    PriceOption("vinimex", "VINIMEX", 75.00),
    PriceOption("vinimex-total", "VINIMEX TOTAL", 80.00),
    PriceOption("osel-bronce", "OSEL BRONCE", 64.00),
    PriceOption("osel-plata", "OSEL PLATA", 69.00),
    PriceOption("osel-oro", "OSEL ORO", 75.00),
    PriceOption("berelinte", "BERELINTE", 67.00),
    PriceOption("berelex", "BERELEX", 78.00),
    PriceOption("berel-100acryl", "BEREL 100ACRYL", 80.00),
]

COLOR_INTENSITIES = [
    AdjustmentOption("intensidad-1", "Intensidad 1", 0.00),
    AdjustmentOption("intensidad-2", "Intensidad 2", 0.00),
    AdjustmentOption("intensidad-3", "Intensidad 3", 0.00),
    AdjustmentOption("intensidad-4", "Intensidad 4", 0.015),
    AdjustmentOption("intensidad-5", "Intensidad 5", 0.030),
    AdjustmentOption("intensidad-6", "Intensidad 6", 0.040),
    AdjustmentOption("intensidad-7", "Intensidad 7", 0.060),
]

SURFACE_STATES = [
    AdjustmentOption("excelente", "Excelente", 0.00),
    AdjustmentOption("bueno", "Bueno", 0.00),
    AdjustmentOption("regular", "Regular", 0.036),
    AdjustmentOption("malo", "Malo", 0.068),
    AdjustmentOption("critico", "Critico", 0.110),
]

TEXTURES = [
    AdjustmentOption("liso-basico", "Liso basico", 0.00),
    AdjustmentOption("liso-fino", "Liso fino", 0.00),
    AdjustmentOption("ultra-liso", "Ultra liso", 0.00),
    AdjustmentOption("rugoso", "Rugoso", 0.040),
    AdjustmentOption("extra-rugoso", "Extra rugoso", 0.095),
]

ADVANCE_DIFFICULTIES = [
    AdjustmentOption("baja", "Baja", 0.00),
    AdjustmentOption("media", "Media", 0.045),
    AdjustmentOption("alta", "Alta", 0.080),
    AdjustmentOption("critica", "Critica", 0.180),
]

OCCUPANCIES = [
    AdjustmentOption("desocupado", "Desocupado", 0.00),
    AdjustmentOption("baja-ocupacion", "Baja ocupacion", 0.035),
    AdjustmentOption("ocupacion-moderada", "Ocupacion moderada", 0.070),
    AdjustmentOption("alta-ocupacion", "Alta ocupacion", 0.110),
    AdjustmentOption("ocupacion-critica", "Ocupacion critica", 0.180),
]

HEIGHT_RISKS = [
    AdjustmentOption("menor-3-mts", "Menor 3 mts", 0.00),
    AdjustmentOption("mayor-3-mts", "Mayor 3 mts", 0.030),
    AdjustmentOption("mayor-6-mts", "Mayor 6 mts", 0.060),
    AdjustmentOption("mayor-8-mts", "Mayor 8 mts", 0.180),
    AdjustmentOption("mayor-12-mts", "Mayor 12 mts", 0.320),
]

AREA_PROTECTIONS = [
    AdjustmentOption("area-libre", "Area libre", 0.00),
    AdjustmentOption("cobertura-ligera", "Cobertura ligera", 0.010),
    AdjustmentOption("proteccion-moderada", "Proteccion moderada", 0.020),
    AdjustmentOption("proteccion-extensa", "Proteccion extensa", 0.060),
    AdjustmentOption("area-sensible", "Area sensible", 0.135),
]

PREPARATIONS = [
    AdjustmentOption("lijado", "Lijado", 0.140),
    AdjustmentOption("resane-menor", "Resane menor", 0.060),
    AdjustmentOption("resane-mayor", "Resane mayor", 0.400),
    AdjustmentOption("sellado", "Sellado", 0.250),
    AdjustmentOption("fondo", "Fondo", 0.327),
    AdjustmentOption("limpieza-mecanica", "Limpieza mecanica", 0.235),
]

SCHEDULES = [
    AdjustmentOption("horario-libre", "Horario libre", 0.00),
    AdjustmentOption("horario-controlado", "Horario controlado", 0.035),
    AdjustmentOption("horario-limitado", "Horario limitado", 0.070),
    AdjustmentOption("horario-restringido", "Horario restringido", 0.120),
    AdjustmentOption("horario-critico", "Horario critico", 0.180),
    AdjustmentOption("urgencia", "Urgencia", 0.320),
    AdjustmentOption("nocturno", "Nocturno", 0.280),
]

SERVICE_TYPES = [
    AdjustmentOption("obra-nueva", "Obra nueva", -0.070),
    AdjustmentOption("mantenimiento", "Mantenimiento", 0.00),
]

STATES = [
    AdjustmentOption("queretaro", "Queretaro", 0.000),
    AdjustmentOption("guanajuato", "Guanajuato", 0.379),
    AdjustmentOption("michoacan", "Michoacan", 0.459),
    AdjustmentOption("estado-de-mexico", "Estado de Mexico", 0.505),
    AdjustmentOption("san-luis-potosi", "San Luis Potosi", 0.516),
    AdjustmentOption("hidalgo", "Hidalgo", 0.528),
    AdjustmentOption("ciudad-de-mexico", "Ciudad de Mexico", 0.539),
    AdjustmentOption("morelos", "Morelos", 0.782),
    AdjustmentOption("aguascalientes", "Aguascalientes", 0.839),
    AdjustmentOption("tlaxcala", "Tlaxcala", 0.874),
    AdjustmentOption("puebla", "Puebla", 0.897),
    AdjustmentOption("jalisco", "Jalisco", 0.919),
    AdjustmentOption("zacatecas", "Zacatecas", 1.091),
    AdjustmentOption("guerrero", "Guerrero", 1.300),
    AdjustmentOption("veracruz", "Veracruz", 1.311),
    AdjustmentOption("colima", "Colima", 1.402),
    AdjustmentOption("tamaulipas", "Tamaulipas", 1.482),
    AdjustmentOption("nayarit", "Nayarit", 1.494),
    AdjustmentOption("oaxaca", "Oaxaca", 1.700),
    AdjustmentOption("coahuila", "Coahuila", 1.734),
    AdjustmentOption("nuevo-leon", "Nuevo Leon", 1.860),
    AdjustmentOption("durango", "Durango", 1.871),
    AdjustmentOption("sinaloa", "Sinaloa", 2.685),
    AdjustmentOption("tabasco", "Tabasco", 2.697),
    AdjustmentOption("chiapas", "Chiapas", 2.800),
    AdjustmentOption("chihuahua", "Chihuahua", 3.028),
    AdjustmentOption("campeche", "Campeche", 3.180),
    AdjustmentOption("baja-california-sur", "Baja California Sur", 3.766),
    AdjustmentOption("yucatan", "Yucatan", 3.546),
    AdjustmentOption("quintana-roo", "Quintana Roo", 3.934),
    AdjustmentOption("sonora", "Sonora", 4.337),
    AdjustmentOption("baja-california", "Baja California", 5.746),
]

CATALOGS = {
    "property_type": PROPERTY_TYPES,
    "work_location": WORK_LOCATIONS,
    "paint_product": PAINT_PRODUCTS,
    "color_intensity": COLOR_INTENSITIES,
    "surface_state": SURFACE_STATES,
    "texture": TEXTURES,
    "advance_difficulty": ADVANCE_DIFFICULTIES,
    "occupancy": OCCUPANCIES,
    "height_risk": HEIGHT_RISKS,
    "area_protection": AREA_PROTECTIONS,
    "preparation": PREPARATIONS,
    "schedule": SCHEDULES,
    "service_type": SERVICE_TYPES,
    "state": STATES,
}


def find_option(catalog_name: str, option_id: str) -> Option:
    for option in CATALOGS[catalog_name]:
        if option.id == option_id:
            return option

    raise KeyError(option_id)


def has_option(catalog_name: str, option_id: str) -> bool:
    return any(option.id == option_id for option in CATALOGS[catalog_name])
