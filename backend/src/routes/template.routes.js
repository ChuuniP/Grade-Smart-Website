const express = require('express');
const router = express.Router();
const templateController = require('../controllers/template.controller');
const authMiddleware = require('../middleware/auth.middleware');

router.get('/', authMiddleware, templateController.getAll);
router.get('/:id/download', authMiddleware, templateController.download);

module.exports = router;
