const { PrismaClient } = require('@prisma/client');

// Khởi tạo client kết nối DB local
const localPrisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.LOCAL_DATABASE_URL || "postgresql://postgres:postgres@127.0.0.1:5432/gradesmart?schema=public"
    }
  }
});

// Khởi tạo client kết nối DB online (Supabase)
const onlinePrisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL
    }
  }
});

async function migrate() {
  if (!process.env.DATABASE_URL || process.env.DATABASE_URL.includes("127.0.0.1") || process.env.DATABASE_URL.includes("localhost")) {
    console.error("❌ Lỗi: DATABASE_URL trong môi trường của bạn đang là local. Vui lòng điền DATABASE_URL của Supabase!");
    process.exit(1);
  }

  console.log("🚀 Bắt đầu quá trình sao chép dữ liệu từ Local sang Supabase...");

  try {
    // 1. Sao chép Users
    console.log("👥 Đang sao chép bảng Users...");
    const users = await localPrisma.user.findMany();
    console.log(`Tìm thấy ${users.length} users ở local.`);
    for (const user of users) {
      await onlinePrisma.user.upsert({
        where: { id_user: user.id_user },
        update: user,
        create: user,
      });
    }

    // 2. Sao chép Templates
    console.log("📝 Đang sao chép bảng Templates...");
    const templates = await localPrisma.template.findMany();
    console.log(`Tìm thấy ${templates.length} templates ở local.`);
    for (const template of templates) {
      await onlinePrisma.template.upsert({
        where: { id_template: template.id_template },
        update: template,
        create: template,
      });
    }

    // 3. Sao chép Results
    console.log("📊 Đang sao chép bảng Results...");
    const results = await localPrisma.result.findMany();
    console.log(`Tìm thấy ${results.length} results ở local.`);
    for (const r of results) {
      await onlinePrisma.result.upsert({
        where: { id_result: r.id_result },
        update: r,
        create: r,
      });
    }

    // 4. Sao chép ResultDetails
    console.log("📋 Đang sao chép bảng ResultDetails...");
    const resultDetails = await localPrisma.resultDetail.findMany();
    console.log(`Tìm thấy ${resultDetails.length} chi tiết đáp án.`);
    for (const rd of resultDetails) {
      await onlinePrisma.resultDetail.upsert({
        where: { id: rd.id },
        update: rd,
        create: rd,
      });
    }

    // 5. Sao chép Batches
    console.log("📦 Đang sao chép bảng Batches...");
    const batches = await localPrisma.batch.findMany();
    console.log(`Tìm thấy ${batches.length} đợt chấm thi.`);
    for (const b of batches) {
      await onlinePrisma.batch.upsert({
        where: { batch_id: b.batch_id },
        update: b,
        create: b,
      });
    }

    // 6. Sao chép BatchDetails
    console.log("🔍 Đang sao chép bảng BatchDetails...");
    const batchDetails = await localPrisma.batchDetail.findMany();
    console.log(`Tìm thấy ${batchDetails.length} chi tiết bài chấm.`);
    for (const bd of batchDetails) {
      await onlinePrisma.batchDetail.upsert({
        where: { id: bd.id },
        update: bd,
        create: bd,
      });
    }

    console.log("✅ Quá trình di chuyển dữ liệu thành công rực rỡ!");
  } catch (error) {
    console.error("❌ Đã xảy ra lỗi trong quá trình di chuyển dữ liệu:", error);
  } finally {
    await localPrisma.$disconnect();
    await onlinePrisma.$disconnect();
  }
}

migrate();
