import time
import asyncio
import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

app = FastAPI(title="Doctor Robot API")

# Enable CORS (Equivalent to app.use(cors()))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHUNK_TIMEOUT = 30.0 # Timeout for external API calls

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        query = body.get("query", "Hello, how are you?")
        session_id = body.get("session_id", f"test-{int(time.time() * 1000)}")

        chat_endpoint = "https://drrobot9-doctor-robot-ai.hf.space/ask"
        payload = {
            "query": query,
            "session_id": session_id,
        }

        start_time = time.time()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                chat_endpoint, 
                json=payload, 
                timeout=CHUNK_TIMEOUT
            )
            data = response.json()

        return {
            "success": True,
            "endpoint": "chat",
            "responseTime": f"{int((time.time() - start_time) * 1000)}ms",
            "statusCode": response.status_code,
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "error": str(e)})

@app.post("/water")
async def water(request: Request):
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

@app.post("/both")
async def both():
    try:
        chat_endpoint = "https://drrobot9-doctor-robot-ai.hf.space/ask"
        water_endpoint = "https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict"

        chat_payload = {
            "query": "Hello, test connection",
            "session_id": f"test-{int(time.time() * 1000)}",
        }
        water_payload = {
            "state": "kaduna",
            "country": "nigeria",
        }

        start_time = time.time()
        
        async with httpx.AsyncClient() as client:
            # Running both requests concurrently (Equivalent to Promise.allSettled)
            async def safe_post(url, payload):
                try:
                    res = await client.post(url, json=payload, timeout=CHUNK_TIMEOUT)
                    return res.json()
                except Exception:
                    return None

            chat_task = safe_post(chat_endpoint, chat_payload)
            water_task = safe_post(water_endpoint, water_payload)
            
            chat_result, water_result = await asyncio.gather(chat_task, water_task)

        return {
            "success": True,
            "responseTime": f"{int((time.time() - start_time) * 1000)}ms",
            "results": {
                "chat": chat_result,
                "water": water_result,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "error": str(e)})

@app.get("/test")
async def test(type: Optional[str] = None):
    if not type:
        return {
            "message": "Test endpoint",
            "usage": "/test?type=chat or /test?type=water",
        }

    try:
        async with httpx.AsyncClient() as client:
            if type == "chat":
                response = await client.post(
                    "https://drrobot9-doctor-robot-ai.hf.space/ask",
                    json={
                        "query": "Hello",
                        "session_id": f"get-{int(time.time() * 1000)}",
                    },
                    timeout=CHUNK_TIMEOUT
                )
                return response.json()

            if type == "water":
                response = await client.post(
                    "https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict",
                    json={
                        "state": "kaduna",
                        "country": "nigeria",
                    },
                    timeout=CHUNK_TIMEOUT
                )
                return response.json()

        raise HTTPException(status_code=400, detail={"error": "Invalid type. Use chat or water"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

@app.get("/")
async def root():
    return {
        "message": "Doctor Robot FastAPI Backend",
        "endpoints": ["/chat", "/water", "/both", "/test"]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
