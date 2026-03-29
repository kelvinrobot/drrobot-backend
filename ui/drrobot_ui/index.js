import React, { useState } from "react";
import StyledButton from "@integratedComponents/StyledButton";
import { WaterRequest } from "./drrobot_pb";
import { DoctorRobot } from "./drrobot_pb_service";
import "./style.css";

const ServiceUI = ({ serviceClient, isComplete }) => {
  const [output, setOutput] = useState(null);

  const ServiceInput = () => {
    const [stateValue, setStateValue] = useState("");
    const [countryValue, setCountryValue] = useState("");

    const isAllowedToRun = () => {
      return stateValue && countryValue;
    };

    const onActionEnd = (response) => {
      const { message, status, statusMessage } = response;

      if (status !== 0) {
        console.error(statusMessage);
        setOutput(null);
        return;
      }

      setOutput({
        success: message.getSuccess(),
        endpoint: message.getEndpoint(),
        responseTime: message.getResponsetime(),
        statusCode: message.getStatuscode(),
        data: message.getDataMap().toObject(),
      });
    };

    const submitAction = () => {
      const methodDescriptor = DoctorRobot.PredictWater;

      const request = new WaterRequest();
      request.setState(stateValue);
      request.setCountry(countryValue);

      const props = {
        request,
        onEnd: onActionEnd,
      };

      serviceClient.unary(methodDescriptor, props);
    };

    return (
      <div className="content-box">
        <h4>Input</h4>

        <div className="content-box">
          <label>State</label>
          <input
            className="input"
            type="text"
            placeholder="e.g. Kaduna"
            value={stateValue}
            onChange={(e) => setStateValue(e.target.value)}
          />
        </div>

        <div className="content-box">
          <label>Country</label>
          <input
            className="input"
            type="text"
            placeholder="e.g. Nigeria"
            value={countryValue}
            onChange={(e) => setCountryValue(e.target.value)}
          />
        </div>

        <div className="content-box">
          <StyledButton
            btnText="Submit"
            variant="contained"
            onClick={submitAction}
            disabled={!isAllowedToRun()}
          />
        </div>
      </div>
    );
  };

  const ServiceOutput = () => {
    if (!output) {
      return (
        <div className="content-box">
          <h4>No response yet...</h4>
        </div>
      );
    }

    return (
      <div className="content-box">
        <h4>Output</h4>

        <div className="content-box">
          <p><strong>Success:</strong> {String(output.success)}</p>
          <p><strong>Endpoint:</strong> {output.endpoint}</p>
          <p><strong>Response Time:</strong> {output.responseTime}</p>
          <p><strong>Status Code:</strong> {output.statusCode}</p>
        </div>

        <div className="content-box">
          <h5>Data</h5>
          {Object.keys(output.data).length === 0 ? (
            <p>No data returned</p>
          ) : (
            <ul>
              {Object.entries(output.data).map(([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong> {value}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="service-container">
      {!isComplete ? <ServiceInput /> : <ServiceOutput />}
    </div>
  );
};

export default ServiceUI;