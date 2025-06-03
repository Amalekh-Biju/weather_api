# Weather API with Frontend

This project is a Weather API built with Python and FastAPI, featuring a simple web frontend to interact with the API. It provides endpoints to get real-time weather information for specific locations (via OpenWeatherMap), placeholder global average weather, and random weather data.

## Features

- **Web Frontend**: Simple HTML, CSS, and JavaScript interface to look up weather.
- **Real-time Weather**: Get current temperature, humidity, and conditions for a specific city using OpenWeatherMap.
- **Placeholder Endpoints**:
  - Average global weather.
  - Weather for a random location from a predefined list.
- **API Documentation**: Automatic interactive API documentation (Swagger UI at `/docs` and ReDoc at `/redoc`).
- **Rate Limiting**: Basic IP-based rate limiting on API requests.
- **Environment Variable Management**: Uses a `.env` file for API key management.

## Project Structure

weather_api/
├── static/ # Frontend files
│ ├── index.html
│ ├── style.css
│ └── script.js
├── .env # Environment variables (API key) - KEEP THIS SECRET
├── .gitignore # Specifies intentionally untracked files that Git should ignore
├── main.py # FastAPI application code
└── requirements.txt # Python dependencies

## Setup and Installation

1.  **Clone the repository (if applicable):**

    ```bash
    # git clone <your-repo-url>
    # cd weather_api
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up OpenWeatherMap API Key:**
    - Sign up for a free account at [OpenWeatherMap](https://openweathermap.org/).
    - Generate an API key from your account dashboard.
    - Create a file named `.env` in the root directory of this project (`weather_api/`).
    - Add your API key to the `.env` file in the following format:
      ```env
      OPENWEATHERMAP_API_KEY="YOUR_API_KEY"
      ```
      Replace `"YOUR_API_KEY"` with your actual OpenWeatherMap API key.
    - **Important for Git users:** Ensure `.env` is listed in your `.gitignore` file to prevent your API key from being committed to version control.

## How to Run

1.  Ensure all dependencies are installed and the `.env` file is configured with your API key.
2.  Navigate to the project's root directory (`weather_api/`) in your terminal.
3.  Run the Uvicorn server:
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag enables auto-reloading, so the server will restart when you make changes to the Python code.

## Accessing the Application

- **Frontend Web Interface:**
  Open your web browser and go to: `http://127.0.0.1:8000/`

- **API Documentation (Swagger UI):**
  `http://127.0.0.1:8000/docs`

- **API Documentation (ReDoc):**
  `http://127.0.0.1:8000/redoc`

## API Endpoints (Consumed by Frontend & Directly Accessible)

The frontend primarily uses these API endpoints. You can also test them directly:

- **`GET /weather/{location_name}`**

  - Description: Get real-time weather for a specific location.
  - Example: `http://127.0.0.1:8000/weather/london`
  - Success Response (200 OK):
    ```json
    {
      "location": "London",
      "temperature": "15.0°C",
      "humidity": "75%",
      "condition": "Cloudy"
    }
    ```
  - Error Response (e.g., 404 Not Found):
    ```json
    {
      "detail": "Weather data not found for location: <location_name>"
    }
    ```

- **`GET /weather/global/average`**

  - Description: Get placeholder average global weather.
  - Example: `http://127.0.0.1:8000/weather/global/average`
  - Success Response (200 OK):
    ```json
    {
      "description": "Average Global Weather (Placeholder)",
      "temperature": "19°C",
      "humidity": "60%"
    }
    ```

- **`GET /weather/random/location`**
  - Description: Get weather for a random location from a predefined list.
  - Example: `http://127.0.0.1:8000/weather/random/location`
  - Success Response (200 OK):
    ```json
    {
      "location": "Sydney",
      "temperature": "25°C",
      "humidity": "60%"
    }
    ```

## Tools Used

- Python
- FastAPI (Web framework)
- Uvicorn (ASGI server)
- OpenWeatherMap API (for real-time weather data)
- `python-dotenv` (for managing environment variables)
- `httpx` (for asynchronous HTTP requests)
- `slowapi` (for rate limiting)
- HTML, CSS, Vanilla JavaScript (for frontend)
