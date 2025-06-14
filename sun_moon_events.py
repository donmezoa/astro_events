from skyfield.api import load, Topos
from skyfield.almanac import find_discrete, risings_and_settings
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta, timezone
import pytz
import math

# Compass direction from azimuth degrees
def azimuth_to_compass(azimuth):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = round(azimuth / 45) % 8
    return directions[index]

# Get lat, lon, and timezone from city name
def get_location_info(city_name):
    geolocator = Nominatim(user_agent="astro_locator")
    location = geolocator.geocode(city_name, exactly_one=True)
    if location is None:
        raise ValueError(f"City '{city_name}' not found.")
    lat, lon = location.latitude, location.longitude
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    timezone = pytz.timezone(timezone_str)
    print(f"Resolved location: {location.address}")
    return lat, lon, timezone

# Main logic
def main(city):
    ts = load.timescale()
    eph = load('de421.bsp')

    lat, lon, tz = get_location_info(city)
    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)

    t0 = ts.now()
    t1 = ts.utc(datetime.now(timezone.utc) + timedelta(days=1))

    f_sun = risings_and_settings(eph, eph['Sun'], observer)
    f_moon = risings_and_settings(eph, eph['Moon'], observer)

    times_sun, events_sun = find_discrete(t0, t1, f_sun)
    times_moon, events_moon = find_discrete(t0, t1, f_moon)

    events = []

    for t, e in zip(times_sun, events_sun):
        kind = 'sunrise' if e else 'sunset'
        events.append((t.utc_datetime(), kind, 'Sun'))

    for t, e in zip(times_moon, events_moon):
        kind = 'moonrise' if e else 'moonset'
        events.append((t.utc_datetime(), kind, 'Moon'))

    # Sort all events and find the next one
    now = datetime.now(timezone.utc)
    next_event = min((e for e in events if e[0] > now), key=lambda x: x[0])

    event_time_utc, kind, body_name = next_event
    event_time_local = event_time_utc.astimezone(tz)

    # Calculate azimuth at that moment
    location = eph['earth'] + observer
    t_event = ts.utc(event_time_utc)
    astrometric = location.at(t_event).observe(eph[body_name])
    alt, az, _ = astrometric.apparent().altaz()

    compass_dir = azimuth_to_compass(az.degrees)

    print(f"City: {city}")
    print(f"Next event: {kind.capitalize()} of the {body_name}")
    print(f"Time: {event_time_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"Azimuth: {az.degrees:.2f}° ({compass_dir})")
    print(f"Altitude at event: {alt.degrees:.2f}°")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Next Sun or Moon Rise/Set Info")
    parser.add_argument("city", help="City name (e.g. 'Cincinnati, OH')")
    args = parser.parse_args()
    main(args.city)

