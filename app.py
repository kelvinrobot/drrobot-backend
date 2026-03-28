import time
import asyncio
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

app = FastAPI(title="Doctor Robot API (Water Borne Disease Focus)")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHUNK_TIMEOUT = 30.0 # Timeout for external API calls

@app.post("/water")
async def water(request: Request):
    """
    Predict water borne diseases based on state and country.
    Expected payload: {"state": "string", "country": "string"}
    """
    try:
        body = await request.json()
        state = body.get("state", "kaduna")
        country = body.get("country", "nigeria")

        water_endpoint = "https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict"
        payload = {
            "state": state,
            "country": country,
        }

        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                water_endpoint, 
                json=payload, 
                timeout=CHUNK_TIMEOUT
            )
            data = response.json()

        return {
            "success": True,
            "endpoint": "water",
            "responseTime": f"{int((time.time() - start_time) * 1000)}ms",
            "statusCode": response.status_code,
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "error": str(e)})

@app.get("/test")
async def test():
    """Simple test for the water endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict",
                json={
                    "state": "kaduna",
                    "country": "nigeria",
                },
                timeout=CHUNK_TIMEOUT
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

@app.get("/")
async def root():
    return {
        "message": "Doctor Robot FastAPI Backend (Water Borne Disease Prediction)",
        "endpoints": ["/water", "/test"]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
