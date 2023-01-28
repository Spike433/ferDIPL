import express from "express";
import { PrismaClient } from "@prisma/client";
const { sanitize } = require("express-xss-sanitizer");

const router = express.Router();
const prisma = new PrismaClient();

router.get("/", async function (req, res, next) {
  res.render("xss", {
    query: "",
    page: 'xss',
    data: undefined,
    user: req.session!.user,
  });
});

router.post("/", async function (req, res, next) {
  let { query, prevent } = req.body;

  if (prevent) {
    query = sanitize(query);
  }

  const data = await prisma.user.findMany({ where: { username: { contains: query } }, take: 10 });

  res.render("xss", {
    data,
    query,
    page: 'xss',
    user: req.session!.user,
  });
});

export { router as xssRouter };
