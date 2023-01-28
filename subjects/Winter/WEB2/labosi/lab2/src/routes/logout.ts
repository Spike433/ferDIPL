import express from "express";

const router = express.Router();

router.get("/", async function (req, res, next) {
  req.session!.user = undefined;

  res.redirect("/");
});

export { router as logoutRouter };
