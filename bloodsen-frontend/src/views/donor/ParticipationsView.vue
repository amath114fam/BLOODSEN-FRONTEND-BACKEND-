<template>
  <div class="participations-view">

    <div class="page-heading-row">
      <div class="page-heading">
        <h2>Mes participations</h2>
        <p>Suivez vos participations aux demandes de sang.</p>
      </div>
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
              <tr v-for="item in participationsAffichees" :key="item.id">

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

      <GamificationCard :profil="profil" />


  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

import AppCard from '@/components/AppCard.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'
import StatCard from '@/components/StatCard.vue'
import GamificationCard from '@/components/GamificationCard.vue'

// ==========================================
// ÉTAT GLOBAL
// ==========================================

const auth = useAuthStore()
const profil = computed(() => auth.user?.profil || {})

const loading = ref(true)
const participations = ref([])

// ==========================================
// CHARGEMENT
// ==========================================

onMounted(async () => {
  try {
    const { data } = await api.get('/participations/')
    participations.value = data
  } catch (e) {
    participations.value = []
  } finally {
    loading.value = false
  }
})

// ==========================================
// STATS
// ==========================================

const stats = computed(() => {
  const p = participations.value || []
  return {
    total: p.length,
    confirmed: p.filter(x => x.statut === 'confirmee').length,
    medicalRefusal: p.filter(x => x.statut === 'annulee').length,
  }
})

// ==========================================
// FILTRES
// ==========================================

const filters = reactive({
  status: '',
  period: '',
})

const statusOptions = [
  { value: '', label: 'Tous' },
  { value: 'confirmee', label: 'Confirmée' },
  { value: 'annulee', label: 'Annulée' },
]

const periodOptions = [
  { value: '', label: 'Toutes les périodes' },
  { value: 'month', label: 'Ce mois' },
  { value: 'year', label: 'Cette année' },
]

// ==========================================
// LISTE FILTRÉE
// ==========================================

const participationsFiltrees = computed(() => {
  let resultat = participations.value || []

  if (filters.status) {
    resultat = resultat.filter(p => p.statut === filters.status)
  }

  if (filters.period === 'month') {
    const maintenant = new Date()
    const debutMois = new Date(maintenant.getFullYear(), maintenant.getMonth(), 1)
    resultat = resultat.filter(p => new Date(p.date_confirmation) >= debutMois)
  } else if (filters.period === 'year') {
    const debutAnnee = new Date(new Date().getFullYear(), 0, 1)
    resultat = resultat.filter(p => new Date(p.date_confirmation) >= debutAnnee)
  }

  return resultat
})

// ==========================================
// TRANSFORMATION POUR L'AFFICHAGE
// ==========================================

const participationsAffichees = computed(() => {
  return participationsFiltrees.value.map(p => ({
    id: p.id,
    facility: p.structure_nom,
    group: p.demande_groupe_sanguin || p.donneur_groupe_sanguin,
    date: formaterDate(p.date_confirmation),
    location: `${p.structure_ville}`,
    status: p.statut === 'confirmee' ? 'confirmed' : 'cancelled',
  }))
})

// ==========================================
// HELPERS
// ==========================================

function formaterDate(dateIso) {
  if (!dateIso) return '—'
  const date = new Date(dateIso)
  const options = { day: '2-digit', month: 'short', year: 'numeric' }
  return date.toLocaleDateString('fr-FR', options)
}

function statusVariant(status) {
  if (status === 'confirmed') return 'success'
  if (status === 'medical_refusal') return 'danger'
  return 'default'
}

function statusLabel(status) {
  if (status === 'confirmed') return 'Confirmée'
  if (status === 'medical_refusal') return 'Refus médical'
  return 'Annulée'
}
</script>

<style scoped>
/* ========================================
   PAGE
======================================== */

.participations-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}



/* ========================================
   CARTE PARTICIPATIONS
======================================== */

.participations-card {
  min-width: 0;
}

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
  -webkit-overflow-scrolling: touch;
}

.participations-table {
  width: 100%;
  min-width: 600px;
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

/* Tablette : stats en 2 colonnes */
@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Mobile */
@media (max-width: 700px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page-heading h2 {
    font-size: 24px;
  }

  .page-heading-row :deep(button) {
    width: 100%;
  }

  .card-header {
    flex-direction: column;
    align-items: stretch;
    padding: 16px 20px;
  }

  .filters-row {
    flex-direction: column;
    align-items: stretch;
  }

  .inline-select {
    width: 100%;
  }

  .inline-select :deep(.select-group) {
    flex: 1;
    min-width: 0;
  }

  .participations-table th,
  .participations-table td {
    padding: 12px 16px;
  }
}
</style>