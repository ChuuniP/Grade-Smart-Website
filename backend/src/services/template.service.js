const prisma = require('../config/prisma');

class TemplateService {
  async getAllTemplates() {
    return prisma.template.findMany();
  }

  async getTemplateById(id) {
    return prisma.template.findUnique({ where: { id_template: id } });
  }
}

module.exports = new TemplateService();
