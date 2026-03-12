import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// Định nghĩa các trang trong hệ thống
const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: { requiresAuth: false }
    },
    {
        path: '/',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { requiresAuth: true }
    },

    // ========================================================
    // THÊM TRANG QUẢN LÝ KHO (INVENTORY HUB) VÀO ĐÂY
    // ========================================================
    {
        path: '/inventory/transaction',
        name: 'InventoryTransaction',
        component: () => import('../views/InventoryTransaction.vue'),
        meta: {
            requiresAuth: true,
            // Chấp nhận MẢNG QUYỀN: Có bất kỳ quyền nào liên quan đến kho thì được vào trang này
            requiresAnyPermission: [
                'FUNC_VIP_NHAP_MOI',
                'FUNC_VIP_XUAT_MOI',
                'FUNC_VIP_NHAP_CU',
                'FUNC_VIP_XUAT_CU',
                'FUNC_THUONG_NHAP',
                'FUNC_THUONG_XUAT',
                'FUNC_LE_NHAP',
                'FUNC_LE_XUAT'
            ]
        }
    },

    // ========================================================
    // TRANG LỊCH SỬ GIAO DỊCH (VỪA THÊM)
    // ========================================================
    {
        path: '/inventory/history',
        name: 'InventoryHistory',
        component: () => import('../views/InventoryHistory.vue'),
        meta: {
            requiresAuth: true,
            // Copy y hệt mảng quyền của trang Transaction
            requiresAnyPermission: [
                'FUNC_VIP_NHAP_MOI',
                'FUNC_VIP_XUAT_MOI',
                'FUNC_VIP_NHAP_CU',
                'FUNC_VIP_XUAT_CU',
                'FUNC_THUONG_NHAP',
                'FUNC_THUONG_XUAT',
                'FUNC_LE_NHAP',
                'FUNC_LE_XUAT'
            ]
        }
    },

    {
        path: '/inventory/dashboard',
        name: 'InventoryDashboard',
        component: () => import('../views/InventoryDashboard.vue'),
        meta: {
            requiresAuth: true,
            requiresAnyPermission: [
                'FUNC_ADMIN_ALL',
                'FUNC_THUONG_NHAP', 'FUNC_THUONG_XUAT',
                'FUNC_LE_NHAP', 'FUNC_LE_XUAT'
            ]
        }
    },


    // ========================================================
    // NHÓM TRANG QUẢN TRỊ ADMIN (Chỉ dành cho Super Admin)
    // ========================================================
    {
        path: '/admin/roles',
        name: 'RoleManagement',
        component: () => import('../views/AdminRoles.vue'),
        meta: { requiresAuth: true, requiresPermission: 'FUNC_ADMIN_ALL' }
    },
    {
        path: '/admin/users',
        name: 'UserManagement',
        component: () => import('../views/AdminUsers.vue'),
        meta: { requiresAuth: true, requiresPermission: 'FUNC_ADMIN_ALL' }
    },
    {
        path: '/admin/permissions',
        name: 'PermissionManagement',
        component: () => import('../views/AdminPermissions.vue'),
        meta: { requiresAuth: true, requiresPermission: 'FUNC_ADMIN_ALL' }
    },
    // ========================================================
    // NHÓM TRANG DANH MỤC (MASTER DATA)
    // ========================================================
    {
        path: '/admin/customers',
        name: 'CustomerManagement',
        component: () => import('../views/CustomerManagement.vue'),
        meta: {
            requiresAuth: true,
            // Cho phép Admin HOẶC nhân viên có quyền Quản lý Khách hàng
            requiresAnyPermission: ['FUNC_ADMIN_ALL', 'FUNC_CUSTOMER_MGR']
        }
    },
    {
        path: '/admin/locations',
        name: 'ViTriKhoManagement',
        component: () => import('../views/ViTriKhoManagement.vue'),
        meta: {
            requiresAuth: true,
            requiresAnyPermission: ['FUNC_ADMIN_ALL', 'FUNC_CUSTOMER_MGR']
        }
    },

    // TRANG BÁO LỖI
    {
        path: '/403',
        name: 'Forbidden',
        component: () => import('../views/Forbidden.vue')
    },
    {
        path: '/:pathMatch(.*)*', // Cú pháp của Vue Router v4 để bắt mọi URL không khớp
        name: 'NotFound',
        redirect: '/' // Tự động đẩy về trang chủ
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// ========================================================
// KẺ GÁC CỔNG (NAVIGATION GUARDS)
// ========================================================
router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore();
    const isAuthenticated = authStore.isAuthenticated;

    // 1. Chặn chưa đăng nhập
    if (to.meta.requiresAuth && !isAuthenticated) {
        return next('/login');
    }

    // 2. Chặn login lại khi đã có phiên
    if (to.path === '/login' && isAuthenticated) {
        return next('/');
    }

    // 3. Phục hồi dữ liệu Pinia khi bấm F5 (Refresh)
    if (isAuthenticated && !authStore.user) {
        try {
            await authStore.fetchMyProfile();
        } catch (error) {
            authStore.logout();
            return next('/login');
        }
    }

    // 4. KIỂM TRA PHÂN QUYỀN (AUTHORIZATION) TỐI ƯU

    // 4.1. Dành cho trang yêu cầu đúng 1 quyền cụ thể (Ví dụ: Trang Admin)
    if (to.meta.requiresPermission) {
        if (!authStore.hasPermission(to.meta.requiresPermission)) {
            console.warn(`Chặn truy cập! Thiếu quyền: ${to.meta.requiresPermission}`);
            return next('/403');
        }
    }

    // 4.2. Dành cho trang chấp nhận nhiều quyền (Ví dụ: Trang Lập Phiếu Kho)
    if (to.meta.requiresAnyPermission) {
        // Dùng hàm .some() của Javascript: Chỉ cần 1 quyền thỏa mãn là trả về true
        const hasAccess = to.meta.requiresAnyPermission.some(permission =>
            authStore.hasPermission(permission)
        );

        if (!hasAccess) {
            console.warn(`Chặn truy cập! Cần ít nhất 1 trong các quyền: ${to.meta.requiresAnyPermission.join(', ')}`);
            return next('/403');
        }
    }

    // Vượt qua mọi trạm gác -> Cho phép chuyển trang
    next();
});

export default router;