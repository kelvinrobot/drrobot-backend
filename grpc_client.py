import grpc
import drrobot_pb2
import drrobot_pb2_grpc

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = drrobot_pb2_grpc.DoctorRobotStub(channel)
        
        print("--- Testing Chat Request ---")
        chat_request = drrobot_pb2.ChatRequest(
            query="Hello, am I talking to a robot?",
            session_id="test_session_123"
        )
        try:
            response = stub.AskChat(chat_request)
            print(f"Success: {response.success}")
            print(f"Data: {response.data}")
            print(f"Status Code: {response.statusCode}")
        except grpc.RpcError as e:
            print(f"gRPC call failed: {e.code()} - {e.details()}")

        print("\n--- Testing Water Born Disease Prediction ---")
        water_request = drrobot_pb2.WaterRequest(
            state="kaduna",
            country="nigeria"
        )
        try:
            response = stub.PredictWater(water_request)
            print(f"Success: {response.success}")
            print(f"Data: {response.data}")
            print(f"Status Code: {response.statusCode}")
        except grpc.RpcError as e:
            print(f"gRPC call failed: {e.code()} - {e.details()}")

if __name__ == "__main__":
    run()
