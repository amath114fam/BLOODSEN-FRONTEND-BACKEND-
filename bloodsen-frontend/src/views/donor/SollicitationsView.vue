<template>
  <div class="sollicitations-view">

    <div class="page-heading">
      <h2>Mes sollicitations</h2>
      <p>Les demandes de sang correspondant à votre profil.</p>
    </div>

    <AppTabs
      v-model="activeTab"
      :tabs="tabs"
      class="view-tabs"
    />

    <div v-if="filteredRequests.length" class="requests-list">

      <AppCard
        v-for="request in filteredRequests"
        :key="request.id"
        padding="24px"
        class="request-card"
      >

        <div class="request-group">
          <strong>{{ request.group }}</strong>
          <span>GROUPE</span>
        </div>

        <div class="request-body">
          <h3>{{ request.facility }}</h3>
          <p>« {{ request.message }} »</p>
        </div>

        <div class="request-actions">

          <template v-if="request.status === 'pending'">

            <AppButton
              variant="primary"
              @click="acceptRequest(request)"
            >
              Accepter le don
            </AppButton>

            <AppButton
              variant="outline"
              @click="declineRequest(request)"
            >
              Décliner
            </AppButton>

          </template>

          <AppButton
            v-else
            variant="secondary"
            :to="`/donneur/sollicitations/${request.id}`"
          >
            Voir le détail
          </AppButton>

        </div>

      </AppCard>

    </div>

    <AppCard v-else padding="0" class="empty-state">

      <div class="empty-icon">
        <Droplet :size="32" :stroke-width="2" />
      </div>

      <h3>{{ emptyStateMessage }}</h3>
      <p>Les nouvelles sollicitations correspondant à votre profil apparaîtront ici.</p>

    </AppCard>

        <!-- ==========================================
         MODAL DE CONFIRMATION
    =========================================== -->
    <div
      v-if="confirmation"
      class="modal-overlay"
      @click.self="fermerConfirmation"
    >
      <div class="modal-box">

        <div
          class="modal-icon"
          :class="confirmation.type === 'accepter' ? 'success' : 'danger'"
        >
          <Check v-if="confirmation.type === 'accepter'" :size="32" :stroke-width="3" />
          <X v-else :size="32" :stroke-width="3" />
        </div>

        <h3>{{ confirmation.titre }}</h3>

        <p>{{ confirmation.message }}</p>

        <div class="modal-actions">
          <AppButton
            variant="outline"
            :disabled="confirmationEnCours"
            @click="fermerConfirmation"
          >
            Annuler
          </AppButton>

          <AppButton
            :variant="confirmation.type === 'accepter' ? 'primary' : 'danger'"
            :disabled="confirmationEnCours"
            @click="confirmerAction"
          >
            <template v-if="confirmationEnCours">
              <span class="spinner-small"></span>
              En cours...
            </template>
            <template v-else>
              {{ confirmation.type === 'accepter' ? 'Accepter' : 'Refuser' }}
            </template>
          </AppButton>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useSollicitationsStore } from '@/stores/sollicitations'
import { Check, X, Droplet } from 'lucide-vue-next'

import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'
import AppTabs from '@/components/AppTabs.vue'

const sollicitationsStore = useSollicitationsStore()

// ==========================================
// ÉTAT
// ==========================================

const activeTab = ref('pending')
const confirmation = ref(null)
const confirmationEnCours = ref(false)

// ==========================================
// CHARGEMENT INITIAL
// ==========================================

onMounted(async () => {
  try {
    await sollicitationsStore.charger()
  } catch (e) {
    // Silencieux : le store a déjà l'erreur
  }
})

// ==========================================
// MAPPING DES STATUTS
// ==========================================
// API : en_attente | acceptee | refusee | expiree
// UI  : pending    | accepted | declined | expired

const STATUT_API_VERS_UI = {
  en_attente: 'pending',
  acceptee: 'accepted',
  refusee: 'declined',
  expiree: 'expired',
}

// Transforme les sollicitations de l'API en un format adapté à l'UI
const requests = computed(() => {
  return (sollicitationsStore.sollicitations || []).map(s => ({
    id: s.id,
    facility: s.structure_nom,
    group: s.groupe_sanguin,
    message: s.message || '',
    status: STATUT_API_VERS_UI[s.statut] || 'pending',
    date: s.date_creation,
  }))
})

// ==========================================
// TABS
// ==========================================

function countByStatus(status) {
  return requests.value.filter(r => r.status === status).length
}

const tabs = computed(() => [
  { value: 'pending', label: 'En attente', count: countByStatus('pending') },
  { value: 'all', label: 'Toutes', count: requests.value.length },
  { value: 'accepted', label: 'Acceptées', count: countByStatus('accepted') },
  { value: 'declined', label: 'Refusées', count: countByStatus('declined') },
  { value: 'expired', label: 'Expirées', count: countByStatus('expired') },
])

const filteredRequests = computed(() => {
  if (activeTab.value === 'all') return requests.value
  return requests.value.filter(r => r.status === activeTab.value)
})

const emptyStateMessage = computed(() => {
  const labels = {
    pending: 'Aucune sollicitation en attente.',
    all: 'Aucune sollicitation pour le moment.',
    accepted: 'Aucune sollicitation acceptée.',
    declined: 'Aucune sollicitation refusée.',
    expired: 'Aucune sollicitation expirée.',
  }
  return labels[activeTab.value]
})



// ==========================================
// MODAL DE CONFIRMATION
// ==========================================

function acceptRequest(request) {
  confirmation.value = {
    type: 'accepter',
    sollicitationId: request.id,
    titre: 'Accepter cette sollicitation ?',
    message: 'En acceptant, vous vous engagez à vous présenter au centre de collecte. Vous pourrez ensuite confirmer votre participation avec la structure.',
  }
}

function declineRequest(request) {
  confirmation.value = {
    type: 'refuser',
    sollicitationId: request.id,
    titre: 'Refuser cette sollicitation ?',
    message: 'En refusant, cette sollicitation sera retirée de votre liste. Vous ne pourrez plus la récupérer.',
  }
}

function fermerConfirmation() {
  if (confirmationEnCours.value) return
  confirmation.value = null
}

async function confirmerAction() {
  if (!confirmation.value) return

  confirmationEnCours.value = true
  try {
    if (confirmation.value.type === 'accepter') {
      await sollicitationsStore.accepter(confirmation.value.sollicitationId)
    } else {
      await sollicitationsStore.refuser(confirmation.value.sollicitationId)
    }
    confirmation.value = null
  } catch (e) {
    // Silencieux
  } finally {
    confirmationEnCours.value = false
  }
}
</script>

<style scoped>
.sollicitations-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-heading h2 {
  margin: 0 0 6px;

  color: var(--bloodsen-dark);

  font-size: 30px;
  font-weight: 700;
}

.page-heading p {
  margin: 0;

  color: #6b7280;

  font-size: 14px;
}

/* ========================================
   LISTE DES CARTES
======================================== */

.requests-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.request-card {
  display: flex;
  align-items: center;
  gap: 24px;
}

/* Bloc groupe sanguin */

.request-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 96px;
  height: 96px;

  border-radius: 10px;

  background-color: #fdf1f1;
}

.request-group strong {
  color: var(--bloodsen-red);

  font-size: 26px;
  font-weight: 800;
  line-height: 1.1;
}

.request-group span {
  margin-top: 4px;

  color: var(--bloodsen-red);

  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

/* Corps */

.request-body {
  flex: 1;
  min-width: 0;
}

.request-body h3 {
  margin: 0 0 8px;

  color: var(--bloodsen-dark);

  font-size: 18px;
  font-weight: 700;
}

.request-body p {
  margin: 0;

  color: #5f6672;

  font-size: 14px;
  font-style: italic;
  line-height: 1.6;
}

/* Actions */

.request-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex-shrink: 0;

  min-width: 170px;
}

.request-actions :deep(.app-button) {
  width: 100%;
}

/* ========================================
   ÉTAT VIDE
======================================== */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;

  padding: 56px 24px;

  text-align: center;
}

.empty-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 64px;
  height: 64px;
  margin-bottom: 20px;

  border-radius: 50%;

  background-color: #fdecec;
  color: var(--bloodsen-red);
}

.empty-icon svg {
  width: 30px;
  height: 30px;
}

.empty-state h3 {
  margin: 0 0 10px;

  color: var(--bloodsen-dark);

  font-size: 18px;
  font-weight: 700;
}

.empty-state p {
  max-width: 420px;
  margin: 0;

  color: #6b7280;

  font-size: 14px;
  line-height: 1.6;
}

/* ========================================
   MODAL DE CONFIRMATION
======================================== */

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
  max-width: 440px;
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
}
.modal-icon.success {
  background-color: #d1fae5;
  color: #059669;
}

.modal-icon.danger {
  background-color: #fee2e2;
  color: #dc2626;
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
/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 700px) {

  .page-heading h2 {
    font-size: 24px;
  }

  .request-card {
    flex-direction: column;
    align-items: stretch;
  }

  .request-group {
    width: 100%;
    height: 80px;
    flex-direction: row;
    gap: 10px;
  }

  .request-actions {
    min-width: 0;
  }

}
</style>