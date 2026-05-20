const path = require('path');
const fs = require('fs');
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
      if (!template.linkImage) return res.status(404).json({ message: 'No download link available' });

      let templatePath = template.linkImage;
      try {
        const parsedUrl = new URL(template.linkImage, 'http://localhost:3000');
        templatePath = decodeURIComponent(parsedUrl.pathname);
      } catch (_err) {
        templatePath = template.linkImage;
      }

      if (templatePath.startsWith('/')) {
        templatePath = templatePath.slice(1);
      }
      if (templatePath.startsWith('templates/')) {
        templatePath = templatePath.slice('templates/'.length);
      }

      const absolutePath = path.join(__dirname, '../../templates', templatePath);
      if (!fs.existsSync(absolutePath)) {
        return res.status(404).json({ message: 'Template file not found' });
      }

      return res.download(absolutePath, `${template.name}.pdf`);
    } catch (error) {
      console.error('Template download error:', error);
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = new TemplateController();
