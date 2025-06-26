These are various python scripts to look at astronomical events. It uses the skyfield.api to determine positions of astronomical positions.




## current_planet_position.py

Help Command
```{}
python current_planet_position.py --help
```
Help Output
```{}
usage: current_planet_position.py [-h] --city CITY [--planet PLANET] [--min-angle MIN_ANGLE]

Show planets visible in the night sky from a given city.

options:
  -h, --help            show this help message and exit
  --city CITY           City name (e.g. 'New York')
  --planet PLANET       Optional specific planet name
  --min-angle MIN_ANGLE
                        Minimum altitude angle in degrees (default: 10)
```

Example Command
```{}
python current_planet_position.py --city Cincinnati
```
Example Output
```{}
It is currently 🌞 Daytime at Cincinnati.

Planets in Cincinnati:
- Mercury: 4.2° alt, 65.6° az — ❌ Not Visible
- Venus: 54.7° alt, 123.7° az — ✅ Visible
- Mars: -26.7° alt, 47.6° az — ❌ Not Visible
- Jupiter: 26.0° alt, 80.2° az — ✅ Visible
- Saturn: 46.6° alt, 205.3° az — ✅ Visible
- Uranus: 52.3° alt, 109.6° az — ✅ Visible
- Neptune: 47.6° alt, 205.7° az — ✅ Visible
```

Another Example Command
```{}
python current_planet_position.py --city Cincinnati --planet Saturn
```
Another Example Output
```{}
Saturn is currently visible at altitude 46.56° and azimuth 205.51°.
```


## deep_object.py
Help Command
```{}
python deep_object.py --help
```
Help Ouput
```{}
usage: deep_object.py [-h] [--days DAYS] city

Get visible deep-sky objects and best viewing times.

positional arguments:
  city         City name (e.g., 'Cincinnati')

options:
  -h, --help   show this help message and exit
  --days DAYS  Number of days to forecast (default: 1)
```

Example Command
```{}
python deep_object.py "Cincinnati"
```
Example Output
```{}
📍 Location: Cincinnati (39.10, -84.51) | Timezone: America/New_York


🗓️  2025-06-26
   ✨ Albireo → Best time: 23:59
   ✨ Messier 8 (Lagoon Nebula) → Best time: 23:59
   ✨ NGC 6530 Cluster → Best time: 23:59
   ✨ Messier 27 (Dumbbell Nebula) → Best time: 23:59
   ✨ Messier 57 (Ring Nebula) → Best time: 23:59
   ✨ Messier 81 (Bode's Galaxy) → Best time: 21:09
   ✨ Messier 82 (Cigar Galaxy) → Best time: 21:09
   ✨ Messier 13 (Hercules Cluster) → Best time: 23:59
   ✨ Double Cluster (h & χ Persei) → Best time: 23:59
```


## planet_viewer.py

Help Command
```{}
python planet_viewer.py --help
```
Help Output
```{}
usage: planet_viewer.py [-h] [--next-visible NEXT_VISIBLE] city

🔭 Planet Viewer: See which planets are visible tonight!

positional arguments:
  city                  City name, e.g. 'New York'

options:
  -h, --help            show this help message and exit
  --next-visible NEXT_VISIBLE
                        Show next nights when a planet (e.g. 'Mars') is visible between sunset and midnight
```



Example Command
```{}
python planet_viewer.py "Cincinnati"
```
Example Output
```{}
🌍 Location: Cincinnati (39.10, -84.51)
🕒 Sunset: 09:07 PM
🕒 Sunrise: 06:14 AM
🌙 Moon phase: New Moon

🔭 Visible planets tonight (above 10° altitude):

  Neptune  - Highest Altitude: 46.8° at 06:07 AM
             👁️ Visible from 02:22 AM to 06:07 AM

  Saturn   - Highest Altitude: 45.9° at 06:07 AM
             👁️ Visible from 02:22 AM to 06:07 AM

  Mars     - Highest Altitude: 37.1° at 09:07 PM
             👁️ Visible from 09:07 PM to 11:22 PM

  Venus    - Highest Altitude: 27.4° at 06:07 AM
             👁️ Visible from 04:37 AM to 06:07 AM

  Uranus   - Highest Altitude: 24.4° at 06:07 AM
             👁️ Visible from 04:52 AM to 06:07 AM

  Mercury  - Highest Altitude: 16.9° at 09:07 PM
             👁️ Visible from 09:07 PM to 09:37 PM
```
Another Example Command
```{}
python planet_viewer.py "Cincinnati" --next-visible Saturn
```
Another Example Output
```{}
🔎 Upcoming Ideal Viewing Dates for Saturn in Cincinnati:

  📅 Aug 05 - Visible from 11:44 PM to 11:44 PM
  📅 Aug 06 - Visible from 11:43 PM to 11:43 PM
  📅 Aug 07 - Visible from 11:42 PM to 11:42 PM
  📅 Aug 08 - Visible from 11:41 PM to 11:41 PM
  📅 Aug 09 - Visible from 11:40 PM to 11:40 PM
```

## sun_directions.py

Help Command
```{}
python sun_directions.py --help
```
Help Output
```{}
usage: sun_directions.py [-h] [--sort] city

Sun directions for 1st day of each month and solstices/equinoxes.

positional arguments:
  city        City name (e.g., 'Cincinnati, OH')

options:
  -h, --help  show this help message and exit
  --sort      Print all sunrises first, then all sunsets
```
Example Command
```{}
python sun_directions.py "Cincinnati"
```
Example Output
```{}
Location: Cincinnati (39.10, -84.51)

Event            Date       | Azimuth    | Altitude   | Dir
Sunrise 01       2025-01-01 | Azimuth: 119.39° | Altitude:  -0.83° | Dir: ESE
Sunset 01        2025-01-01 | Azimuth: 240.66° | Altitude:  -0.83° | Dir: WSW
Sunrise 02       2025-02-01 | Azimuth: 111.33° | Altitude:  -0.83° | Dir: ESE
Sunset 02        2025-02-01 | Azimuth: 248.84° | Altitude:  -0.83° | Dir: WSW
Sunrise 03       2025-03-01 | Azimuth:  98.85° | Altitude:  -0.83° | Dir: E
Sunset 03        2025-03-01 | Azimuth: 261.39° | Altitude:  -0.83° | Dir: W
Sunrise 04       2025-04-01 | Azimuth:  83.21° | Altitude:  -0.83° | Dir: E
Sunset 04        2025-04-01 | Azimuth: 276.55° | Altitude:  -0.83° | Dir: W
Sunrise 05       2025-05-01 | Azimuth:  69.50° | Altitude:  -0.83° | Dir: ENE
Sunset 05        2025-05-01 | Azimuth: 290.33° | Altitude:  -0.83° | Dir: WNW
Sunrise 06       2025-06-01 | Azimuth:  60.20° | Altitude:  -0.83° | Dir: ENE
Sunset 06        2025-06-01 | Azimuth: 299.73° | Altitude:  -0.83° | Dir: WNW
Sunrise 07       2025-07-01 | Azimuth:  58.88° | Altitude:  -0.83° | Dir: ENE
Sunset 07        2025-07-01 | Azimuth: 301.16° | Altitude:  -0.83° | Dir: WNW
Sunrise 08       2025-08-01 | Azimuth:  65.94° | Altitude:  -0.83° | Dir: ENE
Sunset 08        2025-08-01 | Azimuth: 294.20° | Altitude:  -0.83° | Dir: WNW
Sunrise 09       2025-09-01 | Azimuth:  78.86° | Altitude:  -0.83° | Dir: E
Sunset 09        2025-09-01 | Azimuth: 281.35° | Altitude:  -0.83° | Dir: WNW
Sunrise 10       2025-10-01 | Azimuth:  93.70° | Altitude:  -0.83° | Dir: E
Sunset 10        2025-10-01 | Azimuth: 266.06° | Altitude:  -0.83° | Dir: W
Sunrise 11       2025-11-01 | Azimuth: 108.24° | Altitude:  -0.83° | Dir: ESE
Sunset 11        2025-11-01 | Azimuth: 251.57° | Altitude:  -0.83° | Dir: WSW
Sunrise 12       2025-12-01 | Azimuth: 117.94° | Altitude:  -0.83° | Dir: ESE
Sunset 12        2025-12-01 | Azimuth: 241.98° | Altitude:  -0.83° | Dir: WSW

Seasonal Events:
Spring Equinox   2025-03-20 | Azimuth:  61.27° | Altitude: -30.60° | Dir: ENE
Summer Solstice  2025-06-20 | Azimuth: 318.37° | Altitude: -14.95° | Dir: NW
Autumn Equinox   2025-09-22 | Azimuth: 198.90° | Altitude:  49.33° | Dir: SSW
Winter Solstice  2025-12-21 | Azimuth: 143.29° | Altitude:  17.93° | Dir: SE
```




## sun_moon_events.py

Help Command
```{}
python sun_moon_events.py --help
```

Help Output

```{}
usage: sun_moon_events.py [-h] city

Next Sun or Moon Rise/Set Info

positional arguments:
  city        City name (e.g. 'Cincinnati, OH')

options:
  -h, --help  show this help message and exit
```


Example Command
```{}
python sun_moon_events.py "Cincinnati"
```
Example Output
```{}
Resolved location: Cincinnati, Hamilton County, Ohio, United States
City: Cincinnati
Next event: Sunset of the Sun
Time: 2025-06-26 21:06:30 EDT
Azimuth: 301.20° (NW)
Altitude at event: -0.57°
```









