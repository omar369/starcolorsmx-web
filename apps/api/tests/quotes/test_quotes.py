from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_quote_returns_estimated_price():
    response = client.post("/api/v1/quotes/", json=valid_quote_payload())

    assert response.status_code == 200

    data = response.json()

    assert data["customer_name"] == "Juan"
    assert data["paint_product"] == "vin-pro"
    assert data["paint_product_name"] == "VIN PRO"

    assert data["base_price_per_m2"] == 70.0
    assert data["square_meters"] == 100.0
    assert data["subtotal"] == 7000.0

    assert data["total_adjustment_percentage"] == 0.333
    assert data["adjusted_price_per_m2"] == 93.31
    assert data["estimated_price"] == 9331.0

    assert len(data["adjustments"]) == 11

    preparation_adjustment = next(
        adjustment
        for adjustment in data["adjustments"]
        if adjustment["category"] == "Preparación"
    )

    assert preparation_adjustment == {
        "category": "Preparación",
        "option_id": "resane-menor",
        "option_name": "Resane menor",
        "percentage": 0.06,
        "amount": 420.0,
    }


def test_create_quote_supports_multiple_preparations():
    payload = valid_quote_payload()
    payload["preparation"] = ["resane-menor", "sellado", "lijado"]

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 200

    data = response.json()

    preparation_adjustments = [
        adjustment
        for adjustment in data["adjustments"]
        if adjustment["category"] == "Preparación"
    ]

    assert len(preparation_adjustments) == 3
    assert [item["option_id"] for item in preparation_adjustments] == [
        "resane-menor",
        "sellado",
        "lijado",
    ]

    assert data["total_adjustment_percentage"] == 0.723
    assert data["adjusted_price_per_m2"] == 120.61
    assert data["estimated_price"] == 12061.0


def test_list_quote_options_returns_catalogs():
    response = client.get("/api/v1/quotes/options")

    assert response.status_code == 200

    data = response.json()

    assert data["paints"][0] == {
        "id": "vin-r",
        "name": "VIN R",
    }
    assert data["surface_states"][2] == {
        "id": "regular",
        "name": "Regular",
    }
    assert data["service_types"][0] == {
        "id": "obra-nueva",
        "name": "Obra nueva",
    }
    assert data["states"][-1] == {
        "id": "baja-california",
        "name": "Baja California",
    }

    assert "price_per_m2" not in data["paints"][0]
    assert "percentage" not in data["surface_states"][2]
    assert "percentage" not in data["service_types"][0]
    assert "percentage" not in data["states"][-1]


def test_create_quote_rejects_invalid_paint_product():
    payload = valid_quote_payload()
    payload["paint_product"] = "pintura-inventada"

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 422


def test_create_quote_rejects_invalid_preparation():
    payload = valid_quote_payload()
    payload["preparation"] = ["resane-menor", "preparacion-inventada"]

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 422


def test_create_quote_accepts_empty_preparation():
    """
    Empty preparation list is explicitly valid: it means the job requires
    no surface preparation, so no preparation surcharge is applied.
    The schema validator documents this at QuoteCreate.validate_preparation.
    """
    payload = valid_quote_payload()
    payload["preparation"] = []

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 200
    data = response.json()
    preparation_adjustments = [
        adj for adj in data["adjustments"] if adj["category"] == "Preparación"
    ]
    assert preparation_adjustments == []


def test_create_quote_rejects_invalid_email_contact():
    payload = valid_quote_payload()
    payload["contact_method"] = "email"
    payload["contact_value"] = "correo-invalido"

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 422


def test_create_quote_rejects_zero_square_meters():
    payload = valid_quote_payload()
    payload["square_meters"] = 0

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 422


def valid_quote_payload():
    return {
        "property_type": "casa",
        "work_location": "interior",
        "square_meters": 100,
        "service_type": "obra-nueva",
        "paint_product": "vin-pro",
        "color_intensity": "intensidad-4",
        "surface_state": "malo",
        "texture": "rugoso",
        "advance_difficulty": "alta",
        "occupancy": "baja-ocupacion",
        "height_risk": "mayor-6-mts",
        "area_protection": "cobertura-ligera",
        "preparation": ["resane-menor"],
        "schedule": "horario-controlado",
        "place_activities": "Casa habitada durante el trabajo",
        "state": "queretaro",
        "city": "Queretaro",
        "postal_code": "76000",
        "customer_name": "Juan",
        "contact_method": "whatsapp",
        "contact_value": "4427188369",
        "wants_offers": True,
    }


def test_create_quote_rejects_square_meters_below_minimum():
    """
    La API debe rechazar cualquier valor menor a 100 m² con 422.
    El mínimo (ge=100) se definió porque superficies menores están
    fuera del rango de servicio de StarColors.
    """
    payload = valid_quote_payload()
    payload["square_meters"] = 99.99

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 422


def test_create_quote_accepts_minimum_square_meters():
    """
    Exactamente 100 m² debe ser aceptado (límite inclusivo ge=100).
    Verifica que el boundary value no sea rechazado por error off-by-one.
    """
    payload = valid_quote_payload()
    payload["square_meters"] = 100.0

    response = client.post("/api/v1/quotes/", json=payload)

    assert response.status_code == 200
    assert response.json()["square_meters"] == 100.0
