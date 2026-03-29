from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="logistics-agent")

def get_coordinates(place):
    try:
        location = geolocator.geocode(place)

        if location:
            return [location.latitude, location.longitude]

        return None

    except Exception as e:
        return None