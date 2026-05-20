const express = require('express');
const router = express.Router();
const resultController = require('../controllers/result.controller');
const authMiddleware = require('../middleware/auth.middleware');

router.get('/', authMiddleware, resultController.getAll);
router.get('/:id', authMiddleware, resultController.getById);
router.post('/', authMiddleware, resultController.create);
router.put('/:id', authMiddleware, resultController.update);
router.delete('/:id', authMiddleware, resultController.delete);

module.exports = router;
