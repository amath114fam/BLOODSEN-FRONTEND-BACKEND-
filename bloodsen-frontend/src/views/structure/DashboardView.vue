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
            :options="statusOptionsAvecTous"
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
            <tr v-for="request in requestsPaginees" :key="request.reference">

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
              <td>
                <AppBadge :variant="badgeStatutVariant(request.statut)">
                  {{ badgeStatutLabel(request.statut) }}
                </AppBadge>
              </td>
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
            <tr v-if="requestsFiltrees.length === 0">
              <td colspan="6" class="empty-row">
                Aucune demande ne correspond à vos filtres.
              </td>
            </tr>
          </tbody>

        </table>
      </div>

      <div class="requests-footer">

      <span>
        Affichage de {{ requestsPaginees.length }}
        sur {{ requestsFiltrees.length }}
        demande{{ requestsFiltrees.length > 1 ? 's' : '' }}
        filtrée{{ requestsFiltrees.length > 1 ? 's' : '' }}
        (total : {{ stats.total }})
      </span>
      <div class="pagination">
        <button
          type="button"
          :disabled="pageActuelle === 1"
          @click="changerPage(pageActuelle - 1)"
        >
          Précédent
        </button>

        <button
          v-for="n in totalPages"
          :key="n"
          type="button"
          :class="{ active: n === pageActuelle }"
          @click="changerPage(n)"
        >
          {{ n }}
        </button>

        <button
          type="button"
          :disabled="pageActuelle === totalPages"
          @click="changerPage(pageActuelle + 1)"
        >
          Suivant
        </button>
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

        <div class="bar-chart-container">
          <BarChart
            :labels="chartLabels"
            :values="chartValues"
            :peak-index="peakIndex"
          />
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

        <div class="doughnut-container">
          <DoughnutChart
            :labels="breakdownLabels"
            :values="breakdownValues"
          />
        </div>

        <!-- Liste détaillée sous le graphique -->
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
                {{ item.donations }} don{{ item.donations > 1 ? 's' : '' }} ({{ item.percent }}%)
              </span>
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
import { computed, ref, onMounted, watch } from 'vue'
import api from '@/services/api'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import StatCard from '@/components/StatCard.vue'
import BarChart from '@/components/charts/BarChart.vue'
import DoughnutChart from '@/components/charts/DoughnutChart.vue'

// ==========================================
// ÉTAT GLOBAL
// ==========================================

const loading = ref(true)
const erreur = ref('')
const dashboard = ref(null)
const statsData = ref(null)
// ==========================================
// CHARGEMENT DES DONNÉES
// ==========================================

onMounted(async () => {
  try {
    const [dashboardRes, statsRes] = await Promise.all([
      api.get('/dashboard/structure/'),
      api.get('/dashboard/structure/stats/'),
    ])
    dashboard.value = dashboardRes.data
    statsData.value = statsRes.data
  } catch (e) {
    erreur.value = 'Impossible de charger le tableau de bord.'
  } finally {
    loading.value = false
  }
})

// ==========================================
// FILTRES
// ==========================================

const search = ref('')
const statusFilter = ref('')
const groupFilter = ref('')

// ==========================================
// PAGINATION
// ==========================================

const pageActuelle = ref(1)
const elementsParPage = ref(5)

const bloodGroups = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']

const statusOptionsAvecTous = [
  { value: '', label: 'Tous les statuts' },
  { value: 'en_cours', label: 'En cours' },
  { value: 'terminee', label: 'Terminée' },
  { value: 'expiree', label: 'Expirée' },
  { value: 'annulee', label: 'Annulée' },
]

const groupOptions = bloodGroups.map((group) => ({
  value: group,
  label: group,
}))

// ==========================================
// DONNÉES DÉRIVÉES
// ==========================================

// Compteurs (stats globales)
const stats = computed(() => {
  const c = dashboard.value?.compteurs || {}
  return {
    total: (c.demandes_actives || 0) + (c.demandes_terminees || 0),
    inProgress: c.demandes_actives || 0,
    done: c.demandes_terminees || 0,
    participations: c.participations_confirmees || 0,
  }
})

// Demandes récentes (3 dernières de l'API)
const requests = computed(() => {
  const demandes = dashboard.value?.dernieres_demandes || []
  return demandes.map(d => ({
    id: d.id,
    reference: `#DS-${d.id.toString().padStart(4, '0')}`,
    service: d.message || 'Demande de sang',
    group: d.groupe_sanguin,
    date: formaterDate(d.date_creation),
    sent: d.nombre_sollicitations || 0,
    confirmed: d.nombre_participations_confirmees || 0,
    statut: d.statut,   // ← on garde le vrai statut API
  }))
  
})

const requestsFiltrees = computed(() => {
  let resultat = requests.value

  // 1. Filtre recherche (référence ou service)
  const recherche = search.value.trim().toLowerCase()
  if (recherche) {
    resultat = resultat.filter(r =>
      r.reference.toLowerCase().includes(recherche) ||
      r.service.toLowerCase().includes(recherche)
    )
  }

  // 2. Filtre statut
  
  if (statusFilter.value) {
    resultat = resultat.filter(r => r.statut === statusFilter.value)
  }


  // 3. Filtre groupe sanguin
  if (groupFilter.value) {
    resultat = resultat.filter(r => r.group === groupFilter.value)
  }

  return resultat
})

// ==========================================
// PAGINATION
// ==========================================

// Nombre total de pages
const totalPages = computed(() => {
  return Math.max(1, Math.ceil(requestsFiltrees.value.length / elementsParPage.value))
})

// Sous-liste des demandes pour la page actuelle
const requestsPaginees = computed(() => {
  const debut = (pageActuelle.value - 1) * elementsParPage.value
  const fin = debut + elementsParPage.value
  return requestsFiltrees.value.slice(debut, fin)
})

// Change la page (avec borne)
function changerPage(nouvellePage) {
  if (nouvellePage < 1) return
  if (nouvellePage > totalPages.value) return
  pageActuelle.value = nouvellePage
}

// Réinitialise la page à 1 quand les filtres changent
watch([search, statusFilter, groupFilter], () => {
  pageActuelle.value = 1
})
// ==========================================
// FORMATAGE DE DATE
// ==========================================

function formaterDate(dateIso) {
  const date = new Date(dateIso)
  const maintenant = new Date()
  const diffHeures = (maintenant - date) / (1000 * 60 * 60)

  if (diffHeures < 24) {
    const h = date.getHours().toString().padStart(2, '0')
    const m = date.getMinutes().toString().padStart(2, '0')
    return `Aujourd'hui à ${h}:${m}`
  }

  const options = { day: '2-digit', month: 'short', year: 'numeric' }
  return date.toLocaleDateString('fr-FR', options)
}

// ==========================================
// HELPERS STATUTS
// ==========================================

function badgeStatutVariant(statut) {
  if (statut === 'en_cours') return 'info'
  if (statut === 'terminee') return 'success'
  if (statut === 'expiree') return 'warning'
  if (statut === 'annulee') return 'danger'
  return 'default'
}

function badgeStatutLabel(statut) {
  if (statut === 'en_cours') return 'En cours'
  if (statut === 'terminee') return 'Terminée'
  if (statut === 'expiree') return 'Expirée'
  if (statut === 'annulee') return 'Annulée'
  return statut
}
// ==========================================
// CHART HEBDOMADAIRE (données de l'API)
// ==========================================

const chartLabels = computed(() => {
  return statsData.value?.chart_semaine?.map(d => d.jour) || []
})

const chartValues = computed(() => {
  return statsData.value?.chart_semaine?.map(d => d.valeur) || []
})

// Index du pic (valeur maximale)
const peakIndex = computed(() => {
  const vals = chartValues.value
  if (!vals.length) return -1
  const max = Math.max(...vals)
  if (max === 0) return -1
  return vals.findIndex(v => v === max)
})

const totalWeekly = computed(() =>
  chartValues.value.reduce((sum, v) => sum + v, 0)
)

const peakDay = computed(() => {
  const labels = chartLabels.value
  const values = chartValues.value
  if (!labels.length) return { label: '—', value: 0 }
  const max = Math.max(...values)
  const idx = values.findIndex(v => v === max)
  return { label: labels[idx], value: max }
})

// ==========================================
// RÉPARTITION (données de l'API)
// ==========================================

const breakdown = computed(() => {
  const rep = statsData.value?.repartition_groupes || []
  const groupes_rares = ['O-', 'B-', 'AB-']
  return rep.map(item => ({
    label: `Groupe ${item.groupe}`,
    donations: item.dons,
    percent: item.pourcentage,
    danger: groupes_rares.includes(item.groupe),
  }))
})

const breakdownLabels = computed(() => breakdown.value.map(b => b.label))
const breakdownValues = computed(() => breakdown.value.map(b => b.donations))
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

.empty-row {
  padding: 40px 24px !important;
  text-align: center;
  color: #8a94a3;
  font-style: italic;
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