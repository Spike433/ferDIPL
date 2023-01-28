import { PrismaClient } from "@prisma/client";
import express from "express";

const router = express.Router();
const prisma = new PrismaClient();

router.post("/", async function (req, res, next) {
  const subscription = await prisma.subscription.create({
    data: {
      data: JSON.stringify(req.body),
    },
  });

  res.status(200).json(subscription);
});

export { router as subscribeRouter };
