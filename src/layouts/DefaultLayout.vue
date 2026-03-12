<template>
  <div class="default-wrapper">
    <header class="top-navbar">
      <div class="nav-brand">
        <img
          src="../assets/CompanyLogo4.png"
          alt="SpeedUp Logo"
          class="topbar-logo"
        />
      </div>

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

    <main class="main-container">
      <slot></slot>
    </main>

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
import { Package, User, LogOut } from 'lucide-vue-next';
import ConfirmModal from '../components/ConfirmModal.vue'; // Đảm bảo đường dẫn này đúng

const authStore = useAuthStore();
const router = useRouter();

// Biến điều khiển ẩn/hiện popup
const showLogoutConfirm = ref(false);

// Hàm thực thi đăng xuất khi người dùng bấm "Đồng ý"
const executeLogout = () => {
  showLogoutConfirm.value = false; // Đóng popup
  authStore.logout(); // Gọi store để xóa token
  // router.push('/login');        // Nếu trong file authStore.js đã có lệnh push rồi thì có thể bỏ dòng này
};
</script>

<style scoped>
.default-wrapper {
  min-height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.topbar-logo {
  max-height: 65px;
  width: auto;
  object-fit: contain;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.top-navbar {
  height: 70px;
  background-color: #0f3d26;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.nav-brand h2 {
  margin: 0;
  font-size: 1.3rem;
  letter-spacing: 1px;
  color: white;
}
.brand-icon {
  width: 26px;
  height: 26px;
  color: #4caf50;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.avatar {
  width: 36px;
  height: 36px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.avatar-icon {
  width: 20px;
  height: 20px;
  color: white;
}
.user-name {
  font-weight: 600;
}

.btn-logout {
  background: none;
  border: none;
  color: #f5f7fa;
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

.main-container {
  flex: 1;
  padding: 2rem;
  max-width: 1300px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
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
