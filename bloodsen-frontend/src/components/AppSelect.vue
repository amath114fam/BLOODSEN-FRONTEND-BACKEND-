<template>
  <div class="select-group">
    <label v-if="label" :for="id">
      {{ label }}
    </label>

    <select
      :id="id"
      :value="modelValue"
      :disabled="disabled"
      :class="{ 'has-error': error }"
      :aria-invalid="!!error"
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="" disabled>
        {{ placeholder }}
      </option>

      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>

    <p v-if="error" class="field-error">{{ error }}</p>
  </div>
</template>

<script setup>
defineProps({
  id: { type: String, required: true },
  label: { type: String, default: '' },
  placeholder: { type: String, default: 'Sélectionnez une option' },
  options: { type: Array, required: true },
  modelValue: { type: [String, Number], default: '' },
  error: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.select-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

select {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  background-color: white;
  color: #333;
  font-size: 14px;
  outline: none;
  cursor: pointer;
  transition: 0.2s ease;
}

select:focus {
  border-color: var(--bloodsen-red);
}

select.has-error {
  border-color: #dc2626;
}

.field-error {
  margin: 0;
  color: #dc2626;
  font-size: 12px;
}

select:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

@media (max-width: 576px) {
  select {
    padding: 11px 12px;
  }
}
</style>