<template>
  <div class="login-screen">
    <div class="login-container">
      <div class="logo-container">
        <img
          src="../assets/CompanyLogo4.png"
          alt="SpeedUp Logo"
          class="logo-image"
        />
      </div>

      <div class="form-section">
        <h2 class="login-title">Đăng nhập</h2>

        <form @submit.prevent="handleLogin">
          <div class="input-wrapper">
            <User class="input-icon" />
            <input
              type="text"
              class="input-field"
              v-model="username"
              required
              placeholder="Tài khoản"
              autocomplete="username"
            />
          </div>

          <div class="input-wrapper">
            <Lock class="input-icon" />
            <input
              :type="showPassword ? 'text' : 'password'"
              class="input-field"
              v-model="password"
              required
              placeholder="Mật khẩu"
              autocomplete="current-password"
            />
            <button
              type="button"
              class="eye-btn"
              @click="showPassword = !showPassword"
              tabindex="-1"
            >
              <Eye v-if="showPassword" class="eye-icon" />
              <EyeOff v-else class="eye-icon" />
            </button>
          </div>

          <button
            type="submit"
            class="login-btn gradient-bg"
            :disabled="isLoading"
          >
            <Loader2 v-if="isLoading" class="spinner" />
            <span v-else>ĐĂNG NHẬP</span>
          </button>
        </form>
      </div>

      <div class="footer-logos-container">
        <img
          src="../assets/CompanyLogo2.png"
          alt="Partner 1"
          class="footer-image"
        />

        <div class="footer-divider"></div>

        <img
          src="../assets/CompanyLogo3.png"
          alt="Partner 2"
          class="footer-image"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
// Sử dụng icon của Lucide giống hệt Ionicons bên App
import { User, Lock, Eye, EyeOff, Loader2 } from 'lucide-vue-next';
import { useToast } from '../composables/useToast';

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const username = ref('');
const password = ref('');
const isLoading = ref(false);
const showPassword = ref(false);

const handleLogin = async () => {
  if (!username.value || !password.value) {
    toast.error('Vui lòng nhập đủ tài khoản/mật khẩu!');
    return;
  }

  isLoading.value = true;
  try {
    await authStore.login(username.value, password.value);
    toast.success('Đăng nhập thành công!');
    router.push('/');
  } catch (error) {
    toast.error(error.response?.data?.detail || 'Sai tài khoản hoặc mật khẩu!');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* BACKGROUND TỔNG THỂ */
.login-screen {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  /* Cài đặt ảnh nền */
  background-image: url('../assets/DongSon2.png');
  background-size: cover;
  background-position: center;
  /* Phủ một lớp màu xám đè lên ảnh nền để tạo cảm giác opacity 0.08 giống hệt App */
  background-color: rgba(245, 247, 250, 0.92);
  background-blend-mode: overlay;
}

/* KHUNG CHỨA CONTENT Ở GIỮA (ĐÃ PHÓNG TO) */
.login-container {
  width: 100%;
  max-width: 480px; /* Phóng to form từ 400px lên 480px */
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* --- LOGO CÔNG TY --- */
.logo-container {
  margin-bottom: 50px;
  text-align: center;
  width: 100%;
}
.logo-image {
  width: 85%;
  max-height: 110px; /* Phóng to logo */
  object-fit: contain;
}
.fallback-logo {
  color: #0f3d26;
  font-size: 2.5rem;
  margin: 0;
  letter-spacing: 2px;
}

/* --- FORM SECTION --- */
.form-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.login-title {
  font-size: 28px; /* Chữ to hơn */
  font-weight: 700;
  color: #2e7d32;
  margin-bottom: 35px;
  margin-top: 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* --- INPUT WRAPPER --- */
form {
  width: 100%;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  width: 100%;
  height: 60px; /* Input cao hơn (chuẩn web) */
  border-radius: 14px; /* Bo góc mượt hơn */
  margin-bottom: 24px;
  padding: 0 20px;
  border: 1px solid #e0e0e0;
  box-sizing: border-box;
  box-shadow: 0 4px 12px rgba(46, 125, 50, 0.08);
  transition: all 0.3s ease;
}
.input-wrapper:focus-within {
  border-color: #4caf50;
  box-shadow: 0 4px 15px rgba(46, 125, 50, 0.2);
}

.input-icon {
  width: 24px; /* Icon to hơn */
  height: 24px;
  color: #2e7d32;
  margin-right: 15px;
}

.input-field {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  color: #333333;
  font-size: 17px; /* Cỡ chữ nhập to hơn */
  height: 100%;
}
.input-field::placeholder {
  color: #999999;
}

.eye-btn {
  background: transparent;
  border: none;
  padding: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #2e7d32;
}
.eye-icon {
  width: 24px;
  height: 24px;
} /* Icon mắt to hơn */

/* --- NÚT BẤM GRADIENT --- */
.login-btn {
  width: 100%;
  height: 60px; /* Nút bấm cao hơn */
  margin-top: 20px;
  border: none;
  border-radius: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 6px 15px rgba(27, 94, 32, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}
.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(27, 94, 32, 0.4);
}
.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.gradient-bg {
  background: linear-gradient(to right, #1b5e20, #43a047);
  color: #ffffff;
  font-size: 18px; /* Chữ trong nút to hơn */
  font-weight: 700;
  letter-spacing: 1.5px;
}

.spinner {
  width: 26px;
  height: 26px;
  color: #ffffff;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

/* --- FOOTER LOGOS --- */
.footer-logos-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 100px; /* Đẩy logo xuống sâu hơn cho cân đối màn hình web */
  opacity: 0.8;
}
.footer-image {
  height: 55px; /* Logo footer to hơn */
  object-fit: contain;
}
.footer-divider {
  width: 1.5px;
  height: 40px; /* Thanh chia cao hơn */
  background-color: #ccc;
  margin: 0 30px; /* Khoảng cách rộng hơn */
}
</style>
