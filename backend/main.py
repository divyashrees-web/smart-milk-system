
from datetime import datetime, timezone
import random

from fastapi import FastAPI, Query

from database import (
    initialize_database,
    save_reading,
    get_readings,
)

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Smart Milk Chilling System",
    description="AIoT monitoring and predictive maintenance backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()

state = {
    "ambient_temperature_c": 28.5,
    "humidity_percent": 65.0,
    "milk_temperature_simulated_c": 24.0,
    "tank_level_percent": 72.0,
    "cooling_status": "ON",
}


@app.get("/")
def home():
    return {
        "message": "Smart Milk Chilling System API is running!",
        "status": "online",
        "data_mode": "simulated",
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/sensor-data")
def get_sensor_data():
    state["ambient_temperature_c"] = round(
        max(20, min(38, state["ambient_temperature_c"]
                    + random.uniform(-0.3, 0.3))), 1
    )

    state["humidity_percent"] = round(
        max(35, min(90, state["humidity_percent"]
                    + random.uniform(-1, 1))), 1
    )

    if state["cooling_status"] == "ON":
        state["milk_temperature_simulated_c"] -= random.uniform(0.05, 0.2)
        if state["milk_temperature_simulated_c"] <= 20:
            state["cooling_status"] = "OFF"
    else:
        state["milk_temperature_simulated_c"] += random.uniform(0.02, 0.1)
        if state["milk_temperature_simulated_c"] >= 22:
            state["cooling_status"] = "ON"

    state["milk_temperature_simulated_c"] = round(
        state["milk_temperature_simulated_c"], 2
    )

    state["tank_level_percent"] = round(
        max(0, min(100, state["tank_level_percent"]
                    + random.uniform(-0.2, 0.2))), 1
    )

    reading = {
        "tank_id": "TANK_01",
        "ambient_temperature_c": state["ambient_temperature_c"],
        "humidity_percent": state["humidity_percent"],
        "milk_temperature_simulated_c":
            state["milk_temperature_simulated_c"],
        "tank_level_percent": state["tank_level_percent"],
        "cooling_status": state["cooling_status"],
        "power_status": "ON",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data_mode": "simulated",
    }

    save_reading(reading)
    return reading


@app.get("/api/history")
def sensor_history(
    limit: int = Query(default=50, ge=1, le=500)
):
    return {
        "count": len(get_readings(limit)),
        "readings": get_readings(limit),
        "data_mode": "simulated",
    }
