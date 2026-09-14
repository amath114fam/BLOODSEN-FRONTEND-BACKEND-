<template>
  <div class="participations-view">

    <div class="page-heading">
      <h2>Participations</h2>
      <p>Suivez les participations liées à vos demandes.</p>
    </div>

    <!-- Indicateurs -->
    <div class="stats-grid">

      <StatCard
        label="En attente"
        :value="stats.pending"
        icon-tone="neutral"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M12 7V12L15 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Confirmées"
        :value="stats.confirmed"
        icon-tone="success"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Refus médicaux"
        :value="stats.medicalRefusal"
        icon-tone="danger"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L19 6V11C19 15.5 16 19.5 12 21C8 19.5 5 15.5 5 11V6L12 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

    </div>

    <!-- Filtres + Table -->
    <AppCard padding="20px 24px" class="participations-card">

      <div class="filters-row">

        <AppInput
          id="search-participation"
          v-model="filters.search"
          placeholder="Rechercher un donneur..."
          class="search-input"
        >
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" />
              <path d="M21 21L16.5 16.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
          </template>
        </AppInput>

        <AppSelect
          id="request-filter"
          v-model="filters.request"
          placeholder="Toutes les demandes"
          :options="requestOptions"
        />

        <AppSelect
          id="group-filter"
          v-model="filters.group"
          placeholder="Tous les groupes"
          :options="groupOptions"
        />

        <AppSelect
          id="status-filter"
          v-model="filters.status"
          placeholder="Tous les statuts"
          :options="statusOptions"
        />

        <AppInput
          id="date-filter"
          v-model="filters.date"
          type="date"
          class="date-input"
        />

      </div>

      <div v-if="participations.length" class="participations-table-wrapper">
        <table class="participations-table">

          <thead>
            <tr>
              <th>Donneur</th>
              <th>Demande</th>
              <th>Groupe</th>
              <th>Date réponse</th>
              <th>Statut</th>
              <th>Date conf.</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in participations" :key="item.id">

              <td>
                <div class="donor-cell">
                  <span class="donor-avatar">{{ item.donorInitials }}</span>
                  <div>
                    <strong>{{ item.donorName }}</strong>
                    <span class="donor-reference">{{ item.donorReference }}</span>
                  </div>
                </div>
              </td>

              <td>
                <strong>{{ item.requestReference }}</strong>
                <span class="request-service">{{ item.requestService }}</span>
              </td>

              <td>
                <AppBadge variant="danger">{{ item.group }}</AppBadge>
              </td>

              <td class="date-cell">
                {{ item.responseDate }}
              </td>

              <td>
                <AppBadge :variant="statusVariant(item.status)">
                  {{ statusLabel(item.status) }}
                </AppBadge>
              </td>

              <td class="date-cell">
                {{ item.confirmationDate || '—' }}
              </td>

              <td>
                <div class="actions-cell">

                  <AppButton
                    v-if="item.status === 'pending'"
                    variant="primary"
                    size="sm"
                    @click="confirmParticipation(item)"
                  >
                    Confirmer
                  </AppButton>

                  <button
                    v-if="item.status === 'confirmed'"
                    type="button"
                    class="action-icon"
                    aria-label="Appeler le donneur"
                  >
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M5 4H9L11 9L8.5 10.5C9.57 12.67 11.33 14.43 13.5 15.5L15 13L20 15V19C20 20.1 19.1 21 18 21C10.27 21 4 14.73 4 7C4 5.9 4.9 5 6 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </button>

                  <button
                    v-if="item.status === 'medical_refusal'"
                    type="button"
                    class="action-icon"
                    aria-label="Relancer un autre donneur"
                    @click="relaunchRequest(item)"
                  >
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M4 12C4 7.58 7.58 4 12 4C15.31 4 18.17 6.01 19.36 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                      <path d="M20 12C20 16.42 16.42 20 12 20C8.69 20 5.83 17.99 4.64 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                      <path d="M19 5V9H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                      <path d="M5 19V15H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </button>

                  <router-link
                    :to="`/structure/demandes/${item.requestReference}`"
                    class="action-icon"
                    aria-label="Voir le dossier"
                  >
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="5" y="3" width="14" height="18" rx="2" stroke="currentColor" stroke-width="2" />
                      <path d="M9 8H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                      <path d="M9 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                      <path d="M9 16H12" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                    </svg>
                  </router-link>

                </div>
              </td>

            </tr>
          </tbody>

        </table>
      </div>

      <div v-else class="empty-state">

        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>

        <h3>Aucune participation pour le moment.</h3>
        <p>
          Les réponses des donneurs à vos demandes de sang s'afficheront ici
          dès qu'ils confirmeront leur disponibilité.
        </p>

        <AppButton variant="primary" @click="goToRequests">
          <span class="drop-icon">🩸</span>
          Consulter vos demandes
        </AppButton>

      </div>

      <div v-if="participations.length" class="participations-footer">
        <span>
          Affichage de <strong>{{ pagination.from }} à {{ pagination.to }}</strong>
          sur {{ pagination.total }} participations
        </span>

        <div class="pagination">
          <button type="button" :disabled="pagination.page === 1" @click="goToPage(pagination.page - 1)">
            &lt; Précédent
          </button>

          <button
            v-for="p in pagination.totalPages"
            :key="p"
            type="button"
            :class="{ active: p === pagination.page }"
            @click="goToPage(p)"
          >
            {{ p }}
          </button>

          <button type="button" @click="goToPage(pagination.page + 1)">
            Suivant &gt;
          </button>
        </div>
      </div>

    </AppCard>

  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'
import StatCard from '@/components/StatCard.vue'

const router = useRouter()

const stats = ref({
  pending: 12,
  confirmed: 45,
  medicalRefusal: 2,
})

const filters = reactive({
  search: '',
  request: '',
  group: '',
  status: '',
  date: '',
})

const requestOptions = [
  { value: 'DS-2025-142', label: '#DS-2025-142' },
  { value: 'DS-2025-141', label: '#DS-2025-141' },
  { value: 'DS-2025-139', label: '#DS-2025-139' },
]

const groupOptions = [
  { value: 'O-', label: 'O-' },
  { value: 'O+', label: 'O+' },
  { value: 'A+', label: 'A+' },
  { value: 'A-', label: 'A-' },
  { value: 'B+', label: 'B+' },
  { value: 'B-', label: 'B-' },
  { value: 'AB+', label: 'AB+' },
  { value: 'AB-', label: 'AB-' },
]

const statusOptions = [
  { value: 'pending', label: 'En attente' },
  { value: 'confirmed', label: 'Confirmée' },
  { value: 'cancelled', label: 'Annulée' },
  { value: 'medical_refusal', label: 'Refus médical' },
]

const participations = ref([
  {
    id: 1,
    donorInitials: 'AM',
    donorName: 'Amadou M.',
    donorReference: 'DON-SN-8492',
    requestReference: '#DS-2025-142',
    requestService: 'Maternité',
    group: 'O-',
    responseDate: 'Auj., 11:42',
    status: 'pending',
    confirmationDate: null,
  },
  {
    id: 2,
    donorInitials: 'SD',
    donorName: 'Samba D.',
    donorReference: 'DON-SN-7319',
    requestReference: '#DS-2025-141',
    requestService: 'Réanimation',
    group: 'B+',
    responseDate: 'Auj., 10:15',
    status: 'confirmed',
    confirmationDate: 'Auj., 10:25',
  },
  {
    id: 3,
    donorInitials: 'FF',
    donorName: 'Fatou F.',
    donorReference: 'DON-SN-9022',
    requestReference: '#DS-2025-139',
    requestService: 'Chirurgie',
    group: 'A+',
    responseDate: 'Hier, 15:30',
    status: 'cancelled',
    confirmationDate: null,
  },
  {
    id: 4,
    donorInitials: 'IK',
    donorName: 'Ibrahima K.',
    donorReference: 'DON-SN-5120',
    requestReference: '#DS-2025-139',
    requestService: 'Chirurgie',
    group: 'AB+',
    responseDate: '02 Mai, 09:10',
    status: 'medical_refusal',
    confirmationDate: null,
  },
])

const pagination = reactive({
  page: 1,
  from: 1,
  to: 4,
  total: 62,
  totalPages: 3,
})

function statusVariant(status) {
  if (status === 'pending') return 'warning'
  if (status === 'confirmed') return 'success'
  if (status === 'medical_refusal') return 'danger'
  return 'default' // cancelled
}

function statusLabel(status) {
  if (status === 'pending') return 'En attente'
  if (status === 'confirmed') return 'Confirmée'
  if (status === 'medical_refusal') return 'Refus médical'
  return 'Annulée'
}

function confirmParticipation(item) {
  item.status = 'confirmed'
  item.confirmationDate = "Auj., à l'instant"
  // Plus tard : appel API PATCH /participations/:id
}

function relaunchRequest(item) {
  router.push(`/structure/demandes/${item.requestReference.replace('#', '')}`)
}

function goToPage(page) {
  if (page < 1 || page > pagination.totalPages) return
  pagination.page = page
  // Plus tard : appel API paginé GET /participations?page=...
}

function goToRequests() {
  router.push('/structure/demandes')
}
</script>

<style scoped>
.participations-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-heading h2 {
  margin: 0 0 6px;

  color: var(--bloodsen-dark);

  font-size: 30px;
  font-weight: 700;
}

.page-heading p {
  margin: 0;

  max-width: 720px;

  color: #6b7280;

  font-size: 14px;
  line-height: 1.5;
}

/* ========================================
   INDICATEURS
======================================== */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* ========================================
   FILTRES
======================================== */

.filters-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;

  margin-bottom: 20px;
}

.filters-row :deep(.search-input) {
  min-width: 240px;
  flex: 1;
}

.filters-row :deep(.select-group),
.filters-row :deep(.date-input) {
  min-width: 150px;
}

/* ========================================
   TABLE
======================================== */

.participations-table-wrapper {
  overflow-x: auto;
}

.participations-table {
  width: 100%;
  border-collapse: collapse;
}

.participations-table th {
  padding: 12px 20px;

  color: #8a94a3;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;

  white-space: nowrap;
}

.participations-table td {
  padding: 16px 20px;

  border-top: 1px solid #f0f1f3;

  color: var(--bloodsen-dark);
  font-size: 14px;

  vertical-align: middle;

  white-space: nowrap;
}

.donor-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.donor-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 38px;
  height: 38px;

  border-radius: 50%;

  background-color: #f1f3f5;
  color: var(--bloodsen-dark);

  font-size: 12px;
  font-weight: 700;
}

.donor-cell strong {
  display: block;
  font-size: 14px;
}

.donor-reference {
  display: block;
  margin-top: 2px;

  color: #8a94a3;
  font-size: 12.5px;
}

.participations-table td strong {
  display: block;
  font-size: 14px;
}

.request-service {
  display: block;
  margin-top: 2px;

  color: #8a94a3;
  font-size: 12.5px;
}

.date-cell {
  color: #4a5568;
  font-size: 13px;
}

.actions-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.action-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  border: none;
  background: transparent;

  color: #6b7280;

  cursor: pointer;
  text-decoration: none;
}

.action-icon svg {
  width: 18px;
  height: 18px;
}

.action-icon:hover {
  color: var(--bloodsen-red);
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
  max-width: 480px;
  margin: 0 0 24px;

  color: #6b7280;

  font-size: 14px;
  line-height: 1.6;
}

.drop-icon {
  margin-right: 6px;
}

/* ========================================
   FOOTER / PAGINATION
======================================== */

.participations-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;

  gap: 12px;

  padding: 16px 20px 0;

  color: #6b7280;
  font-size: 13px;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 6px;
}

.pagination button {
  padding: 6px 12px;

  border: 1px solid #d9dde2;
  border-radius: 6px;

  background-color: #ffffff;
  color: var(--bloodsen-dark);

  font-family: inherit;
  font-size: 13px;

  cursor: pointer;
}

.pagination button.active {
  background-color: var(--bloodsen-red);
  border-color: var(--bloodsen-red);
  color: #ffffff;
}

.pagination button:disabled {
  color: #c3c9d1;
  cursor: not-allowed;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {

  .page-heading h2 {
    font-size: 24px;
  }

  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-row :deep(.search-input),
  .filters-row :deep(.select-group),
  .filters-row :deep(.date-input) {
    min-width: 100%;
    width: 100%;
  }

  .participations-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .pagination {
    flex-wrap: wrap;
  }

  .empty-state {
    padding: 40px 20px;
  }

}
</style>