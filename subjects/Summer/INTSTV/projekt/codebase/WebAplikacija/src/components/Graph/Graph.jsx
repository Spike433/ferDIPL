import React from "react";
import Trend from "react-trend";
import { LineChart, Line, CartesianGrid, XAxis, YAxis } from "recharts";

function Graph(props) {
  
  const listOfValues = props.data.map((obj) => obj.value);

  return (
    <div>
      <LineChart width={600} height={400} data={props.data}>
        <Line type="monotone" dataKey="value" stroke="#8884d8" />
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="time" />
        <YAxis />
      </LineChart>
      <Trend
        style={{ border: "1px solid black" }}
        smooth
        autoDraw
        autoDrawDuration={3000}
        autoDrawEasing="ease-out"
        data={listOfValues}
        gradient={["#00c6ff", "#3f6deb", "#1c00a7"]}
        radius={1}
        strokeWidth={2}
        strokeLinecap={"butt"}
      />
    </div>
  );
}

export default Graph;
