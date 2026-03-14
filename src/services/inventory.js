// src/services/inventory.js
import apiClient from '../utils/axios';

export const inventoryService = {
    // =========================================================================
    // 1. NHÓM API KHÁCH HÀNG VIP (Quản lý đích danh theo Serial)
    // =========================================================================

    // Nhập hàng mới (Tạo ID thiết bị mới hoặc giữ nguyên ID cũ nếu đã tồn tại)
    importNewVip: (payload) =>
        apiClient.post('/api/warehouse/vip/import-new', payload),

    // Yêu cầu xuất hàng mới (Tự động copy ngày nhập sang bảng xuất)
    exportNewVip: (payload) =>
        apiClient.post('/api/warehouse/vip/export-new', payload),

    // Khách hàng trả lại hàng cũ (Dựa vào Serial truy ngược ID gốc)
    importOldVip: (payload) =>
        apiClient.post('/api/warehouse/vip/import-old', payload),

    // Xuất trả nhà cung cấp hàng cũ (Copy ngày của kho cũ)
    exportOldVip: (payload) =>
        apiClient.post('/api/warehouse/vip/export-old', payload),


    // =========================================================================
    // 2. NHÓM API KHÁCH HÀNG THƯỜNG (Quản lý theo Lô + Có Mã SP - Thuật toán FIFO)
    // =========================================================================

    // Nhập lô hàng mới
    importRegular: (payload) =>
        apiClient.post('/api/warehouse/thuong/import', payload),

    // Xuất hàng (Backend sẽ tự động chạy FIFO vét cạn các lô cũ)
    exportRegular: (payload) =>
        apiClient.post('/api/warehouse/thuong/export', payload),


    // =========================================================================
    // 3. NHÓM API KHÁCH HÀNG LẺ (Quản lý theo Lô + KHÔNG Mã SP - Thuật toán FIFO)
    // =========================================================================

    // Nhập lô hàng lẻ
    importRetail: (payload) =>
        apiClient.post('/api/warehouse/le/import', payload),

    // Xuất hàng lẻ (Backend chạy FIFO)
    exportRetail: (payload) =>
        apiClient.post('/api/warehouse/le/export', payload),

    // =========================================================================
    // 4. NHÓM API LẤY LỊCH SỬ (GET)
    // =========================================================================

    // Lịch sử VIP
    getHistoryVipImportNew: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/vip/import-new?skip=${skip}&limit=${limit}`),
    getHistoryVipExportNew: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/vip/export-new?skip=${skip}&limit=${limit}`),
    getHistoryVipImportOld: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/vip/import-old?skip=${skip}&limit=${limit}`),
    getHistoryVipExportOld: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/vip/export-old?skip=${skip}&limit=${limit}`),

    // Lịch sử Khách Thường
    getHistoryRegularImport: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/thuong/import?skip=${skip}&limit=${limit}`),
    getHistoryRegularExport: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/thuong/export?skip=${skip}&limit=${limit}`),

    // Lịch sử Khách Lẻ
    getHistoryRetailImport: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/le/import?skip=${skip}&limit=${limit}`),
    getHistoryRetailExport: (skip = 0, limit = 50) => apiClient.get(`/api/warehouse/le/export?skip=${skip}&limit=${limit}`),

    // =========================================================================
    // 5. NHÓM API THỐNG KÊ TỒN KHO
    // =========================================================================

    // Tồn kho Khách Thường
    getInventoryRegular: () => apiClient.get('/api/warehouse/thuong/ton-kho'),

    // Tồn kho Khách Lẻ
    getInventoryRetail: () => apiClient.get('/api/warehouse/le/ton-kho'),

    // 6. XUẤT EXCEL
    exportExcelVipOld: (maBill, maKho) => apiClient.get(`/api/warehouse/vip/export-old/excel/${maBill}?ma_kho_spl=${maKho}`, { responseType: 'blob' }),
    exportExcelVipNew: (maBill, maKho) => apiClient.get(`/api/warehouse/vip/export-new/excel/${maBill}?ma_kho_spl=${maKho}`, { responseType: 'blob' }),

    exportExcelRegular: (maBill, maKho) => apiClient.get(`/api/warehouse/thuong/export/excel/${maBill}?ma_kho_spl=${maKho}`, { responseType: 'blob' }),
    exportExcelRetail: (maBill, maKho) => apiClient.get(`/api/warehouse/le/export/excel/${maBill}?ma_kho_spl=${maKho}`, { responseType: 'blob' }),

    // THÊM API GỌI BIỂU ĐỒ
    getChartDataRegular: (timeRange = '7_days') => apiClient.get(`/api/warehouse/thuong/chart?time_range=${timeRange}`),
    getChartDataRetail: (timeRange = '7_days') => apiClient.get(`/api/warehouse/le/chart?time_range=${timeRange}`), // <--- Dòng mới


    checkVipSerial: (serial) => apiClient.get(`/api/warehouse/vip/check-serial/${serial}`),
};