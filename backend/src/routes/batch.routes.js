const express = require('express');
const router = express.Router();
const batchController = require('../controllers/batch.controller');
const authMiddleware = require('../middleware/auth.middleware');

router.post('/upload', authMiddleware, batchController.upload);
router.get('/', authMiddleware, batchController.list);
router.get('/:id/export', authMiddleware, batchController.export);

module.exports = router;
