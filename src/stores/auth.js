import { defineStore } from 'pinia';
import apiClient from '../utils/axios';
import { useToast } from '../composables/useToast';
import router from '../router';

let logoutTimer = null;

// ==========================================
// HÀM GIẢI MÃ JWT (Viết bên ngoài Store cho gọn)
// ==========================================
const parseJwt = (token) => {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
};

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('access_token') || null,
        user: null,
        roles: [],
        permissions: [],
    }),

    getters: {
        isAuthenticated: (state) => !!state.token,

        hasPermission: (state) => (permissionCode) => {
            if (state.permissions.includes('FUNC_ADMIN_ALL')) return true;
            return state.permissions.includes(permissionCode);
        }
    },

    actions: {
        // ==========================================
        // HÀM CÀI ĐẶT ĐỒNG HỒ ĐẾM NGƯỢC (TỰ ĐỘNG KICK)
        // ==========================================
        setupAutoLogout() {
            // 1. Dọn dẹp đồng hồ cũ nếu có (tránh chạy song song nhiều timer)
            if (logoutTimer) {
                clearTimeout(logoutTimer);
                logoutTimer = null;
            }

            if (!this.token) return;

            // 2. Giải mã token lấy hạn sử dụng
            const decodedToken = parseJwt(this.token);
            if (!decodedToken || !decodedToken.exp) return;

            const expirationTimeMs = decodedToken.exp * 1000;
            const currentTimeMs = Date.now();
            const timeUntilExpiry = expirationTimeMs - currentTimeMs;

            // 3. Xử lý thời gian
            if (timeUntilExpiry <= 0) {
                // Đã hết hạn -> Đá ra ngay
                this.logout(true);
            } else {

                logoutTimer = setTimeout(() => {
                    const toast = useToast();
                    toast.info("Phiên đăng nhập đã tự động kết thúc. Vui lòng đăng nhập lại!");
                    this.logout(true); // Truyền true để báo đây là do máy tự auto-logout
                }, timeUntilExpiry);
            }
        },

        // 1. HÀM ĐĂNG NHẬP
        async login(username, password) {
            try {
                const params = new URLSearchParams();
                params.append('grant_type', 'password');
                params.append('username', username);
                params.append('password', password);

                const response = await apiClient.post('/api/auth/login', params, {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                });

                this.token = response.data.access_token;
                localStorage.setItem('access_token', this.token);

                // KÍCH HOẠT HẸN GIỜ SAU KHI ĐĂNG NHẬP
                this.setupAutoLogout();

                await this.fetchMyProfile();
                return true;
            } catch (error) {
                console.error("Lỗi đăng nhập:", error);
                throw error;
            }
        },

        // 2. HÀM LẤY PROFILE & QUYỀN
        async fetchMyProfile() {
            if (!this.token) return;
            try {
                // NẾU LÀ ẤN F5 RELOAD TRANG -> BẬT LẠI ĐỒNG HỒ
                this.setupAutoLogout();

                const response = await apiClient.get('/api/users/me');
                this.user = {
                    id: response.data.id,
                    username: response.data.username,
                    full_name: response.data.full_name
                };
                this.roles = response.data.roles;

                const perms = [];
                response.data.roles.forEach(role => {
                    role.permissions.forEach(p => {
                        if (!perms.includes(p.code)) perms.push(p.code);
                    });
                });
                this.permissions = perms;

            } catch (error) {
                // console.error("Lỗi lấy thông tin cá nhân:", error);
                this.logout(true); // Nếu token hỏng trên server thì ép văng
            }
        },

        // 3. HÀM ĐĂNG XUẤT
        logout(isAutoLogout = false) {
            // 1. Đập vỡ đồng hồ
            if (logoutTimer) {
                clearTimeout(logoutTimer);
                logoutTimer = null;
            }

            // 2. Xóa sạch RAM và Ổ cứng
            this.token = null;
            this.user = null;
            this.roles = [];
            this.permissions = [];
            localStorage.removeItem('access_token');

            // 3. Đẩy về trang Login
            if (router.currentRoute.value.path !== '/login') {
                router.push('/login');
            }

            // 4. Nếu người dùng tự bấm nút Đăng Xuất thì hiện thông báo
            if (!isAutoLogout) {
                const toast = useToast();
                toast.success("Đã đăng xuất thành công!");
            }
        }
    }
});