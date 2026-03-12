<template>
  <GlobalLoading />
  <GlobalToast />
  <router-view />
</template>

<script setup>
import GlobalLoading from './components/GlobalLoading.vue';
import GlobalToast from './components/GlobalToast.vue';
</script>
