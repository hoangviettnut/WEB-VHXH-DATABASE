# Hệ thống thống kê xã Xuân Quang

## Mô tả
Hệ thống quản lý và hiển thị dữ liệu thống kê của xã Xuân Quang với giao diện admin để chỉnh sửa dữ liệu.

## Cấu trúc dự án
```
├── app.py              # Backend API chính
├── wsgi.py             # Entry point cho deployment
├── admin.html          # Dashboard admin
├── index.html          # Trang chính
├── requirements.txt    # Python dependencies
├── render.yaml         # Cấu hình Render deployment
├── Front END/          # CSS, JS, hình ảnh
└── Back END/           # Backend code gốc
```

## Cài đặt local

1. Cài đặt Python 3.8+
2. Cài đặt SQL Server và ODBC Driver
3. Chạy lệnh:
```bash
pip install -r requirements.txt
python app.py
```

## Deploy lên Render

### Bước 1: Push code lên GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/xuan-quang-stats.git
git push -u origin main
```

### Bước 2: Tạo Web Service trên Render
1. Vào https://render.com
2. Click "New +" → "Web Service"
3. Connect với GitHub repository
4. Cấu hình:
   - **Name:** `xuan-quang-stats`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`

### Bước 3: Cấu hình Environment Variables
Trong Render Dashboard → Environment:
- `DATABASE_URL`: `mssql+pyodbc://sa:viet@Viet/Số liệu thống kê của xã Xuân Quang?driver=ODBC+Driver+17+for+SQL+Server`
- `FLASK_ENV`: `production`

## API Endpoints

- `GET /` - Trang chủ
- `GET /admin` - Dashboard admin
- `GET /api/statistics` - Lấy tất cả thống kê
- `GET /api/overview` - Chỉ số tổng quan
- `GET /api/economy` - Dữ liệu kinh tế
- `GET /api/health` - Dữ liệu y tế
- `GET /api/education` - Dữ liệu giáo dục
- `GET /api/infrastructure` - Dữ liệu cơ sở hạ tầng
- `GET /api/digital` - Dữ liệu công nghệ số
- `GET /api/ethnic-groups` - Dữ liệu dân tộc
- `GET /api/villages-htx` - Dữ liệu thôn và HTX
- `GET /api/schools` - Dữ liệu trường học

## Admin Dashboard

- **URL:** `/admin`
- **Username:** `admin`
- **Password:** `admin123`

## Lưu ý

- Cần mở port 1433 cho SQL Server
- Cấu hình firewall cho phép kết nối từ Render
- Đảm bảo SQL Server Authentication mode được bật 