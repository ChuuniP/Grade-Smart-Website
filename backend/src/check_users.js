const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  try {
    const users = await prisma.user.findMany();
    console.log("Users:", users);
  } catch (error) {
    console.error("DB query failed:", error);
  } finally {
    await prisma.$disconnect();
  }
}

main();
