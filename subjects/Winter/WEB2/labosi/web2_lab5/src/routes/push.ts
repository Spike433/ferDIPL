import { PrismaClient } from "@prisma/client";
import webpush from "web-push";
import express from "express";

const router = express.Router();
const prisma = new PrismaClient();

router.post("/", async function (req, res, next) {
  webpush.setVapidDetails(
    "mailto:you@example.com",
    "BMcy7qUab-2BzEpH4uqV1IfW8Oyq2xSDehMLCqo8fcwXngiK-S4OD5tFE1dSRINrN9lqNBoAE3gRafHwCTOX6kA",
    "zwmbHQoEzbNtSRCXQeBdfItT8__aaQr0DjbnmSfcoAA"
  );

  const subscriptions = await prisma.subscription.findMany();

  subscriptions.forEach(async (subscription) => {
    // @ts-ignore - this works
    webpush
      .sendNotification(
        JSON.parse(subscription.data),
        JSON.stringify({
          title: req.body.title,
          body: req.body.body,
          icon: req.body.icon,
          badge: req.body.badge,
          image: req.body.image,
          vibrate: req.body.vibrate,
          tag: req.body.tag,
          renotify: req.body.renotify,
        })
      )
      .catch((err) => {
        prisma.subscription.delete({
          where: {
            id: subscription.id,
          },
        });
      });
  });

  res.status(200).json({ success: true });
});

export { router as pushRouter };
