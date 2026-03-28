import grpc
from concurrent import futures
import time
import httpx
import asyncio
import json

# Import the generated gRPC classes
import drrobot_pb2
import drrobot_pb2_grpc

CHUNK_TIMEOUT = 30.0

class DoctorRobotServicer(drrobot_pb2_grpc.DoctorRobotServicer):
    
    async def _fetch_from_hf(self, url, payload):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=CHUNK_TIMEOUT)
                return response.status_code, response.json()
            except Exception as e:
                print(f"Error fetching from {url}: {e}")
                return 500, {"error": str(e)}

    def PredictWater(self, request, context):
        """Implements the PredictWater gRPC method."""
        print(f"Received WaterRequest: {request.state}, {request.country}")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        water_endpoint = "https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict"
        payload = {
            "state": request.state or "kaduna",
            "country": request.country or "nigeria",
        }
        
        start_time = time.time()
        status_code, data = loop.run_until_complete(self._fetch_from_hf(water_endpoint, payload))
        response_time = f"{int((time.time() - start_time) * 1000)}ms"
        
        string_data = {k: str(v) for k, v in data.items()} if isinstance(data, dict) else {"content": str(data)}
        
        return drrobot_pb2.WaterResponse(
            success=(status_code == 200),
            endpoint="water",
            responseTime=response_time,
            statusCode=status_code,
            data=string_data
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drrobot_pb2_grpc.add_DoctorRobotServicer_to_server(DoctorRobotServicer(), server)
    
    port = "50051"
    server.add_insecure_port(f"[::]:{port}")
    print(f"gRPC Server started on port {port}")
    server.start()
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
