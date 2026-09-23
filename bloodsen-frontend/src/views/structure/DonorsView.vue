<template>
  <div class="donors-view">

    <!-- ==========================================
         EN-TÊTE
    =========================================== -->
    <div class="page-heading-row">
      <div class="page-heading">
        <h2>Donneurs</h2>
        <p>Suivez les donneurs ayant répondu à vos demandes.</p>
      </div>

      <AppButton
        variant="primary"
        to="/structure/demandes/creer"
      >
        <span class="plus-icon">+</span>
        Créer une demande
      </AppButton>
    </div>

    <!-- ==========================================
         STATS
    =========================================== -->
    <div class="stats-grid">

      <StatCard
        label="Donneurs sollicités"
        :value="stats.solicited"
        icon-tone="neutral"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 12L21 4L13 21L11 13L3 12Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Réponses positives"
        :value="stats.positiveResponses"
        icon-tone="success"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="2" />
            <path d="M3 19C3 15.69 5.69 13 9 13C12.31 13 15 15.69 15 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M15 9L17 11L21 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Dons complétés"
        :value="stats.completedDonations"
        icon-tone="danger"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 21C12 21 4 15.5 4 9.5C4 6.46 6.46 4 9.5 4C11.24 4 12.78 4.81 12.78 4.81C12.78 4.81 14.32 4 16.06 4C19.1 4 21.56 6.46 21.56 9.5C21.56 9.83 21.53 10.15 21.47 10.47" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M15 13L18 13L20 10L22 15L23.5 13L24 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

    </div>

    <!-- ==========================================
         FILTRES + TABLEAU
    =========================================== -->
    <AppCard padding="20px 24px" class="donors-card">

      <div class="filters-row">

        <AppInput
          id="search-donor"
          v-model="recherche"
          placeholder="Rechercher par nom, ville..."
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
          id="group-filter"
          v-model="filtreGroupe"
          placeholder="Tous les groupes"
          :options="groupeOptions"
        />

        <AppSelect
          id="participation-filter"
          v-model="filtreParticipation"
          placeholder="Toutes participations"
          :options="participationOptions"
        />

      </div>

      <!-- CHARGEMENT -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-large"></div>
        <p>Chargement des donneurs...</p>
      </div>

      <!-- TABLEAU -->
      <div v-else-if="donneursPaginees.length" class="donors-table-wrapper">
        <table class="donors-table">

          <thead>
            <tr>
              <th>Donneur</th>
              <th>Téléphone</th>
              <th>Groupe sanguin</th>
              <th>Sollicitations</th>
              <th>Dons effectués</th>
              <th>Dernière interaction</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="donor in donneursPaginees" :key="donor.id">

              <td>
                <div class="donor-cell">
                  <span class="donor-avatar">{{ donor.initiales }}</span>
                  <div>
                    <strong>{{ donor.prenom }} {{ donor.nom }}</strong>
                    <span class="donor-reference">
                      {{ donor.ville }}, {{ donor.region }}
                    </span>
                  </div>
                </div>
              </td>

              <td>{{ donor.telephone }}</td>

              <td>
                <AppBadge variant="danger">{{ donor.groupe_sanguin }}</AppBadge>
              </td>

              <td class="count-cell">
                {{ donor.nombre_sollicitations }}
              </td>

              <td class="count-cell">
                <span v-if="donor.nombre_participations > 0" class="success-count">
                  {{ donor.nombre_participations }}
                </span>
                <span v-else class="no-count">—</span>
              </td>

              <td class="date-cell">
                {{ formaterDate(donor.derniere_interaction) }}
              </td>

            </tr>
          </tbody>

        </table>
      </div>

      <!-- ÉTAT VIDE -->
      <div v-else class="empty-state">

        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="2" />
            <circle cx="16" cy="9" r="2.3" stroke="currentColor" stroke-width="2" />
            <path d="M3 19C3 15.69 5.69 13 9 13C12.31 13 15 15.69 15 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M14 14C14.83 13.37 15.86 13 17 13C19.76 13 22 15.24 22 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </div>

        <h3>Aucun donneur n'est encore lié à vos demandes.</h3>
        <p>
          Les donneurs compatibles s'afficheront ici automatiquement dès qu'ils
          répondront aux alertes et notifications de vos demandes de sang en
          cours.
        </p>

        <div class="empty-actions">
          <AppButton variant="outline" to="/structure/demandes">
            <span class="drop-icon">🩸</span>
            Consulter vos demandes en cours
          </AppButton>

          <AppButton variant="primary" to="/structure/demandes/creer">
            <span class="plus-icon">+</span>
            Créer une demande
          </AppButton>
        </div>

      </div>

      <!-- PAGINATION -->
      <div v-if="donneursFiltres.length > 0" class="donors-footer">
        <span>
          Affichage de <strong>{{ donneursPaginees.length }}</strong>
          sur <strong>{{ donneursFiltres.length }}</strong>
          donneur{{ donneursFiltres.length > 1 ? 's' : '' }}
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
            v-for="p in totalPages"
            :key="p"
            type="button"
            :class="{ active: p === pageActuelle }"
            @click="changerPage(p)"
          >
            {{ p }}
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

  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import api from '@/services/api'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'
import StatCard from '@/components/StatCard.vue'

// ==========================================
// ÉTAT GLOBAL
// ==========================================

const loading = ref(true)
const donneurs = ref([])

// ==========================================
// CHARGEMENT
// ==========================================

onMounted(async () => {
  try {
    const { data } = await api.get('/structure/donneurs/')
    donneurs.value = data
  } catch (e) {
    donneurs.value = []
  } finally {
    loading.value = false
  }
})

// ==========================================
// STATS (calculées depuis la liste)
// ==========================================

const stats = computed(() => {
  const d = donneurs.value || []
  return {
    solicited: d.length,
    positiveResponses: d.filter(x => x.nombre_participations > 0).length,
    completedDonations: d.reduce((sum, x) => sum + (x.nombre_participations || 0), 0),
  }
})

// ==========================================
// FILTRES
// ==========================================

const recherche = ref('')
const filtreGroupe = ref('')
const filtreParticipation = ref('')

const groupeOptions = [
  { value: '', label: 'Tous les groupes' },
  { value: 'O+', label: 'O+' },
  { value: 'O-', label: 'O-' },
  { value: 'A+', label: 'A+' },
  { value: 'A-', label: 'A-' },
  { value: 'B+', label: 'B+' },
  { value: 'B-', label: 'B-' },
  { value: 'AB+', label: 'AB+' },
  { value: 'AB-', label: 'AB-' },
]

const participationOptions = [
  { value: '', label: 'Toutes participations' },
  { value: 'avec_don', label: 'Avec don confirmé' },
  { value: 'sans_don', label: 'Sans don confirmé' },
]

// ==========================================
// FILTRAGE
// ==========================================

const donneursFiltres = computed(() => {
  let resultat = donneurs.value || []

  // Recherche
  const r = recherche.value.trim().toLowerCase()
  if (r) {
    resultat = resultat.filter(d =>
      (d.nom || '').toLowerCase().includes(r) ||
      (d.prenom || '').toLowerCase().includes(r) ||
      (d.ville || '').toLowerCase().includes(r) ||
      (d.region || '').toLowerCase().includes(r)
    )
  }

  // Groupe
  if (filtreGroupe.value) {
    resultat = resultat.filter(d => d.groupe_sanguin === filtreGroupe.value)
  }

  // Participation
  if (filtreParticipation.value === 'avec_don') {
    resultat = resultat.filter(d => d.nombre_participations > 0)
  } else if (filtreParticipation.value === 'sans_don') {
    resultat = resultat.filter(d => d.nombre_participations === 0)
  }

  return resultat
})

// ==========================================
// PAGINATION
// ==========================================

const pageActuelle = ref(1)
const elementsParPage = 10

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(donneursFiltres.value.length / elementsParPage))
})

const donneursPaginees = computed(() => {
  const debut = (pageActuelle.value - 1) * elementsParPage
  return donneursFiltres.value.slice(debut, debut + elementsParPage)
})

function changerPage(n) {
  if (n < 1 || n > totalPages.value) return
  pageActuelle.value = n
}

// Reset la page quand les filtres changent
watch([recherche, filtreGroupe, filtreParticipation], () => {
  pageActuelle.value = 1
})

// ==========================================
// HELPERS
// ==========================================

function formaterDate(dateIso) {
  if (!dateIso) return '—'
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
</script>

<style scoped>
.donors-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

  max-width: 720px;

  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.plus-icon {
  margin-right: 6px;
  font-size: 18px;
  line-height: 1;
}

.drop-icon {
  margin-right: 6px;
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
  min-width: 320px;
  flex: 1;
}

.filters-row :deep(.select-group) {
  min-width: 170px;
}

/* ========================================
   ÉTAT DE CHARGEMENT
======================================== */

.loading-state {
  padding: 60px 24px;
  text-align: center;
}

.loading-state p {
  margin: 16px 0 0;

  color: #6b7280;
  font-size: 14px;
}

.spinner-large {
  display: inline-block;
  width: 40px;
  height: 40px;

  border: 3px solid #e6eaf0;
  border-top-color: var(--bloodsen-red);
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========================================
   TABLE
======================================== */

.donors-table-wrapper {
  overflow-x: auto;
}

.donors-table {
  width: 100%;
  border-collapse: collapse;
}

.donors-table th {
  padding: 12px 20px;

  color: #8a94a3;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;
  white-space: nowrap;
}

.donors-table td {
  padding: 16px 20px;

  border-top: 1px solid #f0f1f3;

  color: var(--bloodsen-dark);
  font-size: 14px;

  vertical-align: middle;
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

.count-cell {
  text-align: center;
  font-weight: 600;
}

.success-count {
  color: #1e9e5a;
  font-weight: 700;
}

.no-count {
  color: #c5cdd8;
}

.date-cell {
  color: #4a5568;
  font-size: 13px;
  white-space: nowrap;
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

.empty-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

/* ========================================
   FOOTER / PAGINATION
======================================== */

.donors-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;

  gap: 12px;

  padding: 16px 0 0;

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
  .filters-row :deep(.select-group) {
    min-width: 100%;
    width: 100%;
  }

  .donors-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .empty-actions {
    flex-direction: column;
    width: 100%;
  }

  .empty-actions :deep(button) {
    width: 100%;
  }

}
</style>