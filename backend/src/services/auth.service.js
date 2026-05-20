const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const prisma = require('../config/prisma');

class AuthService {
  async register(username, email, password) {
    const passwordHash = await bcrypt.hash(password, 10);
    return prisma.user.create({
      data: { username, email, password: passwordHash }
    });
  }

  async login(identifier, password) {
    const user = await prisma.user.findFirst({
      where: {
        OR: [
          { username: identifier },
          { email: identifier }
        ]
      }
    });
    if (!user) throw new Error('Invalid credentials');
    
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) throw new Error('Invalid credentials');

    const token = jwt.sign(
      { id_user: user.id_user },
      process.env.JWT_SECRET || 'secret_key',
      { expiresIn: '24h' }
    );

    return { token, user: { id_user: user.id_user, username: user.username } };
  }
}

module.exports = new AuthService();
