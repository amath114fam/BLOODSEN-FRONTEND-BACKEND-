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
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3C12 3 6 10 6 14.5C6 17.54 8.24 20 12 20C15.76 20 18 17.54 18 14.5C18 10 12 3 12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
        </svg>
      </div>

      <h3>{{ emptyStateMessage }}</h3>
      <p>Les nouvelles sollicitations correspondant à votre profil apparaîtront ici.</p>

    </AppCard>

  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'
import AppTabs from '@/components/AppTabs.vue'

const activeTab = ref('pending')

const requests = ref([
  {
    id: 'sol-1',
    facility: 'Hôpital Principal de Dakar',
    group: 'O+',
    message: 'Urgence vitale : Nous avons besoin de donneurs O+ pour une intervention chirurgicale complexe prévue ce soir. Votre geste peut sauver une vie.',
    status: 'pending',
  },
  {
    id: 'sol-2',
    facility: 'Hôpital Dalal Jamm',
    group: 'O+',
    message: 'Besoin urgent : Suite à un accident de la route, nous manquons de poches O+.',
    status: 'pending',
  },
  {
    id: 'sol-3',
    facility: 'Centre de Santé Phillippe',
    group: 'A+',
    message: 'Collecte programmée pour reconstituer nos réserves régionales.',
    status: 'accepted',
  },
  {
    id: 'sol-4',
    facility: 'CHU de Fann',
    group: 'B+',
    message: 'Besoin ponctuel pour un patient en oncologie.',
    status: 'declined',
  },
  {
    id: 'sol-5',
    facility: 'Hôpital Régional de Thiès',
    group: 'O+',
    message: 'Sollicitation expirée faute de réponse dans le délai imparti.',
    status: 'expired',
  },
])

const tabs = computed(() => [
  { value: 'pending', label: 'En attente', count: countByStatus('pending') },
  { value: 'all', label: 'Toutes', count: requests.value.length },
  { value: 'accepted', label: 'Acceptées', count: countByStatus('accepted') },
  { value: 'declined', label: 'Refusées', count: countByStatus('declined') },
  { value: 'expired', label: 'Expirées', count: countByStatus('expired') },
])

function countByStatus(status) {
  return requests.value.filter((r) => r.status === status).length
}

const filteredRequests = computed(() => {
  if (activeTab.value === 'all') return requests.value
  return requests.value.filter((r) => r.status === activeTab.value)
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

function acceptRequest(request) {
  request.status = 'accepted'
  // Plus tard : appel API PATCH /sollicitations/:id/accepter
}

function declineRequest(request) {
  request.status = 'declined'
  // Plus tard : appel API PATCH /sollicitations/:id/decliner
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