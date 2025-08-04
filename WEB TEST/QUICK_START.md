# Hướng dẫn nhanh - Hệ thống Admin Dashboard

## 🚀 Khởi động nhanh

### 1. Khởi động Backend
```bash
cd "Back END"
python app.py
```

### 2. Truy cập ứng dụng
- **Trang chính**: http://localhost:5000
- **Trang admin**: http://localhost:5000/admin

## 🔐 Đăng nhập Admin

### Thông tin đăng nhập mặc định:
- **Username**: `admin`
- **Password**: `admin123`

### Cách truy cập:
1. Mở trang chính http://localhost:5000
2. Click vào nút admin (biểu tượng shield) ở góc dưới bên phải
3. Nhập thông tin đăng nhập
4. Trang admin sẽ mở trong tab mới

## 📊 Sử dụng Admin Dashboard

### Chức năng chính:
- **Xem dữ liệu**: Chọn bảng từ sidebar bên trái
- **Thêm mới**: Click nút "Thêm mới" → Điền thông tin → Lưu
- **Sửa dữ liệu**: Click nút "Sửa" (biểu tượng bút) → Chỉnh sửa → Lưu
- **Xóa dữ liệu**: Click nút "Xóa" (biểu tượng thùng rác) → Xác nhận

### Các bảng có thể quản lý:
1. **Chỉ số tổng quan của xã** - Thông tin cơ bản
2. **Kinh tế** - Dữ liệu kinh tế
3. **Y tế** - Thông tin y tế
4. **Giáo dục** - Dữ liệu giáo dục
5. **Cơ sở hạ tầng** - Thông tin cơ sở hạ tầng
6. **Công nghệ số** - Dữ liệu công nghệ số
7. **Dân số của các dân tộc** - Chi tiết dân tộc
8. **Thôn và HTX** - Thông tin thôn và HTX
9. **Thông tin các trường học** - Chi tiết trường học

## ⚠️ Lưu ý quan trọng

### Bảo mật:
- Thay đổi mật khẩu admin trong file `Back END/app.py`
- Backup database trước khi thực hiện thay đổi lớn
- Không chia sẻ thông tin đăng nhập

### Khi gặp lỗi:
1. **Không kết nối được database**: Kiểm tra SQL Server đã chạy chưa
2. **Lỗi đăng nhập**: Kiểm tra thông tin username/password
3. **Không hiển thị dữ liệu**: Kiểm tra kết nối backend
4. **Lỗi thêm/sửa/xóa**: Kiểm tra quyền database

## 🔧 Test nhanh

### Test kết nối database:
```
GET http://localhost:5000/api/test-connection
```

### Test đăng nhập admin:
```bash
curl -X POST http://localhost:5000/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Test lấy danh sách bảng:
```
GET http://localhost:5000/api/admin/tables
```

## 📱 Giao diện

### Responsive Design:
- **Desktop**: Giao diện đầy đủ với sidebar
- **Tablet**: Tối ưu cho màn hình trung bình  
- **Mobile**: Giao diện tối ưu cho điện thoại

### Tính năng UI:
- ✅ Modal forms cho thêm/sửa
- ✅ Xác nhận trước khi xóa
- ✅ Tìm kiếm trong bảng
- ✅ Loading states
- ✅ Thông báo lỗi/thành công
- ✅ Giao diện hiện đại

## 🎯 Demo

### Quy trình demo:
1. Khởi động backend
2. Mở trang chính
3. Click nút admin
4. Đăng nhập với admin/admin123
5. Chọn bảng "Dân số của các dân tộc"
6. Thêm một dân tộc mới
7. Sửa thông tin dân tộc
8. Xóa dân tộc (test)
9. Tìm kiếm trong bảng

---

**Phiên bản**: 2.0.0 (với Admin Dashboard)  
**Cập nhật**: Thêm hệ thống quản trị database trực tiếp 