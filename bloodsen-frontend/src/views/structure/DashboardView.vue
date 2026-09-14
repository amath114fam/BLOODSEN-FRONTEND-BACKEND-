<template>
  <div class="dashboard-view">

    <div class="page-heading">
      <h2>Tableau de bord</h2>

      <p>
        Supervisez vos demandes de poches de sang, mobilisez les donneurs
        compatibles de Dakar et suivez les dons en temps réel.
      </p>
    </div>

    <!-- Indicateurs -->
    <div class="stats-grid">

      <StatCard
        label="TOTAL DEMANDES"
        :value="stats.total"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="3" width="14" height="18" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M9 8H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M9 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="DEMANDES EN COURS"
        :value="stats.inProgress"
        highlight
        icon-tone="danger"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L14 9H20L15 13L17 20L12 16L7 20L9 13L4 9H10L12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="DEMANDES TERMINÉES"
        :value="stats.done"
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
        label="PARTICIPATIONS"
        :value="stats.participations"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="8" cy="8" r="3" stroke="currentColor" stroke-width="2" />
            <path d="M2 19C2 15.69 4.69 13 8 13C11.31 13 14 15.69 14 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M14 5L16 7L20 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

    </div>

    <!-- Tableau des demandes récentes -->
    <AppCard padding="0" class="requests-card">

      <div class="requests-header">

        <div>
          <h3>Demandes récentes de sang</h3>
          <p>Historique opérationnel et suivi direct des admissions de donneurs</p>
        </div>

        <div class="requests-filters">

          <AppInput
            id="search-request"
            v-model="search"
            placeholder="Référence ou service..."
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
            id="status-filter"
            v-model="statusFilter"
            placeholder="Tous les statuts"
            :options="statusOptions"
          />

          <AppSelect
            id="group-filter"
            v-model="groupFilter"
            placeholder="Tous groupes"
            :options="groupOptions"
          />

        </div>

      </div>

      <div class="requests-table-wrapper">
        <table class="requests-table">

          <thead>
            <tr>
              <th>Demande / Référence</th>
              <th>Groupe</th>
              <th>Date &amp; heure</th>
              <th>Sollicitations &amp; réponses</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="request in requests" :key="request.reference">

              <td>
                <strong>{{ request.reference }}</strong>
                <span class="request-service">{{ request.service }}</span>
              </td>

              <td>
                <span class="group-pill">{{ request.group }}</span>
              </td>

              <td class="date-cell">
                {{ request.date }}
              </td>

              <td class="soliciting-cell">
                {{ request.sent }} envoyées • {{ request.confirmed }} confirmé{{ request.confirmed > 1 ? 's' : '' }}
              </td>

              <td>
                <AppBadge :variant="request.status === 'progress' ? 'info' : 'default'">
                  {{ request.status === 'progress' ? 'En cours' : 'Terminée' }}
                </AppBadge>
              </td>

              <td>
                <router-link
                  :to="`/structure/demandes/${request.reference}`"
                  class="details-link"
                >
                  Détails
                </router-link>
              </td>

            </tr>
          </tbody>

        </table>
      </div>

      <div class="requests-footer">

        <span>Affichage de 6 sur {{ stats.total }} demandes</span>

        <div class="pagination">
          <button type="button">Précédent</button>
          <button type="button" class="active">1</button>
          <button type="button">2</button>
          <button type="button">Suivant</button>
        </div>

      </div>

    </AppCard>

    <!-- Bas de page : chart + répartition -->
    <div class="bottom-grid">

      <AppCard class="weekly-card">

        <div class="weekly-header">
          <div>
            <h3>Demandes de la semaine</h3>
            <p>Volume journalier enregistré au CHNU de Fann</p>
          </div>

          <span class="week-tag">Semaine en cours</span>
        </div>

        <div class="bar-chart">
          <div
            v-for="day in weeklyData"
            :key="day.label"
            class="bar-column"
          >
            <span class="bar-value" :class="{ peak: day.peak }">
              {{ day.value }}
            </span>

            <div
              class="bar"
              :class="{ peak: day.peak, muted: day.muted }"
              :style="{ height: (day.value / maxWeeklyValue) * 90 + 'px' }"
            ></div>

            <span class="bar-label">{{ day.label }}</span>
          </div>
        </div>

        <div class="weekly-footer">
          <span>Pic d'affluence : {{ peakDay.label === 'Mer' ? 'Mercredi' : peakDay.label }} ({{ peakDay.value }})</span>
          <strong>Total : {{ totalWeekly }} poches</strong>
        </div>

      </AppCard>

      <AppCard class="breakdown-card">

        <div class="breakdown-header">
          <h3>Répartition des dons effectifs</h3>
          <span>{{ stats.participations }} poches</span>
        </div>

        <p class="breakdown-subtitle">
          Volume par groupe sanguin dans notre banque
        </p>

        <div class="breakdown-list">

          <div
            v-for="item in breakdown"
            :key="item.label"
            class="breakdown-item"
          >

            <div class="breakdown-item-top">
              <span class="breakdown-label" :class="{ danger: item.danger }">
                {{ item.label }}
              </span>

              <span class="breakdown-value" :class="{ danger: item.danger }">
                {{ item.donations }} dons ({{ item.percent }}%)
              </span>
            </div>

            <div class="breakdown-bar-track">
              <div
                class="breakdown-bar-fill"
                :class="{ danger: item.danger }"
                :style="{ width: item.percent + '%' }"
              ></div>
            </div>

          </div>

        </div>

        <p class="breakdown-alert">
          Besoin prioritaire récurrent : O- et B- sur Dakar
        </p>

      </AppCard>

    </div>

  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import StatCard from '@/components/StatCard.vue'

const search = ref('')
const statusFilter = ref('')
const groupFilter = ref('')

const bloodGroups = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']

const statusOptions = [
  { value: 'progress', label: 'En cours' },
  { value: 'done', label: 'Terminée' },
]

const groupOptions = bloodGroups.map((group) => ({
  value: group,
  label: group,
}))

const stats = ref({
  total: 148,
  inProgress: 6,
  done: 135,
  participations: 428,
})

const requests = ref([
  {
    reference: '#DS-2025-142',
    service: 'Maternité • CHU Fann',
    group: 'O-',
    date: "Aujourd'hui à 11:24",
    sent: 14,
    confirmed: 2,
    status: 'progress',
  },
  {
    reference: '#DS-2025-141',
    service: 'Service Réanimation • CHU Fann',
    group: 'B+',
    date: "Aujourd'hui à 09:40",
    sent: 9,
    confirmed: 1,
    status: 'progress',
  },
  {
    reference: '#DS-2025-139',
    service: 'Chirurgie Cardiovasculaire • Pavillon Spécial',
    group: 'A+',
    date: "Aujourd'hui à 07:15",
    sent: 18,
    confirmed: 5,
    status: 'progress',
  },
  {
    reference: '#DS-2025-138',
    service: 'Urgences Pédiatriques • CHU Fann',
    group: 'O+',
    date: 'Hier à 16:45',
    sent: 18,
    confirmed: 5,
    status: 'done',
  },
  {
    reference: '#DS-2025-135',
    service: 'Oncologie • Hôpital Aristide Le Dantec (Transféré)',
    group: 'AB+',
    date: '05 Mai 2025 à 14:10',
    sent: 18,
    confirmed: 5,
    status: 'done',
  },
  {
    reference: '#DS-2025-131',
    service: 'Chirurgie Orthopédique • CHU Fann',
    group: 'A-',
    date: '03 Mai 2025 à 18:00',
    sent: 18,
    confirmed: 5,
    status: 'done',
  },
])

const weeklyData = ref([
  { label: 'Lun', value: 4 },
  { label: 'Mar', value: 7 },
  { label: 'Mer', value: 10, peak: true },
  { label: 'Jeu', value: 5 },
  { label: 'Ven', value: 6 },
  { label: 'Sam', value: 2, muted: true },
  { label: 'Dim', value: 3, muted: true },
])

const maxWeeklyValue = computed(() =>
  Math.max(...weeklyData.value.map((d) => d.value))
)

const totalWeekly = computed(() =>
  weeklyData.value.reduce((sum, d) => sum + d.value, 0)
)

const peakDay = computed(() =>
  weeklyData.value.reduce((max, d) => (d.value > max.value ? d : max))
)

const breakdown = ref([
  { label: 'O Positif (O+)', donations: 205, percent: 48 },
  { label: 'A Positif (A+)', donations: 112, percent: 26 },
  { label: 'B Positif (B+)', donations: 68, percent: 16 },
  { label: 'O Négatif & Rares', donations: 43, percent: 10, danger: true },
])

// TODO : remplacer stats/requests/weeklyData/breakdown par un appel API réel
</script>

<style scoped>
.dashboard-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========================================
   EN-TÊTE DE PAGE
======================================== */

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
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

/* ========================================
   TABLEAU DES DEMANDES
======================================== */

.requests-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;

  gap: 16px;

  padding: 20px 24px;

  border-bottom: 1px solid #e7e9ed;
}

.requests-header h3 {
  margin: 0 0 4px;

  color: var(--bloodsen-dark);

  font-size: 17px;
  font-weight: 700;
}

.requests-header p {
  margin: 0;

  color: #6b7280;

  font-size: 13px;
}

.requests-filters {
  display: flex;
  align-items: center;
  gap: 10px;

  flex-wrap: wrap;
}

.requests-filters :deep(.search-input),
.requests-filters :deep(.select-group),
.requests-filters :deep(.app-select) {
  margin: 0;
}

.requests-filters :deep(.search-input) {
  min-width: 220px;
}

.requests-filters :deep(.select-group select),
.requests-filters :deep(.app-select select) {
  min-width: 150px;
}

/* ========================================
   TABLE
======================================== */

.requests-table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.requests-table th {
  padding: 12px 24px;

  color: #8a94a3;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;

  white-space: nowrap;
}

.requests-table td {
  padding: 16px 24px;

  border-top: 1px solid #f0f1f3;

  color: var(--bloodsen-dark);
  font-size: 14px;

  vertical-align: middle;
}

.requests-table td strong {
  display: block;
  font-size: 14px;
}

.request-service {
  display: block;

  margin-top: 2px;

  color: #8a94a3;
  font-size: 12.5px;
}

.group-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-width: 44px;
  padding: 4px 10px;

  border: 1px solid #f0d3d3;
  border-radius: 20px;

  background-color: #fdf1f1;
  color: var(--bloodsen-red);

  font-size: 12px;
  font-weight: 700;
}

.date-cell,
.soliciting-cell {
  color: #4a5568;
  font-size: 13px;
  white-space: nowrap;
}

.details-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  padding: 7px 16px;

  border: 1px solid #d9dde2;
  border-radius: 6px;

  color: var(--bloodsen-dark);

  font-size: 13px;
  font-weight: 600;

  text-decoration: none;

  white-space: nowrap;
}

.details-link:hover {
  border-color: var(--bloodsen-red);
  color: var(--bloodsen-red);
}

/* ========================================
   FOOTER DU TABLEAU
======================================== */

.requests-footer {
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
  gap: 6px;
  flex-wrap: wrap;
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
  background-color: var(--bloodsen-dark);
  border-color: var(--bloodsen-dark);
  color: #ffffff;
}

/* ========================================
   BAS DE PAGE
======================================== */

.bottom-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 20px;
}

/* Chart */

.weekly-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;

  margin-bottom: 20px;
}

.weekly-header h3 {
  margin: 0 0 4px;

  color: var(--bloodsen-dark);

  font-size: 16px;
  font-weight: 700;
}

.weekly-header p {
  margin: 0;

  color: #6b7280;

  font-size: 13px;
}

.week-tag {
  padding: 5px 12px;

  border-radius: 20px;

  background-color: #f1f3f5;
  color: #4a5568;

  font-size: 12px;
  font-weight: 600;

  white-space: nowrap;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;

  gap: 12px;

  height: 130px;

  margin-bottom: 16px;
}

.bar-column {
  display: flex;
  flex-direction: column;
  align-items: center;

  gap: 6px;

  flex: 1;
}

.bar-value {
  color: #4a5568;
  font-size: 12px;
  font-weight: 600;
}

.bar-value.peak {
  color: var(--bloodsen-red);
  font-weight: 700;
}

.bar {
  width: 100%;
  max-width: 28px;

  border-radius: 4px 4px 0 0;

  background-color: var(--bloodsen-dark);
}

.bar.peak {
  background-color: var(--bloodsen-red);
}

.bar.muted {
  background-color: #d9dde2;
}

.weekly-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 6px;

  padding-top: 14px;

  border-top: 1px solid #f0f1f3;

  color: #6b7280;
  font-size: 13px;
}

.weekly-footer strong {
  color: var(--bloodsen-dark);
}

/* Breakdown */

.breakdown-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 6px;
}

.breakdown-header h3 {
  margin: 0;

  color: var(--bloodsen-dark);

  font-size: 16px;
  font-weight: 700;
}

.breakdown-header span {
  color: #6b7280;
  font-size: 13px;
}

.breakdown-subtitle {
  margin: 4px 0 20px;

  color: #6b7280;

  font-size: 13px;
}

.breakdown-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.breakdown-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 4px;

  margin-bottom: 6px;
}

.breakdown-label {
  color: var(--bloodsen-dark);
  font-size: 13.5px;
  font-weight: 600;
}

.breakdown-label.danger {
  color: var(--bloodsen-red);
}

.breakdown-value {
  color: #6b7280;
  font-size: 13px;
}

.breakdown-value.danger {
  color: var(--bloodsen-red);
  font-weight: 600;
}

.breakdown-bar-track {
  height: 6px;

  border-radius: 4px;

  background-color: #f1f3f5;
  overflow: hidden;
}

.breakdown-bar-fill {
  height: 100%;

  border-radius: 4px;

  background-color: var(--bloodsen-dark);
}

.breakdown-bar-fill.danger {
  background-color: var(--bloodsen-red);
}

.breakdown-alert {
  margin: 18px 0 0;

  color: var(--bloodsen-red);

  font-size: 13px;
  font-weight: 600;
}

/* ========================================
   RESPONSIVE
======================================== */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .bottom-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page-heading h2 {
    font-size: 24px;
  }

  .requests-header {
    flex-direction: column;
    align-items: stretch;
  }

  .requests-filters {
    width: 100%;
  }

  .requests-filters :deep(.search-input) {
    min-width: 100%;
  }

  .requests-filters :deep(.select-group) {
    flex: 1;
    min-width: 0;
  }

  .weekly-card,
  .breakdown-card {
    padding: 20px !important;
  }

  .bar-chart {
    gap: 6px;
  }

  .requests-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>