import json
import logging
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

LOG_FILE = Path("weather.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

def _request(url: str) -> dict:
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode())

def geocode(city: str) -> tuple[str, float, float]:
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=en&format=json"
    data = _request(url)
    if not data.get("results"):
        logging.error("Fant ikke byen: %s", city)
        sys.exit(1)
    r = data["results"][0]
    return r["name"], r["latitude"], r["longitude"]

def fetch_weather(lat: float, lon: float) -> dict:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    return _request(url)

def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "Haugesund"
    try:
        name, lat, lon = geocode(city)
        data = fetch_weather(lat, lon)
    except (urllib.error.URLError, OSError) as e:
        logging.error("Kunne ikke hente værdata: %s", e)
        return
    current = data["current_weather"]
    logging.info(
        "%s | %.1f°C | Wind %.1f km/h %s | %s",
        name,
        current["temperature"],
        current["windspeed"],
        _wind_direction(current["winddirection"]),
        current["time"],
    )

def _wind_direction(deg: float) -> str:
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(deg / 45) % 8]

if __name__ == "__main__":
    main()
