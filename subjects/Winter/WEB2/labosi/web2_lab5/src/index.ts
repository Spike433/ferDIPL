import express from "express";
import path from "path";

const app = express();

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(express.static(path.join(__dirname, "../public")));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

import { pushRouter, subscribeRouter, recordingRouter } from "./routes";

app.use("/api/push", pushRouter);
app.use("/api/subscribe", subscribeRouter);
app.use("/api/recordings", recordingRouter);

const server = app.listen(process.env.PORT || 8000);
