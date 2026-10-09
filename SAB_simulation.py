import os
import json
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------
# SYSTEMATIC AUTOMATE BARRIER (SAB) CONFIGURATION & THREAT CONSTANTS
# ---------------------------------------------------------------------
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"         # Normal / Operational
COLOR_YELLOW = "\033[93m"        # Moderate Risk
COLOR_ORANGE = "\033[38;5;208m"  # High Risk
COLOR_RED = "\033[91m"           # Critical Threat

SAB_CONFIG = {
    "1": {
        "name": "Rain & Storm Mitigation",
        "power_coeff": 0.45,
        "water_coeff": 12.5,
        "transparency": 40,
        "high_threshold": 7.5,
        "high_protocol": "TRIGGERED: Cloud Redirection & Flood Diversion Active",
        "low_protocol": "TRIGGERED: Local Reservoir Rain Harvesting Active",
    },
    "2": {
        "name": "Extreme Heat & UV Harvesting",
        "power_coeff": 0.85,
        "water_coeff": 1.8,
        "transparency": 75,
        "high_threshold": 8.0,
        "high_protocol": "TRIGGERED: Micro-Climate Shading & EV Grid Off-loading Active",
        "low_protocol": "TRIGGERED: Atmospheric Moisture Condensation Active",
    },
    "3": {
        "name": "Normal Monitoring State",
        "power_coeff": 0.05,
        "water_coeff": 0.2,
        "transparency": 95,
        "high_threshold": 10.0,
        "high_protocol": "Standby Operations",
        "low_protocol": "Standby Operations",
    },
}

def clear_screen():
    """Clears terminal screen for clean cross-platform interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------------------------------------------------------------------
# 1. HIERARCHICAL ADMINISTRATIVE GEO-SPATIAL RESOLVER
# ---------------------------------------------------------------------
def fetch_location_geo_and_area(city_name: str, province_state: str, country_name: str):
    params = {
        "city": city_name,
        "state": province_state,
        "country": country_name,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    encoded_params = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    url = f"https://nominatim.openstreetmap.org/search?{encoded_params}"

    headers = {"User-Agent": "Systematic-Automate-Barrier-Enterprise/4.4"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            if not data:
                query_str = f"{city_name}, {province_state}, {country_name}".strip(", ")
                fallback_url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query_str)}&format=json&addressdetails=1&limit=1"
                req_fallback = urllib.request.Request(fallback_url, headers=headers)
                with urllib.request.urlopen(req_fallback, timeout=5) as resp_fb:
                    data = json.loads(resp_fb.read().decode("utf-8"))

            if data:
                item = data[0]
                bounding_box = [float(x) for x in item["boundingbox"]]
                
                lat_diff = abs(bounding_box[1] - bounding_box[0]) * 111000.0
                lon_diff = abs(bounding_box[3] - bounding_box[2]) * 111000.0 * 0.85
                computed_area_sqm = max(lat_diff * lon_diff, 500000.0)

                address = item.get("address", {})
                country_code = address.get("country_code", "").upper()
                resolved_type = item.get("type", "location").upper()

                return {
                    "lat": float(item["lat"]),
                    "lon": float(item["lon"]),
                    "display_name": item["display_name"],
                    "country_code": country_code,
                    "resolved_type": resolved_type,
                    "computed_area_sqm": computed_area_sqm
                }
            return None
    except Exception as e:
        print(f"[API ERROR] Hierarchical geocoding lookup failed: {e}")
        return None

# ---------------------------------------------------------------------
# 2. DYNAMIC CURRENCY & REAL-TIME FX CONVERSION
# ---------------------------------------------------------------------
def get_currency_code_from_country_code(country_code_iso2: str) -> str:
    if not country_code_iso2:
        return "USD"
    
    url = f"https://restcountries.com/v3.1/alpha/{country_code_iso2}"
    req = urllib.request.Request(url, headers={"User-Agent": "Systematic-Automate-Barrier-Enterprise/4.4"})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            currencies = data[0].get("currencies", {})
            if currencies:
                return list(currencies.keys())[0]
    except Exception:
        pass
    return "USD"

def fetch_live_currency_rate(country_code_iso2: str):
    currency_code = get_currency_code_from_country_code(country_code_iso2)
    
    if currency_code == "PHP":
        return "PHP", 1.0

    url = f"https://api.frankfurter.app/latest?from={currency_code}&to=PHP"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            php_rate = data.get("rates", {}).get("PHP", 56.0)
            return currency_code, php_rate
    except Exception:
        fallback_rates = {"USD": 56.5, "EUR": 61.2, "JPY": 0.38, "GBP": 72.0, "SGD": 42.1}
        rate = fallback_rates.get(currency_code, 56.0)
        return currency_code, rate

# ---------------------------------------------------------------------
# 3. LIVE SATELLITE TELEMETRY & PROCESSING
# ---------------------------------------------------------------------
def fetch_live_satellite_telemetry(lat: float, lon: float):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current="
        f"temperature_2m,relative_humidity_2m,rain,showers,weather_code,uv_index"
    )

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("current", {})
    except Exception as e:
        print(f"[API ERROR] Satellite telemetry feed failed: {e}")
        return None

def determine_threat_color(intensity: float, weather_mode: str):
    if intensity < 4.0:
        return COLOR_GREEN, "GOOD (NORMAL STATE)"
    elif 4.0 <= intensity < 6.5:
        return COLOR_YELLOW, "MODERATE RISK"
    elif 6.5 <= intensity < 8.5:
        return COLOR_ORANGE, "HIGH RISK / VERY BAD"
    else:
        return COLOR_RED, "SEVERE DANGEROUS THREAT"

def convert_telemetry_to_sab_mode(telemetry_data: dict):
    temp_c = telemetry_data.get("temperature_2m", 25.0)
    rain_mm = telemetry_data.get("rain", 0.0) + telemetry_data.get("showers", 0.0)
    uv_index = telemetry_data.get("uv_index", 3.0)

    if rain_mm > 0.5:
        mode = "1"
        intensity = min(10.0, max(1.0, 1.0 + (rain_mm * 0.45)))
    elif temp_c > 32.0 or uv_index > 6.0:
        mode = "2"
        intensity = min(10.0, max(1.0, (temp_c - 20.0) * 0.4 + (uv_index * 0.3)))
    else:
        mode = "3"
        intensity = 2.5

    return mode, round(intensity, 2), temp_c, rain_mm, uv_index

def process_sab_logic(weather_mode: str, intensity: float, area: float) -> dict:
    cfg = SAB_CONFIG[weather_mode]
    power = area * intensity * cfg["power_coeff"]
    water = area * intensity * cfg["water_coeff"]
    transparency = cfg["transparency"]

    protocol = cfg["high_protocol"] if intensity > cfg["high_threshold"] else cfg["low_protocol"]

    return {
        "mode_name": cfg["name"],
        "transparency": transparency,
        "power_kw": power,
        "water_liters": water,
        "protocol": protocol,
    }

# ---------------------------------------------------------------------
# 4. ROBUST CONTINUATION PROMPT WITH TYPO AUTO-CORRECTION
# ---------------------------------------------------------------------
def prompt_continuation() -> bool:
    """Handles continuation prompt with typo correction and validation loop."""
    valid_yes = {"yes", "y", "yws", "ye", "ys", "sure", "ok"}
    valid_no = {"no", "n", "noo", "exit", "quit"}

    while True:
        user_input = input("Run another disambiguated scan? (yes/no): ").strip().lower()
        if user_input in valid_yes:
            return True
        elif user_input in valid_no:
            return False
        else:
            print(f"⚠️  Invalid selection ('{user_input}'). Please type 'yes' or 'no'.")

def main():
    while True:
        clear_screen()
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("=================================================================")
        print("  SYSTEMATIC AUTOMATE BARRIER (SAB) - ENTERPRISE ENGINE v4.4    ")
        print("  HIERARCHICAL ADMINISTRATIVE GEO-DISAMBIGUATION ACTIVE          ")
        print(f"  Live Timestamp: {current_time_str} UTC                         ")
        print("=================================================================")

        print("\n--- [ ENTER GEO-SPATIAL TARGET PARAMETERS ] ---")
        city = input("Enter City / District  (e.g., Dasmariñas, Springfield, London): ").strip()
        province = input("Enter Province / State (e.g., Cavite, Metro Manila, Illinois): ").strip()
        country = input("Enter Country          (e.g., Philippines, United States, UK): ").strip()

        print("\n[INITIATING HIERARCHICAL SATELLITE SCAN & GEO-BOUNDING...]")
        geo_data = fetch_location_geo_and_area(city, province, country)

        if not geo_data:
            print("❌ Geocoding Disambiguation Failed. Please check parameters or network.")
            if not prompt_continuation():
                break
            continue

        print(f"✓ Target Resolved  : {geo_data['display_name']}")
        print(f"✓ Boundary Type    : {geo_data['resolved_type']}")
        print(f"✓ ISO Country Code : {geo_data['country_code']}")
        print(f"✓ Coordinates Found: Lat {geo_data['lat']}, Lon {geo_data['lon']}")
        print(f"✓ Auto Surface Area: {geo_data['computed_area_sqm']:,.2f} Sq Meters")

        telemetry = fetch_live_satellite_telemetry(geo_data["lat"], geo_data["lon"])
        if not telemetry:
            print("❌ Satellite Data Link Unavailable.")
            if not prompt_continuation():
                break
            continue

        mode, intensity, temp_c, rain_mm, uv = convert_telemetry_to_sab_mode(telemetry)
        result = process_sab_logic(mode, intensity, geo_data["computed_area_sqm"])

        # Currency Calculation
        curr_code, php_rate = fetch_live_currency_rate(geo_data["country_code"])
        local_currency_value = (result["power_kw"] * 0.12)
        value_in_php = local_currency_value * php_rate

        # Threat Assessment
        color_code, threat_label = determine_threat_color(intensity, mode)

        print("\n=================================================================")
        print("           SYSTEMATIC AUTOMATE BARRIER (SAB) OUTPUT              ")
        print("=================================================================")
        print(f"• Resolved Target     : {geo_data['display_name']}")
        print(f"• Satellite Telemetry : {temp_c}°C | Rain: {rain_mm} mm/h | UV: {uv}")
        print(f"• Auto Coverage Area  : {geo_data['computed_area_sqm']:,.2f} m²")
        print(f"• Active SAB Mode     : {result['mode_name']}")
        print(f"• Threat Level        : {color_code}{threat_label} (Intensity: {intensity}/10.0){COLOR_RESET}")
        print(f"• Barrier Transparency: {result['transparency']}%")
        print(f"• Clean Power Output  : {result['power_kw']:,.2f} kW")
        print(f"• Purified Water Yield: {result['water_liters']:,.2f} Liters")
        print(f"• Live Economic Yield : {local_currency_value:,.2f} {curr_code} ({value_in_php:,.2f} PHP)")
        print(f"• Defense Protocol    : {color_code}{result['protocol']}{COLOR_RESET}")
        print("=================================================================\n")

        if not prompt_continuation():
            print("\nSystematic Automate Barrier System Shutting Down.")
            break

if __name__ == "__main__":
    main()
