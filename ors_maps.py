import requests

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjBkNjA0NzEyNDliNzRkYzk5MDM0YzJkZTE0N2QzN2VmIiwiaCI6Im11cm11cjY0In0="

def get_route_ors(coordinates):
    """
    coordinates format:
    [[lon, lat], [lon, lat]]
    """

    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": coordinates
    }

    try:
        response = requests.post(url, json=body, headers=headers)

        if response.status_code != 200:
            print("ORS ERROR:", response.text)  # 🔥 DEBUG
            return None

        data = response.json()

        coords = data["features"][0]["geometry"]["coordinates"]

        return coords  # [[lon, lat], ...]

    except Exception as e:
        print("EXCEPTION:", str(e))
        return None