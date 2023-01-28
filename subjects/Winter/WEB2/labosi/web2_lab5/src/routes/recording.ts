import { PrismaClient } from "@prisma/client";
import express from "express";

const router = express.Router();
const prisma = new PrismaClient();

router.get("/", async function (req, res, next) {
  const recordings = await prisma.recording.findMany();

  res.status(200).json(recordings);
});

router.post("/", async function (req, res, next) {
  const { name, data } = req.body;

  const recording = await prisma.recording.create({
    data: {
      name,
      data,
    },
  });

  res.status(200).json(recording);
});

router.delete("/:id", async function (req, res, next) {
  const { id } = req.params;

  const recording = await prisma.recording.delete({
    where: {
      id: Number(id),
    },
  });

  res.status(200).json(recording);
});

export { router as recordingRouter };
