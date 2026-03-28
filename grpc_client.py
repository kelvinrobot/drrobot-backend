import grpc
import time
import sys
import drrobot_pb2
import drrobot_pb2_grpc

def run():
    # Use command-line arguments for state and country or default values
    state = sys.argv[1] if len(sys.argv) > 1 else "kaduna"
    country = sys.argv[2] if len(sys.argv) > 2 else "nigeria"

    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = drrobot_pb2_grpc.DoctorRobotStub(channel)
        
        print(f"\n--- gRPC Call: PredictWater (State: {state}, Country: {country}) ---")
        
        water_request = drrobot_pb2.WaterRequest(
            state=state,
            country=country
        )
        
        try:
            start_time = time.time()
            response = stub.PredictWater(water_request)
            end_time = time.time()
            
            print(f"Success: {response.success}")
            print(f"Status Code: {response.statusCode}")
            print(f"Data: {response.data}")
            print(f"Backend Wall-clock Time: {response.responseTime}")
            print(f"Full Round-trip Time: {int((end_time - start_time) * 1000)}ms")
            
        except grpc.RpcError as e:
            print(f"gRPC call failed: {e.code()} - {e.details()}")

if __name__ == "__main__":
    run()
