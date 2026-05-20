const authService = require('../services/auth.service');

class AuthController {
  async register(req, res) {
    try {
      const { username, email, password } = req.body;
      const user = await authService.register(username, email, password);
      res.status(201).json(user);
    } catch (error) {
      res.status(400).json({ error: error.message, message: error.message });
    }
  }

  async login(req, res) {
    try {
      const { username, email, password } = req.body;
      const identifier = username || email;
      const result = await authService.login(identifier, password);
      res.json(result);
    } catch (error) {
      res.status(401).json({ error: error.message, message: error.message });
    }
  }
}

module.exports = new AuthController();
