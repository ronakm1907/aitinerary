import json
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-in-prod")
app.jinja_env.globals.update(current_year=datetime.now().year)

SAVE_FILE = os.path.join(app.root_path, "saved_itineraries.json")
USERS_FILE = os.path.join(app.root_path, "users.json")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def write_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def get_current_user():
    return session.get("username")


@app.context_processor
def inject_user_context():
    return {
        "logged_in": get_current_user() is not None,
        "current_user": get_current_user()
    }

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


def default_activity_plan(intensity, nights):
    sample = [
        {
            "day_number": 1,
            "title": "Arrive and Explore the Old Town",
            "activities": ["Check into your hotel", "Take a walking tour of the historic district", "Enjoy a welcome dinner at a local restaurant"],
            "guidelines": "After arriving, take some time to settle in, exchange currency if needed, and walk the nearby streets to get familiar with local landmarks.",
            "estimated_cost": 120
        },
        {
            "day_number": 2,
            "title": "Cultural Highlights and Local Cuisine",
            "activities": ["Visit the museum district", "Sample regional specialties at a market", "Attend an evening cultural show"],
            "guidelines": "Start early at the museums to avoid lines, and book dinner reservations for popular local eateries.",
            "estimated_cost": 150
        },
        {
            "day_number": 3,
            "title": "Scenic Adventure",
            "activities": ["Take a nature hike", "Enjoy a scenic viewpoint", "Relax with a casual dinner"],
            "guidelines": "Wear comfortable shoes for the hike, carry water, and plan transportation back to the city in advance.",
            "estimated_cost": 110
        }
    ]
    if intensity == "Active":
        sample[1]["activities"] = ["Join a morning hike", "Try a local adventure tour", "Finish with a lively dinner"]
        sample[1]["guidelines"] = "Book your adventure tour in advance and bring layered clothing for changing weather." 
        sample[1]["estimated_cost"] = 165
    elif intensity == "Relaxed":
        sample[1]["activities"] = ["Stroll through a botanical garden", "Enjoy a leisurely brunch", "Have a relaxing dinner with views"]
        sample[1]["guidelines"] = "Plan for a slow morning, and leave plenty of time to relax between activities."
        sample[1]["estimated_cost"] = 130

    while len(sample) < nights:
        next_day = len(sample) + 1
        sample.append({
            "day_number": next_day,
            "title": f"More {intensity.lower()} travel experiences",
            "activities": [
                "Visit a local attraction",
                "Enjoy a casual meal",
                "Take time to relax and explore at your own pace"
            ],
            "guidelines": "Use this day to follow your energy level and explore something local. Book any attractions ahead if needed.",
            "estimated_cost": 100
        })

    return sample[:nights]


def ai_recommend_daily_plan(destination, intensity, nights, travelers, budget_per_person):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return default_activity_plan(intensity, nights)

    prompt = (
        f"You are a travel itinerary assistant. Create a day-by-day itinerary for {nights} night(s) in {destination} "
        f"for {travelers} guest(s). The traveler prefers a {intensity} pace. "
        f"Provide practical post-arrival guidelines to follow each day. "
        f"Keep the plan within a budget of ${budget_per_person} per person. "
        "Output only valid JSON with a top-level key named days, where each day item contains: day_number, title, activities, guidelines, estimated_cost. "
        "Activities should be a short array of tasks or experiences, and guidelines should be a clear sentence for travelers."
    )

    try:
        import openai
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful travel planning assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=450,
            temperature=0.8,
        )
        text = response.choices[0].message.content.strip()
        plan = json.loads(text)
        if isinstance(plan, dict) and "days" in plan and isinstance(plan["days"], list):
            return plan["days"]
    except Exception:
        pass

    return default_activity_plan(intensity, nights)


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
    daily_plan = ai_recommend_daily_plan(destination, intensity, nights, travelers, budget_per_person)

    chosen_flight = flight_options[0] if flight_options else None
    chosen_hotel = hotel_options[0] if hotel_options else None
    chosen_car = car_options[0] if car_options else None

    flight_total = chosen_flight["price"] if chosen_flight else 0
    hotel_total = (chosen_hotel["price_per_night"] * hotel_rooms) * nights if chosen_hotel else 0
    car_total = (chosen_car["daily_price"] * nights) if chosen_car else 0
    activities_total = sum(day.get("estimated_cost", 0) for day in daily_plan)
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
        "daily_plan": daily_plan,
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


def load_saved_itineraries():
    if not os.path.exists(SAVE_FILE):
        return []
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def write_saved_itineraries(saved_list):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(saved_list, f, indent=2)


def save_itinerary_data(itinerary, values=None):
    saved_list = load_saved_itineraries()
    record = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.now().isoformat(),
        "destination": itinerary.get("destination"),
        "dates": itinerary.get("dates"),
        "travelers": itinerary.get("travelers"),
        "total_budget": itinerary.get("total_budget"),
        "grand_total": itinerary.get("totals", {}).get("grand_total", 0),
        "intensity": itinerary.get("preferences", {}).get("intensity", "Any"),
        "values": values or {},
        "data": itinerary
    }
    saved_list.append(record)
    write_saved_itineraries(saved_list)
    return record


def find_saved_itinerary(itinerary_id):
    for item in load_saved_itineraries():
        if item.get("id") == itinerary_id:
            return item
    return None


def build_values_from_itinerary(itinerary):
    values = {}
    preferences = itinerary.get("preferences", {})
    values["destination"] = itinerary.get("destination", "")
    dates = itinerary.get("dates", "").split(" to ")
    if len(dates) == 2:
        values["start_date"], values["end_date"] = dates
    values["travelers"] = itinerary.get("travelers", "1")
    values["budget_per_person"] = itinerary.get("budget_per_person", "")
    values["preferred_airlines"] = preferences.get("preferred_airlines", "")
    values["flight_time_range"] = preferences.get("flight_time_range", "")
    values["flight_budget"] = itinerary.get("totals", {}).get("flight", "")
    values["hotel_star"] = preferences.get("hotel_star", "")
    values["hotel_rooms"] = preferences.get("hotel_rooms", "")
    values["hotel_budget"] = ""
    values["car_type"] = itinerary.get("car", {}).get("type", "Any")
    values["car_budget"] = ""
    values["intensity"] = preferences.get("intensity", "Any")
    return values


@app.route("/", methods=["GET", "POST"])
def index():
    itinerary = None
    values = {}
    if request.method == "POST":
        values = request.form.to_dict()
        itinerary = build_itinerary(request.form)
        session["last_values"] = values
    else:
        values = session.get("last_values", {})

    context = common_context()
    context.update({"itinerary": itinerary, "values": values, "active_page": "home"})
    return render_template("index.html", **context)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    message = ""
    next_url = request.args.get("next") or request.form.get("next") or url_for("index")
    if request.method == "POST":
        mode = request.form.get("mode", "signin")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if not username or not password:
            message = "Please enter both username and password."
        else:
            users = load_users()
            if mode == "signup":
                if username in users:
                    message = "Username already exists. Choose another."
                else:
                    users[username] = password
                    write_users(users)
                    session["username"] = username
                    return redirect(next_url)
            else:
                if username in users and users[username] == password:
                    session["username"] = username
                    return redirect(next_url)
                message = "Invalid username or password."

    return render_template("signin.html", active_page="signin", message=message, next_url=next_url)


@app.route("/signout")
def signout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/partners")
def partners():
    return render_template("partners.html", active_page="partners")


@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/save", methods=["POST"])
def save_itinerary():
    if get_current_user() is None:
        return redirect(url_for("signin", next=url_for("index")))

    itinerary_json = request.form.get("itinerary_json")
    values_json = request.form.get("values_json")
    values = {}
    if values_json:
        try:
            values = json.loads(values_json)
        except Exception:
            values = {}

    if not itinerary_json:
        return redirect(url_for("index"))

    try:
        itinerary = json.loads(itinerary_json)
        saved_item = save_itinerary_data(itinerary, values)
        session["last_values"] = values
        session["last_saved_id"] = saved_item["id"]
    except Exception:
        return redirect(url_for("index"))

    return redirect(url_for("saved", saved="true"))


@app.route("/saved")
def saved():
    if get_current_user() is None:
        return redirect(url_for("signin", next=url_for("saved")))

    saved_itineraries = load_saved_itineraries()
    saved_flag = request.args.get("saved") == "true"
    return render_template("saved.html", active_page="saved", saved_itineraries=saved_itineraries, saved_flag=saved_flag)


@app.route("/saved/<itinerary_id>")
def saved_detail(itinerary_id):
    if get_current_user() is None:
        return redirect(url_for("signin", next=url_for("saved_detail", itinerary_id=itinerary_id)))

    saved_item = find_saved_itinerary(itinerary_id)
    if not saved_item:
        return redirect(url_for("saved"))

    itinerary = saved_item.get("data")
    values = saved_item.get("values") or build_values_from_itinerary(itinerary)
    context = common_context()
    context.update({"itinerary": itinerary, "values": values, "active_page": "saved"})
    return render_template("index.html", **context)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    message_sent = False
    if request.method == "POST":
        message_sent = True

    return render_template("contact.html", active_page="contact", message_sent=message_sent)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
