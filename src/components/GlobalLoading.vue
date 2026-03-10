<template>
  <div v-if="appStore.isLoading" class="loading-overlay">
    <div class="spinner-box">
      <Loader2 class="spinner-icon" />
      <p>Đang xử lý...</p>
    </div>
  </div>
</template>

<script setup>
import { useAppStore } from '../stores/app';
import { Loader2 } from 'lucide-vue-next';

const appStore = useAppStore();
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  inset: 0;
  /* Phủ lớp màu tối hơi trong suốt và làm mờ nền phía sau */
  background-color: rgba(15, 61, 38, 0.4);
  backdrop-filter: blur(2px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Đảm bảo nó luôn nằm trên cùng mọi thứ (kể cả Modal) */
}

.spinner-box {
  background: white;
  padding: 1.5rem 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner-icon {
  width: 40px;
  height: 40px;
  color: #2e7d32; /* Màu xanh lá secondary */
  animation: spin 1s linear infinite; /* Hiệu ứng xoay tròn */
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

p {
  margin: 0;
  color: #0f3d26;
  font-weight: 600;
  letter-spacing: 0.5px;
}
</style>
