<template>
  <span
    class="app-badge"
    :class="`app-badge--${variant}`"
  >
    <slot />
  </span>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'default'
  }
})
</script>

<style scoped>
.app-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
}

/* Défaut */
.app-badge--default {
  background-color: #f1f1f1;
  color: #555;
}

/* Succès */
.app-badge--success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

/* Attention */
.app-badge--warning {
  background-color: #fff3cd;
  color: #856404;
}

/* Danger */
.app-badge--danger {
  background-color: #fdecea;
  color: #c62828;
}

/* Information */
.app-badge--info {
  background-color: #e3f2fd;
  color: #1565c0;
}
</style>