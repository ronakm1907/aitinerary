from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.jinja_env.globals.update(current_year=datetime.now().year)

# Placeholder connectors for external booking APIs.
# Replace these with real API clients or SDKs for hotels, car rentals, flights, and activities.

def fetch_flight_options(destination, preferred_airlines, time_range, budget):
    sample = [
        {
            "airline": "SkyLine Airways",
            "route": f"{destination} inbound",
            "time": "08:00 - 12:00",
            "price": 320,
            "booking_url": "https://example.com/flight/skyline"
        },
        {
            "airline": "AeroExpress",
            "route": f"{destination} outbound",
            "time": "13:00 - 17:00",
            "price": 280,
            "booking_url": "https://example.com/flight/aeroexpress"
        },
        {
            "airline": "JetSet",
            "route": f"{destination} nonstop",
            "time": "18:00 - 22:00",
            "price": 360,
            "booking_url": "https://example.com/flight/jetset"
        }
    ]
    if preferred_airlines:
        airlines = [a.strip().lower() for a in preferred_airlines.split(",") if a.strip()]
        if airlines:
            sample = [f for f in sample if f["airline"].lower() in airlines or any(a in f["airline"].lower() for a in airlines)]
    if budget:
        sample = [f for f in sample if f["price"] <= budget]
    return sample or sample[:1]


def fetch_hotel_options(destination, star_rating, rooms, budget_per_night):
    sample = [
        {
            "name": "City View Suites",
            "price_per_night": 140,
            "rating": 4,
            "rooms_available": 3,
            "type": "Hotel",
            "booking_url": "https://example.com/hotel/city-view-suites"
        },
        {
            "name": "Cozy Apartments",
            "price_per_night": 95,
            "rating": 3,
            "rooms_available": 5,
            "type": "Apartment",
            "booking_url": "https://example.com/hotel/cozy-apartments"
        },
        {
            "name": "Luxury Resort Retreat",
            "price_per_night": 250,
            "rating": 5,
            "rooms_available": 2,
            "type": "Resort",
            "booking_url": "https://example.com/hotel/luxury-resort"
        }
    ]
    return [h for h in sample if h["rating"] >= star_rating and h["rooms_available"] >= rooms and (budget_per_night == 0 or h["price_per_night"] <= budget_per_night)]


def fetch_car_rental_options(destination, car_type, budget_per_day):
    sample = [
        {
            "name": "Standard Sedan",
            "daily_price": 38,
            "type": "Sedan",
            "provider": "FastRental",
            "booking_url": "https://example.com/car/standard-sedan"
        },
        {
            "name": "SUV Adventure",
            "daily_price": 62,
            "type": "SUV",
            "provider": "RoadTrip Rentals",
            "booking_url": "https://example.com/car/suv-adventure"
        },
        {
            "name": "Compact Eco",
            "daily_price": 28,
            "type": "Compact",
            "provider": "GreenWheels",
            "booking_url": "https://example.com/car/compact-eco"
        }
    ]
    return [c for c in sample if (c["type"] == car_type or car_type == "Any") and (budget_per_day == 0 or c["daily_price"] <= budget_per_day)]


def fetch_activity_options(destination, intensity):
    sample = [
        {"name": "City Walking Tour", "category": "Relaxed", "price": 45},
        {"name": "Mountain Hike", "category": "Active", "price": 65},
        {"name": "Wine Tasting Experience", "category": "Relaxed", "price": 85},
        {"name": "Museum Day Pass", "category": "Moderate", "price": 25},
        {"name": "River Kayaking", "category": "Active", "price": 75}
    ]
    return [a for a in sample if intensity == "Any" or a["category"] == intensity]


def build_itinerary(form_data):
    destination = form_data.get("destination")
    start_date = form_data.get("start_date")
    end_date = form_data.get("end_date")
    travelers = int(form_data.get("travelers", 1) or 1)
    budget_per_person = int(form_data.get("budget_per_person", 0) or 0)
    preferred_airlines = form_data.get("preferred_airlines", "")
    flight_time_range = form_data.get("flight_time_range", "")
    flight_budget = int(form_data.get("flight_budget", 0) or 0)
    hotel_star = int(form_data.get("hotel_star", 0) or 0)
    hotel_rooms = int(form_data.get("hotel_rooms", 1) or 1)
    hotel_budget = int(form_data.get("hotel_budget", 0) or 0)
    car_type = form_data.get("car_type", "Any")
    car_budget = int(form_data.get("car_budget", 0) or 0)
    intensity = form_data.get("intensity", "Any")

    try:
        nights = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        nights = max(nights, 1)
    except Exception:
        nights = 1

    flight_options = fetch_flight_options(destination, preferred_airlines, flight_time_range, flight_budget)
    hotel_options = fetch_hotel_options(destination, hotel_star, hotel_rooms, hotel_budget)
    car_options = fetch_car_rental_options(destination, car_type, car_budget)
    activity_options = fetch_activity_options(destination, intensity)

    chosen_flight = flight_options[0] if flight_options else None
    chosen_hotel = hotel_options[0] if hotel_options else None
    chosen_car = car_options[0] if car_options else None
    chosen_activities = activity_options[:3]

    flight_total = chosen_flight["price"] if chosen_flight else 0
    hotel_total = (chosen_hotel["price_per_night"] * hotel_rooms) * nights if chosen_hotel else 0
    car_total = (chosen_car["daily_price"] * nights) if chosen_car else 0
    activities_total = sum(a["price"] for a in chosen_activities)
    total_trip_cost = flight_total + hotel_total + car_total + activities_total
    total_budget = budget_per_person * travelers

    budget_match = "Within budget" if total_trip_cost <= total_budget else "Over budget"

    return {
        "destination": destination,
        "dates": f"{start_date} to {end_date}",
        "travelers": travelers,
        "budget_per_person": budget_per_person,
        "total_budget": total_budget,
        "nights": nights,
        "flight": chosen_flight,
        "hotel": chosen_hotel,
        "car": chosen_car,
        "activities": chosen_activities,
        "preferences": {
            "preferred_airlines": preferred_airlines,
            "flight_time_range": flight_time_range,
            "intensity": intensity,
            "hotel_star": hotel_star,
            "hotel_rooms": hotel_rooms
        },
        "totals": {
            "flight": flight_total,
            "hotel": hotel_total,
            "car": car_total,
            "activities": activities_total,
            "grand_total": total_trip_cost,
            "budget_match": budget_match
        }
    }


def common_context():
    return {
        "filters": {
            "accommodation_types": ["Any", "Hotel", "Apartment", "Resort"],
            "car_types": ["Any", "Sedan", "SUV", "Compact"],
            "intensity_options": ["Any", "Relaxed", "Moderate", "Active"]
        }
    }


@app.route("/", methods=["GET", "POST"])
def index():
    itinerary = None
    if request.method == "POST":
        itinerary = build_itinerary(request.form)

    context = common_context()
    context.update({"itinerary": itinerary, "active_page": "home"})
    return render_template("index.html", **context)


@app.route("/signin")
def signin():
    return render_template("signin.html", active_page="signin")


@app.route("/partners")
def partners():
    return render_template("partners.html", active_page="partners")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    message_sent = False
    if request.method == "POST":
        message_sent = True

    return render_template("contact.html", active_page="contact", message_sent=message_sent)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
