// ========================================
// SCRIPT CHÍNH CHO TRANG THỐNG KÊ XÃ XUÂN QUANG
// ========================================

// Khởi tạo khi trang web được load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Trang web thống kê xã Xuân Quang đã được khởi tạo');
    
    // Khởi tạo các chức năng
    initBackToTop();
    initSmoothScrolling();
    initDataDisplay();
    initResponsiveNavigation();
    initSidebar();
    initCollapsibleCards();
    initSubTableSearch();
    initThemeToggle(); // Thêm theme toggle
    // Thử tải dữ liệu từ database trước, nếu không được thì dùng dữ liệu mẫu
    loadDataFromDatabase();
});

// ========================================
// KHỞI TẠO SIDEBAR
// ========================================
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const main = document.querySelector('.main');

    if (!sidebar || !sidebarToggle || !sidebarClose) {
        console.error('Không tìm thấy các phần tử sidebar');
        return;
    }

    // Mở sidebar
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.add('active');
        main.classList.add('sidebar-open');
        document.body.style.overflow = 'hidden';
    });

    // Đóng sidebar
    sidebarClose.addEventListener('click', function() {
        sidebar.classList.remove('active');
        main.classList.remove('sidebar-open');
        document.body.style.overflow = '';
    });

    // Đóng sidebar khi click bên ngoài
    document.addEventListener('click', function(e) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('active');
            main.classList.remove('sidebar-open');
            document.body.style.overflow = '';
        }
    });

    // Xử lý navigation links trong sidebar
    const sidebarNavLinks = document.querySelectorAll('.sidebar-nav-link');
    sidebarNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Đóng sidebar trước khi scroll
                sidebar.classList.remove('active');
                main.classList.remove('sidebar-open');
                document.body.style.overflow = '';
                
                // Kiểm tra nếu là sub-table link
                if (this.classList.contains('sidebar-sub-link')) {
                    const cardId = this.getAttribute('data-card-id');
                    const card = document.getElementById(cardId);
                    
                    if (card) {
                        // Scroll đến card và mở nó
                        setTimeout(() => {
                            card.scrollIntoView({
                                behavior: 'smooth',
                                block: 'start'
                            });
                            
                            // Mở card nếu nó đang đóng
                            const cardContent = card.querySelector('.card-content');
                            const toggleIcon = card.querySelector('.toggle-icon');
                            
                            if (cardContent && cardContent.style.maxHeight === '0px' || !cardContent.style.maxHeight) {
                                toggleCard(cardId);
                            }
                        }, 300);
                    }
                } else {
                    // Scroll đến section bình thường
                    setTimeout(() => {
                        targetSection.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }, 300);
                }
            }
        });
    });
}

// ========================================
// CHỨC NĂNG SEARCH
// ========================================
// CHỨC NĂNG COLLAPSIBLE CARDS
// ========================================
function initCollapsibleCards() {
    const cardHeaders = document.querySelectorAll('.card-header');
    
    cardHeaders.forEach(header => {
        header.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const card = this.closest('.collapsible-card');
            if (card) {
                const cardId = card.id;
                toggleCard(cardId);
            }
        });
    });
}

function toggleCard(cardId) {
    console.log('Toggling card:', cardId);
    const card = document.getElementById(cardId);
    
    if (!card) {
        console.error('Card not found:', cardId);
        return;
    }
    
    const content = card.querySelector('.card-content');
    const icon = card.querySelector('.toggle-icon');
    
    if (!content || !icon) {
        console.error('Content or icon not found in card:', cardId);
        return;
    }
    
    if (content.classList.contains('expanded')) {
        // Thu gọn
        content.classList.remove('expanded');
        icon.classList.remove('rotated');
        console.log('Card collapsed:', cardId);
    } else {
        // Mở rộng
        content.classList.add('expanded');
        icon.classList.add('rotated');
        console.log('Card expanded:', cardId);
    }
}

// ========================================
// CHỨC NĂNG BACK TO TOP
// ========================================
function initBackToTop() {
    const backToTopButton = document.getElementById('back-to-top');
    
    // Hiển thị/ẩn button khi scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });
    
    // Xử lý click để scroll lên đầu
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ========================================
// CHỨC NĂNG SMOOTH SCROLLING
// ========================================
function initSmoothScrolling() {
    // Xử lý smooth scrolling cho navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ========================================
// CHỨC NĂNG RESPONSIVE NAVIGATION
// ========================================
function initResponsiveNavigation() {
    // Thêm active class cho navigation links khi scroll
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('.section');
        const navLinks = document.querySelectorAll('.nav-link');
        
        let current = '';
        const headerHeight = document.querySelector('.header').offsetHeight;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop - headerHeight - 100;
            const sectionHeight = section.clientHeight;
            
            if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// ========================================
// CHỨC NĂNG HIỂN THỊ DỮ LIỆU
// ========================================
function initDataDisplay() {
    // Chuẩn bị cho việc hiển thị dữ liệu từ database
    console.log('Hệ thống hiển thị dữ liệu đã sẵn sàng');
    
    // Các hàm này sẽ được gọi khi có dữ liệu từ database
    window.updateMainStats = updateMainStats;
    window.updateTableData = updateTableData;
    window.formatNumber = formatNumber;
    window.calculatePercentage = calculatePercentage;
}

// ========================================
// HÀM CẬP NHẬT THỐNG KÊ CHÍNH
// ========================================
function updateMainStats(data) {
    // Cập nhật dữ liệu cho các thống kê chính
    // data: object chứa dữ liệu từ database
    
    if (data.dienTich !== undefined) {
        document.getElementById('dien-tich').textContent = formatNumber(data.dienTich);
    }
    
    if (data.danSo !== undefined) {
        document.getElementById('dan-so').textContent = formatNumber(data.danSo);
    }
    
    if (data.tongSoDanToc !== undefined) {
        document.getElementById('tong-so-dan-toc').textContent = formatNumber(data.tongSoDanToc);
    }
    
    if (data.tonGiao !== undefined) {
        document.getElementById('ton-giao').textContent = data.tonGiao;
    }
    
    // Cập nhật thống kê kinh tế
    if (data.soHoNgheo !== undefined) {
        document.getElementById('so-ho-ngheo').textContent = formatNumber(data.soHoNgheo);
    }
    
    if (data.soHoCanNgheo !== undefined) {
        document.getElementById('so-ho-can-ngheo').textContent = formatNumber(data.soHoCanNgheo);
    }
    
    if (data.thuNhapBinhQuan !== undefined) {
        document.getElementById('thu-nhap-binh-quan').textContent = formatNumber(data.thuNhapBinhQuan);
    }
    
    if (data.soThon !== undefined) {
        document.getElementById('so-thon').textContent = formatNumber(data.soThon);
    }
    
    if (data.soHoKinhDoanhNhoLe !== undefined) {
        document.getElementById('so-ho-kinh-doanh-nho-le').textContent = formatNumber(data.soHoKinhDoanhNhoLe);
    }
    
    // Cập nhật thống kê y tế
    if (data.soTramYTe !== undefined) {
        document.getElementById('so-tram-y-te').textContent = formatNumber(data.soTramYTe);
    }
    
    if (data.soPhongKhamTuNhan !== undefined) {
        document.getElementById('so-phong-kham-tu-nhan').textContent = formatNumber(data.soPhongKhamTuNhan);
    }
    
    if (data.soLuongCanBoYTe !== undefined) {
        document.getElementById('so-luong-can-bo-y-te').textContent = formatNumber(data.soLuongCanBoYTe);
    }
    
    if (data.tyLeNguoiDanThamGiaBHYT !== undefined) {
        document.getElementById('ty-le-nguoi-dan-tham-gia-bhyt').textContent = formatNumber(data.tyLeNguoiDanThamGiaBHYT);
    }
    
    // Cập nhật thống kê giáo dục
    if (data.tongSoTruongHoc !== undefined) {
        document.getElementById('tong-so-truong-hoc').textContent = formatNumber(data.tongSoTruongHoc);
    }
    
    if (data.tongSoHocSinh !== undefined) {
        document.getElementById('tong-so-hoc-sinh').textContent = formatNumber(data.tongSoHocSinh);
    }
    
    if (data.truongChuanQG !== undefined) {
        document.getElementById('truong-chuan-qg').textContent = formatNumber(data.truongChuanQG);
    }
    
    // Cập nhật thống kê cơ sở hạ tầng
    if (data.duongGTNTDuocCungHoa !== undefined) {
        document.getElementById('duong-gtnt-duoc-cung-hoa').textContent = formatNumber(data.duongGTNTDuocCungHoa);
    }
    
    if (data.cho !== undefined) {
        document.getElementById('cho').textContent = formatNumber(data.cho);
    }
    
    if (data.nganHang !== undefined) {
        document.getElementById('ngan-hang').textContent = formatNumber(data.nganHang);
    }
    
    if (data.buuDien !== undefined) {
        document.getElementById('buu-dien').textContent = formatNumber(data.buuDien);
    }
    
    if (data.nhaVanHoa !== undefined) {
        document.getElementById('nha-van-hoa').textContent = formatNumber(data.nhaVanHoa);
    }
    
    if (data.tyLeSuDungDienAnToan !== undefined) {
        document.getElementById('ty-le-su-dung-dien-an-toan').textContent = formatNumber(data.tyLeSuDungDienAnToan);
    }
    
    if (data.tyLeSuDungNuocSach !== undefined) {
        document.getElementById('ty-le-su-dung-nuoc-sach').textContent = formatNumber(data.tyLeSuDungNuocSach);
    }
    
    // Cập nhật thống kê công nghệ số
    if (data.dichVuCongTrucTuyen !== undefined) {
        document.getElementById('dich-vu-cong-truc-tuyen').textContent = data.dichVuCongTrucTuyen;
    }
    
    if (data.doiCongNgheSoCongDong !== undefined) {
        document.getElementById('doi-cong-nghe-so-cong-dong').textContent = formatNumber(data.doiCongNgheSoCongDong);
    }
    
    if (data.tyLeHoGiaDinhCoDienThoaiDiDong !== undefined) {
        document.getElementById('ty-le-ho-gia-dinh-co-dien-thoai-di-dong').textContent = formatNumber(data.tyLeHoGiaDinhCoDienThoaiDiDong);
    }
    
    if (data.tyLeHoGiaDinhTruyCapInternet !== undefined) {
        document.getElementById('ty-le-ho-gia-dinh-truy-cap-internet').textContent = formatNumber(data.tyLeHoGiaDinhTruyCapInternet);
    }
    
    if (data.soNguoiBietSuDungCongNgheSo !== undefined) {
        document.getElementById('so-nguoi-biet-su-dung-cong-nghe-so').textContent = formatNumber(data.soNguoiBietSuDungCongNgheSo);
    }
}

// ========================================
// HÀM CẬP NHẬT DỮ LIỆU BẢNG
// ========================================
function updateTableData(tableId, data) {
    // Cập nhật dữ liệu cho các bảng con
    // tableId: ID của bảng cần cập nhật
    // data: array chứa dữ liệu từ database
    
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    
    data.forEach((row, index) => {
        const tr = document.createElement('tr');
        
        // Thêm cột STT
        const sttTd = document.createElement('td');
        sttTd.textContent = index + 1;
        tr.appendChild(sttTd);
        
        // Tạo các cột dữ liệu dựa trên cấu trúc dữ liệu
        Object.values(row).forEach(value => {
            const td = document.createElement('td');
            td.textContent = typeof value === 'number' ? formatNumber(value) : value;
            tr.appendChild(td);
        });
        
        tbody.appendChild(tr);
    });
}

// ========================================
// HÀM ĐỊNH DẠNG SỐ
// ========================================
function formatNumber(num) {
    if (num === null || num === undefined) return '0';
    
    // Định dạng số với dấu phẩy ngăn cách hàng nghìn
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// ========================================
// HÀM TÍNH PHẦN TRĂM
// ========================================
function calculatePercentage(part, total) {
    if (total === 0) return 0;
    return ((part / total) * 100).toFixed(1);
}



// ========================================
// HÀM LOAD DỮ LIỆU TỪ DATABASE
// ========================================
async function loadDataFromDatabase() {
    try {
        console.log('Đang tải dữ liệu từ database...');
        
        // Gọi API để lấy dữ liệu từ Backend
        const response = await fetch('http://localhost:5000/api/statistics');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            const data = result.data;
            
            // Cập nhật thống kê chính
            if (data.overview) {
                updateMainStats({
                    dienTich: data.overview.Dien_tich,
                    danSo: data.overview.Dan_so,
                    tongSoDanToc: data.overview.Tong_so_dan_toc,
                    tonGiao: data.overview.Ton_giao
                });
            }
            
            // Cập nhật thống kê kinh tế
            if (data.economy) {
                updateMainStats({
                    soHoNgheo: data.economy.So_ho_ngheo,
                    soHoCanNgheo: data.economy.So_ho_can_ngheo,
                    thuNhapBinhQuan: data.economy.Thu_nhap_binh_quan,
                    soThon: data.economy.So_thon,
                    soHoKinhDoanhNhoLe: data.economy.So_ho_kinh_doanh_nho_le
                });
            }
            
            // Cập nhật thống kê y tế
            if (data.health) {
                updateMainStats({
                    soTramYTe: data.health.So_tram_y_te,
                    soPhongKhamTuNhan: data.health.So_phong_kham_tu_nhan,
                    soLuongCanBoYTe: data.health.So_luong_can_bo_y_te,
                    tyLeNguoiDanThamGiaBHYT: data.health.Ty_le_nguoi_dan_tham_gia_BHYT
                });
            }
            
            // Cập nhật thống kê giáo dục
            if (data.education) {
                updateMainStats({
                    tongSoTruongHoc: data.education.Tong_so_truong_hoc,
                    tongSoHocSinh: data.education.Tong_so_hoc_sinh,
                    truongChuanQG: data.education.Truong_chuan_QG
                });
            }
            
            // Cập nhật thống kê cơ sở hạ tầng
            if (data.infrastructure) {
                updateMainStats({
                    duongGTNTDuocCungHoa: data.infrastructure.Duong_GTNT_duoc_cung_hoa,
                    cho: data.infrastructure.Cho,
                    nganHang: data.infrastructure.Ngan_hang,
                    buuDien: data.infrastructure.Buu_dien,
                    nhaVanHoa: data.infrastructure.Nha_van_hoa,
                    tyLeSuDungDienAnToan: data.infrastructure.Ty_le_su_dung_dien_an_toan,
                    tyLeSuDungNuocSach: data.infrastructure.Ty_le_su_dung_nuoc_sach
                });
            }
            
            // Cập nhật thống kê công nghệ số
            if (data.digital) {
                updateMainStats({
                    dichVuCongTrucTuyen: data.digital.Dich_vu_cong_truc_tuyen,
                    doiCongNgheSoCongDong: data.digital.Doi_cong_nghe_so_cong_dong,
                    tyLeHoGiaDinhCoDienThoaiDiDong: data.digital.Ty_le_ho_gia_dinh_co_dien_thoai_di_dong,
                    tyLeHoGiaDinhTruyCapInternet: data.digital.Ty_le_ho_gia_dinh_truy_cap_internet,
                    soNguoiBietSuDungCongNgheSo: data.digital.So_nguoi_biet_su_dung_cong_nghe_so
                });
            }
            
            // Cập nhật bảng dân tộc
            if (data.ethnic_groups && data.ethnic_groups.length > 0) {
                const ethnicData = data.ethnic_groups.map(item => ({
                    tenDanToc: item.Ten_dan_toc,
                    soLuong: item.So_luong,
                    tyLe: calculatePercentage(item.So_luong, data.overview.Dan_so)
                }));
                updateTableData('dan-so-dan-toc-table', ethnicData);
            }
            
            // Cập nhật bảng thôn và HTX
            if (data.villages_htx && data.villages_htx.length > 0) {
                const villagesData = data.villages_htx.map(item => ({
                    tenThon: item.Ten_thon,
                    soHTX: item.So_HTX,
                    quyMo: item.Quy_mo,
                    linhVucHoatDong: item.Linh_vuc_hoat_dong,
                    moHinhKinhTeHieuQua: item.Mo_hinh_kinh_te_hieu_qua
                }));
                updateTableData('thon-htx-table', villagesData);
            }
            
            // Cập nhật bảng trường học
            if (data.schools && data.schools.length > 0) {
                const schoolsData = data.schools.map(item => ({
                    tenTruong: item.Ten_truong,
                    capTruong: item.Cap_truong,
                    soLuongHocSinh: item.So_luong_hoc_sinh_cua_truong,
                    datChuanQG: item.Dat_chuan_QG
                }));
                updateTableData('truong-hoc-table', schoolsData);
            }
            
            console.log('✅ Dữ liệu đã được tải thành công từ database');
            
            // Hiển thị thông báo thành công
            showNotification('Dữ liệu đã được cập nhật từ database', 'success');
            
        } else {
            throw new Error(result.message || 'Có lỗi xảy ra khi lấy dữ liệu');
        }
        
    } catch (error) {
        console.error('❌ Lỗi khi tải dữ liệu:', error);
        
        // Hiển thị thông báo lỗi
        showNotification('Không thể kết nối với database. Vui lòng kiểm tra Backend server.', 'error');
        
        console.log('❌ Không thể tải dữ liệu từ database');
    }
}

// ========================================
// HÀM UTILITY
// ========================================
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('loading');
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('loading');
    }
}



// ========================================
// CHỨC NĂNG TÌM KIẾM TRONG BẢNG CON
// ========================================
function initSubTableSearch() {
    // Initialize search for Dân số các dân tộc table
    const danTocSearch = document.getElementById('dan-so-dan-toc-search');
    if (danTocSearch) {
        danTocSearch.addEventListener('input', function() {
            filterTableRows('dan-so-dan-toc-table', this.value, 'dan-toc');
        });
    }
    
    // Initialize search for Thôn và HTX table
    const thonHTXSearch = document.getElementById('thon-htx-search');
    if (thonHTXSearch) {
        thonHTXSearch.addEventListener('input', function() {
            filterTableRows('thon-htx-table', this.value, 'thon-htx');
        });
    }
    
    // Initialize search for Trường học table
    const truongHocSearch = document.getElementById('truong-hoc-search');
    if (truongHocSearch) {
        truongHocSearch.addEventListener('input', function() {
            filterTableRows('truong-hoc-table', this.value, 'truong-hoc');
        });
    }
}

function filterTableRows(tableId, searchQuery, tableType) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr');
    const query = searchQuery.toLowerCase().trim();
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let shouldShow = false;
        
        if (query === '') {
            // Show all rows if search is empty
            row.classList.remove('table-row-hidden');
            removeHighlights(row);
            return;
        }
        
        // Check each cell for matches
        cells.forEach(cell => {
            const cellText = cell.textContent.toLowerCase();
            if (cellText.includes(query)) {
                shouldShow = true;
                // Highlight matching text
                highlightText(cell, query);
            }
        });
        
        if (shouldShow) {
            row.classList.remove('table-row-hidden');
        } else {
            row.classList.add('table-row-hidden');
            removeHighlights(row);
        }
    });
    
    // Show "no results" message if no rows are visible
    showNoResultsMessage(tableId, query);
}

function highlightText(element, query) {
    const text = element.textContent;
    const regex = new RegExp(`(${query})`, 'gi');
    element.innerHTML = text.replace(regex, '<span class="highlight">$1</span>');
}

function removeHighlights(element) {
    const highlights = element.querySelectorAll('.highlight');
    highlights.forEach(highlight => {
        const parent = highlight.parentNode;
        parent.textContent = parent.textContent;
    });
}

function showNoResultsMessage(tableId, query) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const visibleRows = tbody.querySelectorAll('tr:not(.table-row-hidden)');
    
    // Remove existing no-results message
    const existingMessage = tbody.querySelector('.no-results-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Add no-results message if no visible rows
    if (visibleRows.length === 0 && query !== '') {
        const noResultsRow = document.createElement('tr');
        noResultsRow.className = 'no-results-message';
        noResultsRow.innerHTML = `
            <td colspan="100%" style="text-align: center; padding: 20px; color: #6c757d; font-style: italic;">
                <i class="fas fa-search"></i> Không tìm thấy kết quả cho "${query}"
            </td>
        `;
        tbody.appendChild(noResultsRow);
    }
}

// ========================================
// HÀM HIỂN THỊ THÔNG BÁO
// ========================================
function showNotification(message, type = 'info') {
    // Tạo notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Thêm vào body
    document.body.appendChild(notification);
    
    // Tự động ẩn sau 5 giây
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Export các hàm để có thể sử dụng từ bên ngoài
window.loadDataFromDatabase = loadDataFromDatabase;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.toggleCard = toggleCard;
window.showNotification = showNotification;

// ========================================
// CHỨC NĂNG THEME TOGGLE (CHẾ ĐỘ TỐI/SÁNG)
// ========================================
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    if (!themeToggle || !themeIcon) {
        console.error('Không tìm thấy theme toggle elements');
        return;
    }
    
    // Lấy theme từ localStorage hoặc mặc định là 'light'
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    // Xử lý click event
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Cập nhật theme
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
        
        console.log('Theme đã chuyển sang:', newTheme);
    });
}

function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('theme-icon');
    if (!themeIcon) return;
    
    if (theme === 'dark') {
        themeIcon.className = 'fas fa-moon';
        themeIcon.title = 'Chuyển sang chế độ sáng';
    } else {
        themeIcon.className = 'fas fa-sun';
        themeIcon.title = 'Chuyển sang chế độ tối';
    }
}

// ========================================
// WEATHER WIDGET TOGGLE FUNCTION
// ========================================
function toggleWeatherWidget() {
    const weatherWidget = document.getElementById('weatherWidget');
    if (weatherWidget) {
        weatherWidget.classList.toggle('collapsed');
        
        // Lưu trạng thái vào localStorage
        const isCollapsed = weatherWidget.classList.contains('collapsed');
        localStorage.setItem('weatherWidgetCollapsed', isCollapsed);
        
        console.log('Weather widget toggled:', isCollapsed ? 'collapsed' : 'expanded');
    }
}

// Khôi phục trạng thái widget khi load trang
document.addEventListener('DOMContentLoaded', function() {
    const weatherWidget = document.getElementById('weatherWidget');
    if (weatherWidget) {
        const isCollapsed = localStorage.getItem('weatherWidgetCollapsed') === 'true';
        if (isCollapsed) {
            weatherWidget.classList.add('collapsed');
        }
    }
});

 