// package: drrobot
// file: drrobot.proto

import * as jspb from "google-protobuf";

export class WaterRequest extends jspb.Message {
  getState(): string;
  setState(value: string): void;

  getCountry(): string;
  setCountry(value: string): void;

  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): WaterRequest.AsObject;
  static toObject(includeInstance: boolean, msg: WaterRequest): WaterRequest.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: WaterRequest, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): WaterRequest;
  static deserializeBinaryFromReader(message: WaterRequest, reader: jspb.BinaryReader): WaterRequest;
}

export namespace WaterRequest {
  export type AsObject = {
    state: string,
    country: string,
  }
}

export class WaterResponse extends jspb.Message {
  getSuccess(): boolean;
  setSuccess(value: boolean): void;

  getEndpoint(): string;
  setEndpoint(value: string): void;

  getResponsetime(): string;
  setResponsetime(value: string): void;

  getStatuscode(): number;
  setStatuscode(value: number): void;

  getDataMap(): jspb.Map<string, string>;
  clearDataMap(): void;
  serializeBinary(): Uint8Array;
  toObject(includeInstance?: boolean): WaterResponse.AsObject;
  static toObject(includeInstance: boolean, msg: WaterResponse): WaterResponse.AsObject;
  static extensions: {[key: number]: jspb.ExtensionFieldInfo<jspb.Message>};
  static extensionsBinary: {[key: number]: jspb.ExtensionFieldBinaryInfo<jspb.Message>};
  static serializeBinaryToWriter(message: WaterResponse, writer: jspb.BinaryWriter): void;
  static deserializeBinary(bytes: Uint8Array): WaterResponse;
  static deserializeBinaryFromReader(message: WaterResponse, reader: jspb.BinaryReader): WaterResponse;
}

export namespace WaterResponse {
  export type AsObject = {
    success: boolean,
    endpoint: string,
    responsetime: string,
    statuscode: number,
    dataMap: Array<[string, string]>,
  }
}

