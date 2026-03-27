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

    def AskChat(self, request, context):
        """Implements the AskChat gRPC method."""
        print(f"Received ChatRequest: {request.query}")
        
        # We need an event loop for httpx
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        chat_endpoint = "https://drrobot9-doctor-robot-ai.hf.space/ask"
        payload = {
            "query": request.query or "Hello, how are you?",
            "session_id": request.session_id or f"grpc-{int(time.time() * 1000)}",
        }
        
        start_time = time.time()
        status_code, data = loop.run_until_complete(self._fetch_from_hf(chat_endpoint, payload))
        response_time = f"{int((time.time() - start_time) * 1000)}ms"
        
        # Convert dictionary data to string map for proto
        # Note: If the HF data is nested, this simple string conversion might be necessary 
        # or the proto message needs to be more complex (e.g. using google.protobuf.Struct).
        string_data = {k: str(v) for k, v in data.items()} if isinstance(data, dict) else {"content": str(data)}
        
        return drrobot_pb2.ChatResponse(
            success=(status_code == 200),
            endpoint="chat",
            responseTime=response_time,
            statusCode=status_code,
            data=string_data
        )

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

    def GetBoth(self, request, context):
        """Implements the GetBoth gRPC method (Combined call)."""
        print(f"Received GetBoth request")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        chat_endpoint = "https://drrobot9-doctor-robot-ai.hf.space/ask"
        water_endpoint = "https://drrobot9-doctor-robot-waterborn-disease.hf.space/predict"

        chat_payload = {
            "query": request.query or "Hello, test connection",
            "session_id": f"grpc-both-{int(time.time() * 1000)}",
        }
        water_payload = {
            "state": "kaduna",
            "country": "nigeria",
        }

        async def fetch_both():
            async with httpx.AsyncClient() as client:
                async def safe_post(url, payload, tag):
                    try:
                        res = await client.post(url, json=payload, timeout=CHUNK_TIMEOUT)
                        # Match the specific response types
                        data = res.json()
                        string_data = {k: str(v) for k, v in data.items()} if isinstance(data, dict) else {"content": str(data)}
                        
                        if tag == "chat":
                            return drrobot_pb2.ChatResponse(
                                success=(res.status_code == 200),
                                endpoint="chat",
                                responseTime="N/A",
                                statusCode=res.status_code,
                                data=string_data
                            )
                        else:
                            return drrobot_pb2.WaterResponse(
                                success=(res.status_code == 200),
                                endpoint="water",
                                responseTime="N/A",
                                statusCode=res.status_code,
                                data=string_data
                            )
                    except Exception as e:
                        print(f"Error in {tag}: {e}")
                        return None

                return await asyncio.gather(
                    safe_post(chat_endpoint, chat_payload, "chat"),
                    safe_post(water_endpoint, water_payload, "water")
                )

        start_time = time.time()
        chat_res, water_res = loop.run_until_complete(fetch_both())
        response_time = f"{int((time.time() - start_time) * 1000)}ms"

        return drrobot_pb2.BothResponse(
            success=True,
            responseTime=response_time,
            results=drrobot_pb2.BothResponse.Results(
                chat=chat_res,
                water=water_res
            )
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
