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

      // Nếu linkImage là đường dẫn online (http hoặc https) và không phải localhost thì tải và gửi dưới dạng attachment để tải về trực tiếp
      if (template.linkImage.startsWith('http://') || template.linkImage.startsWith('https://')) {
        if (!template.linkImage.includes('localhost') && !template.linkImage.includes('127.0.0.1')) {
          const response = await fetch(template.linkImage);
          if (!response.ok) {
            return res.status(response.status).json({ message: `Không thể tải file template từ online: ${response.statusText}` });
          }
          
          res.setHeader('Content-Type', 'application/pdf');
          res.setHeader('Content-Disposition', `attachment; filename="${template.name}.pdf"`);
          
          const arrayBuffer = await response.arrayBuffer();
          const buffer = Buffer.from(arrayBuffer);
          return res.send(buffer);
        }
      }

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
