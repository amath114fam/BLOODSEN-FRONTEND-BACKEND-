<template>
  <div class="historique-view">

    <div class="page-heading">
      <h2>Mon historique</h2>
      <p>Retrouvez l'historique de vos participations et dons confirmés.</p>
    </div>

    <!-- Indicateurs -->
    <div class="stats-grid">

      <StatCard label="TOTAL DES PARTICIPATIONS" :value="stats.total">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="POINTS OBTENUS" :value="`${stats.points} pts`" icon-tone="success">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L14 9H20L15 13L17 20L12 16L7 20L9 13L4 9H10L12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

    </div>

    <!-- Journal d'activités -->
    <AppCard padding="0" class="activity-card">

      <div class="card-header">

        <div class="card-title">
          <span class="title-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 17L9 11L13 15L21 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M15 7H21V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>
          <h3>Journal d'activités</h3>
        </div>

        <div class="filters-row">

          <div class="inline-select">
            <span class="inline-select-label">Période:</span>
            <AppSelect
              id="period-filter"
              v-model="filters.period"
              placeholder="Toutes"
              :options="periodOptions"
            />
          </div>

          <div class="inline-select">
            <span class="inline-select-label">Statut:</span>
            <AppSelect
              id="status-filter"
              v-model="filters.status"
              placeholder="Tous"
              :options="statusOptions"
            />
          </div>

          <div class="inline-select">
            <span class="inline-select-label">Structure:</span>
            <AppSelect
              id="facility-filter"
              v-model="filters.facility"
              placeholder="Toutes"
              :options="facilityOptions"
            />
          </div>

        </div>

      </div>

      <div class="activity-table-wrapper">
        <table class="activity-table">

          <thead>
            <tr>
              <th>Date</th>
              <th>Structure de santé</th>
              <th>Groupe</th>
              <th>Type d'événement</th>
              <th>Statut</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="entry in entries" :key="entry.id">

              <td class="date-cell">
                {{ entry.date }}
              </td>

              <td>
                <strong>{{ entry.facility }}</strong>
                <span class="facility-location">{{ entry.location }}</span>
              </td>

              <td>
                <span class="group-text">{{ entry.group }}</span>
              </td>

              <td class="event-cell">
                {{ entry.eventType }}
              </td>

              <td>
                <AppBadge :variant="statusVariant(entry.status)">
                  {{ statusLabel(entry.status) }}
                </AppBadge>
              </td>

            </tr>
          </tbody>

        </table>
      </div>

      <div class="activity-footer">

        <span>Affichage de {{ pagination.from }}-{{ pagination.to }} sur {{ pagination.total }} entrées</span>

        <div class="pagination">
          <button type="button" :disabled="pagination.page === 1" @click="goToPage(pagination.page - 1)">
            Précédent
          </button>
          <button type="button" :disabled="pagination.page === pagination.totalPages" @click="goToPage(pagination.page + 1)">
            Suivant
          </button>
        </div>

      </div>

    </AppCard>

  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

import AppCard from '@/components/AppCard.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import StatCard from '@/components/StatCard.vue'

const stats = ref({
  total: 12,
  points: 450,
})

const filters = reactive({
  period: '',
  status: '',
  facility: '',
})

const periodOptions = [
  { value: 'month', label: 'Ce mois' },
  { value: 'year', label: 'Cette année' },
  { value: 'all', label: 'Toutes' },
]

const statusOptions = [
  { value: 'confirmed', label: 'Confirmé' },
  { value: 'cancelled', label: 'Annulé' },
]

const facilityOptions = [
  { value: 'hopital-principal', label: 'Hôpital Principal de Dakar' },
  { value: 'cnts-fann', label: 'Centre de Transfusion Sanguine' },
  { value: 'clinique-madeleine', label: 'Clinique de la Madeleine' },
  { value: 'hopital-ouakam', label: "Hôpital Militaire d'Ouakam" },
]

const entries = ref([
  {
    id: 1,
    date: '12 Oct 2023',
    facility: 'Hôpital Principal de Dakar',
    location: 'Plateau, Dakar',
    group: 'O+',
    eventType: 'Don de sang',
    status: 'confirmed',
  },
  {
    id: 2,
    date: '05 Aoû 2023',
    facility: 'Centre de Transfusion Sanguine',
    location: 'Fann, Dakar',
    group: 'O+',
    eventType: 'Don de sang',
    status: 'cancelled',
  },
  {
    id: 3,
    date: '20 Mai 2023',
    facility: 'Clinique de la Madeleine',
    location: 'Dakar Centre',
    group: 'O+',
    eventType: 'Don de sang',
    status: 'confirmed',
  },
  {
    id: 4,
    date: '15 Jan 2023',
    facility: "Hôpital Militaire d'Ouakam",
    location: 'Ouakam, Dakar',
    group: 'O+',
    eventType: 'Don de sang',
    status: 'confirmed',
  },
])

const pagination = reactive({
  page: 1,
  from: 1,
  to: 4,
  total: 12,
  totalPages: 3,
})

function statusVariant(status) {
  return status === 'confirmed' ? 'success' : 'default'
}

function statusLabel(status) {
  return status === 'confirmed' ? 'Confirmé' : 'Annulé'
}

function goToPage(page) {
  if (page < 1 || page > pagination.totalPages) return
  pagination.page = page
  // Plus tard : appel API paginé GET /historique?page=...
}

// TODO : remplacer stats/entries par un appel API réel
</script>

<style scoped>
.historique-view {
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

  color: #6b7280;

  font-size: 14px;
}

/* ========================================
   INDICATEURS
======================================== */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

/* ========================================
   CARTE JOURNAL D'ACTIVITÉS
======================================== */

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;

  gap: 12px;

  padding: 18px 24px;

  border-bottom: 1px solid #e7e9ed;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--bloodsen-red);
}

.title-icon svg {
  width: 18px;
  height: 18px;
}

.card-title h3 {
  margin: 0;

  color: var(--bloodsen-dark);

  font-size: 16px;
  font-weight: 700;
}

.filters-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.inline-select {
  display: flex;
  align-items: center;
  gap: 8px;
}

.inline-select-label {
  color: #6b7280;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.inline-select :deep(.select-group) {
  min-width: 130px;
}

/* ========================================
   TABLE
======================================== */

.activity-table-wrapper {
  overflow-x: auto;
}

.activity-table {
  width: 100%;
  border-collapse: collapse;
}

.activity-table th {
  padding: 12px 24px;

  color: #8a94a3;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;

  white-space: nowrap;
}

.activity-table td {
  padding: 16px 24px;

  border-top: 1px solid #f0f1f3;

  color: var(--bloodsen-dark);
  font-size: 14px;

  vertical-align: middle;

  white-space: nowrap;
}

.activity-table td strong {
  display: block;
  font-size: 14px;
  white-space: normal;
}

.facility-location {
  display: block;
  margin-top: 2px;

  color: #8a94a3;
  font-size: 12.5px;
}

.group-text {
  color: var(--bloodsen-red);
  font-size: 14px;
  font-weight: 700;
}

.date-cell,
.event-cell {
  color: #4a5568;
  font-size: 13px;
}

/* ========================================
   FOOTER / PAGINATION
======================================== */

.activity-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;

  gap: 12px;

  padding: 16px 24px;

  color: #6b7280;
  font-size: 13px;
}

.pagination {
  display: flex;
  gap: 8px;
}

.pagination button {
  padding: 7px 16px;

  border: 1px solid #d9dde2;
  border-radius: 6px;

  background-color: #ffffff;
  color: var(--bloodsen-dark);

  font-family: inherit;
  font-size: 13px;
  font-weight: 600;

  cursor: pointer;
}

.pagination button:not(:disabled):hover {
  border-color: var(--bloodsen-red);
  color: var(--bloodsen-red);
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

  .card-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }

  .inline-select :deep(.select-group) {
    flex: 1;
    min-width: 0;
  }

  .activity-footer {
    flex-direction: column;
    align-items: flex-start;
  }

}
</style>