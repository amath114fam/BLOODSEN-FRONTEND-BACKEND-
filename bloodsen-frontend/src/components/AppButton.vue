<template>
  <component
    :is="to ? 'router-link' : 'button'"
    :to="to || undefined"
    class="app-button"
    :class="[`app-button--${variant}`, `app-button--${size}`]"
    :disabled="!to && disabled"
  >
    <slot />
  </component>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary' // primary | secondary | outline | danger
  },
  size: {
    type: String,
    default: 'md' // sm | md | lg
  },
  disabled: {
    type: Boolean,
    default: false
  },
  to: {
    type: [String, Object],
    default: null
  }
})
</script>

<style scoped>
.app-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;

  border: none;
  border-radius: 8px;

  font-family: 'Poppins', sans-serif;
  font-weight: 600;

  text-decoration: none;

  cursor: pointer;
  transition: 0.2s ease;
}

.app-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Tailles */
.app-button--sm { padding: 8px 16px; font-size: 13px; }
.app-button--md { padding: 12px 24px; font-size: 14px; }
.app-button--lg { padding: 14px 28px; font-size: 15px; }

/* Variantes */
.app-button--primary {
  background-color: var(--bloodsen-red);
  color: white;
}
.app-button--primary:hover:not(:disabled) {
  opacity: 0.9;
}

.app-button--secondary {
  background-color: var(--bloodsen-light);
  color: var(--bloodsen-dark);
  border: 1px solid var(--bloodsen-border);
}
.app-button--secondary:hover:not(:disabled) {
  background-color: #eef0f2;
}

.app-button--outline {
  background-color: transparent;
  color: var(--bloodsen-red);
  border: 1px solid var(--bloodsen-red);
}
.app-button--outline:hover:not(:disabled) {
  background-color: #fdecea;
}

.app-button--danger {
  background-color: transparent;
  color: #c62828;
  border: 1px solid #c62828;
}
.app-button--danger:hover:not(:disabled) {
  background-color: #fdecea;
}
.app-button :deep(svg) {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
</style>