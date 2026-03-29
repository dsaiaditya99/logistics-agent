import streamlit as st
import random
import requests
import folium
from streamlit_folium import st_folium
from geocode import get_coordinates
from ors_maps import get_route_ors

st.set_page_config(layout="wide")
st.title("🚚 AI Logistics Optimization Agent")

# -------------------------------
# SESSION STATE
# -------------------------------
if "response" not in st.session_state:
    st.session_state.response = None

if "locations" not in st.session_state:
    st.session_state.locations = []

if "places" not in st.session_state:
    st.session_state.places = []

# -------------------------------
# INPUT: LOCATIONS
# -------------------------------
user_input = st.text_input(
    "Enter locations (comma separated)",
    placeholder="Guntur, Chennai"
)

if user_input:
    temp_locations = []
    temp_places = []

    places = user_input.split(",")

    for place in places:
        place = place.strip()

        if not place:
            continue

        coords = get_coordinates(place)

        if coords:
            temp_locations.append(coords)
            temp_places.append(place)
        else:
            st.warning(f"❌ Could not find: {place}")

    if temp_locations:
        st.session_state.locations = temp_locations
        st.session_state.places = temp_places

# Show valid places
if st.session_state.places:
    st.success(f"✅ Locations detected: {', '.join(st.session_state.places)}")

# -------------------------------
# QUERY
# -------------------------------
query = st.text_input("Ask something (e.g., Optimize route)")

# -------------------------------
# BUTTON
# -------------------------------
if st.button("Run Agent"):

    if len(st.session_state.locations) < 2:
        st.error("❌ Please enter at least 2 valid locations")
        st.stop()

    try:
        res = requests.post(
            "https://logistics-agent-cerf.onrender.com/ask",
            json={
                "query": query,
                "locations": st.session_state.locations
            }
        )

        if res.status_code == 200:
            st.session_state.response = res.json()
        else:
            st.error("Backend error: " + res.text)

    except requests.exceptions.ConnectionError:
        st.error("🚨 Backend not running")

# -------------------------------
# DISPLAY
# -------------------------------
if st.session_state.response:

    data = st.session_state.response

    st.write("### 🤖 Agent Response")
    st.write(data)

    if "route" in str(data):

        route = data["response"]["route"]

        locations = st.session_state.locations
        places = st.session_state.places

        # -------------------------------
        # MAP CENTER
        # -------------------------------
        avg_lat = sum(loc[0] for loc in locations) / len(locations)
        avg_lon = sum(loc[1] for loc in locations) / len(locations)

        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

        # -------------------------------
        # MARKERS
        # -------------------------------
        for i, loc in enumerate(locations):
            color = "green" if i == 0 else "red" if i == len(locations)-1 else "blue"

            folium.Marker(
                location=loc,
                popup=places[i],
                icon=folium.Icon(color=color)
            ).add_to(m)

        # -------------------------------
        # ROUTE DRAWING (REAL ROADS)
        # -------------------------------
        ordered_locations = [locations[i] for i in route]

        for i in range(len(ordered_locations) - 1):

            # Convert to ORS format (lon, lat)
            segment = [
                [ordered_locations[i][1], ordered_locations[i][0]],
                [ordered_locations[i+1][1], ordered_locations[i+1][0]]
            ]

            route_coords = get_route_ors(segment)

            if route_coords:

                # Convert back to (lat, lon)
                route_coords = [[lat, lon] for lon, lat in route_coords]

                # Simulated traffic
                traffic = random.choice(["low", "medium", "high"])

                color = "green" if traffic == "low" else "orange" if traffic == "medium" else "red"

                folium.PolyLine(
                    route_coords,
                    weight=6,
                    color=color,
                    opacity=0.8
                ).add_to(m)

            else:
                # fallback line
                folium.PolyLine(
                    [ordered_locations[i], ordered_locations[i+1]],
                    weight=3,
                    color="gray",
                    dash_array="5"
                ).add_to(m)

        # -------------------------------
        # DISPLAY MAP
        # -------------------------------
        st.write("### 🗺️ Optimized Route Map")
        st_folium(m, width=900, height=500)

        # -------------------------------
        # LEGEND
        # -------------------------------
        st.markdown("""
        ### 🚦 Traffic Legend
        - 🟢 Green → Low Traffic  
        - 🟡 Orange → Moderate Traffic  
        - 🔴 Red → Heavy Traffic  
        """)