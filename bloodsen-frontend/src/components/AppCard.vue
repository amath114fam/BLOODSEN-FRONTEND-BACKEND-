<template>
  <div class="app-card" :style="{ padding }">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  padding: {
    type: String,
    default: '24px'
  }
})
</script>

<style scoped>
.app-card {
  width: 100%;
  box-sizing: border-box;
  background-color: white;
  border: 1px solid var(--bloodsen-border);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

@media (max-width: 576px) {
  .app-card {
    padding: 16px;
    border-radius: 10px;
  }
}
</style>