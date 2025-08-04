# Hệ thống thống kê xã Xuân Quang

## Mô tả
Hệ thống thống kê xã Xuân Quang là một ứng dụng web hiển thị các số liệu thống kê quan trọng của xã, bao gồm thông tin về kinh tế, y tế, giáo dục, cơ sở hạ tầng và công nghệ số.

## Tính năng chính

### Trang chính (index.html)
- **Hiển thị dữ liệu thống kê**: Các chỉ số tổng quan, kinh tế, y tế, giáo dục, cơ sở hạ tầng, công nghệ số
- **Bảng con chi tiết**: Dân số các dân tộc, thôn và HTX, thông tin trường học
- **Tìm kiếm**: Chức năng tìm kiếm trong các bảng con
- **Giao diện responsive**: Tương thích với các thiết bị di động
- **Widget thời tiết**: Hiển thị thông tin thời tiết hiện tại

### Trang Admin Dashboard (admin.html)
- **Quản lý database trực tiếp**: Thêm, sửa, xóa dữ liệu trong các bảng
- **Giao diện quản trị hiện đại**: Dashboard với sidebar và bảng dữ liệu
- **Tìm kiếm và lọc**: Tìm kiếm dữ liệu trong bảng
- **Modal forms**: Form thêm/sửa dữ liệu với giao diện thân thiện
- **Xác nhận xóa**: Modal xác nhận trước khi xóa dữ liệu

## Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.7+
- SQL Server
- ODBC Driver cho SQL Server

### Cài đặt dependencies
```bash
cd "Back END"
pip install -r requirements.txt
```

### Cấu hình database
Chỉnh sửa thông tin kết nối trong file `Back END/app.py`:
```python
DB_CONFIG = {
    'server': 'Viet',  # Tên server SQL Server
    'database': 'Số liệu thống kê của xã Xuân Quang',  # Tên database
    'username': 'sa',  # Username
    'password': 'viet',  # Password
    'driver': '{ODBC Driver 17 for SQL Server}'  # Driver ODBC
}
```

### Chạy ứng dụng
```bash
cd "Back END"
python app.py
```

Sau khi chạy, ứng dụng sẽ khởi động tại:
- **Trang chính**: http://localhost:5000 (thông qua backend)
- **Trang admin**: http://localhost:5000/admin

## Sử dụng

### Trang chính
1. Mở trình duyệt và truy cập http://localhost:5000
2. Sử dụng sidebar để điều hướng giữa các phần
3. Click vào các bảng con để xem chi tiết
4. Sử dụng thanh tìm kiếm để lọc dữ liệu

### Trang Admin
1. Click vào nút admin (biểu tượng shield) ở góc dưới bên phải trang chính
2. Nhập thông tin đăng nhập:
   - **Username**: admin
   - **Password**: admin123
3. Sau khi đăng nhập thành công, trang admin sẽ mở trong tab mới
4. Chọn bảng cần quản lý từ sidebar bên trái
5. Sử dụng các nút "Thêm mới", "Sửa", "Xóa" để quản lý dữ liệu

## Cấu trúc database

Hệ thống sử dụng các bảng sau:
- `1. Chỉ số tổng quan của xã` - Thông tin cơ bản
- `2. Kinh tế` - Dữ liệu kinh tế
- `3. Y tế` - Thông tin y tế
- `4. Giáo Dục` - Dữ liệu giáo dục
- `5. Cơ sở hạ tầng` - Thông tin cơ sở hạ tầng
- `6. Công nghệ số` - Dữ liệu công nghệ số
- `1.1. Dân số của các dân tộc` - Chi tiết dân tộc
- `2.1. Thôn và HTX` - Thông tin thôn và HTX
- `4.1. Thông tin các trường học.` - Chi tiết trường học

## API Endpoints

### Public APIs
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

### Admin APIs
- `POST /api/admin/login` - Đăng nhập admin
- `GET /api/admin/tables` - Lấy danh sách bảng
- `GET /api/admin/table/<table_name>` - Lấy dữ liệu bảng
- `POST /api/admin/table/<table_name>/update` - Cập nhật dữ liệu
- `POST /api/admin/table/<table_name>/insert` - Thêm dữ liệu mới
- `DELETE /api/admin/table/<table_name>/delete` - Xóa dữ liệu

## Bảo mật

- Mật khẩu admin được mã hóa bằng SHA-256
- Thông tin đăng nhập mặc định: admin/admin123
- Trong môi trường production, nên thay đổi thông tin đăng nhập và lưu trong database

## Ghi chú

- Đảm bảo SQL Server đang chạy trước khi khởi động ứng dụng
- Kiểm tra kết nối database bằng endpoint `/api/test-connection`
- Backup database thường xuyên trước khi thực hiện thay đổi dữ liệu
- Logs được ghi vào console để debug

## Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Kết nối database
2. Thông tin đăng nhập SQL Server
3. ODBC Driver đã được cài đặt
4. Firewall không chặn kết nối 