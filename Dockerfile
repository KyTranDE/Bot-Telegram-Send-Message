# Sử dụng một base image cho Python
FROM python:3.9

# Đặt thư mục làm việc trong container
WORKDIR /app

# Copy các file requirements.txt và cài đặt các package cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn của bạn vào thư mục làm việc
COPY . .

# Chạy file Python đầu tiên khi container được khởi động
CMD ["python", "mainbonbanh.py"]
