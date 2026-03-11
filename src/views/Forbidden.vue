<template>
  <div class="forbidden-container">
    <div class="forbidden-box">
      <div class="icon-wrapper bg-rose-light">
        <ShieldAlert class="forbidden-icon text-rose" />
      </div>

      <h1 class="error-code">403</h1>
      <h2 class="error-title">Truy Cập Bị Từ Chối</h2>
      <p class="error-message">
        Rất tiếc, tài khoản của bạn không có đủ quyền hạn để xem trang này.
        <br />
        Nếu bạn cho rằng đây là sự nhầm lẫn, vui lòng liên hệ quản trị viên.
      </p>

      <div class="action-buttons">
        <button @click="$router.back()" class="btn btn-outline">
          <ArrowLeft class="icon-sm" /> Quay Lại
        </button>
        <button @click="$router.push('/')" class="btn btn-primary">
          <Home class="icon-sm" /> Về Trang Chủ
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ShieldAlert, Home, ArrowLeft } from 'lucide-vue-next';
import { useRouter } from 'vue-router';

const router = useRouter();
</script>

<style scoped>
.forbidden-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 2rem;
  animation: fadeIn 0.4s ease-out;
}

.forbidden-box {
  background: #ffffff;
  padding: 3.5rem 3rem;
  border-radius: 20px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05),
    0 8px 10px -6px rgba(0, 0, 0, 0.01);
  text-align: center;
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #e2e8f0;
}

/* Icon Styling */
.icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.5rem;
}

.forbidden-icon {
  width: 40px;
  height: 40px;
}

.bg-rose-light {
  background-color: #ffe4e6;
}
.text-rose {
  color: #e11d48;
}

/* Typography */
.error-code {
  font-size: 4rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
  line-height: 1;
  letter-spacing: -0.05em;
}

.error-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #334155;
  margin: 0.5rem 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.error-message {
  color: #64748b;
  margin-bottom: 2.5rem;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.85rem 1.25rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.icon-sm {
  width: 18px;
  height: 18px;
}

/* Primary Button (Nút chính) */
.btn-primary {
  background-color: #0f3d26;
  color: #ffffff;
  border: none;
  box-shadow: 0 4px 6px -1px rgba(15, 61, 38, 0.2);
}

.btn-primary:hover {
  background-color: #1a5c3a;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px -2px rgba(15, 61, 38, 0.3);
}

/* Outline Button (Nút phụ) */
.btn-outline {
  background-color: transparent;
  color: #475569;
  border: 1px solid #cbd5e1;
}

.btn-outline:hover {
  background-color: #f8fafc;
  color: #0f172a;
  border-color: #94a3b8;
}

@media (max-width: 480px) {
  .action-buttons {
    flex-direction: column;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
