import { PrismaClient } from "@prisma/client";
import express from "express";
import bcrypt from "bcrypt";

const router = express.Router();
const prisma = new PrismaClient();

router.get("/", async function (req, res, next) {
  res.render("login", {
    page: 'login',
    error: undefined,
    user: req.session!.user,
  });
});

router.post("/", async function (req, res, next) {
  const { username, password } = req.body;

  const user = await prisma.user.findFirst({ where: { username } });

  if (user == undefined || !bcrypt.compareSync(password, user.password)) {
    res.render("login", {
      page: 'login',
      user: req.session!.user,
      error: "Invalid username and/or password.",
    });
    return;
  }

  req.session!.user = user;
  req.session!.save(() => {});

  res.redirect("/");
});

export { router as loginRouter };
