const prisma = require('../config/prisma');
const omrService = require('./omr.service');

class BatchService {
  async createBatchWithTests(userId, templateId, batchName, images) {
    const batch = await prisma.batch.create({
      data: {
        name: batchName,
        id_user: userId,
        id_template: templateId
      }
    });

    const testPromises = images.map(async (img) => {
      const omrResult = await omrService.processImage(img.url);
      return prisma.test.create({
        data: {
          id_batch: batch.id_batch,
          imageUrl: img.url,
          score: omrResult.score,
          id_student: omrResult.test_code,
          test_code: omrResult.test_code,
          status: 'completed'
        }
      });
    });

    await Promise.all(testPromises);

    return prisma.batch.findUnique({
      where: { id_batch: batch.id_batch },
      include: { tests: true }
    });
  }

  async getBatchExportData(batchId) {
    return prisma.batch.findUnique({
      where: { id_batch: batchId },
      include: {
        tests: true,
        user: { select: { username: true } },
        template: { select: { name: true } }
      }
    });
  }
}

module.exports = new BatchService();
