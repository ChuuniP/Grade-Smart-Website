const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  try {
    const batches = await prisma.batch.findMany({
      include: {
        user: {
          select: {
            username: true,
            fullName: true
          }
        },
        result: {
          select: {
            name: true,
            totalQuestions: true
          }
        },
        details: true
      },
      orderBy: {
        time: 'desc'
      }
    });

    if (batches.length === 0) {
      console.log("No batches found in the database.");
      return;
    }

    console.log("=== BATCHES IN DATABASE ===");
    console.log(JSON.stringify(batches, null, 2));
  } catch (error) {
    console.error("DB query failed:", error);
  } finally {
    await prisma.$disconnect();
  }
}

main();
