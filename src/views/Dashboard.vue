<template>
  <component :is="currentLayout">
    <div class="dashboard-wrapper">
      <div class="welcome-banner">
        <div class="banner-content">
          <div class="banner-text">
            <h2>
              Xin chào, {{ authStore.user?.full_name || 'Nhân viên' }}! 👋
            </h2>
            <p>
              Chào mừng bạn đến với Hệ thống Quản trị Kho hàng SpeedUp. Chúc bạn
              một ngày làm việc hiệu quả.
            </p>
          </div>
          <div class="banner-date">
            <CalendarDays class="date-icon" />
            <span>{{ currentDate }}</span>
          </div>
        </div>
      </div>

      <div v-if="hasNoPermissions" class="empty-state-container">
        <div class="empty-illustration">
          <ShieldAlert class="empty-icon-main" />
        </div>
        <h3>Chưa được cấp quyền truy cập</h3>
        <p class="text-muted text-center max-w-md">
          Tài khoản của bạn hiện chưa được phân bổ vào nhóm quyền hạn nào để
          thực hiện nghiệp vụ. Vui lòng liên hệ
          <strong>Quản trị viên (Admin)</strong> hoặc
          <strong>Quản lý kho</strong> để được hỗ trợ cấp quyền.
        </p>
        <button class="btn-contact" @click="contactAdmin">
          <Mail class="btn-icon" /> Gửi yêu cầu cấp quyền
        </button>
      </div>

      <div v-else class="main-content-area">
        <div v-if="canAccessInventory" class="dashboard-section">
          <div class="section-header">
            <h3 class="section-title">📦 Nghiệp Vụ Kho Bãi</h3>
            <span class="section-divider"></span>
          </div>

          <div class="card-grid">
            <template v-for="card in inventoryCards" :key="card.route">
              <div
                v-if="card.show"
                class="action-card"
                @click="router.push(card.route)"
              >
                <div :class="['icon-wrapper', card.colorClass]">
                  <component :is="card.icon" class="icon-lg" />
                </div>
                <div class="card-content">
                  <h4>{{ card.title }}</h4>
                  <p>{{ card.description }}</p>
                </div>
                <div class="card-action">
                  <ChevronRight class="action-icon" />
                </div>
              </div>
            </template>
          </div>
        </div>

        <div v-if="canAccessMasterData" class="dashboard-section mt-5">
          <div class="section-header">
            <h3 class="section-title">📁 Danh Mục Cơ Sở</h3>
            <span class="section-divider"></span>
          </div>

          <div class="card-grid">
            <div
              v-for="card in masterDataCards"
              :key="card.route"
              class="action-card"
              @click="router.push(card.route)"
            >
              <div :class="['icon-wrapper', card.colorClass]">
                <component :is="card.icon" class="icon-lg" />
              </div>
              <div class="card-content">
                <h4>{{ card.title }}</h4>
                <p>{{ card.description }}</p>
              </div>
              <div class="card-action">
                <ChevronRight class="action-icon" />
              </div>
            </div>
          </div>
        </div>

        <div v-if="isAdmin" class="dashboard-section mt-5">
          <div class="section-header">
            <h3 class="section-title">⚙️ Quản Trị Hệ Thống</h3>
            <span class="section-divider"></span>
          </div>

          <div class="card-grid">
            <div
              v-for="card in adminCards"
              :key="card.route"
              class="action-card"
              @click="router.push(card.route)"
            >
              <div :class="['icon-wrapper', card.colorClass]">
                <component :is="card.icon" class="icon-lg" />
              </div>
              <div class="card-content">
                <h4>{{ card.title }}</h4>
                <p>{{ card.description }}</p>
              </div>
              <div class="card-action">
                <ChevronRight class="action-icon" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </component>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

import AdminLayout from '../layouts/AdminLayout.vue';
import DefaultLayout from '../layouts/DefaultLayout.vue';

// IMPORT THÊM MapPin
import {
  Users,
  ShieldCheck,
  Key,
  Archive,
  History,
  BarChart3,
  ChevronRight,
  CalendarDays,
  ShieldAlert,
  Mail,
  MapPin,
} from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();

// Ngày tháng hiện tại cho Banner
const currentDate = ref(
  new Intl.DateTimeFormat('vi-VN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date())
);

// LOGIC PHÂN QUYỀN
const currentLayout = computed(() => {
  if (authStore.hasPermission('FUNC_ADMIN_ALL')) return AdminLayout;
  return DefaultLayout;
});

const isAdmin = computed(() => authStore.hasPermission('FUNC_ADMIN_ALL'));

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

// Quyền truy cập Danh Mục
const canAccessMasterData = computed(() => {
  return isAdmin.value || authStore.hasPermission('FUNC_CUSTOMER_MGR');
});

const hasNoPermissions = computed(
  () =>
    !isAdmin.value && !canAccessInventory.value && !canAccessMasterData.value
);

const contactAdmin = () => {
  alert('Đã gửi yêu cầu cấp quyền đến Quản trị viên!');
};

// CẤU HÌNH DỮ LIỆU HIỂN THỊ
const inventoryCards = computed(() => [
  {
    title: 'Lập Phiếu Kho',
    description: 'Tạo mới phiếu yêu cầu Nhập, Xuất, hoặc Trả hàng.',
    route: '/inventory/transaction',
    icon: Archive,
    colorClass: 'bg-amber-light text-amber',
    show: true,
  },
  {
    title: 'Lịch Sử Giao Dịch',
    description: 'Tra cứu chi tiết, tải Excel các phiếu đã hoàn tất.',
    route: '/inventory/history',
    icon: History,
    colorClass: 'bg-green-light text-green',
    show: true,
  },
  {
    title: 'Thống Kê Tồn Kho',
    description: 'Xem biểu đồ báo cáo số lượng tồn kho theo lô.',
    route: '/inventory/dashboard',
    icon: BarChart3,
    colorClass: 'bg-blue-light text-blue',
    show: canAccessStats.value,
  },
]);

// CẤU HÌNH CARD DANH MỤC
const masterDataCards = [
  {
    title: 'Khách Hàng & Đối Tác',
    description: 'Quản lý thông tin, địa chỉ, SĐT của khách hàng.',
    route: '/admin/customers',
    icon: Users,
    colorClass: 'bg-emerald-light text-emerald',
  },
  {
    title: 'Danh Mục Kho Hàng',
    description: 'Thiết lập các vị trí chi nhánh kho trên hệ thống.',
    route: '/admin/locations',
    icon: MapPin,
    colorClass: 'bg-orange-light text-orange',
  },
];

const adminCards = [
  {
    title: 'Quản Lý Người Dùng',
    description: 'Thêm, sửa, thu hồi vai trò và cấp tài khoản cho nhân viên.',
    route: '/admin/users',
    icon: Users,
    colorClass: 'bg-purple-light text-purple',
  },
  {
    title: 'Quản Lý Vai Trò',
    description: 'Thiết lập các nhóm quyền (Role) trong hệ thống.',
    route: '/admin/roles',
    icon: ShieldCheck,
    colorClass: 'bg-indigo-light text-indigo',
  },
  {
    title: 'Quản Lý Chức Năng',
    description: 'Cấu hình mã quyền hạn cho từng tác vụ phần mềm.',
    route: '/admin/permissions',
    icon: Key,
    colorClass: 'bg-rose-light text-rose',
  },
];
</script>

<style scoped>
/* Giới hạn max-width ở 1100px để giao diện tập trung, không bị loãng */
.dashboard-wrapper {
  max-width: 1100px;
  margin: 0 auto;
  padding-bottom: 2rem;
  animation: fadeIn 0.4s ease-out;
}

.mt-5 {
  margin-top: 2rem;
}

/* BANNER CHÀO MỪNG */
.welcome-banner {
  background: linear-gradient(135deg, #0f3d26 0%, #1a5c3a 100%);
  border-radius: 16px;
  padding: 2rem;
  color: white;
  margin-bottom: 2.5rem;
  box-shadow: 0 10px 15px -3px rgba(15, 61, 38, 0.2);
}

.banner-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.banner-text h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
}

.banner-text p {
  margin: 0;
  color: white;
  font-size: 1rem;
}

.banner-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  backdrop-filter: blur(4px);
  font-size: 0.95rem;
  font-weight: 500;
}

.date-icon {
  width: 18px;
  height: 18px;
}

/* CÁC SECTION VÀ CARD */
.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #334155;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section-divider {
  flex-grow: 1;
  height: 1px;
  background: linear-gradient(90deg, #e2e8f0 0%, transparent 100%);
}

.dashboard-section {
  margin-bottom: 3rem;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 1.25rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.02);
}

.action-card:hover {
  transform: translateY(-4px);
  border-color: #cbd5e1;
  box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.08);
}

.icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.icon-lg {
  width: 26px;
  height: 26px;
}

.card-content h4 {
  margin: 0 0 0.35rem 0;
  font-size: 1.05rem;
  font-weight: 600;
  color: #1e293b;
}
.card-content p {
  margin: 0;
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.4;
}
.card-action {
  display: flex;
  align-items: center;
  padding-left: 0.5rem;
}
.action-icon {
  width: 20px;
  height: 20px;
  color: #cbd5e1;
  transition: all 0.3s;
}
.action-card:hover .action-icon {
  color: #10b981;
  transform: translateX(4px);
}

/* Bảng màu Utility */
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

/* Thêm màu cho Danh Mục (Mới) */
.bg-emerald-light {
  background-color: #d1fae5;
}
.text-emerald {
  color: #059669;
}
.bg-orange-light {
  background-color: #ffedd5;
}
.text-orange {
  color: #ea580c;
}

/* TRẠNG THÁI TRỐNG (EMPTY STATE) */
.empty-state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: #ffffff;
  border: 1px dashed #cbd5e1;
  border-radius: 16px;
  margin-top: 1rem;
}

.empty-illustration {
  width: 80px;
  height: 80px;
  background: #fee2e2;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.empty-icon-main {
  width: 40px;
  height: 40px;
  color: #ef4444;
}
.empty-state-container h3 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  color: #1e293b;
}
.max-w-md {
  max-width: 28rem;
}
.text-center {
  text-align: center;
}

.btn-contact {
  margin-top: 2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #0f3d26;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-contact:hover {
  background: #1a5c3a;
}
.btn-icon {
  width: 18px;
  height: 18px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
