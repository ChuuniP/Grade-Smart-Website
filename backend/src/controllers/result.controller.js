const resultService = require('../services/result.service');

class ResultController {
  async getAll(req, res) {
    try {
      const results = await resultService.getAllResults();
      res.json(results);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async getById(req, res) {
    try {
      const result = await resultService.getResultById(req.params.id);
      if (!result) return res.status(404).json({ message: 'Không tìm thấy bộ đáp án.' });
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async create(req, res) {
    try {
      const newResult = await resultService.createResult(req.body);
      res.status(201).json(newResult);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async update(req, res) {
    try {
      const updatedResult = await resultService.updateResult(req.params.id, req.body);
      res.json(updatedResult);
    } catch (error) {
      res.status(400).json({ error: error.message });
    }
  }

  async delete(req, res) {
    try {
      await resultService.deleteResult(req.params.id);
      res.json({ message: 'Xóa bộ đáp án thành công.' });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = new ResultController();
