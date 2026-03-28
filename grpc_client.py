import grpc
import time
import drrobot_pb2
import drrobot_pb2_grpc

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = drrobot_pb2_grpc.DoctorRobotStub(channel)
        
        while True:
            print("\n" + "="*30)
            print(" Doctor Robot gRPC Client ")
            print(" (Water Borne Disease) ")
            print("="*30)
            print("1. Test PredictWater (Disease Prediction)")
            print("2. Exit")
            
            choice = input("\nEnter your choice (1-2): ")
            
            if choice == '1':
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
                    print(f"Response Time: {response.responseTime}")
                except grpc.RpcError as e:
                    print(f"gRPC call failed: {e.code()} - {e.details()}")

            elif choice == '2':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    run()
