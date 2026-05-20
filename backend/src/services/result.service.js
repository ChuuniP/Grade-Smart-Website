const prisma = require('../config/prisma');

class ResultService {
  async getAllResults() {
    return prisma.result.findMany({
      include: {
        template: true,
        details: {
          orderBy: { question: 'asc' }
        }
      }
    });
  }

  async getResultById(id) {
    return prisma.result.findUnique({
      where: { id_result: id },
      include: {
        template: true,
        details: {
          orderBy: { question: 'asc' }
        }
      }
    });
  }

  async createResult(data) {
    const { name, id_template, totalQuestions, answers } = data;

    // Constraint validation: "số lượng câu hỏi không được vượt quá số lượng câu hỏi của form bài kiểm tra"
    const template = await prisma.template.findUnique({
      where: { id_template }
    });

    if (!template) {
      throw new Error('Không tìm thấy mẫu phiếu tương ứng.');
    }

    if (totalQuestions > template.totalQuestions) {
      throw new Error(`Số lượng câu hỏi của bộ đáp án (${totalQuestions}) không được vượt quá số lượng câu hỏi tối đa của mẫu phiếu (${template.totalQuestions})!`);
    }

    return prisma.$transaction(async (tx) => {
      const result = await tx.result.create({
        data: {
          name,
          id_template,
          totalQuestions
        }
      });

      if (answers && answers.length > 0) {
        const detailsData = answers.map((ans, idx) => ({
          id_result: result.id_result,
          question: idx + 1,
          answer: ans || ''
        }));

        await tx.resultDetail.createMany({
          data: detailsData
        });
      }

      return tx.result.findUnique({
        where: { id_result: result.id_result },
        include: {
          template: true,
          details: {
            orderBy: { question: 'asc' }
          }
        }
      });
    });
  }

  async updateResult(id, data) {
    const { name, answers } = data;

    return prisma.$transaction(async (tx) => {
      // Update name if provided
      if (name !== undefined) {
        await tx.result.update({
          where: { id_result: id },
          data: { name }
        });
      }

      // Update individual questions if answers are provided
      if (answers && answers.length > 0) {
        // Delete old details
        await tx.resultDetail.deleteMany({
          where: { id_result: id }
        });

        // Insert new details
        const detailsData = answers.map((ans, idx) => ({
          id_result: id,
          question: idx + 1,
          answer: ans || ''
        }));

        await tx.resultDetail.createMany({
          data: detailsData
        });
      }

      return tx.result.findUnique({
        where: { id_result: id },
        include: {
          template: true,
          details: {
            orderBy: { question: 'asc' }
          }
        }
      });
    });
  }

  async deleteResult(id) {
    return prisma.result.delete({
      where: { id_result: id }
    });
  }
}

module.exports = new ResultService();
