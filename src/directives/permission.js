import { useAuthStore } from '../stores/auth';

export const permissionDirective = {
    // mounted là vòng đời khi thẻ HTML vừa được nhúng vào giao diện
    mounted(el, binding) {
        const authStore = useAuthStore();
        const requiredPermission = binding.value; // Lấy giá trị truyền vào (VD: 'FUNC_VIP_NHAP_MOI')

        if (!requiredPermission) return;

        // Kiểm tra xem User có quyền này không
        const hasAccess = authStore.hasPermission(requiredPermission);

        // Nếu KHÔNG CÓ QUYỀN -> Tháo gỡ thẻ HTML này khỏi giao diện (Xóa luôn khỏi DOM)
        if (!hasAccess) {
            el.parentNode && el.parentNode.removeChild(el);
        }
    }
};