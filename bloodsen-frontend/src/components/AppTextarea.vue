<template>
  <div class="textarea-group">
    <label v-if="label" :for="id">
      {{ label }}<span v-if="required" class="required">*</span>
    </label>

    <textarea
      :id="id"
      :placeholder="placeholder"
      :value="modelValue"
      :rows="rows"
      :maxlength="maxlength"
      :disabled="disabled"
      class="textarea-field"
      :class="{ 'textarea-field--error': error }"
      @input="$emit('update:modelValue', $event.target.value)"
    ></textarea>

    <span v-if="error" class="textarea-error">{{ error }}</span>
    <span v-else-if="hint" class="textarea-hint">{{ hint }}</span>
  </div>
</template>

<script setup>
defineProps({
  id: { type: String, required: true },
  label: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  rows: { type: Number, default: 4 },
  maxlength: { type: [Number, String], default: null },
  modelValue: { type: String, default: '' },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  error: { type: String, default: '' },
  hint: { type: String, default: '' }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.textarea-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: var(--bloodsen-dark);
}

.required {
  color: var(--bloodsen-red);
  margin-left: 2px;
}

.textarea-field {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  border: 1px solid var(--bloodsen-border);
  border-radius: 8px;
  background-color: white;
  color: var(--bloodsen-dark);
  font-size: 14px;
  font-family: 'Poppins', sans-serif;
  line-height: 1.5;
  resize: vertical;
  outline: none;
  transition: 0.2s ease;
}

.textarea-field:focus {
  border-color: var(--bloodsen-red);
}

.textarea-field:disabled {
  background-color: var(--bloodsen-light);
  cursor: not-allowed;
  opacity: 0.7;
}

.textarea-field--error {
  border-color: #c62828;
}

.textarea-error {
  font-size: 12px;
  color: #c62828;
}

.textarea-hint {
  font-size: 12px;
  color: #888;
}

@media (max-width: 576px) {
  .textarea-field {
    padding: 11px 12px;
  }
}
</style>