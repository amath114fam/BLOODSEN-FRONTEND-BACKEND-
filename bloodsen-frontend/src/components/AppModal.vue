<template>
  <Teleport to="body">
    <div v-if="open" class="modal-overlay" @click.self="close">
      <div class="modal" :class="`modal--${size}`">
        <button
          class="modal-close"
          type="button"
          aria-label="Fermer"
          @click="close"
        >
          ×
        </button>

        <div class="modal-content">
          <slot />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  open: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'md' // 'sm' | 'md' | 'lg'
  }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

const handleKeydown = (e) => {
  if (e.key === 'Escape' && props.open) close()
}

watch(
  () => props.open,
  (isOpen) => {
    document.body.style.overflow = isOpen ? 'hidden' : ''
  }
)

onMounted(() => document.addEventListener('keydown', handleKeydown))
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background-color: rgba(0, 0, 0, 0.5);
}

.modal {
  position: relative;
  z-index: 1001;

  width: 100%;
  min-height: 200px;

  padding: 24px;

  background: white;
  color: var(--bloodsen-dark);

  border-radius: 12px;
  box-sizing: border-box;
  display: block;
}

.modal--sm {
  max-width: 360px;
}

.modal--md {
  max-width: 500px;
}

.modal--lg {
  max-width: 720px;
}

.modal-close {
  position: absolute;
  top: 12px;
  right: 16px;

  border: none;
  background: transparent;

  font-size: 24px;
  line-height: 1;

  color: var(--bloodsen-gray, #555);
  cursor: pointer;
}

.modal-content {
  padding-top: 10px;
}

@media (max-width: 576px) {
  .modal-overlay {
    padding: 12px;
  }

  .modal {
    max-width: 100%;
    padding: 20px 16px;
    border-radius: 10px;
  }
}
</style>