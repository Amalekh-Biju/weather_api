from dotenv import load_dotenv
import os
import random
import httpx

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/weather"

if not OPENWEATHERMAP_API_KEY:
    print("WARNING: OPENWEATHERMAP_API_KEY not found. Real-time weather data may not be available.")

app = FastAPI(title="Weather API", description="An API to get weather information with a frontend.")

app.mount("/static", StaticFiles(directory="static"), name="static")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

random_locations_data = [
    {"location": "Sydney", "temperature": "25°C", "humidity": "60%"},
    {"location": "Cairo", "temperature": "30°C", "humidity": "40%"},
    {"location": "Moscow", "temperature": "10°C", "humidity": "75%"},
    {"location": "Beijing", "temperature": "20°C", "humidity": "50%"},
    {"location": "Delhi", "temperature": "35°C", "humidity": "45%"}
]
average_global_weather_data = {
    "description": "Average Global Weather (Placeholder)",
    "temperature": "19°C",
    "humidity": "60%"
}

async def fetch_weather_from_openweathermap(city_name: str):
    if not OPENWEATHERMAP_API_KEY:
        raise HTTPException(status_code=503, detail="Weather service unavailable: API key not configured.")
    params = {"q": city_name, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENWEATHERMAP_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "location": data.get("name", city_name),
                "temperature": f"{data['main']['temp']}°C",
                "humidity": f"{data['main']['humidity']}%",
                "condition": data['weather'][0]['description'] if data.get('weather') else "N/A"
            }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                 raise HTTPException(status_code=503, detail="Weather service authentication failed. Check API key.")
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Weather data not found for location: {city_name}")
            else:
                raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching weather data: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Weather service request failed: {str(e)}")
        except KeyError:
            raise HTTPException(status_code=500, detail="Error parsing weather data from provider.")

@app.get("/", response_class=HTMLResponse)
@limiter.limit("10/minute")
async def read_root_frontend(request: Request):
    """Serves the main HTML frontend page."""
    with open("static/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/weather/{location_name}")
@limiter.limit("10/minute")
async def get_weather_for_location_api(request: Request, location_name: str):
    """
    Get real-time weather for a specific location using OpenWeatherMap.
    - **location_name**: The name of the city (e.g., london, newyork, tokyo).
    """
    return await fetch_weather_from_openweathermap(location_name)

@app.get("/weather/global/average")
@limiter.limit("5/minute")
async def get_average_global_weather_api(request: Request):
    """
    Get the average global weather (placeholder data).
    """
    return average_global_weather_data

@app.get("/weather/random/location")
@limiter.limit("5/minute")
async def get_random_weather_api(request: Request):
    """
    Get weather for a random location from a predefined list.
    """
    if not random_locations_data:
        raise HTTPException(status_code=500, detail="No random locations available.")
    return random.choice(random_locations_data)