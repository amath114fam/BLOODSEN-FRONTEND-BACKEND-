<template>
  <div v-if="visible" class="modal-overlay" @click.self="annuler">
    <div class="modal-box">

      <div class="modal-icon">
        <LogOut :size="32" :stroke-width="2.5" />
      </div>

      <h3>Se déconnecter ?</h3>

      <p>
        Vous serez redirigé vers la page de connexion.
        Vous devrez saisir vos identifiants pour revenir.
      </p>

      <div class="modal-actions">
        <AppButton
          variant="outline"
          :disabled="chargement"
          @click="annuler"
        >
          Annuler
        </AppButton>

        <AppButton
          variant="danger"
          :disabled="chargement"
          @click="confirmer"
        >
          <template v-if="chargement">
            <span class="spinner-small"></span>
            Déconnexion...
          </template>
          <template v-else>
            Se déconnecter
          </template>
        </AppButton>
      </div>

    </div>
  </div>
</template>

<script setup>
import { LogOut } from 'lucide-vue-next'
import AppButton from '@/components/AppButton.vue'

defineProps({
  visible: { type: Boolean, default: false },
  chargement: { type: Boolean, default: false },
})

const emit = defineEmits(['annuler', 'confirmer'])

function annuler() {
  emit('annuler')
}

function confirmer() {
  emit('confirmer')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;

  z-index: 9999;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 24px;

  background-color: rgba(11, 25, 43, 0.65);

  animation: fadeIn 0.2s ease;
}

.modal-box {
  max-width: 420px;
  width: 100%;

  padding: 36px 32px;

  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);

  text-align: center;

  animation: scaleIn 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 64px;
  height: 64px;
  margin-bottom: 20px;

  border-radius: 50%;

  background-color: #fdecec;
  color: var(--bloodsen-red);
}

.modal-box h3 {
  margin: 0 0 12px;

  color: var(--bloodsen-dark);
  font-size: 20px;
  font-weight: 700;
}

.modal-box p {
  margin: 0 0 28px;

  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.spinner-small {
  display: inline-block;
  width: 14px;
  height: 14px;

  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to   { transform: scale(1);   opacity: 1; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 700px) {
  .modal-actions {
    flex-direction: column-reverse;
  }

  .modal-actions :deep(button) {
    width: 100%;
  }
}
</style>