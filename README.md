# Grade Smart Website

## Giới thiệu đồ án

Grade Smart Website là một ứng dụng web hỗ trợ chấm điểm bài thi OMR (Optical Mark Recognition) tự động. Dự án bao gồm backend được xây dựng bằng Node.js với Express và Prisma, frontend sử dụng HTML/CSS/JavaScript thuần, và tích hợp các script Python cho xử lý hình ảnh OMR.

## Cách chạy web ở local

### Yêu cầu hệ thống
- Node.js (phiên bản 16 trở lên)
- PostgreSQL database
- Python (cho các script OMR)

### Cài đặt và chạy

1. **Clone repository:**
   ```
   git clone https://github.com/ChuuniP/Grade-Smart-Website.git
   cd grade-smart-website
   ```

2. **Cài đặt dependencies cho backend:**
   ```
   cd backend
   npm install
   ```

3. **Cấu hình database:**
   - Tạo database PostgreSQL.
   - Sao chép file `.env.example` thành `.env` và cập nhật `DATABASE_URL` với thông tin database của bạn.
   - Chạy migration Prisma:
     ```
     npx prisma migrate dev
     ```
   - (Tùy chọn) Chạy script init.sql để khởi tạo dữ liệu mẫu.

4. **Chạy backend:**
   ```
   npm run dev  # hoặc npm start
   ```
   Server sẽ chạy trên http://localhost:5000

5. **Mở frontend:**
   - Mở file `frontend/pages/login.html` trong trình duyệt web.
   - Hoặc serve static files từ backend nếu đã cấu hình.

## Các chức năng hiện tại

- **Đăng nhập/Đăng ký:** Xác thực người dùng với JWT.
- **Quản lý Templates:** Tạo và quản lý mẫu bài thi OMR.
- **Quản lý Batches:** Tạo và quản lý lô bài thi.
- **Xử lý OMR:** Upload và chấm điểm bài thi tự động sử dụng Python scripts.
- **Dashboard:** Tổng quan về các lô bài thi và kết quả.
- **Chấm điểm tức thì:** Chức năng chấm điểm nhanh cho bài thi đơn lẻ.

## Chức năng đang cập nhật

- Báo cáo và thống kê chi tiết
- Xuất kết quả ra file PDF/Excel
- Tích hợp AI nâng cao cho nhận dạng
- Giao diện responsive cho mobile
- Hệ thống thông báo và email</content>
<parameter name="filePath">e:/Antigravity/Grade Smart/README.md