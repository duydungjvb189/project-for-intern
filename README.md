# 🧩 JVB Backend Project

## 📖 Giới thiệu

Dự án backend được phát triển bằng **FastAPI** kết hợp với **SQLAlchemy** và **MySQL**.  
Dự án được đóng gói và chạy hoàn toàn trong **Docker** để đảm bảo dễ triển khai và thống nhất môi trường.

---

## 🚀 Công nghệ sử dụng

- 🐍 **Python 3.10+**
- ⚡ **FastAPI**
- 🗃️ **SQLAlchemy**
- 🧱 **MySQL**
- 🐳 **Docker / Docker Compose**

---

## ⚙️ Cấu trúc thư mục

```
project/
├── jvb_backend/         # Source code backend (FastAPI)
├── images/              # Ảnh minh họa (tùy chọn)
├── docker-compose.yml   # File cấu hình Docker
└── README.md
```

---

## 🧰 Cách cài đặt & chạy dự án

### 1️⃣ Clone dự án

```bash
git clone https://gitlab.com/<tên-người-dùng>/<tên-dự-án>.git
cd <tên-dự-án>
```

### 2️⃣ Tạo file môi trường

Tạo file `.env` (nếu có) trong thư mục gốc, ví dụ:

```
DB_HOST=db
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=jvb_database
```

### 3️⃣ Khởi động bằng Docker

```bash
docker-compose up -d
```

Sau đó truy cập:
```
http://localhost:8000/docs
```

Đây là giao diện **Swagger UI** của FastAPI.

---

## 🧠 Một số lệnh hữu ích

Dừng tất cả container:
```bash
docker-compose down
```

Xem log backend:
```bash
docker logs -f <container_name>
```

---

## 📌 Ghi chú

- Dự án đang trong giai đoạn phát triển ban đầu.  
- Vui lòng tạo nhánh riêng cho từng tính năng theo convention:
  ```
  feature/<tên-tính-năng>
  bugfix/<tên-sửa-lỗi>
  ```

---

## 👨‍💻 Thông tin tác giả

**Nguyễn Duy Dũng**  
📧 Email: (cập nhật sau)  
🌐 GitLab: [gitlab.com/duydungjvb189](https://gitlab.com/duydungjvb189)

---

> Phiên bản: 0.1.0  
> Ngày khởi tạo: 2025-10-31  
> Framework: FastAPI
