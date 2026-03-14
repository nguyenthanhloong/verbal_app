import axios from 'axios';
import { useAppStore } from '../stores/app';
import { useAuthStore } from '../stores/auth';
import { useToast } from '../composables/useToast';
import router from '../router';

const apiClient = axios.create({
    baseURL: import.meta.env.MODE === 'development' ? 'http://localhost:8000' : '',
    timeout: 10000,
});

// CỜ CHỐNG BÃO LỖI: Ngăn chặn việc hiện nhiều thông báo khi nhiều API cùng tạch 401
let isSessionExpired = false;

apiClient.interceptors.request.use(
    (config) => {
        const appStore = useAppStore();
        appStore.startLoading();

        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        const appStore = useAppStore();
        appStore.stopLoading();
        return Promise.reject(error);
    }
);

apiClient.interceptors.response.use(
    (response) => {
        const appStore = useAppStore();
        appStore.stopLoading();
        return response;
    },
    (error) => {
        const appStore = useAppStore();
        appStore.stopLoading();

        // KIỂM TRA LỖI 401 (HẾT HẠN TOKEN)
        if (error.response && error.response.status === 401) {
            // Kiểm tra cờ, nếu chưa bị báo hết phiên thì mới xử lý
            if (!isSessionExpired) {
                isSessionExpired = true; // Kéo cờ lên để chặn các request 401 khác (nếu có)

                // console.error("Token hết hạn hoặc không hợp lệ. Đang đăng xuất...");

                const authStore = useAuthStore();

                // Gọi logout(true) để báo hệ thống không hiển thị toast "Đã đăng xuất thành công"
                authStore.logout(true);

                // Khởi tạo và hiển thị Toast "Hết phiên" duy nhất 1 lần
                const toast = useToast();

                if (router.currentRoute.value.path !== '/login') {
                    router.push('/login');
                }

                // Hạ cờ xuống sau 3 giây để sẵn sàng cho phiên đăng nhập tiếp theo của người dùng
                setTimeout(() => {
                    isSessionExpired = false;
                }, 3000);
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;