import { PrismaClient } from "@prisma/client";
import express from "express";

const router = express.Router();
const prisma = new PrismaClient();

router.get("/", function (req, res, next) {
  res.render("access", {
    page: 'access',
    user: req.session!.user,
  });
});

router.get("/bad/user/:id", async function (req, res, next) {
  const { id } = req.params;
  
  const data = await prisma.user.findFirst({where:{id: parseInt(id)}});

  res.render("user", {
    data,
    page: 'access',
    user: req.session!.user,
  });
});

router.get("/good/user/:id", async function (req, res, next) {
  const { id } = req.params;

  if (req.session?.user == undefined || (req.session?.user.id != id && req.session?.user.role != 'admin')) {
    res.render('403',{
      page: '403',
      user: req.session!.user,
    });
    return;
  }
  
  const data = await prisma.user.findFirst({where:{id: parseInt(id)}});

  res.render("user", {
    data,
    page: 'access',
    user: req.session!.user,
  });
});

export { router as accessRouter };
