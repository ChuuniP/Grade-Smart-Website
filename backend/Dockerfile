# Sử dụng hình ảnh Node.js LTS chính thức (Slim) làm nền tảng
FROM node:20-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Cài đặt Python 3, pip và các thư viện hệ thống cần thiết cho OpenCV
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt các thư viện Python cần thiết cho script OMR (sử dụng --break-system-packages trên Debian mới)
RUN pip3 install --no-cache-dir --break-system-packages \
    opencv-python-headless \
    numpy \
    Pillow

# Thiết lập biến môi trường chỉ định đường dẫn chạy Python cho Node.js
ENV PYTHON=python3
ENV PORT=3000
ENV NODE_ENV=production

# Sao chép các tệp package.json và package-lock.json trước để tối ưu hóa bộ nhớ đệm Docker
COPY package*.json ./

# Cài đặt toàn bộ dependencies (bao gồm prisma trong devDependencies để generate Client)
RUN npm install

# Sao chép toàn bộ mã nguồn backend vào container
COPY . .

# Đảm bảo các thư mục upload và template tồn tại
RUN mkdir -p uploads templates

# Sinh mã Prisma Client cho môi trường Linux trong Docker
RUN npx prisma generate

# Mở cổng 3000 của container
EXPOSE 3000

# Khởi chạy ứng dụng Express server
CMD ["node", "src/app.js"]
