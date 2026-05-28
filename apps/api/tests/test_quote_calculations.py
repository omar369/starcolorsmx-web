from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_payload(**overrides):
    payload = {
        "property_type": "casa",
        "work_location": "interior",
        "square_meters": 40,
        "service_type": "mantenimiento",
        "paint_product": "vin-r",
        "color_intensity": "intensidad-1",
        "surface_state": "bueno",
        "texture": "liso-basico",
        "advance_difficulty": "baja",
        "occupancy": "desocupado",
        "height_risk": "menor-3-mts",
        "area_protection": "area-libre",
        "preparation": ["lijado", "sellado", "resane-menor"],
        "schedule": "horario-libre",
        "place_activities": "Habitación residencial",
        "state": "queretaro",
        "city": "Querétaro",
        "postal_code": "76000",
        "customer_name": "Omar",
        "contact_method": "whatsapp",
        "contact_value": "4421234567",
        "wants_offers": False,
    }

    payload.update(overrides)
    return payload


def print_quote_result(label: str, data: dict):
    print("\n" + "=" * 80)
    print(label)
    print("-" * 80)
    print(f"Cliente: {data['customer_name']}")
    print(f"Pintura: {data['paint_product_name']}")
    print(f"m²: {data['square_meters']}")
    print(f"Precio base/m²: ${data['base_price_per_m2']}")
    print(f"Porcentaje total: {data['total_adjustment_percentage']}")
    print(f"Precio ajustado/m²: ${data['adjusted_price_per_m2']}")
    print(f"Precio Previo ajustes: ${data['subtotal']}")
    print(f"Total con ajustes: ${data['estimated_price']}")
    print("Ajustes:")
    for adjustment in data["adjustments"]:
        print(
            f"  - {adjustment['category']}: "
            f"{adjustment['option_name']} "
            f"({adjustment['percentage']}) "
            f"${adjustment['amount']}"
        )
    print("=" * 80)


def test_quote_calculation_basic_case():
    response = client.post("/api/v1/quotes/", json=make_payload())

    assert response.status_code == 200

    data = response.json()

    print_quote_result("Caso 1: básico residencial", data)

    assert data["base_price_per_m2"] == 55.0
    assert data["square_meters"] == 40.0
    assert data["subtotal"] == 2200.0


def test_quote_calculation_with_small_positive_adjustment():
    response = client.post(
        "/api/v1/quotes/",
        json=make_payload(
            service_type="obra-nueva",
            advance_difficulty="media",
            height_risk="mayor-3-mts",
            preparation= ["lijado", "sellado", "resane-menor"],
        ),
    )

    assert response.status_code == 200

    data = response.json()

    print_quote_result("Caso 2: ajuste pequeño positivo", data)

    assert data["paint_product_name"] == "VIN R"


def test_quote_calculation_premium_complex_case():
    response = client.post(
        "/api/v1/quotes/",
        json=make_payload(
            square_meters=120,
            paint_product="vinimex-total",
            color_intensity="intensidad-6",
            surface_state="regular",
            texture="rugoso",
            advance_difficulty="alta",
            occupancy="ocupacion-moderada",
            height_risk="mayor-6-mts",
            area_protection="proteccion-moderada",
            preparation= ["lijado", "sellado", "resane-menor"],
            schedule="horario-limitado",
            state="guanajuato",
        ),
    )

    assert response.status_code == 200

    data = response.json()

    print_quote_result("Caso 3: proyecto complejo premium", data)

    assert data["paint_product_name"] == "VINIMEX TOTAL"


def test_quote_calculation_high_risk_case():
    response = client.post(
        "/api/v1/quotes/",
        json=make_payload(
            square_meters=80,
            paint_product="berel-100acryl",
            surface_state="malo",
            texture="extra-rugoso",
            advance_difficulty="critica",
            occupancy="alta-ocupacion",
            height_risk="mayor-12-mts",
            area_protection="area-sensible",
            preparation= ["lijado", "sellado", "resane-menor"],
            schedule="urgencia",
            state="ciudad-de-mexico",
        ),
    )

    assert response.status_code == 200

    data = response.json()

    print_quote_result("Caso 4: alto riesgo / alta complejidad", data)

    assert data["paint_product_name"] == "BEREL 100ACRYL"


def test_quote_calculation_negative_service_adjustment():
    response = client.post(
        "/api/v1/quotes/",
        json=make_payload(
            square_meters=60,
            service_type="obra-nueva",
            paint_product="vin-r",
            color_intensity="intensidad-1",
            surface_state="excelente",
            texture="liso-basico",
            advance_difficulty="baja",
            occupancy="desocupado",
            height_risk="menor-3-mts",
            area_protection="area-libre",
            preparation= ["resane-menor"],
            schedule="horario-libre",
            state="queretaro",
        ),
    )

    assert response.status_code == 200

    data = response.json()

    print_quote_result("Caso 5: obra nueva con descuento", data)

    assert data["total_adjustment_percentage"] < 0.20
