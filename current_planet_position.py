import argparse
from skyfield.api import load, Topos
from datetime import datetime
from geopy.geocoders import Nominatim

# Load ephemeris and planet data
eph = load('de421.bsp')
planets = eph
ts = load.timescale()

planet_names = {
    'Mercury': planets['mercury'],
    'Venus': planets['venus'],
    'Mars': planets['mars'],
    'Jupiter': planets['jupiter barycenter'],
    'Saturn': planets['saturn barycenter'],
    'Uranus': planets['uranus barycenter'],
    'Neptune': planets['neptune barycenter']
}

def get_observer(city_name):
    """Returns a Skyfield Topos object for a city name using geopy."""
    geolocator = Nominatim(user_agent="planet_viewer")
    location = geolocator.geocode(city_name)
    if not location:
        raise ValueError("Could not find the specified city.")
    return Topos(latitude_degrees=location.latitude, longitude_degrees=location.longitude)

def check_single_planet(observer, ts, planet_name, min_angle):
    """Check visibility of a single planet."""
    name = planet_name.capitalize()
    if name not in planet_names:
        raise ValueError(f"Unknown planet: {name}")
    planet = planet_names[name]
    now = ts.now()
    astrometric = (planets['earth'] + observer).at(now).observe(planet)
    alt, az, distance = astrometric.apparent().altaz()
    return (alt.degrees > min_angle, alt.degrees, az.degrees)

def get_visible_planets(observer, ts, min_angle):
    """Return a list of currently visible planets above the altitude threshold."""
    visible = []
    now = ts.now()
    for name, planet in planet_names.items():
        astrometric = (planets['earth'] + observer).at(now).observe(planet)
        alt, az, distance = astrometric.apparent().altaz()
        if alt.degrees > min_angle:
            visible.append((name, alt.degrees, az.degrees))
    return visible


def main():
    parser = argparse.ArgumentParser(description="Show planets visible in the night sky from a given city.")
    parser.add_argument('--city', type=str, required=True, help="City name (e.g. 'New York')")
    parser.add_argument('--planet', type=str, help="Optional specific planet name")
    parser.add_argument('--min-angle', type=float, default=10,
                        help="Minimum altitude angle in degrees (default: 10)")
    args = parser.parse_args()

    try:
        observer = get_observer(args.city)
    except ValueError as e:
        print(e)
        return

    if args.planet and args.planet.lower() != 'all':
        try:
            visible, alt, az = check_single_planet(observer, ts, args.planet, args.min_angle)
            if visible:
                print(f"{args.planet.capitalize()} is currently visible at altitude {alt:.2f}° and azimuth {az:.2f}°.")
            else:
                print(f"{args.planet.capitalize()} is currently below {args.min_angle}° altitude and likely not visible.")
        except ValueError as e:
            print(e)
    else:
        now = ts.now()
        # Sun position to determine day/night
        sun = planets['sun']
        astrometric_sun = (planets['earth'] + observer).at(now).observe(sun)
        alt_sun, _, _ = astrometric_sun.apparent().altaz()
        is_daytime = alt_sun.degrees > 0

        print(f"It is currently {'🌞 Daytime' if is_daytime else '🌙 Nighttime'} at {args.city}.\n")
        print(f"Planets in {args.city}:")

        for name, planet in planet_names.items():
            astrometric = (planets['earth'] + observer).at(now).observe(planet)
            alt, az, _ = astrometric.apparent().altaz()
            is_visible = alt.degrees > args.min_angle
            status = "✅ Visible" if is_visible else "❌ Not Visible"
            print(f"- {name}: {alt.degrees:.1f}° alt, {az.degrees:.1f}° az — {status}")


if __name__ == "__main__":
    main()
