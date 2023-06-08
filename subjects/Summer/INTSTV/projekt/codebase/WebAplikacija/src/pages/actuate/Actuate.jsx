import React, { useEffect, useState } from "react";
import mqtt from "precompiled-mqtt";
import { Button, Typography } from "@mui/material";

const URL = "ws://161.53.19.19:56183";
//const URL = "wss://test.mosquitto.org:8081/";

const Actuate = () => {
  const [client, setClient] = useState(null);

  useEffect(() => {
    console.log("Connecting to broker from actuation page");
    const cli = mqtt.connect(URL);
    cli.on("connect", () => {
      console.log("Connected to broker from actuation page");
      setClient(cli);
    });
  }, []);

  function handleActuationClick() {
    console.log("client ", client);
    client.publish("grupa23", "disabled");
    console.log("succesfuly disabled");
  }

  return (
    <div className="mt-24 grid">
      <div className="flex justify-center text-black">
        <Typography variant="h4" gutterBottom>
          If you want to stop actuation, click on the button below!
        </Typography>
      </div>
      <div className="flex justify-center mt-4">
        <Button size="large" variant="contained" onClick={handleActuationClick}>
          Stop
        </Button>
      </div>
    </div>
  );
};

export default Actuate;
