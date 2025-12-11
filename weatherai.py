import tkinter as tk
from tkinter import ttk, messagebox
import requests
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import threading
import numpy as np

# Weather code mapping with icons
WEATHER_CODES = {
    0: ("Clear sky", "☀️"), 1: ("Mainly clear", "☀️"), 2: ("Partly cloudy", "⛅"), 3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"), 48: ("Fog", "🌫️"), 51: ("Light drizzle", "🌦️"), 53: ("Drizzle", "🌧️"),
    55: ("Dense drizzle", "🌧️"), 56: ("Freezing drizzle", "🌨️"), 57: ("Freezing drizzle", "🌨️"),
    61: ("Light rain", "🌦️"), 63: ("Rain", "🌧️"), 65: ("Heavy rain", "⛈️"), 66: ("Freezing rain", "🌨️"),
    67: ("Heavy freezing rain", "🌨️"), 71: ("Light snow", "🌨️"), 73: ("Snow", "❄️"),
    75: ("Heavy snow", "❄️❄️"), 77: ("Snow grains", "🌨️"), 80: ("Rain showers", "🌦️"),
    81: ("Rain showers", "🌧️"), 82: ("Violent showers", "⛈️"), 85: ("Snow showers", "🌨️"),
    86: ("Heavy snow showers", "❄️❄️"), 95: ("Thunderstorm", "⛈️"), 96: ("Thunderstorm + hail", "🌩️"),
    99: ("Thunderstorm + heavy hail", "🌩️🌩️")
}

# ------------------------------
# Functions
# ------------------------------
def get_coordinates(location):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location.strip(), "count": 1, "language": "en"}
    try:
        r = requests.get(url, params=params, timeout=10).json()
        if "results" not in r or len(r["results"]) == 0:
            raise ValueError(f"Location '{location}' not found. Try a city name.")
        place = r["results"][0]
        return place["latitude"], place["longitude"], place["name"], place.get("country", "")
    except Exception as e:
        raise ValueError(f"Network error: {str(e)}")

def to_datetime(ts, tz):
    """Convert Open-Meteo timestamp to pandas datetime with timezone, remove tz for display."""
    if isinstance(ts, (list, np.ndarray)):
        ts = ts[0] if len(ts) > 0 else 0
    if isinstance(ts, bytes):
        ts = int(ts.decode())
    if isinstance(ts, (int, float)):
        ts_dt = pd.to_datetime(ts, unit="s", utc=True)
    else:
        ts_dt = pd.to_datetime(ts, utc=True)
    ts_dt = ts_dt.tz_convert(str(tz))  # convert to local time
    ts_dt = ts_dt.tz_localize(None)     # remove tz info for display
    return ts_dt

def fetch_weather(location):
    lat, lon, place_name, country = get_coordinates(location)

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    client = openmeteo_requests.Client(session=retry_session)

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "apparent_temperature", "weather_code", "is_day"],
        "hourly": ["temperature_2m", "weather_code"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "auto"
    }

    responses = client.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    tz = response.Timezone()
    if isinstance(tz, bytes):
        tz = tz.decode("utf-8")

    # --- Current Weather ---
    current = response.Current()
    current_time = to_datetime(current.Time(), tz)
    temp = round(current.Variables(0).Value(), 1)
    feels = round(current.Variables(1).Value(), 1)
    code = int(current.Variables(2).Value())
    desc, icon = WEATHER_CODES.get(code, ("Unknown", "🌐"))

    # --- Hourly (next 24h) ---
    hourly = response.Hourly()
    times = pd.to_datetime(np.array(hourly.Time()), unit="s", utc=True).tz_convert(tz).tz_localize(None)
    temps = hourly.Variables(0).ValuesAsNumpy()
    codes = hourly.Variables(1).ValuesAsNumpy().astype(int)
    hourly_data = []
    for t, temp_val, code_val in zip(times[:24], temps[:24], codes[:24]):
        d, ico = WEATHER_CODES.get(code_val, ("Unknown", "🌐"))
        hourly_data.append({"time": t.strftime("%H:%M"), "temp": f"{round(temp_val,1)}°", "desc": d, "icon": ico})

    # --- Daily (next 7 days) ---
    daily = response.Daily()
    dates = pd.to_datetime(np.array(daily.Time()), unit="s", utc=True).tz_convert(tz).tz_localize(None)
    codes_daily = daily.Variables(0).ValuesAsNumpy().astype(int)
    max_temps = daily.Variables(1).ValuesAsNumpy()
    min_temps = daily.Variables(2).ValuesAsNumpy()
    daily_data = []
    for date, code_val, t_max, t_min in zip(dates[:7], codes_daily[:7], max_temps[:7], min_temps[:7]):
        d, ico = WEATHER_CODES.get(code_val, ("Unknown", "🌐"))
        daily_data.append({
            "date": date.strftime("%a %b %d"),
            "desc": d,
            "icon": ico,
            "high": f"{round(t_max,1)}°",
            "low": f"{round(t_min,1)}°"
        })

    place = f"{place_name}, {country}" if country else place_name
    return {
        "place": place,
        "current": {
            "time": current_time.strftime("%A, %B %d • %H:%M"),
            "temp": f"{temp}°",
            "feels": f"Feels like {feels}°",
            "desc": desc,
            "icon": icon
        },
        "hourly": hourly_data,
        "daily": daily_data
    }

# ------------------------------
# GUI
# ------------------------------
class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather • Modern GUI")
        self.root.geometry("900x700")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        # Header
        tk.Label(self.root, text="Weather", font=("Helvetica", 36, "bold"), fg="#00bfff", bg="#121212").pack(pady=10)
        tk.Label(self.root, text="Enter city name below", font=("Helvetica", 12), fg="#888", bg="#121212").pack()

        # Entry + Search
        frame = tk.Frame(self.root, bg="#121212")
        frame.pack(pady=10)
        self.location_entry = tk.Entry(frame, font=("Helvetica", 14), width=30, justify="center",
                                       relief="flat", bg="#2d2d2d", fg="white", insertbackground="white")
        self.location_entry.pack(side="left", padx=5)
        self.location_entry.insert(0, "e.g. Paris, Tokyo, New York")
        self.location_entry.bind("<FocusIn>", lambda e: self.clear_placeholder())
        tk.Button(frame, text="Search", font=("Helvetica", 12, "bold"), bg="#00bfff", fg="white",
                  relief="flat", cursor="hand2", command=self.load_weather_thread).pack(side="left", padx=5)

        # Loading Label
        self.loading_label = tk.Label(self.root, text="", font=("Helvetica", 10), fg="#00bfff", bg="#121212")
        self.loading_label.pack(pady=5)

        # Current Weather Frame
        self.current_frame = tk.Frame(self.root, bg="#1e1e1e", relief="flat", bd=2)
        self.current_frame.pack(pady=20, padx=50, fill="x")
        self.icon_label = tk.Label(self.current_frame, text="🌤️", font=("Helvetica", 80), bg="#1e1e1e", fg="white")
        self.icon_label.pack(pady=10)
        self.place_label = tk.Label(self.current_frame, text="Loading...", font=("Helvetica", 20, "bold"), fg="white", bg="#1e1e1e")
        self.place_label.pack()
        self.time_label = tk.Label(self.current_frame, text="", font=("Helvetica", 10), fg="#aaa", bg="#1e1e1e")
        self.time_label.pack()
        self.temp_label = tk.Label(self.current_frame, text="", font=("Helvetica", 48, "bold"), fg="white", bg="#1e1e1e")
        self.temp_label.pack(pady=5)
        self.feels_label = tk.Label(self.current_frame, text="", font=("Helvetica", 12), fg="#aaa", bg="#1e1e1e")
        self.feels_label.pack()
        self.desc_label = tk.Label(self.current_frame, text="", font=("Helvetica", 16), fg="#00bfff", bg="#1e1e1e")
        self.desc_label.pack(pady=10)

        # Hourly Forecast
        tk.Label(self.root, text="Hourly Forecast", font=("Helvetica", 14, "bold"), fg="#00bfff", bg="#121212").pack(anchor="w", padx=50, pady=(20,5))
        self.hourly_table = ttk.Treeview(self.root, columns=("Time","Icon","Temp","Desc"), show="headings", height=5)
        for col in ("Time","Icon","Temp","Desc"):
            self.hourly_table.heading(col, text=col)
        self.hourly_table.pack(fill="x", padx=50)

        # Daily Forecast
        tk.Label(self.root, text="7-Day Forecast", font=("Helvetica", 14, "bold"), fg="#00bfff", bg="#121212").pack(anchor="w", padx=50, pady=(20,5))
        self.daily_table = ttk.Treeview(self.root, columns=("Day","Icon","High","Low","Desc"), show="headings", height=7)
        for col in ("Day","Icon","High","Low","Desc"):
            self.daily_table.heading(col, text=col)
        self.daily_table.pack(fill="both", expand=True, padx=50, pady=(0,30))

        # Footer
        tk.Label(self.root, text="Powered by Open-Meteo API • Made with ❤️", font=("Helvetica", 9), fg="#555", bg="#121212").pack(side="bottom", pady=10)

        self.root.bind("<Return>", lambda e: self.load_weather_thread())

    def clear_placeholder(self):
        if self.location_entry.get().startswith("e.g."):
            self.location_entry.delete(0, "end")
            self.location_entry.config(fg="white")

    def load_weather_thread(self):
        threading.Thread(target=self.show_weather, daemon=True).start()

    def show_weather(self):
        location = self.location_entry.get().strip()
        if not location or location.startswith("e.g."):
            self.root.after(0, lambda: messagebox.showwarning("Input Required", "Please enter a city name."))
            return

        self.root.after(0, lambda: self.loading_label.config(text="Fetching weather data..."))

        try:
            data = fetch_weather(location)
            self.root.after(0, lambda d=data: self.update_ui(d))
        except Exception as e:
            self.root.after(0, lambda msg=str(e): self.show_error(msg))
        finally:
            self.root.after(0, lambda: self.loading_label.config(text=""))

    def show_error(self, message):
        messagebox.showerror("Weather Error", message)

    def update_ui(self, data):
        # Current
        self.place_label.config(text=data["place"])
        self.time_label.config(text=data["current"]["time"])
        self.temp_label.config(text=data["current"]["temp"])
        self.feels_label.config(text=data["current"]["feels"])
        self.desc_label.config(text=data["current"]["desc"])
        self.icon_label.config(text=data["current"]["icon"])

        # Hourly
        for row in self.hourly_table.get_children():
            self.hourly_table.delete(row)
        for h in data["hourly"]:
            self.hourly_table.insert("", "end", values=(h["time"], h["icon"], h["temp"], h["desc"]))

        # Daily
        for row in self.daily_table.get_children():
            self.daily_table.delete(row)
        for d in data["daily"]:
            self.daily_table.insert("", "end", values=(d["date"], d["icon"], d["high"], d["low"], d["desc"]))

    def run(self):
        self.root.mainloop()


# Run the app
if __name__ == "__main__":
    app = WeatherApp()
    app.run()
