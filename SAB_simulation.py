def get_weather_mode():
    while True:
        mode = input("Select Weather Mode (1: Rainy/Storm, 2: Extreme Heat, 3: Normal): ").strip()
        if mode in ["1", "2", "3"]:
            return mode
        print("Invalid selection. Please enter 1, 2, or 3.")

def get_intensity():
    while True:
        try:
            val = float(input("Enter Environmental Intensity Level (1.0 to 10.0): "))
            if 1.0 <= val <= 10.0:
                return val
            print("Intensity must be between 1.0 and 10.0.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_area():
    while True:
        try:
            area = float(input("Enter SAB Coverage Area in Sq Meters: "))
            if area > 0:
                return area
            print("Area must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid area size.")

def process_sab_logic(weather_mode, intensity, area):
    if weather_mode == "1":
        mode_name = "Rain & Storm Mitigation"
        power = area * intensity * 0.45
        water = area * intensity * 12.5
        transparency = 40
        if intensity > 7.5:
            protocol = "TRIGGERED: Cloud Redirection & Flood Diversion Active"
        else:
            protocol = "TRIGGERED: Local Reservoir Rain Harvesting Active"

    elif weather_mode == "2":
        mode_name = "Extreme Heat & UV Harvesting"
        power = area * intensity * 0.85
        water = area * intensity * 1.8
        transparency = 75
        if intensity > 8.0:
            protocol = "TRIGGERED: Micro-Climate Shading & EV Grid Off-loading Active"
        else:
            protocol = "TRIGGERED: Atmospheric Moisture Condensation Active"

    else:
        mode_name = "Normal Monitoring State"
        power = area * intensity * 0.05
        water = area * intensity * 0.2
        transparency = 95
        protocol = "Standby Operations"

    print("\nSAB SYSTEM OUTPUT")
    print(f"Active Mode: {mode_name}")
    print(f"Barrier Transparency: {transparency}%")
    print(f"Clean Power Generated: {power:.2f} kW")
    print(f"Purified Water Produced: {water:.2f} Liters")
    print(f"Safety & Balance Logic: {protocol}\n")

print("SAB SYSTEM INITIALIZED")
while True:
    mode = get_weather_mode()
    lvl = get_intensity()
    sqm = get_area()
    
    process_sab_logic(mode, lvl, sqm)
    
    cont = input("Do you want to run another environmental scan? (yes/no): ").strip().lower()
    if cont not in ["yes", "y"]:
        print("SAB System Shutting Down.")
        break
