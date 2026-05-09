const express = require('express');
const router = express.Router();
const omrController = require('../controllers/omr.controller');
const multer = require('multer');

const upload = multer({ dest: 'uploads/' });

router.post('/process', upload.single('image'), omrController.processImage);

module.exports = router;
