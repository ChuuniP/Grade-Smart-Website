const batchService = require('../services/batch.service');

class BatchController {
  async upload(req, res) {
    try {
      const { resultId, name, images } = req.body;
      const userId = req.userData.id_user;
      const result = await batchService.createBatch(userId, resultId, name, images);
      res.status(201).json(result);
    } catch (error) {
      console.error("Batch Upload Error Details:", error);
      res.status(500).json({ error: error.message });
    }
  }

  async export(req, res) {
    try {
      const batchId = req.params.id;
      const data = await batchService.getBatchExportData(batchId);
      if (!data) return res.status(404).json({ message: 'Batch not found' });
      res.json(data);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async list(req, res) {
    try {
      const userId = req.userData.id_user;
      const batches = await batchService.getAllBatches(userId);
      res.json(batches);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = new BatchController();
