<template>
  <nav class="app-tabs">
    <button
      v-for="tab in tabs"
      :key="tab.value"
      type="button"
      class="app-tab"
      :class="{ active: modelValue === tab.value }"
      @click="$emit('update:modelValue', tab.value)"
    >
      {{ tab.label }}
      <span v-if="tab.count !== undefined && tab.count !== null" class="tab-count">
        {{ tab.count }}
      </span>
    </button>
  </nav>
</template>

<script setup>
defineProps({
  tabs: {
    type: Array,
    required: true, // [{ value: 'pending', label: 'En attente', count: 2 }, ...]
  },
  modelValue: {
    type: String,
    required: true,
  },
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.app-tabs {
  display: flex;
  align-items: center;
  gap: 28px;

  border-bottom: 1px solid #e7e9ed;

  overflow-x: auto;
}

.app-tab {
  display: flex;
  align-items: center;
  gap: 6px;

  padding: 0 0 12px;

  border: none;
  border-bottom: 2px solid transparent;
  background: transparent;

  color: #6b7280;

  font-family: inherit;
  font-size: 14px;
  font-weight: 600;

  white-space: nowrap;
  cursor: pointer;

  transition: color 0.15s ease, border-color 0.15s ease;
}

.app-tab:hover {
  color: var(--bloodsen-dark);
}

.app-tab.active {
  border-bottom-color: var(--bloodsen-red);
  color: var(--bloodsen-red);
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-width: 18px;
  height: 18px;
  padding: 0 5px;

  border-radius: 9px;

  background-color: #f1f3f5;
  color: #6b7280;

  font-size: 11px;
  font-weight: 700;
}

.app-tab.active .tab-count {
  background-color: #fdecec;
  color: var(--bloodsen-red);
}

@media (max-width: 700px) {
  .app-tabs {
    gap: 20px;
  }
}
</style>