import argparse
from skyfield.api import load, Topos, Star, utc, wgs84
from skyfield.data import hipparcos
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta, time
import pytz
import numpy as np

# Define known Deep Sky Objects (DSOs) with approximate RA/Dec (J2000)
deep_sky_objects = {
    "Albireo": (292.680, 27.963),
    "Messier 8 (Lagoon Nebula)": (270.925, -24.375),
    "NGC 6530 Cluster": (271.075, -24.35),
    "Messier 27 (Dumbbell Nebula)": (299.9, 22.72),
    "Messier 57 (Ring Nebula)": (283.396, 33.03),
    "Messier 81 (Bode's Galaxy)": (148.888, 69.065),
    "Messier 82 (Cigar Galaxy)": (149.0, 69.7),
    "Messier 13 (Hercules Cluster)": (250.421, 36.460),
    "Messier 31 (Andromeda Galaxy)": (10.684, 41.269),
    "Double Cluster (h & χ Persei)": (37.708, 57.137),
    "Messier 45 (Pleiades)": (56.75, 24.1167),
    "Messier 42 (Orion Nebula)": (83.822, -5.391),
}

def parse_args():
    parser = argparse.ArgumentParser(description="Get visible deep-sky objects and best viewing times.")
    parser.add_argument("city", help="City name (e.g., 'Cincinnati')")
    parser.add_argument("--days", type=int, default=1, help="Number of days to forecast (default: 1)")
    return parser.parse_args()

def get_location(city_name):
    geolocator = Nominatim(user_agent="deep_object_locator")
    location = geolocator.geocode(city_name)
    if not location:
        raise ValueError(f"Could not find location for city: {city_name}")
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
    timezone = pytz.timezone(timezone_str)
    return location.latitude, location.longitude, timezone

def is_object_visible(obj, observer, ts, start_time, end_time, threshold_degrees=10):
    # Create an array of evenly spaced times between start and end
    time_range = [start_time + (end_time - start_time) * i / 19 for i in range(20)]
    times = ts.utc(time_range)
    
    # Calculate altitudes
    altitudes = observer.at(times).observe(obj).apparent().altaz()[0].degrees

    # Determine if it's ever visible and when it's best (max altitude)
    if np.any(altitudes > threshold_degrees):
        best_idx = np.argmax(altitudes)
        return True, times[best_idx].utc_datetime()
    else:
        return False, None

def main():
    args = parse_args()

    # Load timescale and ephemeris
    ts = load.timescale()

    # Get observer's location
    try:
        latitude, longitude, timezone = get_location(args.city)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    observer_location = wgs84.latlon(latitude, longitude)

    print(f"\n📍 Location: {args.city} ({latitude:.2f}, {longitude:.2f}) | Timezone: {timezone.zone}\n")

    now_local = datetime.now(timezone)
    eph = load('de440s.bsp')  # Needed for Earth/Sun
    earth = eph["earth"]
    sun = eph["sun"]

    for day_offset in range(args.days):
        day = now_local + timedelta(days=day_offset)
        date_str = day.strftime("%Y-%m-%d")
        print(f"\n🗓️  {date_str}")

        # Define local sunset and midnight
        t0 = timezone.localize(datetime.combine(day.date(), time(12)))
        t_ts = ts.from_datetime(t0)
        observer = earth + observer_location
        sunset_time = observer.at(t_ts).observe(sun).apparent().altaz()[0].degrees
        sunset = None
        for minute in range(1440):
            dt = t0 + timedelta(minutes=minute)
            t = ts.from_datetime(dt)
            alt = observer.at(t).observe(sun).apparent().altaz()[0].degrees
            if alt < -0.833:
                sunset = dt
                break
        if sunset is None:
            print("☀️  No sunset found!")
            continue

        midnight = timezone.localize(datetime.combine(day.date(), time(23, 59)))

        # Check visibility of each DSO
        for name, (ra, dec) in deep_sky_objects.items():
            star = Star(ra_hours=ra / 15.0, dec_degrees=dec)
            # Convert sunset and midnight to UTC naive datetimes
            sunset_utc = sunset.astimezone(utc)
            midnight_utc = midnight.astimezone(utc)

            visible, best_time = is_object_visible(star, observer, ts, sunset_utc, midnight_utc)
            if visible:
                best_time_local = best_time.astimezone(timezone).strftime("%H:%M")
                print(f"   ✨ {name} → Best time: {best_time_local}")

if __name__ == "__main__":
    main()

