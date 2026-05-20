const prisma = require('../config/prisma');
const omrService = require('./omr.service');

class BatchService {
  async createBatch(userId, resultId, batchName, images) {
    const batch = await prisma.batch.create({
      data: {
        name: batchName,
        id_user: userId,
        result_id: resultId,
        total_tests: images.length
      }
    });

    const detailPromises = images.map(async (img) => {
      // If the OMR was already processed on the frontend and results are provided, save directly!
      if (img.score !== undefined) {
        return prisma.batchDetail.create({
          data: {
            batch_id: batch.batch_id,
            file_name: img.filename || img.url || 'unknown_file.jpg',
            student_id: img.studentId || '',
            test_code: img.paperCode || '',
            score: typeof img.score === 'number' ? img.score : parseFloat(img.score) || 0.0
          }
        });
      }

      // Fallback: process image using OMR service
      try {
        const omrResult = await omrService.processImage(img.url);
        return prisma.batchDetail.create({
          data: {
            batch_id: batch.batch_id,
            file_name: img.url || 'unknown_file.jpg',
            student_id: omrResult.studentId || '',
            test_code: omrResult.paperCode || '',
            score: omrResult.score || 0.0
          }
        });
      } catch (err) {
        console.error(`Error processing image ${img.url} in batch:`, err);
        return prisma.batchDetail.create({
          data: {
            batch_id: batch.batch_id,
            file_name: img.url || 'unknown_file.jpg',
            student_id: 'N/A',
            test_code: 'N/A',
            score: 0.0
          }
        });
      }
    });

    await Promise.all(detailPromises);

    return prisma.batch.findUnique({
      where: { batch_id: batch.batch_id },
      include: { details: true }
    });
  }

  async getBatchExportData(batchId) {
    return prisma.batch.findUnique({
      where: { batch_id: batchId },
      include: {
        details: true,
        user: { select: { username: true } },
        result: { select: { name: true } }
      }
    });
  }

  async getAllBatches(userId) {
    return prisma.batch.findMany({
      where: { id_user: userId },
      orderBy: { time: 'desc' },
      include: {
        details: true,
        user: { select: { username: true, fullName: true } },
        result: { select: { name: true, totalQuestions: true } }
      }
    });
  }
}

module.exports = new BatchService();
