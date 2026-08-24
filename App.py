import urllib.parse
import requests

# 1. Set the city name
city_name = "New York"

# 2. Fake a browser identity so the server doesn't block Google Colab
headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
}

# 3. Safely encode the city name for the web URL
safe_city = urllib.parse.quote(city_name)

# 4. Step 1 URL: Find the coordinates
geo_base = "https://open-meteo.com"
geo_params = f"?name={safe_city}&count=1&language=en&format=json"
geo_url = geo_base + geo_params

# Fetch coordinates with browser identity headers
geo_response = requests.get(geo_url, headers=headers)

if geo_response.status_code == 200:
    try:
        geo_data = geo_response.json()
        
        if "results" in geo_data and len(geo_data["results"]) > 0:
            first_city = geo_data["results"][0]
            lat = first_city["latitude"]
            lon = first_city["longitude"]
            
            # 5. Step 2 URL: Get the Air Quality
            aqi_base = "https://open-meteo.com"
            aqi_params = f"?latitude={lat}&longitude={lon}&current=us_aqi"
            aqi_url = aqi_base + aqi_params
            
            # Fetch AQI data
            aqi_response = requests.get(aqi_url, headers=headers).json()
            current_aqi = aqi_response["current"]["us_aqi"]
            
            print(f"Success! The current AQI in {city_name} is: {current_aqi}")
            
            # 6. Basic Alert Threshold logic
            if current_aqi > 100:
                print("🚨 ALERT: Air quality is unhealthy! Avoid prolonged outdoor activity.")
            elif current_aqi > 50:
                print("⚠️ Notice: Air quality is moderate.")
            else:
                print("✅ Clean Air: Air quality is good today!")
                
        else:
            print(f"Could not find any city named '{city_name}'. Check your spelling.")
    except ValueError:
        print("Error: The server sent back a broken webpage text instead of data. The website might be busy.")
else:
    print(f"Could not connect to the location service. (Status Code: {geo_response.status_code})")
