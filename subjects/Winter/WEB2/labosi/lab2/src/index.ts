import { PrismaClient } from "@prisma/client";
import express from "express";
import path from "path";

import session from "express-session";
const MemoryStore = require("memorystore")(session);

const app = express();
const prisma = new PrismaClient();

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: true }));

app.use(
  session({
    cookie: { maxAge: 86400000 },
    store: new MemoryStore({
      checkPeriod: 86400000,
    }),
    resave: false,
    saveUninitialized: true,
    secret: process.env.SESSION_KEY!,
  })
);

import { accessRouter, homeRouter, loginRouter, logoutRouter, xssRouter } from "./routes";

app.use("/", homeRouter);
app.use("/xss", xssRouter);
app.use("/login", loginRouter);
app.use("/logout", logoutRouter);
app.use("/access", accessRouter);

const server = app.listen(process.env.PORT || 8000);
