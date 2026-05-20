const bcrypt = require('bcryptjs');
const prisma = require('./src/config/prisma');

async function main() {
  const existing = await prisma.user.findUnique({
    where: { username: 'user1' }
  });

  if (existing) {
    console.log('User already exists:', existing.username);
    return;
  }

  const passwordHash = await bcrypt.hash('123456', 10);
  const user = await prisma.user.create({
    data: {
      username: 'user1',
      email: 'user1@example.com',
      password: passwordHash
    }
  });

  console.log('Created user:', user.username);
}

main()
  .catch((error) => {
    console.error('Failed to seed user:', error);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
