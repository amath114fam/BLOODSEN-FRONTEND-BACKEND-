<template>
  <div class="requests-view">

    <!-- ==========================================
         EN-TÊTE
    =========================================== -->
    <div class="page-heading-row">
      <div class="page-heading">
        <h2>Mes demandes de sang</h2>
        <p>Gérez vos demandes en cours, terminées et annulées.</p>
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

      <StatCard label="TOTAL" :value="stats.total">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="3" width="14" height="18" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M9 8H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M9 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="EN COURS" :value="stats.en_cours" highlight icon-tone="danger">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M12 7V12L15 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="TERMINÉES" :value="stats.terminee" icon-tone="success">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="ANNULÉES" :value="stats.annulee">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M9 9L15 15M15 9L9 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </template>
      </StatCard>

    </div>

    <!-- ==========================================
         LISTE
    =========================================== -->
    <AppCard padding="0" class="requests-card">

      <div class="requests-header">
        <div>
          <h3>Liste des demandes</h3>
          <p>Suivi opérationnel des admissions et des sollicitations</p>
        </div>

        <div class="requests-filters">

          <AppInput
            id="search-request"
            v-model="recherche"
            placeholder="Rechercher..."
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
            id="filter-statut"
            v-model="filtreStatut"
            placeholder="Tous les statuts"
            :options="statutOptions"
          />

          <AppSelect
            id="filter-groupe"
            v-model="filtreGroupe"
            placeholder="Tous groupes"
            :options="groupeOptions"
          />

          <AppSelect
            id="filter-urgence"
            v-model="filtreUrgence"
            placeholder="Toutes urgences"
            :options="urgenceOptions"
          />

        </div>
      </div>

      <!-- ÉTAT DE CHARGEMENT -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-large"></div>
        <p>Chargement des demandes...</p>
      </div>

      <!-- ÉTAT VIDE -->
      <div v-else-if="demandesPaginees.length === 0" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>Aucune demande trouvée</h3>
        <p v-if="demandesFiltrees.length === 0 && demandesStore.demandes.length === 0">
          Vous n'avez encore créé aucune demande.
        </p>
        <p v-else>
          Aucune demande ne correspond à vos filtres.
        </p>
        <AppButton
          v-if="demandesStore.demandes.length === 0"
          variant="primary"
          to="/structure/demandes/creer"
        >
          Créer ma première demande
        </AppButton>
      </div>

      <!-- TABLEAU -->
      <div v-else class="requests-table-wrapper">
        <table class="requests-table">

          <thead>
            <tr>
              <th>Référence</th>
              <th>Groupe</th>
              <th>Quantité</th>
              <th>Urgence</th>
              <th>Date limite</th>
              <th>Sollicitations</th>
              <th>Statut</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="demande in demandesPaginees" :key="demande.id">

              <td>
                <strong>#DS-{{ demande.id.toString().padStart(4, '0') }}</strong>
                <span v-if="demande.message" class="request-service">
                  {{ demande.message.slice(0, 40) }}{{ demande.message.length > 40 ? '...' : '' }}
                </span>
              </td>

              <td>
                <span class="group-pill">{{ demande.groupe_sanguin }}</span>
              </td>

              <td>
                {{ demande.quantite }} poche{{ demande.quantite > 1 ? 's' : '' }}
              </td>

              <td>
                <AppBadge :variant="urgenceVariant(demande.urgence)">
                  {{ urgenceLabel(demande.urgence) }}
                </AppBadge>
              </td>

              <td class="date-cell">
                {{ formaterDate(demande.date_limite) }}
              </td>

              <td class="soliciting-cell">
                {{ demande.nombre_sollicitations || 0 }} envoyée{{ (demande.nombre_sollicitations || 0) > 1 ? 's' : '' }}
                <span v-if="demande.nombre_participations_confirmees > 0" class="confirmed-info">
                  • {{ demande.nombre_participations_confirmees }} confirmé{{ demande.nombre_participations_confirmees > 1 ? 's' : '' }}
                </span>
              </td>

              <td>
                <AppBadge :variant="statutVariant(demande.statut)">
                  {{ statutLabel(demande.statut) }}
                </AppBadge>
              </td>

              <td>
                <div class="actions-cell">
                  <button
                    v-if="demande.statut === 'en_cours'"
                    type="button"
                    class="action-button danger"
                    @click="ouvrirConfirmationAnnulation(demande)"
                  >
                    Annuler
                  </button>
                  <span v-else class="no-action">—</span>
                </div>
              </td>

            </tr>
          </tbody>

        </table>
      </div>

      <!-- FOOTER -->
      <div v-if="demandesFiltrees.length > 0" class="requests-footer">
        <span>
          Affichage de {{ demandesPaginees.length }}
          sur {{ demandesFiltrees.length }}
          demande{{ demandesFiltrees.length > 1 ? 's' : '' }}
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

    <!-- ==========================================
         MODAL DE CONFIRMATION
    =========================================== -->
    <div v-if="demandeAnnulation" class="modal-overlay" @click.self="fermerConfirmation">
      <div class="modal-box">
        <div class="modal-icon danger">
          <AlertTriangle :size="32" :stroke-width="2.5" />
        </div>
        <h3>Annuler cette demande ?</h3>
        <p>
          La demande <strong>#DS-{{ demandeAnnulation.id.toString().padStart(4, '0') }}</strong>
          sera marquée comme annulée. Cette action est irréversible.
        </p>

        <div class="modal-actions">
          <AppButton
            variant="outline"
            :disabled="annulationEnCours"
            @click="fermerConfirmation"
          >
            Retour
          </AppButton>
          <AppButton
            variant="primary"
            :disabled="annulationEnCours"
            @click="confirmerAnnulation"
          >
            <template v-if="annulationEnCours">
              <span class="spinner-small"></span>
              Annulation...
            </template>
            <template v-else>
              Oui, annuler
            </template>
          </AppButton>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useDemandesStore } from '@/stores/demandes'
import { AlertTriangle } from 'lucide-vue-next'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'
import StatCard from '@/components/StatCard.vue'

const demandesStore = useDemandesStore()

// ==========================================
// CHARGEMENT INITIAL
// ==========================================

const loading = ref(true)

onMounted(async () => {
  try {
    await demandesStore.chargerDemandes()
  } finally {
    loading.value = false
  }
})

// ==========================================
// FILTRES
// ==========================================

const recherche = ref('')
const filtreStatut = ref('')
const filtreGroupe = ref('')
const filtreUrgence = ref('')

const statutOptions = [
  { value: '', label: 'Tous les statuts' },
  { value: 'en_cours', label: 'En cours' },
  { value: 'terminee', label: 'Terminée' },
  { value: 'expiree', label: 'Expirée' },
  { value: 'annulee', label: 'Annulée' },
]

const groupeOptions = [
  { value: '', label: 'Tous groupes' },
  { value: 'O+', label: 'O+' },
  { value: 'O-', label: 'O-' },
  { value: 'A+', label: 'A+' },
  { value: 'A-', label: 'A-' },
  { value: 'B+', label: 'B+' },
  { value: 'B-', label: 'B-' },
  { value: 'AB+', label: 'AB+' },
  { value: 'AB-', label: 'AB-' },
]

const urgenceOptions = [
  { value: '', label: 'Toutes urgences' },
  { value: 'vitale', label: 'Urgence vitale' },
  { value: 'urgent', label: 'Urgent' },
  { value: 'programme', label: 'Programmé' },
]

// ==========================================
// STATS (calculées depuis la liste)
// ==========================================

const stats = computed(() => {
  const d = demandesStore.demandes || []
  return {
    total: d.length,
    en_cours: d.filter(x => x.statut === 'en_cours').length,
    terminee: d.filter(x => x.statut === 'terminee').length,
    annulee: d.filter(x => x.statut === 'annulee').length,
  }
})

// ==========================================
// FILTRAGE
// ==========================================

const demandesFiltrees = computed(() => {
  let resultat = demandesStore.demandes || []

  // Recherche (référence ou message)
  const r = recherche.value.trim().toLowerCase()
  if (r) {
    resultat = resultat.filter(d =>
      `#ds-${d.id.toString().padStart(4, '0')}`.includes(r) ||
      (d.message || '').toLowerCase().includes(r)
    )
  }

  // Statut
  if (filtreStatut.value) {
    resultat = resultat.filter(d => d.statut === filtreStatut.value)
  }

  // Groupe
  if (filtreGroupe.value) {
    resultat = resultat.filter(d => d.groupe_sanguin === filtreGroupe.value)
  }

  // Urgence
  if (filtreUrgence.value) {
    resultat = resultat.filter(d => d.urgence === filtreUrgence.value)
  }

  return resultat
})

// ==========================================
// PAGINATION
// ==========================================

const pageActuelle = ref(1)
const elementsParPage = 10

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(demandesFiltrees.value.length / elementsParPage))
})

const demandesPaginees = computed(() => {
  const debut = (pageActuelle.value - 1) * elementsParPage
  return demandesFiltrees.value.slice(debut, debut + elementsParPage)
})

function changerPage(n) {
  if (n < 1 || n > totalPages.value) return
  pageActuelle.value = n
}

// Reset la page à 1 quand les filtres changent
watch([recherche, filtreStatut, filtreGroupe, filtreUrgence], () => {
  pageActuelle.value = 1
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

function urgenceVariant(urgence) {
  if (urgence === 'vitale') return 'danger'
  if (urgence === 'urgent') return 'warning'
  return 'default'
}

function urgenceLabel(urgence) {
  if (urgence === 'vitale') return 'Vitale'
  if (urgence === 'urgent') return 'Urgent'
  if (urgence === 'programme') return 'Programmé'
  return urgence
}

function statutVariant(statut) {
  if (statut === 'en_cours') return 'info'
  if (statut === 'terminee') return 'success'
  if (statut === 'expiree') return 'warning'
  if (statut === 'annulee') return 'danger'
  return 'default'
}

function statutLabel(statut) {
  if (statut === 'en_cours') return 'En cours'
  if (statut === 'terminee') return 'Terminée'
  if (statut === 'expiree') return 'Expirée'
  if (statut === 'annulee') return 'Annulée'
  return statut
}

// ==========================================
// ANNULATION (modal)
// ==========================================

const demandeAnnulation = ref(null)
const annulationEnCours = ref(false)

function ouvrirConfirmationAnnulation(demande) {
  demandeAnnulation.value = demande
}

function fermerConfirmation() {
  if (annulationEnCours.value) return
  demandeAnnulation.value = null
}

async function confirmerAnnulation() {
  if (!demandeAnnulation.value) return

  annulationEnCours.value = true
  try {
    await demandesStore.annulerDemande(demandeAnnulation.value.id)
    demandeAnnulation.value = null
  } catch (e) {
    // Silencieux : le store a déjà l'erreur
  } finally {
    annulationEnCours.value = false
  }
}
</script>

<style scoped>
.requests-view {
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
  flex-wrap: wrap;
  gap: 16px;
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
  line-height: 1.5;
}

.plus-icon {
  margin-right: 6px;
  font-size: 18px;
  line-height: 1;
}

/* ========================================
   STATS
======================================== */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

/* ========================================
   CARTE DES DEMANDES
======================================== */

.requests-card {
  overflow: hidden;
}

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

.requests-filters :deep(.search-input) {
  min-width: 200px;
}

.requests-filters :deep(.select-group select),
.requests-filters :deep(select) {
  min-width: 150px;
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

.spinner-small {
  display: inline-block;
  width: 14px;
  height: 14px;

  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========================================
   ÉTAT VIDE
======================================== */

.empty-state {
  padding: 60px 24px;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.empty-state h3 {
  margin: 0 0 8px;

  color: var(--bloodsen-dark);
  font-size: 18px;
  font-weight: 700;
}

.empty-state p {
  margin: 0 0 20px;

  color: #6b7280;
  font-size: 14px;
}

/* ========================================
   TABLEAU
======================================== */

.requests-table-wrapper {
  overflow-x: auto;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.requests-table th {
  padding: 12px 20px;

  color: #8a94a3;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  text-align: left;
  white-space: nowrap;
}

.requests-table td {
  padding: 16px 20px;

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

.confirmed-info {
  color: #1e9e5a;
  font-weight: 600;
}

.actions-cell {
  display: flex;
  gap: 6px;
  align-items: center;
}

.action-button {
  padding: 6px 12px;

  border: 1px solid #d9dde2;
  border-radius: 6px;

  background-color: #ffffff;
  color: var(--bloodsen-dark);

  font-family: inherit;
  font-size: 13px;
  font-weight: 600;

  cursor: pointer;

  transition: 0.15s ease;
}

.action-button.danger {
  border-color: #f0d3d3;
  color: var(--bloodsen-red);
}

.action-button.danger:hover {
  background-color: #fdecec;
}

.no-action {
  color: #c5cdd8;
}

/* ========================================
   FOOTER + PAGINATION
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

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ========================================
   MODAL
======================================== */

.modal-overlay {
  position: fixed;
  inset: 0;

  z-index: 9999;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 24px;

  background-color: rgba(11, 25, 43, 0.6);

  animation: fadeIn 0.2s ease;
}

.modal-box {
  max-width: 420px;
  width: 100%;

  padding: 32px 28px;

  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);

  text-align: center;
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

.modal-icon.danger {
  background-color: #fef3c7;
}

.modal-box h3 {
  margin: 0 0 12px;

  color: var(--bloodsen-dark);
  font-size: 20px;
  font-weight: 700;
}

.modal-box p {
  margin: 0 0 24px;

  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

.modal-box p strong {
  color: var(--bloodsen-dark);
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
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

  .requests-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .modal-actions {
    flex-direction: column-reverse;
  }

  .modal-actions :deep(button) {
    width: 100%;
  }
}
</style>