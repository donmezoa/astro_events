import argparse
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from astral.sun import sun
from astral.location import LocationInfo
from skyfield.api import load, Topos
from timezonefinder import TimezoneFinder
import pytz

# Map display names to Skyfield barycenter keys (used in de440.bsp)
planet_map = {
    "Mercury": "Mercury BARYCENTER",
    "Venus": "Venus BARYCENTER",
    "Mars": "MARS BARYCENTER",
    "Jupiter": "Jupiter BARYCENTER",
    "Saturn": "Saturn BARYCENTER",
    "Uranus": "Uranus BARYCENTER",
    "Neptune": "Neptune BARYCENTER"
}

# Return the current moon phase name for a given datetime
def moon_phase(date):
    epoch = datetime(2001, 1, 1, tzinfo=date.tzinfo)
    diff = date - epoch
    days = diff.days + (diff.seconds / 86400)
    lunations = 0.20439731 + (days * 0.03386319269)
    pos = lunations % 1
    phases = [
        "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
        "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"
    ]
    index = int((pos * 8) + 0.5) % 8
    return phases[index]

# Get latitude, longitude, and timezone from a city name
def get_coordinates_and_timezone(city_name):
    geolocator = Nominatim(user_agent="planet_viewer")
    location = geolocator.geocode(city_name)
    if not location:
        raise ValueError(f"Could not find coordinates for city '{city_name}'")

    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    if not timezone:
        raise ValueError(f"Could not determine timezone for '{city_name}'")

    return location.latitude, location.longitude, timezone

# Get planets visible tonight between sunset and sunrise
def find_visible_planets(lat, lon, tz_str, date=None):
    ts = load.timescale()
    planets = load('de440.bsp')
    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    timezone = pytz.timezone(tz_str)

    now = datetime.now(timezone) if not date else date

    # Get sunset/sunrise for the date
    city = LocationInfo(latitude=lat, longitude=lon, timezone=tz_str)
    s = sun(city.observer, date=now.date(), tzinfo=timezone)
    sunset = s["sunset"]
    sunrise = s["sunrise"] + timedelta(days=1)  # Next morning

    # Prepare time intervals between sunset and sunrise
    times = []
    current_time = sunset
    while current_time < sunrise:
        times.append(ts.from_datetime(current_time))
        current_time += timedelta(minutes=15)

    visible_planets = []

    # Check each planet's altitude over the night
    for display_name, kernel_name in planet_map.items():
        planet = planets[kernel_name]
        max_alt = -90
        best_time = None
        first_visible = None
        last_visible = None

        for t in times:
            alt, _, _ = observer.at(t).observe(planet).apparent().altaz()
            alt_deg = alt.degrees
            dt = t.utc_datetime().replace(tzinfo=pytz.UTC).astimezone(timezone)

            if alt_deg > max_alt:
                max_alt = alt_deg
                best_time = dt

            if alt_deg > 10:  # Visibility threshold
                if first_visible is None:
                    first_visible = dt
                last_visible = dt

        # Only include if visible at some point above 10°
        if max_alt > 10 and first_visible and last_visible:
            visible_planets.append((display_name, max_alt, best_time, first_visible, last_visible))

    return visible_planets, sunset, sunrise, moon_phase(now)

# Look ahead up to 120 days for when a specific planet is visible between sunset and midnight
def find_next_visible_dates(lat, lon, tz_str, target_name):
    ts = load.timescale()
    planets = load('de440.bsp')
    earth = planets['earth']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    timezone = pytz.timezone(tz_str)

    kernel_name = planet_map.get(target_name.capitalize())
    if not kernel_name:
        raise ValueError(f"Invalid planet name: {target_name}")

    planet = planets[kernel_name]
    found = []

    # Check next 120 days
    for i in range(1, 121):
        date = datetime.now(timezone).date() + timedelta(days=i)
        city = LocationInfo(latitude=lat, longitude=lon, timezone=tz_str)
        s = sun(city.observer, date=date, tzinfo=timezone)
        sunset = s["sunset"]
        midnight = datetime.combine(date, datetime.min.time(), tzinfo=timezone) + timedelta(hours=22, minutes=59)

        # Sample time range between sunset and midnight
        times = []
        current_time = sunset
        while current_time < midnight:
            times.append(ts.from_datetime(current_time))
            current_time += timedelta(minutes=15)

        first_visible = None
        last_visible = None
        for t in times:
            alt, _, _ = observer.at(t).observe(planet).apparent().altaz()
            alt_deg = alt.degrees
            dt = t.utc_datetime().replace(tzinfo=pytz.UTC).astimezone(timezone)
            if alt_deg > 10:
                if first_visible is None:
                    first_visible = dt
                last_visible = dt

        # If visible, log the date and time range
        if first_visible and last_visible:
            found.append((date.strftime('%b %d'), first_visible.strftime('%I:%M %p'), last_visible.strftime('%I:%M %p')))
            if len(found) >= 5:
                break  # Limit to 5 dates

    return found

# Command-line entry point
def main():
    parser = argparse.ArgumentParser(
        description="🔭 Planet Viewer: See which planets are visible tonight!"
    )
    parser.add_argument("city", type=str, help="City name, e.g. 'New York'")
    parser.add_argument("--next-visible", type=str, help="Show next nights when a planet (e.g. 'Mars') is visible between sunset and midnight")
    args = parser.parse_args()

    try:
        lat, lon, timezone_str = get_coordinates_and_timezone(args.city)

        # Option: list next visible nights for a specific planet
        if args.next_visible:
            planet_name = args.next_visible.capitalize()
            print(f"\n🔎 Upcoming Ideal Viewing Dates for {planet_name} in {args.city}:\n")
            upcoming = find_next_visible_dates(lat, lon, timezone_str, planet_name)
            if upcoming:
                for date, start, end in upcoming:
                    print(f"  📅 {date} - Visible from {start} to {end}")
            else:
                print("  No ideal dates found in the next 120 days.")
            return

        # Default: show tonight's visibility
        planets, sunset, sunrise, moon = find_visible_planets(lat, lon, timezone_str)

        print(f"\n🌍 Location: {args.city} ({lat:.2f}, {lon:.2f})")
        print(f"🕒 Sunset: {sunset.strftime('%I:%M %p')}")
        print(f"🕒 Sunrise: {sunrise.strftime('%I:%M %p')}")
        print(f"🌙 Moon phase: {moon}")
        print("\n🔭 Visible planets tonight (above 10° altitude):\n")

        if planets:
            for name, alt, best, start, end in sorted(planets, key=lambda x: -x[1]):
                print(f"  {name:<8} - Highest Altitude: {alt:.1f}° at {best.strftime('%I:%M %p')}")
                print(f"             👁️ Visible from {start.strftime('%I:%M %p')} to {end.strftime('%I:%M %p')}\n")
        else:
            print("  No planets visible tonight above 10°.")

    except Exception as e:
        print(f"❌ Error: {e}")

# Start script
if __name__ == "__main__":
    main()
