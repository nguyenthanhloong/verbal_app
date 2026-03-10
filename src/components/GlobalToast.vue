<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast-item"
        :class="`toast-${toast.type}`"
      >
        <div class="toast-icon">
          <CheckCircle v-if="toast.type === 'success'" />
          <AlertCircle v-if="toast.type === 'error'" />
        </div>
        <div class="toast-content">{{ toast.message }}</div>
        <button class="toast-close" @click="removeToast(toast.id)">
          <X class="icon-sm" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToast } from '../composables/useToast';
import { CheckCircle, AlertCircle, X } from 'lucide-vue-next';

const { toasts, removeToast } = useToast();
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 300px;
  color: white;
  font-weight: 500;
}

/* Màu sắc theo Theme của bạn */
.toast-success {
  background-color: #2e7d32;
  border-left: 6px solid #4caf50;
}
.toast-error {
  background-color: #ef4444;
  border-left: 6px solid #b91c1c;
}
.toast-info {
  background-color: #5378e5;
  border-left: 6px solid #2481e4;
}

.toast-icon {
  display: flex;
  align-items: center;
  width: 24px;
  height: 24px;
}
.toast-content {
  flex: 1;
  font-size: 0.95rem;
}
.toast-close {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  opacity: 0.7;
  transition: 0.2s;
  display: flex;
}
.toast-close:hover {
  opacity: 1;
}
.icon-sm {
  width: 16px;
  height: 16px;
}

/* Hiệu ứng trượt vào/ra (Vue Transition) */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(50px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(50px);
}
</style>
