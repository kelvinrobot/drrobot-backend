import React, { useState } from "react";
import StyledButton from "@integratedComponents/StyledButton";
import "./style.css";

const ServiceUI = ({ serviceClient, isComplete }) => {
    const [output, setOutput] = useState();

    const ServiceInput = () => {
        const [input, setInput] = useState();

        const isAllowedToRun = () => {
            return !!input;
        };

        const onActionEnd = (response) => {
            const { message, status, statusMessage } = response;

            if (status !== 0) {
                throw new Error(statusMessage);
            }

            // setOutput(message.getValue());
        };

        const submitAction = () => {
            // const methodDescriptor = ;
            // const request = new methodDescriptor.requestType();

            // request.setValue(input)

            const props = {
                request,
                preventCloseServiceOnEnd: false,
                onEnd: onActionEnd,
            };

            serviceClient.unary(methodDescriptor, props);
        };

        return (
            <div className={"content-box"}>
                <h4>{"Input"}</h4>
                <div className={"content-box"}>
                    {/* Input blocks here */}
                </div>
                <div className={"content-box"}>
                    <StyledButton
                        btnText={"Submit"}
                        variant={"contained"}
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
                <div className={"content-box"}>
                    <h4>
                        {"Something went wrong..."}
                    </h4>
                </div>
            );
        }

        return (
            <div className={"content-box"}>
                <h4>
                    {"Output"}
                </h4>
                <div className={"content-box"}>
                    {/* Output blocks here */}
                </div>
            </div>
        );
    };

    return (
        <div className={"service-container"}>
            {!isComplete ? <ServiceInput /> : <ServiceOutput />}
        </div>
    );
};

export default ServiceUI;
