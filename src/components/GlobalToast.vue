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
          <AlertCircle v-else-if="toast.type === 'error'" />
          <AlertTriangle v-else-if="toast.type === 'warning'" />
          <Info v-else />
        </div>

        <div class="toast-content">
          <p v-if="toast.title" class="toast-title">{{ toast.title }}</p>
          <p class="toast-message">{{ toast.message }}</p>
        </div>

        <button
          class="toast-close"
          @click="removeToast(toast.id)"
          aria-label="Đóng"
        >
          <X class="icon-sm" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToast } from '../composables/useToast';
import {
  CheckCircle,
  AlertCircle,
  AlertTriangle,
  Info,
  X,
} from 'lucide-vue-next';

const { toasts, removeToast } = useToast();
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast-item {
  pointer-events: auto;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  min-width: 320px;
  max-width: 400px;
  border: 1px solid #f3f4f6;
  border-left-width: 4px;
}

.toast-success {
  border-left-color: #10b981;
}
.toast-success .toast-icon {
  color: #10b981;
}

.toast-error {
  border-left-color: #ef4444;
}
.toast-error .toast-icon {
  color: #ef4444;
}

.toast-warning {
  border-left-color: #f59e0b;
}
.toast-warning .toast-icon {
  color: #f59e0b;
}

.toast-info {
  border-left-color: #3b82f6;
}
.toast-info .toast-icon {
  color: #3b82f6;
}

.toast-icon {
  flex-shrink: 0;
  margin-top: 2px;
}
.toast-icon svg {
  width: 20px;
  height: 20px;
}

.toast-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toast-title {
  margin: 0;
  font-weight: 600;
  font-size: 0.95rem;
  color: #111827;
}

.toast-message {
  margin: 0;
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 4px;
  margin: -4px -4px 0 0;
  border-radius: 4px;
  display: flex;
  transition: all 0.2s;
}

.toast-close:hover {
  background-color: #f3f4f6;
  color: #4b5563;
}

.toast-move,
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.toast-leave-active {
  position: absolute;
}
</style>
