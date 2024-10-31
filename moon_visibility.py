import ephem
import datetime
# from datetime import datetime, timezone, timedelta
import math
from datetime import timezone
from cls_target import Target


def setup_observer(location_lat, location_lon, location_elevation, date_time):
    observer = ephem.Observer()
    observer.lat = str(location_lat)
    observer.long = str(location_lon)
    observer.elevation = location_elevation
    observer.date = date_time

    return observer


def get_moon_illumination(observer):

    # Get the moon object
    moon = ephem.Moon(observer)

    # Calculate moon phase percentage
    moon_phase = int(moon.phase)

    return moon_phase


def calculate_angular_distance(observer, target):

    # Get the Moon's current position
    moon = ephem.Moon(observer)
    print(f'moon ra: {moon.ra}')
    print(f'moon dec: {moon.dec}')
    # Convert Moon's RA and Dec to degrees
    moon_ra = math.degrees(moon.ra)
    moon_dec = math.degrees(moon.dec)
    print(f'moon_ra: {moon_ra}')
    print(f'moon_dec: {moon_dec}')

    # Convert target RA and Dec to degrees (if not already)
    target_ra_deg = target.ra  # Assuming target RA is already in degrees
    target_dec_deg = target.dec  # Assuming target Dec is already in degrees

    # Use the spherical law of cosines to calculate angular separation
    ra_diff = math.radians(moon_ra - target_ra_deg)
    moon_dec_rad = math.radians(moon_dec)
    target_dec_rad = math.radians(target_dec_deg)

    # Formula for angular separation in degrees
    angle = math.acos(
        math.sin(moon_dec_rad) * math.sin(target_dec_rad) +
        math.cos(moon_dec_rad) * math.cos(target_dec_rad) * math.cos(ra_diff)
    )

    # Convert angle from radians to degrees
    angular_distance = "{:.4f}".format(math.degrees(angle))

    return angular_distance


def is_moon_above_horizon(observer):

    if observer.date is None:
        print('appears no date was supplied')
        observer.date = datetime.datetime.now(timezone.utc)

    # Get the Moon's current position
    moon = ephem.Moon(observer)

    # Get the Moon's altitude (in degrees)
    moon_altitude = moon.alt

    # Check if the Moon is above the horizon
    is_above = moon_altitude > 0  # True if altitude is positive (above horizon)
    degrees_total = math.degrees(moon_altitude)

    return is_above, degrees_total


# NOTE!!! ensure the datetime is calculated from the earliest , middle or latest date time of the set of fits subs

observer_properties = setup_observer(43.379444, -79.8147, 100, datetime.datetime.now(timezone.utc))

print(f'observer_properties.lat is : {observer_properties.lat}')
print(f'observer_properties.long is : {observer_properties.lon}')
print(f'observer_properties.elevation is : {observer_properties.elevation:.0f} meters')
print(f'observer_properties.date is : {observer_properties.date}')

# Call the function to check if the Moon is above the horizon returning status and degrees
moon_status, moon_altitude_degrees = is_moon_above_horizon(observer_properties)

target_1 = Target('TCrb', 240.27084, 25.903056)  # these values to be pulled from fit header

if moon_status:
    moon_status = 'above'
    # Moon is currently up at location above and local location time
    # Call function to calculate angular distance between moon and target(get from fit file target coordinates)
    angular_separation = calculate_angular_distance(observer_properties, target_1)
    # Call the function to get the illumination percent of the moon
    illumination = get_moon_illumination(observer_properties)
    print(f"The Moon illumination of {illumination}% is {moon_status} the horizon. Current altitude: {moon_altitude_degrees:.4f}° with angular separation of {angular_separation} degrees")
else:
    moon_status = 'below'
    angular_separation = calculate_angular_distance(observer_properties, target_1)
    illumination = get_moon_illumination(observer_properties)
    print(f"The Moon illumination of {illumination}% is {moon_status} the horizon. Current altitude: {moon_altitude_degrees:.4f}° with angular separation of {angular_separation}°")
