import logging
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

import main as weather

app = FastAPI(title="Værdashboard")

_cached: dict = {}


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, city: str = "Haugesund"):
    global _cached
    if not _cached or _cached.get("city_name") != city:
        _cached = _fetch_weather(city)
    return _render_html(_cached)


@app.post("/refresh")
async def refresh(city: str = Form("Haugesund")):
    global _cached
    _cached = _fetch_weather(city)
    return RedirectResponse(url=f"/?city={city}", status_code=303)


def _fetch_weather(city: str) -> dict:
    name, lat, lon = weather.geocode(city)
    data = weather.fetch_weather(lat, lon)
    current = data["current_weather"]
    return {
        "city_name": name,
        "temperature": current["temperature"],
        "windspeed": current["windspeed"],
        "winddirection": current["winddirection"],
        "winddir_text": weather._wind_direction(current["winddirection"]),
        "time": current["time"],
    }


def _render_html(w: dict) -> str:
    temp = f"{w['temperature']:.1f}"
    wind = f"{w['windspeed']:.1f}"
    return f"""<!DOCTYPE html>
<html lang="nb">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Værdashboard – {w['city_name']}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0f0f1a;color:#e0e0e0;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.container{{max-width:480px;width:90%;padding:2rem}}
.card{{background:linear-gradient(145deg,#1a1a2e,#16213e);border-radius:1.5rem;padding:2.5rem 2rem;box-shadow:0 8px 32px rgba(0,0,0,.5);text-align:center}}
h1{{font-size:1.5rem;font-weight:500;color:#a0a0c0;margin-bottom:.5rem;letter-spacing:.02em}}
.city{{font-size:2rem;font-weight:700;margin-bottom:1.5rem;color:#fff}}
.temp{{font-size:4.5rem;font-weight:800;color:#f0c060;line-height:1;margin-bottom:.25rem}}
.temp::after{{content:"°C";font-size:2rem;opacity:.5}}
.details{{display:flex;justify-content:center;gap:2rem;margin:1.5rem 0 2rem;font-size:1rem}}
.details span{{display:flex;flex-direction:column;align-items:center;gap:.25rem}}
.details .label{{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:#8080a0}}
.details .value{{font-size:1.25rem;font-weight:600;color:#d0d0f0}}
.time{{font-size:.85rem;color:#606080;margin-bottom:1.5rem}}
form{{display:flex;gap:.5rem}}
input[type=text]{{flex:1;padding:.75rem 1rem;border:1px solid #2a2a4a;border-radius:.75rem;background:#12122a;color:#e0e0e0;font-size:.95rem;outline:none;transition:border-color .2s}}
input[type=text]:focus{{border-color:#5050a0}}
button{{padding:.75rem 1.25rem;border:none;border-radius:.75rem;background:linear-gradient(135deg,#3a3a8a,#4a4aaa);color:#fff;font-size:.95rem;font-weight:600;cursor:pointer;white-space:nowrap;transition:transform .15s,box-shadow .15s}}
button:hover{{transform:translateY(-2px);box-shadow:0 4px 16px rgba(74,74,170,.4)}}
button:active{{transform:translateY(0)}}
@media(max-width:480px){{.container{{padding:1rem}}.card{{padding:1.5rem 1rem}}.temp{{font-size:3.5rem}}.details{{gap:1.25rem}}}}
</style>
</head>
<body>
<div class="container">
<div class="card">
<h1>Værdashboard</h1>
<div class="city">{w['city_name']}</div>
<div class="temp">{temp}</div>
<div class="details">
<span><span class="label">Vind</span><span class="value">{wind} km/t</span></span>
<span><span class="label">Retning</span><span class="value">{w['winddir_text']}</span></span>
</div>
<div class="time">Sist oppdatert: {w['time']}</div>
<form action="/refresh" method="post">
<input type="text" name="city" value="{w['city_name']}" placeholder="Skriv inn by ...">
<button type="submit">🔄 Hent</button>
</form>
</div>
</div>
</body>
</html>"""
