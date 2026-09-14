<template>
  <div class="participations-view">

    <div class="page-heading-row">
      <div class="page-heading">
        <h2>Mes participations</h2>
        <p>Suivez vos participations aux demandes de sang.</p>
      </div>

      <AppButton variant="primary" to="/donneur/sollicitations">
        Nouvelle participation
      </AppButton>
    </div>

    <!-- Indicateurs -->
    <div class="stats-grid">

      <StatCard label="PARTICIPATIONS" :value="stats.total">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="DONS CONFIRMÉS" :value="stats.confirmed" icon-tone="success">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="REFUS MÉDICAUX" :value="stats.medicalRefusal" icon-tone="danger">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L19 6V11C19 15.5 16 19.5 12 21C8 19.5 5 15.5 5 11V6L12 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

    </div>

    <div class="content-grid">

      <!-- Liste des participations -->
      <AppCard padding="0" class="participations-card">

        <div class="card-header">

          <div class="card-title">
            <span class="info-dot">i</span>
            <h3>Liste des participations</h3>
          </div>

          <div class="filters-row">

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
              <span class="inline-select-label">Période:</span>
              <AppSelect
                id="period-filter"
                v-model="filters.period"
                placeholder="Cette année"
                :options="periodOptions"
              />
            </div>

          </div>

        </div>

        <div class="participations-table-wrapper">
          <table class="participations-table">

            <thead>
              <tr>
                <th>Structure de santé</th>
                <th>Groupe</th>
                <th>Date</th>
                <th>Lieu</th>
                <th>Statut</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="item in participations" :key="item.id">

                <td>
                  <strong>{{ item.facility }}</strong>
                </td>

                <td>
                  <span class="group-text">{{ item.group }}</span>
                </td>

                <td class="date-cell">
                  {{ item.date }}
                </td>

                <td class="location-cell">
                  {{ item.location }}
                </td>

                <td>
                  <AppBadge :variant="statusVariant(item.status)">
                    {{ statusLabel(item.status) }}
                  </AppBadge>
                </td>

              </tr>
            </tbody>

          </table>
        </div>

      </AppCard>

      <!-- Engagement -->
      <EngagementCard
        level="Donneur Argent"
        progress-label="Prochain palier"
        :current="engagement.current"
        :target="engagement.target"
        low-tier-label="ARGENT"
        high-tier-label="OR (HÉROS)"
        :participations="engagement.participations"
        :points="engagement.points"
      />

    </div>

  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

import AppCard from '@/components/AppCard.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'
import StatCard from '@/components/StatCard.vue'
import EngagementCard from '@/components/EngagementCard.vue'

const stats = ref({
  total: 28,
  confirmed: 28,
  medicalRefusal: 1,
})

const filters = reactive({
  status: '',
  period: '',
})

const statusOptions = [
  { value: 'confirmed', label: 'Confirmée' },
  { value: 'medical_refusal', label: 'Refus médical' },
  { value: 'cancelled', label: 'Annulée' },
]

const periodOptions = [
  { value: 'month', label: 'Ce mois' },
  { value: 'year', label: 'Cette année' },
  { value: 'all', label: 'Toutes les périodes' },
]

const participations = ref([
  { id: 1, facility: 'Hôpital Principal', group: 'O+', date: '12 Oct 2023', location: 'Dakar, Plateau', status: 'confirmed' },
  { id: 2, facility: 'Centre de Santé Phillippe', group: 'A+', date: '24 Oct 2023', location: 'Yoff, Dakar', status: 'confirmed' },
  { id: 3, facility: 'Hôpital Dalal Jamm', group: 'O+', date: '05 Sep 2023', location: 'Guédiawaye', status: 'confirmed' },
  { id: 4, facility: 'Clinique des Madeleines', group: 'B-', date: '20 Août 2023', location: 'Dakar, Centre', status: 'confirmed' },
  { id: 5, facility: "Hôpital Militaire d'Ouakam", group: 'O+', date: '15 Juil 2023', location: 'Ouakam, Dakar', status: 'confirmed' },
])

const engagement = ref({
  current: 24,
  target: 30,
  participations: 28,
  points: 1420,
})

function statusVariant(status) {
  if (status === 'confirmed') return 'success'
  if (status === 'medical_refusal') return 'danger'
  return 'default' // cancelled
}

function statusLabel(status) {
  if (status === 'confirmed') return 'Confirmée'
  if (status === 'medical_refusal') return 'Refus médical'
  return 'Annulée'
}

// TODO : remplacer stats/participations/engagement par un appel API réel
</script>

<style scoped>
.participations-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========================================
   EN-TÊTE
======================================== */

.page-heading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
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
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* ========================================
   GRILLE PRINCIPALE
======================================== */

.content-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 20px;
  align-items: start;
}

/* ========================================
   CARTE PARTICIPATIONS
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

.info-dot {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 20px;
  height: 20px;

  border-radius: 50%;

  background-color: var(--bloodsen-red);
  color: #ffffff;

  font-size: 11px;
  font-weight: 700;
  font-style: italic;
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
  min-width: 140px;
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
  padding: 12px 24px;

  color: #8a94a3;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;

  white-space: nowrap;
}

.participations-table td {
  padding: 16px 24px;

  border-top: 1px solid #f0f1f3;

  color: var(--bloodsen-dark);
  font-size: 14px;

  vertical-align: middle;

  white-space: nowrap;
}

.participations-table td strong {
  white-space: normal;
}

.group-text {
  color: var(--bloodsen-red);
  font-size: 14px;
  font-weight: 700;
}

.date-cell,
.location-cell {
  color: #4a5568;
  font-size: 13px;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {

  .page-heading h2 {
    font-size: 24px;
  }

  .page-heading-row :deep(button) {
    width: 100%;
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

}
</style>