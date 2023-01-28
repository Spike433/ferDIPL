import { PrismaClient } from "@prisma/client";
import express from "express";

const router = express.Router();
const prisma = new PrismaClient();

router.get("/", function (req, res, next) {
  res.render("home", {
    page: 'home',
    user: req.session!.user,
  });
});

export { router as homeRouter };
