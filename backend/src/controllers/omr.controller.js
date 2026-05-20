const omrService = require('../services/omr.service');

class OMRController {
  async processImage(req, res) {
    try {
      if (!req.file) {
        return res.status(400).json({ error: 'No image uploaded' });
      }

      const imagePath = req.file.path;
      const answers = req.body.answers || null;
      const result = await omrService.processImage(imagePath, answers);

      res.json(result);
    } catch (error) {
      console.error('OMR processing error:', error);
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = new OMRController();
