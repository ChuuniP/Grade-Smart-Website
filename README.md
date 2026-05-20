# Grade Smart Website

## Giới thiệu đồ án

Grade Smart Website là một ứng dụng web hỗ trợ chấm điểm bài thi OMR (Optical Mark Recognition) tự động. Dự án bao gồm backend được xây dựng bằng Node.js với Express và Prisma, frontend sử dụng HTML/CSS/JavaScript thuần, và tích hợp các script Python cho xử lý hình ảnh OMR.

## Hướng dẫn khởi chạy ứng dụng ở Local

### Yêu cầu hệ thống
- **Node.js**: Phiên bản 16 trở lên.
- **PostgreSQL**: Cơ sở dữ liệu đang hoạt động.
- **Python**: Dùng để chạy các script xử lý ảnh OMR.

---

### Bước 1: Khởi động Backend

1. **Cài đặt thư viện dependencies:**
   Di chuyển vào thư mục `backend` và cài đặt các gói cần thiết:
   ```bash
   cd backend
   npm install
   ```

2. **Cấu hình Database:**
   - Tạo một database trống trong PostgreSQL (ví dụ: `gradesmart`).
   - Sao chép file `.env.example` thành `.env` và thiết lập biến môi trường `DATABASE_URL`. Ví dụ:
     ```env
     DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/gradesmart?schema=public"
     ```
   - Đẩy cấu hình cơ sở dữ liệu lên database:
     ```bash
     npx prisma db push
     ```

3. **Khởi tạo dữ liệu mẫu (Seed User):**
   Chạy script để tạo tài khoản đăng nhập mặc định:
   ```bash
   node seed-user.js
   ```

4. **Khởi động server backend:**
   ```bash
   npm run dev
   ```
   Server backend sẽ hoạt động tại địa chỉ: **`http://localhost:3000`**

---

### Bước 2: Khởi động Frontend

Vì frontend sử dụng HTML/JS thuần và cần gọi API tới backend bằng giao thức HTTP, việc mở trực tiếp file HTML (`file://`) có thể gây ra lỗi CORS hoặc hạn chế quyền truy cập `localStorage`. Do đó, bạn nên khởi chạy frontend thông qua một web server tĩnh.

#### Cách 1: Sử dụng Python (Khuyên dùng nếu đã cài Python)
Di chuyển vào thư mục `frontend` và khởi chạy server tĩnh bằng Python:
```bash
cd frontend
python -m http.server 8080
```

#### Cách 2: Sử dụng http-server của Node.js
Nếu không có Python, bạn có thể sử dụng gói `http-server` thông qua `npx`:
```bash
cd frontend
npx http-server -p 8080
```

Sau khi khởi động server frontend thành công, hãy truy cập địa chỉ sau trên trình duyệt:
**`http://localhost:8080/pages/login.html`**

---

### Thông tin đăng nhập mặc định
Bạn có thể đăng nhập bằng tài khoản mặc định được khởi tạo từ bước chạy seed dữ liệu:
* **Username:** `user1`
* **Password:** `123456`

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