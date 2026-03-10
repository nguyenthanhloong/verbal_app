<template>
  <div class="app-wrapper">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <img
          src="../assets/CompanyLogo4.png"
          alt="SpeedUp Logo"
          class="sidebar-logo"
        />
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item">
          <LayoutDashboard class="nav-icon" /> Dashboard
        </router-link>

        <div class="nav-group">QUẢN TRỊ HỆ THỐNG</div>

        <router-link
          to="/admin/users"
          class="nav-item"
          v-permission="'FUNC_ADMIN_ALL'"
        >
          <Users class="nav-icon" /> Người Dùng
        </router-link>

        <router-link
          to="/admin/roles"
          class="nav-item"
          v-permission="'FUNC_ADMIN_ALL'"
        >
          <ShieldCheck class="nav-icon" /> Vai Trò (Roles)
        </router-link>

        <router-link
          to="/admin/permissions"
          class="nav-item"
          v-permission="'FUNC_ADMIN_ALL'"
        >
          <Key class="nav-icon" /> Chức Năng (Perms)
        </router-link>
      </nav>
    </aside>

    <div class="main-content">
      <header class="topbar">
        <div class="topbar-left"></div>
        <div class="user-profile" v-if="authStore.user">
          <div class="avatar"><User class="avatar-icon" /></div>
          <span class="user-name">{{ authStore.user.full_name }}</span>
          <button
            @click="showLogoutConfirm = true"
            class="btn-logout"
            title="Đăng xuất"
          >
            <LogOut class="logout-icon" />
          </button>
        </div>
      </header>

      <main class="page-content">
        <slot></slot>
      </main>
    </div>

    <ConfirmModal
      :isOpen="showLogoutConfirm"
      title="Xác nhận Đăng xuất"
      message="Bạn có chắc chắn muốn kết thúc phiên làm việc và đăng xuất khỏi hệ thống?"
      confirmButtonClass="btn-danger"
      @confirm="executeLogout"
      @cancel="showLogoutConfirm = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import ConfirmModal from '../components/ConfirmModal.vue'; // Đảm bảo đường dẫn này đúng

import {
  Database,
  LayoutDashboard,
  Users,
  ShieldCheck,
  Key,
  User,
  LogOut,
} from 'lucide-vue-next';

const authStore = useAuthStore();
const router = useRouter();

// Biến điều khiển ẩn/hiện popup
const showLogoutConfirm = ref(false);

// Hàm thực thi đăng xuất
const executeLogout = () => {
  showLogoutConfirm.value = false;
  authStore.logout();
};
</script>

<style scoped>
.app-wrapper {
  display: flex;
  height: 100vh;
  background-color: #f5f7fa;
  overflow: hidden;
}

.sidebar {
  width: 260px;
  background-color: #0f3d26;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  box-shadow: 4px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 10;
}
.sidebar-logo {
  max-height: 65px;
  width: auto;
  object-fit: contain;
  margin-left: 40px;
}

.sidebar-brand {
  height: 70px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  border-bottom: 1px solid #2e5c46;
}
.sidebar-brand h2 {
  margin: 0;
  color: #fff;
  font-size: 1.25rem;
  letter-spacing: 1px;
}
.brand-icon {
  width: 24px;
  height: 24px;
  color: #4caf50;
}

.sidebar-nav {
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.nav-group {
  font-size: 0.75rem;
  color: #aaaaaa;
  text-transform: uppercase;
  margin: 1rem 0 0.5rem 0.5rem;
  font-weight: bold;
  letter-spacing: 0.5px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #e0e0e0;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;
  font-weight: 500;
}
.nav-item:hover {
  background-color: #1d3b2e;
  color: #fff;
}
.nav-item.router-link-active {
  background-color: #2e7d32;
  color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.nav-icon {
  width: 18px;
  height: 18px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.topbar {
  height: 70px;
  background-color: #ffffff;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
  z-index: 5;
}
.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.avatar {
  width: 36px;
  height: 36px;
  background-color: #e0e0e0;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #0f3d26;
}
.avatar-icon {
  width: 20px;
  height: 20px;
}
.user-name {
  font-weight: 600;
  color: #333;
}
.btn-logout {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background 0.2s;
  display: flex;
  align-items: center;
}
.btn-logout:hover {
  background: rgba(239, 68, 68, 0.1);
}
.logout-icon {
  width: 20px;
  height: 20px;
}

.page-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

/* Thêm class nút màu đỏ cho ConfirmModal */
:deep(.btn-danger) {
  background-color: #ef4444 !important;
  color: white !important;
  border: none !important;
}
:deep(.btn-danger:hover) {
  background-color: #dc2626 !important;
}
</style>
