#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend API cho hệ thống thống kê xã Xuân Quang
Kết nối Frontend với SQL Server Database
"""

from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import pyodbc
import logging
from datetime import datetime
import hashlib
import os

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Cho phép CORS để Frontend có thể gọi API

# Cấu hình kết nối SQL Server
import os

# Lấy DATABASE_URL từ environment variable hoặc sử dụng cấu hình mặc định
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Sử dụng DATABASE_URL từ environment
    DB_CONFIG = {
        'connection_string': DATABASE_URL
    }
else:
    # Cấu hình mặc định cho local development
    DB_CONFIG = {
        'server': 'Viet',
        'database': 'Số liệu thống kê của xã Xuân Quang',
        'username': 'sa',
        'password': 'viet',
        'driver': '{ODBC Driver 17 for SQL Server}'  # Hoặc '{SQL Server}' tùy theo driver đã cài
    }

# Thông tin đăng nhập admin (trong thực tế nên lưu trong database)
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': hashlib.sha256('admin123'.encode()).hexdigest()  # Mã hóa password
}

# Danh sách các bảng trong database
DATABASE_TABLES = [
    {'name': '1. Chỉ số tổng quan của xã', 'display_name': 'Chỉ số tổng quan của xã'},
    {'name': '2. Kinh tế', 'display_name': 'Kinh tế'},
    {'name': '3. Y tế ', 'display_name': 'Y tế'},
    {'name': '4. Giáo Dục', 'display_name': 'Giáo dục'},
    {'name': '5. Cơ sở hạ tầng', 'display_name': 'Cơ sở hạ tầng'},
    {'name': '6. Công nghệ số', 'display_name': 'Công nghệ số'},
    {'name': '1.1. Dân số của các dân tộc', 'display_name': 'Dân số của các dân tộc'},
    {'name': '2.1. Thôn và HTX', 'display_name': 'Thôn và HTX'},
    {'name': '4.1. Thông tin các trường học.', 'display_name': 'Thông tin các trường học'}
]

def get_db_connection():
    """Tạo kết nối đến SQL Server"""
    try:
        if 'connection_string' in DB_CONFIG:
            # Sử dụng connection string từ DATABASE_URL
            conn = pyodbc.connect(DB_CONFIG['connection_string'])
        else:
            # Sử dụng cấu hình mặc định
            conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"UID={DB_CONFIG['username']};"
                f"PWD={DB_CONFIG['password']};"
                "Trusted_Connection=no;"
            )
            conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        logger.error(f"Lỗi kết nối database: {e}")
        return None

def execute_query(query, params=None):
    """Thực thi query và trả về kết quả"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Lấy tên cột
        columns = [column[0] for column in cursor.description]
        
        # Lấy dữ liệu
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        logger.error(f"Lỗi thực thi query: {e}")
        if conn:
            conn.close()
        return None

def execute_update(query, params=None):
    """Thực thi query cập nhật (INSERT, UPDATE, DELETE)"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Lỗi thực thi update query: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

# ===== ADMIN AUTHENTICATION =====
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """API đăng nhập admin"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Vui lòng nhập đầy đủ thông tin đăng nhập'
            }), 400
        
        # Kiểm tra thông tin đăng nhập
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if username == ADMIN_CREDENTIALS['username'] and hashed_password == ADMIN_CREDENTIALS['password']:
            return jsonify({
                'success': True,
                'message': 'Đăng nhập thành công',
                'token': 'admin_token_' + datetime.now().strftime('%Y%m%d%H%M%S')
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Tên đăng nhập hoặc mật khẩu không đúng'
            }), 401
            
    except Exception as e:
        logger.error(f"Lỗi đăng nhập admin: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Có lỗi xảy ra khi đăng nhập'
        }), 500

# ===== ADMIN DASHBOARD APIs =====
@app.route('/api/admin/tables', methods=['GET'])
def get_database_tables():
    """Lấy danh sách các bảng trong database"""
    try:
        return jsonify({
            'success': True,
            'data': DATABASE_TABLES,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Lỗi lấy danh sách bảng: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Có lỗi xảy ra khi lấy danh sách bảng'
        }), 500

@app.route('/api/admin/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    """Lấy dữ liệu của một bảng cụ thể"""
    try:
        # Kiểm tra bảng có tồn tại không
        table_exists = any(table['name'] == table_name for table in DATABASE_TABLES)
        if not table_exists:
            return jsonify({
                'success': False,
                'message': 'Bảng không tồn tại'
            }), 404
        
        query = f"SELECT * FROM [{table_name}]"
        data = execute_query(query)
        
        if data is not None:
            return jsonify({
                'success': True,
                'data': data,
                'table_name': table_name,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không thể lấy dữ liệu từ bảng'
            }), 500
            
    except Exception as e:
        logger.error(f"Lỗi lấy dữ liệu bảng {table_name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Có lỗi xảy ra khi lấy dữ liệu bảng'
        }), 500

@app.route('/api/admin/table/<table_name>/update', methods=['POST'])
def update_table_data(table_name):
    """Cập nhật dữ liệu trong bảng"""
    try:
        data = request.get_json()
        record_id = data.get('id')
        update_data = data.get('data')
        
        logger.info(f"Cập nhật bảng {table_name} với dữ liệu: {update_data}")
        
        if not update_data:
            return jsonify({
                'success': False,
                'message': 'Thiếu dữ liệu cần cập nhật'
            }), 400
        
        # Kiểm tra xem bảng có cột ID không
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': 'Không thể kết nối database'
            }), 500
        
        try:
            cursor = conn.cursor()
            
            # Lấy thông tin cột của bảng
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", (table_name,))
            columns = [row[0] for row in cursor.fetchall()]
            
            logger.info(f"Các cột trong bảng {table_name}: {columns}")
            
            # Kiểm tra xem có cột ID không
            has_id_column = 'ID' in columns or 'id' in columns
            
            if has_id_column and not record_id:
                return jsonify({
                    'success': False,
                    'message': 'Thiếu ID bản ghi cần cập nhật'
                }), 400
            
            # Lọc dữ liệu chỉ giữ lại các cột có trong bảng và loại bỏ cột ID tự động tăng
            filtered_data = {}
            for key, value in update_data.items():
                if key in columns:
                    # Loại bỏ cột ID/STT nếu nó là tự động tăng
                    if key.upper() in ['ID', 'STT']:
                        # Kiểm tra xem cột có phải là IDENTITY không
                        cursor.execute(f"""
                            SELECT COLUMNPROPERTY(OBJECT_ID('{table_name}'), '{key}', 'IsIdentity')
                        """)
                        is_identity = cursor.fetchone()[0]
                        if is_identity:
                            logger.info(f"Bỏ qua cột {key} vì nó là IDENTITY")
                            continue
                    filtered_data[key] = value
            
            logger.info(f"Dữ liệu đã lọc: {filtered_data}")
            
            if not filtered_data:
                return jsonify({
                    'success': False,
                    'message': 'Không có dữ liệu hợp lệ để cập nhật'
                }), 400
            
            # Tạo câu lệnh UPDATE
            if has_id_column:
                # Bảng có cột ID - cập nhật theo ID
                set_clauses = []
                params = []
                
                for key, value in filtered_data.items():
                    if key.upper() != 'ID':  # Không cập nhật cột ID
                        set_clauses.append(f"[{key}] = ?")
                        params.append(value)
                
                params.append(record_id)
                query = f"UPDATE [{table_name}] SET {', '.join(set_clauses)} WHERE ID = ?"
            else:
                # Bảng không có cột ID - cập nhật tất cả các bản ghi (vì chỉ có 1 bản ghi)
                set_clauses = []
                params = []
                
                for key, value in filtered_data.items():
                    set_clauses.append(f"[{key}] = ?")
                    params.append(value)
                
                query = f"UPDATE [{table_name}] SET {', '.join(set_clauses)}"
            
            logger.info(f"Query UPDATE: {query}")
            logger.info(f"Parameters: {params}")
            
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Cập nhật thành công bảng {table_name}")
            
            return jsonify({
                'success': True,
                'message': 'Cập nhật dữ liệu thành công'
            })
            
        except Exception as e:
            logger.error(f"Lỗi thực thi update query: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return jsonify({
                'success': False,
                'message': f'Lỗi cập nhật dữ liệu: {str(e)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Lỗi cập nhật dữ liệu bảng {table_name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Có lỗi xảy ra khi cập nhật dữ liệu'
        }), 500

@app.route('/api/admin/table/<table_name>/insert', methods=['POST'])
def insert_table_data(table_name):
    """Thêm dữ liệu mới vào bảng"""
    try:
        data = request.get_json()
        insert_data = data.get('data')
        
        logger.info(f"Thêm dữ liệu vào bảng {table_name} với dữ liệu: {insert_data}")
        
        if not insert_data:
            return jsonify({
                'success': False,
                'message': 'Thiếu dữ liệu cần thêm'
            }), 400
        
        # Kiểm tra xem bảng có cột ID không
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': 'Không thể kết nối database'
            }), 500
        
        try:
            cursor = conn.cursor()
            
            # Lấy thông tin cột của bảng
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", (table_name,))
            columns = [row[0] for row in cursor.fetchall()]
            
            logger.info(f"Các cột trong bảng {table_name}: {columns}")
            
            # Lọc dữ liệu chỉ giữ lại các cột có trong bảng và loại bỏ cột ID tự động tăng
            filtered_data = {}
            for key, value in insert_data.items():
                if key in columns:
                    # Loại bỏ cột ID/STT nếu nó là tự động tăng
                    if key.upper() in ['ID', 'STT']:
                        # Kiểm tra xem cột có phải là IDENTITY không
                        cursor.execute(f"""
                            SELECT COLUMNPROPERTY(OBJECT_ID('{table_name}'), '{key}', 'IsIdentity')
                        """)
                        is_identity = cursor.fetchone()[0]
                        if is_identity:
                            logger.info(f"Bỏ qua cột {key} vì nó là IDENTITY")
                            continue
                    filtered_data[key] = value
            
            logger.info(f"Dữ liệu đã lọc: {filtered_data}")
            
            if not filtered_data:
                return jsonify({
                    'success': False,
                    'message': 'Không có dữ liệu hợp lệ để thêm'
                }), 400
            
            # Tạo câu lệnh INSERT
            insert_columns = list(filtered_data.keys())
            placeholders = ['?' for _ in insert_columns]
            values = list(filtered_data.values())
            
            query = f"INSERT INTO [{table_name}] ([{'], ['.join(insert_columns)}]) VALUES ({', '.join(placeholders)})"
            
            logger.info(f"Query INSERT: {query}")
            logger.info(f"Parameters: {values}")
            
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Thêm dữ liệu thành công vào bảng {table_name}")
            
            return jsonify({
                'success': True,
                'message': 'Thêm dữ liệu thành công'
            })
            
        except Exception as e:
            logger.error(f"Lỗi thực thi insert query: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return jsonify({
                'success': False,
                'message': f'Lỗi thêm dữ liệu: {str(e)}'
            }), 500
            
    except Exception as e:
        logger.error(f"Lỗi thêm dữ liệu bảng {table_name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Có lỗi xảy ra khi thêm dữ liệu'
        }), 500

@app.route('/api/admin/table/<table_name>/delete', methods=['DELETE'])
def delete_table_data(table_name):
    """Xóa dữ liệu từ bảng"""
    try:
        data = request.get_json()
        record_id = data.get('id')
        
        logger.info(f"Xóa dữ liệu bảng {table_name} với ID: {record_id}")
        
        if not record_id:
            return jsonify({
                'success': False,
                'message': 'Thiếu ID bản ghi cần xóa'
            }), 400
        
        # Kiểm tra xem bảng có cột ID không
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'message': 'Không thể kết nối database'
            }), 500
        
        try:
            cursor = conn.cursor()
            
            # Lấy thông tin cột của bảng
            cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ?", (table_name,))
            columns = [row[0] for row in cursor.fetchall()]
            
            logger.info(f"Các cột trong bảng {table_name}: {columns}")
            
            # Xác định cột ID để xóa - có thể là ID hoặc STT
            id_column = None
            if 'ID' in columns:
                id_column = 'ID'
            elif 'STT' in columns:
                id_column = 'STT'
            elif 'id' in columns:
                id_column = 'id'
            elif 'stt' in columns:
                id_column = 'stt'
            
            if not id_column:
                return jsonify({
                    'success': False,
                    'message': 'Không tìm thấy cột ID trong bảng'
                }), 400
            
            logger.info(f"Sử dụng cột {id_column} để xóa")
            
            query = f"DELETE FROM [{table_name}] WHERE [{id_column}] = ?"
            success = execute_update(query, [record_id])
            
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Xóa dữ liệu thành công'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Không thể xóa dữ liệu'
                }), 500
                
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Lỗi xóa dữ liệu bảng {table_name}: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Có lỗi xảy ra khi xóa dữ liệu'
        }), 500

# ===== EXISTING APIs =====
@app.route('/')
def home():
    """Trang chủ API"""
    return jsonify({
        'message': 'API Backend cho hệ thống thống kê xã Xuân Quang',
        'version': '1.0.0',
        'endpoints': {
            '/api/statistics': 'Lấy tất cả thống kê',
            '/api/overview': 'Lấy chỉ số tổng quan',
            '/api/economy': 'Lấy dữ liệu kinh tế',
            '/api/health': 'Lấy dữ liệu y tế',
            '/api/education': 'Lấy dữ liệu giáo dục',
            '/api/infrastructure': 'Lấy dữ liệu cơ sở hạ tầng',
            '/api/digital': 'Lấy dữ liệu công nghệ số',
            '/api/ethnic-groups': 'Lấy dữ liệu dân tộc',
            '/api/villages-htx': 'Lấy dữ liệu thôn và HTX',
            '/api/schools': 'Lấy dữ liệu trường học',
            '/admin': 'Trang quản trị admin'
        }
    })

@app.route('/admin')
def admin_dashboard():
    """Trang dashboard admin"""
    try:
        with open('admin.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Trang admin không tồn tại", 404

@app.route('/api/statistics', methods=['GET'])
def get_all_statistics():
    """Lấy tất cả thống kê từ database"""
    try:
        # Lấy chỉ số tổng quan
        overview_query = "SELECT * FROM [1. Chỉ số tổng quan của xã]"
        overview_data = execute_query(overview_query)
        
        # Lấy dữ liệu kinh tế
        economy_query = "SELECT * FROM [2. Kinh tế]"
        economy_data = execute_query(economy_query)
        
        # Lấy dữ liệu y tế
        health_query = "SELECT * FROM [3. Y tế ]"
        health_data = execute_query(health_query)
        
        # Lấy dữ liệu giáo dục
        education_query = "SELECT * FROM [4. Giáo Dục]"
        education_data = execute_query(education_query)
        
        # Lấy dữ liệu cơ sở hạ tầng
        infrastructure_query = "SELECT * FROM [5. Cơ sở hạ tầng]"
        infrastructure_data = execute_query(infrastructure_query)
        
        # Lấy dữ liệu công nghệ số
        digital_query = "SELECT * FROM [6. Công nghệ số]"
        digital_data = execute_query(digital_query)
        
        # Lấy dữ liệu dân tộc
        ethnic_query = "SELECT * FROM [1.1. Dân số của các dân tộc]"
        ethnic_data = execute_query(ethnic_query)
        
        # Lấy dữ liệu thôn và HTX
        villages_query = "SELECT * FROM [2.1. Thôn và HTX]"
        villages_data = execute_query(villages_query)
        
        # Lấy dữ liệu trường học
        schools_query = "SELECT * FROM [4.1. Thông tin các trường học.]"
        schools_data = execute_query(schools_query)
        
        # Kết hợp dữ liệu
        response_data = {
            'overview': overview_data[0] if overview_data else {},
            'economy': economy_data[0] if economy_data else {},
            'health': health_data[0] if health_data else {},
            'education': education_data[0] if education_data else {},
            'infrastructure': infrastructure_data[0] if infrastructure_data else {},
            'digital': digital_data[0] if digital_data else {},
            'ethnic_groups': ethnic_data,
            'villages_htx': villages_data,
            'schools': schools_data
        }
        
        return jsonify({
            'success': True,
            'data': response_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy thống kê: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Có lỗi xảy ra khi lấy dữ liệu từ database'
        }), 500

@app.route('/api/overview', methods=['GET'])
def get_overview():
    """Lấy chỉ số tổng quan"""
    try:
        query = "SELECT * FROM [1. Chỉ số tổng quan của xã]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data[0],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu tổng quan'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu tổng quan: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/economy', methods=['GET'])
def get_economy():
    """Lấy dữ liệu kinh tế"""
    try:
        query = "SELECT * FROM [2. Kinh tế]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data[0],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu kinh tế'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu kinh tế: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def get_health():
    """Lấy dữ liệu y tế"""
    try:
        query = "SELECT * FROM [3. Y tế ]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data[0],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu y tế'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu y tế: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/education', methods=['GET'])
def get_education():
    """Lấy dữ liệu giáo dục"""
    try:
        query = "SELECT * FROM [4. Giáo Dục]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data[0],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu giáo dục'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu giáo dục: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/infrastructure', methods=['GET'])
def get_infrastructure():
    """Lấy dữ liệu cơ sở hạ tầng"""
    try:
        query = "SELECT * FROM [5. Cơ sở hạ tầng]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data[0],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu cơ sở hạ tầng'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu cơ sở hạ tầng: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/digital', methods=['GET'])
def get_digital():
    """Lấy dữ liệu công nghệ số"""
    try:
        query = "SELECT * FROM [6. Công nghệ số]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data[0],
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu công nghệ số'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu công nghệ số: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ethnic-groups', methods=['GET'])
def get_ethnic_groups():
    """Lấy dữ liệu dân tộc"""
    try:
        query = "SELECT * FROM [1.1. Dân số của các dân tộc]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu dân tộc'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu dân tộc: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/villages-htx', methods=['GET'])
def get_villages_htx():
    """Lấy dữ liệu thôn và HTX"""
    try:
        query = "SELECT * FROM [2.1. Thôn và HTX]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu thôn và HTX'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu thôn và HTX: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/schools', methods=['GET'])
def get_schools():
    """Lấy dữ liệu trường học"""
    try:
        query = "SELECT * FROM [4.1. Thông tin các trường học.]"
        data = execute_query(query)
        
        if data:
            return jsonify({
                'success': True,
                'data': data,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không tìm thấy dữ liệu trường học'
            }), 404
            
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu trường học: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """Kiểm tra kết nối database"""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({
                'success': True,
                'message': 'Kết nối database thành công',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không thể kết nối database'
            }), 500
    except Exception as e:
        logger.error(f"Lỗi kiểm tra kết nối: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi kết nối database'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint không tồn tại',
        'message': 'Vui lòng kiểm tra lại URL'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Lỗi server nội bộ',
        'message': 'Vui lòng thử lại sau'
    }), 500

if __name__ == '__main__':
    import os
    
    # Kiểm tra xem có đang chạy trên production không
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    if debug:
        print("=" * 60)
        print("🚀 KHỞI ĐỘNG BACKEND API CHO HỆ THỐNG THỐNG KÊ XÃ XUÂN QUANG")
        print("=" * 60)
        print(f"📊 Database: {DB_CONFIG['database']}")
        print(f"🖥️  Server: {DB_CONFIG['server']}")
        print(f"👤 User: {DB_CONFIG['username']}")
        print("=" * 60)
        print("🌐 API sẽ chạy tại: http://localhost:5000")
        print("📋 Các endpoint có sẵn:")
        print("   - GET /api/statistics - Lấy tất cả thống kê")
        print("   - GET /api/overview - Chỉ số tổng quan")
        print("   - GET /api/economy - Dữ liệu kinh tế")
        print("   - GET /api/health - Dữ liệu y tế")
        print("   - GET /api/education - Dữ liệu giáo dục")
        print("   - GET /api/infrastructure - Dữ liệu cơ sở hạ tầng")
        print("   - GET /api/digital - Dữ liệu công nghệ số")
        print("   - GET /api/ethnic-groups - Dữ liệu dân tộc")
        print("   - GET /api/villages-htx - Dữ liệu thôn và HTX")
        print("   - GET /api/schools - Dữ liệu trường học")
        print("   - GET /api/test-connection - Kiểm tra kết nối DB")
        print("=" * 60)
        
        # Kiểm tra kết nối database trước khi khởi động
        print("🔍 Đang kiểm tra kết nối database...")
        conn = get_db_connection()
        if conn:
            print("✅ Kết nối database thành công!")
            conn.close()
        else:
            print("❌ Không thể kết nối database!")
            print("💡 Vui lòng kiểm tra:")
            print("   - SQL Server đã chạy chưa?")
            print("   - Thông tin đăng nhập có đúng không?")
            print("   - Driver ODBC đã cài đặt chưa?")
            print("   - Firewall có chặn kết nối không?")
        
        print("=" * 60)
    
    # Khởi động server
    app.run(host='0.0.0.0', port=port, debug=debug) 