<template>
  <AppCard padding="20px" class="stat-card">

    <div class="stat-card-top">
      <span class="stat-card-label">{{ label }}</span>

      <span class="stat-card-icon" :class="iconTone">
        <slot name="icon" />
      </span>
    </div>

    <div class="stat-card-value-row">
      <strong class="stat-card-value" :class="{ highlight: highlight }">
        {{ value }}
      </strong>

      <slot name="extra" />
    </div>

  </AppCard>
</template>

<script setup>
import AppCard from '@/components/AppCard.vue'

defineProps({
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  highlight: {
    type: Boolean,
    default: false,
  },
  iconTone: {
    type: String,
    default: 'neutral', // 'neutral' | 'danger' | 'success'
  },
})
</script>

<style scoped>
.stat-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 14px;
}

.stat-card-label {
  color: #6b7280;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.stat-card-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 26px;
  height: 26px;

  border-radius: 6px;

  background-color: #f1f3f5;
  color: #6b7280;
}

.stat-card-icon.danger {
  background-color: #fdecec;
  color: var(--bloodsen-red);
}

.stat-card-icon.success {
  background-color: #eafaf0;
  color: #1e9e5a;
}

.stat-card-icon svg {
  width: 15px;
  height: 15px;
}

.stat-card-value-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.stat-card-value {
  display: block;

  color: var(--bloodsen-dark);

  font-size: 30px;
  font-weight: 700;
  line-height: 1;
}

.stat-card-value.highlight {
  color: var(--bloodsen-red);
}
</style>