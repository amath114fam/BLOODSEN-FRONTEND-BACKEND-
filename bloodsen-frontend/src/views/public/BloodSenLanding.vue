<script setup>
import { ref } from 'vue'
import AppButton from '@/components/AppButton.vue'
import AppModal from '@/components/AppModal.vue'

const showModal = ref(false)
</script>

<template>
  <AppButton @click="showModal = true">
    Ouvrir la modal
  </AppButton>

  <AppModal
    :open="showModal"
    @close="showModal = false"
  >
    <h2>Confirmer votre action</h2>

    <p>
      Voulez-vous continuer cette opération ?
    </p>

    <AppButton @click="showModal = false">
      Confirmer
    </AppButton>
  </AppModal>
</template>