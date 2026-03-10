<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal-content confirm-modal">
      <div class="confirm-header">
        <div class="warning-icon-box">
          <AlertTriangle class="warning-icon" />
        </div>
        <h3 class="confirm-title">{{ title }}</h3>
      </div>

      <p class="confirm-message">{{ message }}</p>

      <div class="modal-actions">
        <button @click="$emit('cancel')" class="btn btn-secondary">
          Hủy bỏ
        </button>
        <button
          @click="$emit('confirm')"
          class="btn"
          :class="confirmButtonClass"
        >
          Đồng ý
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { AlertTriangle } from 'lucide-vue-next';

defineProps({
  isOpen: Boolean,
  title: { type: String, default: 'Xác nhận hành động' },
  message: {
    type: String,
    default: 'Bạn có chắc chắn muốn thực hiện hành động này?',
  },
  confirmButtonClass: { type: String, default: 'btn-save' }, // Dùng btn-save hoặc btn-logout(màu đỏ)
});

defineEmits(['confirm', 'cancel']);
</script>

<style scoped>
/* Kế thừa từ admin.css nhưng tinh chỉnh cho nhỏ gọn hơn */
.confirm-modal {
  max-width: 400px;
  padding: 1.5rem 2rem;
}
.confirm-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.warning-icon-box {
  background: rgba(245, 158, 11, 0.1);
  padding: 1rem;
  border-radius: 50%;
  display: flex;
}
.warning-icon {
  color: #f59e0b;
  width: 32px;
  height: 32px;
}
.confirm-title {
  margin: 0;
  color: #0f3d26;
  font-size: 1.3rem;
  text-align: center;
}
.confirm-message {
  text-align: center;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}
.modal-actions {
  justify-content: center;
  border-top: none;
  padding-top: 0;
  margin-top: 0;
}
.btn {
  min-width: 100px;
  justify-content: center;
}
</style>
