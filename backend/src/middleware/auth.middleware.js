const jwt = require('jsonwebtoken');
const prisma = require('../config/prisma');

module.exports = async (req, res, next) => {
  try {
    if (!req.headers.authorization) {
      return res.status(401).json({ message: 'Auth failed: Missing token' });
    }
    const token = req.headers.authorization.split(' ')[1];
    const decodedToken = jwt.verify(token, process.env.JWT_SECRET || 'secret_key');
    
    // Verify user exists in the database to prevent foreign key errors with stale tokens
    const userExists = await prisma.user.findUnique({
      where: { id_user: decodedToken.id_user }
    });
    
    if (!userExists) {
      return res.status(401).json({ message: 'User no longer exists. Please log in again.' });
    }
    
    req.userData = { id_user: decodedToken.id_user };
    next();
  } catch (error) {
    res.status(401).json({ message: 'Auth failed: Invalid token' });
  }
};
