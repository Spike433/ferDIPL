import { PrismaClient } from '@prisma/client'
import bcrypt from "bcrypt";

const prisma = new PrismaClient()

async function main() {
  await prisma.user.create({
    data: {
      username: "user",
      password: bcrypt.hashSync('password', 10),
      role: "user"
    }
  })
  await prisma.user.create({
    data: {
      username: "admin",
      password: bcrypt.hashSync('password', 10),
      role: "admin"
    }
  })
}

main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })
