import urllib.parse
import requests
import streamlit as st

# 1. App Title and UI Elements
st.title("🌍 Live Air Quality Monitor")
st.write("Check the real-time air quality index (AQI) for any city.")

# Creates a text entry box that defaults to "New York"
city_name = st.text_input("Enter a city name:", "New York")

# 2. Add the browser identity header that worked on your iPad
headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
}

# 3. Clean up the city name string for web addresses
safe_city = urllib.parse.quote(city_name)

# 4. Use your exact working URL format to find coordinates
geo_base = "https://open-meteo.com"
geo_params = f"?name={safe_city}&count=1&language=en&format=json"
geo_url = geo_base + geo_params

# Run code when the user clicks the button
if st.button("Check Air Quality"):
    geo_response = requests.get(geo_url, headers=headers)
    
    if geo_response.status_code == 200:
        try:
            geo_data = geo_response.json()
            
            if "results" in geo_data and len(geo_data["results"]) > 0:
                first_city = geo_data["results"][0]
                lat = first_city["latitude"]
                lon = first_city["longitude"]
                
                # 5. Use your exact working URL format to get the Air Quality
                aqi_base = "https://open-meteo.com"
                aqi_params = f"?latitude={lat}&longitude={lon}&current=us_aqi"
                aqi_url = aqi_base + aqi_params
                
                # Fetch AQI data
                aqi_response = requests.get(aqi_url, headers=headers).json()
                current_aqi = aqi_response["current"]["us_aqi"]
                
                # 6. Streamlit Visual Outputs (Replaces print statements)
                st.metric(label=f"Current US AQI in {city_name}", value=current_aqi)
                
                # Threshold Alerts
                if current_aqi > 100:
                    st.error("🚨 ALERT: Air quality is unhealthy! Avoid prolonged outdoor activity.")
                elif current_aqi > 50:
                    st.warning("⚠️ Notice: Air quality is moderate.")
                else:
                    st.success("✅ Clean Air: Air quality is good today!")
                    
            else:
                st.error(f"Could not find any city named '{city_name}'. Check your spelling.")
        except ValueError:
            st.error("The server sent back a broken webpage text instead of data.")
    else:
        st.error(f"Could not connect to the location service. (Status Code: {geo_response.status_code})")
