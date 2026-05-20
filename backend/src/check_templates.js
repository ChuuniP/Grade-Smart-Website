const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  try {
    const templates = await prisma.template.findMany({
      include: {
        results: {
          include: {
            details: true
          }
        }
      }
    });
    console.log("Templates in database:");
    for (const t of templates) {
      console.log(`- ID: ${t.id_template}, Name: ${t.name}, Total Questions: ${t.totalQuestions}`);
      if (t.results && t.results.length > 0) {
        for (const r of t.results) {
          console.log(`  Result Name: ${r.name}, Questions count: ${r.totalQuestions}`);
          if (r.details) {
            const sortedDetails = [...r.details].sort((a, b) => a.question - b.question);
            const answersList = sortedDetails.map(d => `${d.question}: ${d.answer}`).join(", ");
            console.log(`  Answers: ${answersList}`);
          }
        }
      } else {
        console.log("  No results/answers found.");
      }
    }
  } catch (error) {
    console.error("DB query failed:", error);
  } finally {
    await prisma.$disconnect();
  }
}

main();
