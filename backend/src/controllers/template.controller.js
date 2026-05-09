const templateService = require('../services/template.service');

class TemplateController {
  async getAll(req, res) {
    try {
      const templates = await templateService.getAllTemplates();
      res.json(templates);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async download(req, res) {
    try {
      const template = await templateService.getTemplateById(req.params.id);
      if (!template) return res.status(404).json({ message: 'Template not found' });
      // In a real app, this would generate a signed URL or serve the file
      res.json({ downloadLink: template.linkImage.replace('.png', '.pdf') });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = new TemplateController();
