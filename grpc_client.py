import grpc
import drrobot_pb2
import drrobot_pb2_grpc

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = drrobot_pb2_grpc.DoctorRobotStub(channel)
        
        while True:
            print("\n" + "="*30)
            print(" Doctor Robot gRPC Client Test ")
            print("="*30)
            print("1. Test AskChat (Chatbot)")
            print("2. Test PredictWater (Disease Prediction)")
            print("3. Test Both")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                query = input("Enter your message (or leave blank for default): ") or "Hello, am I talking to a robot?"
                print("\n--- Testing Chat Request ---")
                chat_request = drrobot_pb2.ChatRequest(
                    query=query,
                    session_id=f"cli_{int(time.time())}"
                )
                try:
                    response = stub.AskChat(chat_request)
                    print(f"Success: {response.success}")
                    print(f"Data: {response.data}")
                    print(f"Status Code: {response.statusCode}")
                except grpc.RpcError as e:
                    print(f"gRPC call failed: {e.code()} - {e.details()}")

            elif choice == '2':
                state = input("Enter state (default: kaduna): ") or "kaduna"
                country = input("Enter country (default: nigeria): ") or "nigeria"
                print("\n--- Testing Water Born Disease Prediction ---")
                water_request = drrobot_pb2.WaterRequest(
                    state=state,
                    country=country
                )
                try:
                    response = stub.PredictWater(water_request)
                    print(f"Success: {response.success}")
                    print(f"Data: {response.data}")
                    print(f"Status Code: {response.statusCode}")
                except grpc.RpcError as e:
                    print(f"gRPC call failed: {e.code()} - {e.details()}")

            elif choice == '3':
                print("\n--- Testing Both Endpoints (Combined Request) ---")
                chat_request = drrobot_pb2.ChatRequest(
                    query="Hello, combined test",
                    session_id=f"cli_both_{int(time.time())}"
                )
                try:
                    response = stub.GetBoth(chat_request)
                    print(f"Success: {response.success}")
                    print(f"Response Time: {response.responseTime}")
                    print(f"Chat Result: {response.results.chat.data}")
                    print(f"Water Result: {response.results.water.data}")
                except grpc.RpcError as e:
                    print(f"gRPC call failed: {e.code()} - {e.details()}")

            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    import time
    run()
