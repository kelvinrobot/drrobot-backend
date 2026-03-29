// package: drrobot
// file: drrobot.proto

var drrobot_pb = require("./drrobot_pb");
var grpc = require("@improbable-eng/grpc-web").grpc;

var DoctorRobot = (function () {
  function DoctorRobot() {}
  DoctorRobot.serviceName = "drrobot.DoctorRobot";
  return DoctorRobot;
}());

DoctorRobot.PredictWater = {
  methodName: "PredictWater",
  service: DoctorRobot,
  requestStream: false,
  responseStream: false,
  requestType: drrobot_pb.WaterRequest,
  responseType: drrobot_pb.WaterResponse
};

exports.DoctorRobot = DoctorRobot;

function DoctorRobotClient(serviceHost, options) {
  this.serviceHost = serviceHost;
  this.options = options || {};
}

DoctorRobotClient.prototype.predictWater = function predictWater(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(DoctorRobot.PredictWater, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

exports.DoctorRobotClient = DoctorRobotClient;

