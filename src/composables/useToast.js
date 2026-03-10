import { ref } from 'vue';

// Khai báo state ở bên ngoài để nó trở thành Global State (dùng chung cho mọi component)
const toasts = ref([]);
let toastId = 0;

export function useToast() {
    const addToast = (message, type = 'success', duration = 3000) => {
        const id = toastId++;
        toasts.value.push({ id, message, type });

        // Tự động xóa Toast sau thời gian duration (mặc định 3 giây)
        setTimeout(() => {
            removeToast(id);
        }, duration);
    };

    const removeToast = (id) => {
        toasts.value = toasts.value.filter((t) => t.id !== id);
    };

    // Các hàm viết sẵn cho tiện sử dụng
    const success = (message, duration) => addToast(message, 'success', duration);
    const error = (message, duration) => addToast(message, 'error', duration);
    const info = (message, duration) => addToast(message, 'info', duration);

    return { toasts, success, error, removeToast, info };
}