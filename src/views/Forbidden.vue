<template>
  <div class="forbidden-container">
    <div class="forbidden-box">
      <ShieldAlert class="forbidden-icon" />
      <h1>403 - TỪ CHỐI TRUY CẬP</h1>
      <p class="text-muted">
        Bạn không có quyền hạn (Permission) để xem trang này.
      </p>
      <button @click="$router.push('/')" class="btn btn-primary mt-4">
        <Home class="icon-sm" /> Quay Về Trang Chủ
      </button>
    </div>
  </div>
</template>

<script setup>
import { ShieldAlert, Home } from 'lucide-vue-next';
</script>

<style scoped>
.forbidden-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}
.forbidden-box {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  text-align: center;
  max-width: 500px;
  border-top: 5px solid #ef4444;
}
.forbidden-icon {
  width: 64px;
  height: 64px;
  color: #ef4444;
  margin-bottom: 1rem;
}
h1 {
  color: #0f3d26;
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
}
.text-muted {
  color: #aaaaaa;
  margin-bottom: 2rem;
}
.mt-4 {
  margin-top: 1rem;
}
.icon-sm {
  width: 18px;
  height: 18px;
}
</style>
