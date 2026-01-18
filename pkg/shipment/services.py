# pkg/shipment/services.py (Final Server-Side Calculation Logic)

from pkg.models import City, State, ShippingRate 
import random

def generate_tracking_number():
    """Generates a unique 10-digit tracking number."""
    return 'JX' + ''.join(str(random.randint(0, 9)) for _ in range(8))





def calculate_rate(pickup_city_id, delivery_city_id, weight_kg):
    if weight_kg <= 0:
        raise ValueError("Invalid package weight.")

    pickup_city = City.query.get(pickup_city_id)
    delivery_city = City.query.get(delivery_city_id)

    if not pickup_city or not delivery_city:
        raise ValueError("Invalid pickup or delivery city.")

    # -------- DISTANCE LOGIC --------
    if pickup_city.state_id == delivery_city.state_id:
        distance_km = 50      # intra-state
    else:
        distance_km = 450     # inter-state

    # -------- REALISTIC VEHICLE RULES --------
    VEHICLES = [
        {
            "type": "bike",
            "max_kg": 15,
            "base": 2000,
            "per_kg": 100,
            "per_km": 30
        },
        {
            "type": "van",
            "max_kg": 500,
            "base": 7000,
            "per_kg": 80,
            "per_km": 80
        },
        {
            "type": "bus",
            "max_kg": 2000,
            "base": 20000,
            "per_kg": 60,
            "per_km": 150
        }
    ]

    selected_vehicle = None

    for vehicle in VEHICLES:
        if weight_kg <= vehicle["max_kg"]:
            selected_vehicle = vehicle
            break

    if not selected_vehicle:
        raise ValueError("Package exceeds maximum supported weight.")

    # -------- PRICE CALCULATION --------
    amount = (
        selected_vehicle["base"]
        + (weight_kg * selected_vehicle["per_kg"])
        + (distance_km * selected_vehicle["per_km"])
    )

    return {
        "vehicle_type": selected_vehicle["type"],
        "distance_km": distance_km,
        "calculated_amount": round(amount, 2)
    }
