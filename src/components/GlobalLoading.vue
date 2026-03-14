<template>
  <Transition name="fade">
    <div v-if="appStore.isLoading" class="loading-overlay">
      <div class="loading-card">
        <div class="icon-wrapper">
          <Loader2 class="spinner-icon" stroke-width="2.5" />
        </div>

        <div class="text-content">
          <h3>Đang xử lý...</h3>
          <p>Hệ thống đang đồng bộ dữ liệu kho, vui lòng đợi.</p>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useAppStore } from '../stores/app';
import { Loader2 } from 'lucide-vue-next';

const appStore = useAppStore();
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, backdrop-filter 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

.loading-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 24, 39, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-card {
  background: #ffffff;
  padding: 24px 32px;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 340px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  animation: slideUp 0.3s ease-out forwards;
}

.icon-wrapper {
  background: #e8f5e9;
  padding: 14px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner-icon {
  width: 28px;
  height: 28px;
  color: #2e7d32;
  animation: spin 1s linear infinite;
}

.text-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.text-content h3 {
  margin: 0;
  color: #111827;
  font-size: 1.125rem;
  font-weight: 600;
}

.text-content p {
  margin: 0;
  color: #6b7280;
  font-size: 0.875rem;
  line-height: 1.4;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes slideUp {
  0% {
    opacity: 0;
    transform: translateY(15px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
