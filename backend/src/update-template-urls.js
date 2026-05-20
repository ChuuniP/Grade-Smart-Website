const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  let projectRef = process.env.SUPABASE_PROJECT_REF;

  if (!projectRef && process.env.DATABASE_URL) {
    // Thử trích xuất từ DATABASE_URL
    // Ví dụ: postgresql://postgres.abcdefghijklmopq:[password]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
    const dbUrl = process.env.DATABASE_URL;
    const matchUser = dbUrl.match(/postgres\.([a-zA-Z0-9_-]+):/);
    if (matchUser && matchUser[1]) {
      projectRef = matchUser[1];
    } else {
      const matchHost = dbUrl.match(/db\.([a-zA-Z0-9_-]+)\.supabase/);
      if (matchHost && matchHost[1]) {
        projectRef = matchHost[1];
      }
    }
  }

  if (!projectRef) {
    console.error("❌ Lỗi: Không thể tự động xác định Supabase Project Ref.");
    console.error("Vui lòng đặt biến môi trường SUPABASE_PROJECT_REF trong tệp .env!");
    process.exit(1);
  }

  console.log(`📡 Phát hiện Supabase Project Ref: ${projectRef}`);
  console.log("🔄 Bắt đầu cập nhật đường dẫn PDF sang Supabase Storage...");

  // Định nghĩa các URL công khai tương ứng trên Supabase Storage
  const files = {
    "Form 20": `https://${projectRef}.supabase.co/storage/v1/object/public/templates/Form%2020.pdf`,
    "Form 40": `https://${projectRef}.supabase.co/storage/v1/object/public/templates/Form%2040.pdf`,
    "Form 50": `https://${projectRef}.supabase.co/storage/v1/object/public/templates/Form%2050.pdf`,
    "Form 60": `https://${projectRef}.supabase.co/storage/v1/object/public/templates/Form%2060.pdf`,
    "Form 100": `https://${projectRef}.supabase.co/storage/v1/object/public/templates/Form%20100.pdf`,
    "Form 120": `https://${projectRef}.supabase.co/storage/v1/object/public/templates/Form%20120.pdf`
  };

  try {
    for (const [name, url] of Object.entries(files)) {
      const templates = await prisma.template.findMany({
        where: { name: name }
      });

      if (templates.length > 0) {
        for (const t of templates) {
          await prisma.template.update({
            where: { id_template: t.id_template },
            data: { linkImage: url }
          });
          console.log(`✅ Cập nhật thành công cho "${name}" -> ${url}`);
        }
      } else {
        console.log(`⚠️ Không tìm thấy template "${name}" trong cơ sở dữ liệu để cập nhật.`);
      }
    }
    console.log("🎉 Hoàn thành cập nhật tất cả URL Template online!");
  } catch (error) {
    console.error("❌ Đã xảy ra lỗi khi cập nhật:", error);
  } finally {
    await prisma.$disconnect();
  }
}

main();
