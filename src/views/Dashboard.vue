<template>
  <component :is="currentLayout">
    <div class="dashboard-wrapper">
      <div class="page-header">
        <div class="title-group">
          <LayoutDashboard class="title-icon" />
          <div>
            <h2>Bảng Điều Khiển</h2>
            <p class="text-muted mt-1 mb-0">
              Chào mừng bạn quay lại. Dưới đây là các chức năng dành riêng cho
              vai trò của bạn.
            </p>
          </div>
        </div>
      </div>

      <div v-if="canAccessInventory" class="dashboard-section">
        <!-- <h3 class="section-title">📦 Nghiệp Vụ Kho Bãi</h3> -->
        <div class="card-grid">
          <div
            class="action-card"
            @click="$router.push('/inventory/transaction')"
          >
            <div class="icon-wrapper bg-amber-light text-amber">
              <Archive class="icon-lg" />
            </div>
            <div class="card-content">
              <h4>Lập Phiếu Kho</h4>
              <p>Tạo mới phiếu yêu cầu Nhập, Xuất, hoặc Trả hàng.</p>
            </div>
          </div>

          <div class="action-card" @click="$router.push('/inventory/history')">
            <div class="icon-wrapper bg-green-light text-green">
              <History class="icon-lg" />
            </div>
            <div class="card-content">
              <h4>Lịch Sử Giao Dịch</h4>
              <p>Tra cứu chi tiết, tải Excel các phiếu đã hoàn tất.</p>
            </div>
          </div>

          <div
            v-if="canAccessStats"
            class="action-card"
            @click="$router.push('/inventory/dashboard')"
          >
            <div class="icon-wrapper bg-blue-light text-blue">
              <BarChart3 class="icon-lg" />
            </div>
            <div class="card-content">
              <h4>Thống Kê Tồn Kho</h4>
              <p>Xem biểu đồ báo cáo số lượng tồn kho theo lô.</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isAdmin" class="dashboard-section mt-5">
        <!-- <h3 class="section-title">⚙️ Quản Trị Hệ Thống</h3> -->
        <div class="card-grid">
          <div class="action-card" @click="$router.push('/admin/users')">
            <div class="icon-wrapper bg-purple-light text-purple">
              <Users class="icon-lg" />
            </div>
            <div class="card-content">
              <h4>Quản Lý Người Dùng</h4>
              <p>Thêm, sửa, xóa và cấp tài khoản cho nhân viên.</p>
            </div>
          </div>

          <div class="action-card" @click="$router.push('/admin/roles')">
            <div class="icon-wrapper bg-indigo-light text-indigo">
              <ShieldCheck class="icon-lg" />
            </div>
            <div class="card-content">
              <h4>Quản Lý Vai Trò</h4>
              <p>Thiết lập các nhóm quyền (Role) trong hệ thống.</p>
            </div>
          </div>

          <div class="action-card" @click="$router.push('/admin/permissions')">
            <div class="icon-wrapper bg-rose-light text-rose">
              <Key class="icon-lg" />
            </div>
            <div class="card-content">
              <h4>Quản Lý Chức Năng</h4>
              <p>Cấu hình mã quyền hạn cho từng tác vụ phần mềm.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </component>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

import AdminLayout from '../layouts/AdminLayout.vue';
import DefaultLayout from '../layouts/DefaultLayout.vue';

import {
  LayoutDashboard,
  FileText,
  Users,
  ShieldCheck,
  Key,
  Archive,
  History,
  BarChart3,
} from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();

const currentLayout = computed(() => {
  if (authStore.hasPermission('FUNC_ADMIN_ALL')) {
    return AdminLayout;
  }
  return DefaultLayout;
});

// Kiểm tra quyền Admin
const isAdmin = computed(() => authStore.hasPermission('FUNC_ADMIN_ALL'));

// Kiểm tra quyền truy cập kho chung (Lập phiếu, Lịch sử)
const canAccessInventory = computed(() => {
  const inventoryPermissions = [
    'FUNC_VIP_NHAP_MOI',
    'FUNC_VIP_XUAT_MOI',
    'FUNC_VIP_NHAP_CU',
    'FUNC_VIP_XUAT_CU',
    'FUNC_THUONG_NHAP',
    'FUNC_THUONG_XUAT',
    'FUNC_LE_NHAP',
    'FUNC_LE_XUAT',
  ];
  return (
    isAdmin.value ||
    inventoryPermissions.some((perm) => authStore.hasPermission(perm))
  );
});

// Kiểm tra quyền truy cập Thống kê (Chỉ Admin hoặc Kho Thường/Lẻ)
const canAccessStats = computed(() => {
  const statPermissions = [
    'FUNC_THUONG_NHAP',
    'FUNC_THUONG_XUAT',
    'FUNC_LE_NHAP',
    'FUNC_LE_XUAT',
  ];
  return (
    isAdmin.value ||
    statPermissions.some((perm) => authStore.hasPermission(perm))
  );
});
</script>

<style scoped>
.dashboard-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 2rem;
}

.page-header {
  margin-bottom: 2.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #0f3d26;
}

.title-icon {
  width: 36px;
  height: 36px;
  color: #2e7d32;
  background: #f0fdf4;
  padding: 6px;
  border-radius: 10px;
}

.title-group h2 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
}

/* Các Section Nhóm */
.dashboard-section {
  margin-bottom: 2.5rem;
}

.section-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 1.25rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Lưới Thẻ Chức Năng */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border-color: #cbd5e1;
}

/* Icon trong Thẻ */
.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-lg {
  width: 24px;
  height: 24px;
}

/* Nội dung Text trong Thẻ */
.card-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #1e293b;
  font-weight: 600;
}

.card-content p {
  margin: 0;
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.4;
}

/* --- BẢNG MÀU HIỆN ĐẠI TỪ TAILWIND --- */
.bg-amber-light {
  background-color: #fef3c7;
}
.text-amber {
  color: #d97706;
}

.bg-green-light {
  background-color: #dcfce7;
}
.text-green {
  color: #15803d;
}

.bg-blue-light {
  background-color: #e0f2fe;
}
.text-blue {
  color: #0369a1;
}

.bg-gray-light {
  background-color: #f1f5f9;
}
.text-gray {
  color: #475569;
}

.bg-purple-light {
  background-color: #f3e8ff;
}
.text-purple {
  color: #7e22ce;
}

.bg-indigo-light {
  background-color: #e0e7ff;
}
.text-indigo {
  color: #4338ca;
}

.bg-rose-light {
  background-color: #ffe4e6;
}
.text-rose {
  color: #be123c;
}
</style>
