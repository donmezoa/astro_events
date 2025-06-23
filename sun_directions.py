import argparse
from datetime import datetime, timedelta
from skyfield.api import load, Topos
from skyfield import almanac
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="sun_direction_locator")
    location = geolocator.geocode(city_name)
    if not location:
        raise ValueError(f"Could not find coordinates for city: {city_name}")
    return location.latitude, location.longitude

def get_timezone(lat, lon):
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    return pytz.timezone(tz_name)

def azimuth_to_compass(azimuth):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    index = round(azimuth / 22.5) % 16
    return directions[index]

def print_event(label, dt, az, alt):
    compass = azimuth_to_compass(az)
    print(f"{label:<16} {dt:%Y-%m-%d} | Azimuth: {az:6.2f}° | Altitude: {alt:6.2f}° | Dir: {compass}")

def sun_az_alt(lat, lon, ts, eph, time):
    sun = eph['Sun']
    earth = eph['earth']
    observer = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    astrometric = observer.at(time).observe(sun).apparent()
    alt, az, _ = astrometric.altaz()
    return az.degrees, alt.degrees

def find_sunrise_sunset(observer, ts, eph, dt, timezone):
    t0 = ts.utc(dt.year, dt.month, dt.day)
    t1 = ts.utc(dt.year, dt.month, dt.day + 1)
    f = almanac.sunrise_sunset(eph, observer)
    times, events = almanac.find_discrete(t0, t1, f)

    sun_times = {}
    for t, event in zip(times, events):
        local_time = t.astimezone(timezone)
        az, alt = sun_az_alt(observer.latitude.degrees, observer.longitude.degrees, ts, eph, t)
        event_type = 'Sunrise' if event == 1 else 'Sunset'
        sun_times[event_type] = (local_time.strftime("%H:%M:%S"), az, alt)
    return sun_times

def main(city, sort):
    lat, lon = get_coordinates(city)
    tz = get_timezone(lat, lon)

    eph = load('de421.bsp')
    ts = load.timescale()
    observer = Topos(latitude_degrees=lat, longitude_degrees=lon)

    print(f"Location: {city} ({lat:.2f}, {lon:.2f})\n")
    print(f"{'Event':<16} {'Date':<10} | Azimuth    | Altitude   | Dir")

    sunrise_events = []
    sunset_events = []

    for month in range(1, 13):
        dt = datetime(datetime.now().year, month, 1, tzinfo=tz)
        events = find_sunrise_sunset(observer, ts, eph, dt, tz)
        
        if 'Sunrise' in events:
            time_str, az, alt = events['Sunrise']
            hour, minute, second = map(int, time_str.split(":"))
            event_time = datetime(dt.year, dt.month, dt.day, hour, minute, second, tzinfo=tz)
            sunrise_events.append(('Sunrise', event_time, az, alt, month))
        
        if 'Sunset' in events:
            time_str, az, alt = events['Sunset']
            hour, minute, second = map(int, time_str.split(":"))
            event_time = datetime(dt.year, dt.month, dt.day, hour, minute, second, tzinfo=tz)
            sunset_events.append(('Sunset', event_time, az, alt, month))

    if sort:
        # Print all sunrises first
        for label, event_time, az, alt, month in sunrise_events:
            print_event(f"{label} {month:02}", event_time, az, alt)
        # Then all sunsets
        for label, event_time, az, alt, month in sunset_events:
            print_event(f"{label} {month:02}", event_time, az, alt)
    else:
        # Interleave sunrise/sunset by month
        for month in range(1, 13):
            sr = next((e for e in sunrise_events if e[4] == month), None)
            ss = next((e for e in sunset_events if e[4] == month), None)
            if sr:
                label, event_time, az, alt, _ = sr
                print_event(f"{label} {month:02}", event_time, az, alt)
            if ss:
                label, event_time, az, alt, _ = ss
                print_event(f"{label} {month:02}", event_time, az, alt)

    # Solstices and Equinoxes
    print("\nSeasonal Events:")
    f = almanac.seasons(eph)
    t0 = ts.utc(datetime.now().year, 1, 1)
    t1 = ts.utc(datetime.now().year + 1, 1, 1)
    times, events = almanac.find_discrete(t0, t1, f)
    season_names = ['Spring Equinox', 'Summer Solstice', 'Autumn Equinox', 'Winter Solstice']

    for t, e in zip(times, events):
        local_dt = t.astimezone(tz)
        az, alt = sun_az_alt(lat, lon, ts, eph, t)
        print_event(season_names[e], local_dt, az, alt)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sun directions for 1st day of each month and solstices/equinoxes.")
    parser.add_argument("city", help="City name (e.g., 'Cincinnati, OH')")
    parser.add_argument("--sort", action="store_true", help="Print all sunrises first, then all sunsets")
    args = parser.parse_args()
    main(args.city, args.sort)
