<template>
  <div class="select-group">
    <label v-if="label" :for="id">
      {{ label }}
    </label>

    <select
      :id="id"
      :value="modelValue"
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
  </div>
</template>

<script setup>
defineProps({
  id: {
    type: String,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Sélectionnez une option'
  },
  options: {
    type: Array,
    required: true
  },
  modelValue: {
    type: String,
    default: ''
  }
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

@media (max-width: 576px) {
  select {
    padding: 11px 12px;
  }
}
</style>