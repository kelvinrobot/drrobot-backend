// package: drrobot
// file: drrobot.proto

import * as drrobot_pb from "./drrobot_pb";
import {grpc} from "@improbable-eng/grpc-web";

type DoctorRobotPredictWater = {
  readonly methodName: string;
  readonly service: typeof DoctorRobot;
  readonly requestStream: false;
  readonly responseStream: false;
  readonly requestType: typeof drrobot_pb.WaterRequest;
  readonly responseType: typeof drrobot_pb.WaterResponse;
};

export class DoctorRobot {
  static readonly serviceName: string;
  static readonly PredictWater: DoctorRobotPredictWater;
}

export type ServiceError = { message: string, code: number; metadata: grpc.Metadata }
export type Status = { details: string, code: number; metadata: grpc.Metadata }

interface UnaryResponse {
  cancel(): void;
}
interface ResponseStream<T> {
  cancel(): void;
  on(type: 'data', handler: (message: T) => void): ResponseStream<T>;
  on(type: 'end', handler: (status?: Status) => void): ResponseStream<T>;
  on(type: 'status', handler: (status: Status) => void): ResponseStream<T>;
}
interface RequestStream<T> {
  write(message: T): RequestStream<T>;
  end(): void;
  cancel(): void;
  on(type: 'end', handler: (status?: Status) => void): RequestStream<T>;
  on(type: 'status', handler: (status: Status) => void): RequestStream<T>;
}
interface BidirectionalStream<ReqT, ResT> {
  write(message: ReqT): BidirectionalStream<ReqT, ResT>;
  end(): void;
  cancel(): void;
  on(type: 'data', handler: (message: ResT) => void): BidirectionalStream<ReqT, ResT>;
  on(type: 'end', handler: (status?: Status) => void): BidirectionalStream<ReqT, ResT>;
  on(type: 'status', handler: (status: Status) => void): BidirectionalStream<ReqT, ResT>;
}

export class DoctorRobotClient {
  readonly serviceHost: string;

  constructor(serviceHost: string, options?: grpc.RpcOptions);
  predictWater(
    requestMessage: drrobot_pb.WaterRequest,
    metadata: grpc.Metadata,
    callback: (error: ServiceError|null, responseMessage: drrobot_pb.WaterResponse|null) => void
  ): UnaryResponse;
  predictWater(
    requestMessage: drrobot_pb.WaterRequest,
    callback: (error: ServiceError|null, responseMessage: drrobot_pb.WaterResponse|null) => void
  ): UnaryResponse;
}

