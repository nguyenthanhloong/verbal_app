<template>
  <Transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click.self="handleCancel">
      <div class="modal-content confirm-modal">
        <div class="confirm-body">
          <div :class="['icon-box', type]">
            <AlertTriangle
              v-if="type === 'warning'"
              class="icon warning-icon"
            />
            <Trash2 v-else-if="type === 'danger'" class="icon danger-icon" />
            <Info v-else class="icon info-icon" />
          </div>

          <div class="text-content">
            <h3 class="confirm-title">{{ title }}</h3>
            <p class="confirm-message">{{ message }}</p>
          </div>
        </div>

        <div class="modal-actions">
          <button
            @click="handleCancel"
            class="btn btn-outline"
            :disabled="isLoading"
          >
            Hủy bỏ
          </button>
          <button
            @click="$emit('confirm')"
            class="btn"
            :class="confirmButtonClass || defaultButtonClass"
            :disabled="isLoading"
          >
            <Loader2 v-if="isLoading" class="spinner" />
            <span v-else>Đồng ý</span>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { onMounted, onUnmounted, computed } from 'vue';
import { AlertTriangle, Trash2, Info, Loader2 } from 'lucide-vue-next';

const props = defineProps({
  isOpen: Boolean,
  title: { type: String, default: 'Xác nhận hành động' },
  message: {
    type: String,
    default: 'Bạn có chắc chắn muốn thực hiện hành động này?',
  },
  type: { type: String, default: 'warning' }, // 'warning', 'danger', 'info'
  confirmButtonClass: { type: String, default: '' },
  isLoading: { type: Boolean, default: false }, // Disable nút khi đang xử lý
});

const emit = defineEmits(['confirm', 'cancel']);

// Tự động chọn class màu nút dựa trên type nếu không truyền confirmButtonClass
const defaultButtonClass = computed(() => {
  if (props.type === 'danger') return 'btn-danger';
  if (props.type === 'warning') return 'btn-warning';
  return 'btn-primary';
});

// Xử lý đóng modal bằng phím ESC
const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.isOpen && !props.isLoading) {
    handleCancel();
  }
};

const handleCancel = () => {
  if (!props.isLoading) emit('cancel');
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease, backdrop-filter 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  backdrop-filter: blur(0px);
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: scale(0.95);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 24, 39, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9998;
}

.confirm-modal {
  background: #ffffff;
  width: 100%;
  max-width: 480px;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.confirm-body {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 24px;
}

/* Các loại Icon Box */
.icon-box {
  flex-shrink: 0;
  padding: 10px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.icon-box.warning {
  background: #fef3c7;
}
.icon-box.danger {
  background: #fee2e2;
}
.icon-box.info {
  background: #e0f2fe;
}

.icon {
  width: 24px;
  height: 24px;
}
.warning-icon {
  color: #d97706;
}
.danger-icon {
  color: #dc2626;
}
.info-icon {
  color: #0284c7;
}

/* Text Content */
.text-content {
  flex: 1;
}
.confirm-title {
  margin: 0 0 8px 0;
  color: #111827;
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.5;
}
.confirm-message {
  margin: 0;
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Nút bấm */
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: 100px;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-outline {
  background: white;
  border-color: #d1d5db;
  color: #374151;
}
.btn-outline:hover:not(:disabled) {
  background: #f3f4f6;
}

.btn-warning {
  background: #f59e0b;
  color: white;
}
.btn-warning:hover:not(:disabled) {
  background: #d97706;
}

.btn-danger {
  background: #ef4444;
  color: white;
}
.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-primary {
  background: #2e7d32;
  color: white;
} /* Màu xanh kho */

.spinner {
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
}
</style>
