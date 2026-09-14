<template>
  <div class="app-input">

    <label
      v-if="label"
      :for="id"
    >
      {{ label }}
    </label>

    <div
      class="input-wrapper"
      :class="{ 'has-icon': $slots.icon, 'has-toggle': type === 'password', 'has-trailing': $slots.trailing }"
    >

      <span
        v-if="$slots.icon"
        class="input-icon"
      >
        <slot name="icon" />
      </span>

      <input
        :id="id"
        :type="internalType"
        :placeholder="placeholder"
        :value="modelValue"
        :required="required"
        :disabled="disabled"
        @input="$emit('update:modelValue', $event.target.value)"
      />

      <button
        v-if="type === 'password'"
        type="button"
        class="toggle-visibility"
        :aria-label="showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
        @click="showPassword = !showPassword"
      >
        <svg
          v-if="!showPassword"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M2 12C2 12 5.5 5 12 5C18.5 5 22 12 22 12C22 12 18.5 19 12 19C5.5 19 2 12 2 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" />
        </svg>

        <svg
          v-else
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M3 3L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          <path d="M10.6 10.6C10.2 11 10 11.5 10 12C10 13.1 10.9 14 12 14C12.5 14 13 13.8 13.4 13.4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M6.7 6.7C4.5 8.1 3 10 2 12C2 12 5.5 19 12 19C14 19 15.6 18.4 17 17.6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          <path d="M15.5 8.5C18.6 10 20 12 20 12C20 12 19.4 13.3 18.2 14.7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </button>

      <span
        v-if="$slots.trailing"
        class="input-trailing"
      >
        <slot name="trailing" />
      </span>

    </div>

    <p
      v-if="error"
      class="error-message"
    >
      {{ error }}
    </p>

    <p
      v-else-if="hint"
      class="hint-message"
    >
      {{ hint }}
    </p>

  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  id: { type: String, default: '' },
  label: { type: String, default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  modelValue: { type: [String, Number], default: '' },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  error: { type: String, default: '' },
  hint: { type: String, default: '' },
})

defineEmits(['update:modelValue'])

const showPassword = ref(false)

const internalType = computed(() => {
  if (props.type !== 'password') return props.type
  return showPassword.value ? 'text' : 'password'
})
</script>

<style scoped>
.app-input {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.app-input label {
  color: var(--bloodsen-dark);
  font-size: 13px;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 12px;
  border: 1px solid #d9dde2;
  border-radius: 4px;
  background-color: #ffffff;
  color: var(--bloodsen-dark);
  font-family: inherit;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s ease;
}

.input-wrapper.has-icon input {
  padding-left: 38px;
}

.input-wrapper.has-toggle input,
.input-wrapper.has-trailing input {
  padding-right: 38px;
}

.input-wrapper input::placeholder {
  color: #9aa4b2;
}

.input-wrapper input:focus {
  border-color: var(--bloodsen-red);
}

.input-wrapper input:disabled {
  background-color: #f1f3f5;
  cursor: not-allowed;
}

.input-icon,
.input-trailing {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9aa4b2;
  pointer-events: none;
}

.input-icon {
  left: 12px;
}

.input-trailing {
  right: 12px;
}

.input-icon svg,
.input-trailing svg {
  width: 17px;
  height: 17px;
}

.toggle-visibility {
  position: absolute;
  right: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: #9aa4b2;
  cursor: pointer;
}

.toggle-visibility svg {
  width: 18px;
  height: 18px;
}

.toggle-visibility:hover {
  color: var(--bloodsen-dark);
}

.error-message {
  margin: 0;
  color: var(--bloodsen-red);
  font-size: 12px;
}

.hint-message {
  margin: 0;
  color: #697386;
  font-size: 12px;
}
</style>