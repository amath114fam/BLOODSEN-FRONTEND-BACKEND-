<template>
  <div class="participations-view">

    <!-- ==========================================
         EN-TÊTE
    =========================================== -->
    <div class="page-heading">
      <h2>Participations</h2>
      <p>Suivez les participations liées à vos demandes.</p>
    </div>

    <!-- ==========================================
         STATS
    =========================================== -->
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

    <!-- ==========================================
         FILTRES + TABLEAU
    =========================================== -->
    <AppCard padding="20px 24px" class="participations-card">

      <div class="filters-row">

        <AppInput
          id="search-participation"
          v-model="recherche"
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
          id="group-filter"
          v-model="filtreGroupe"
          placeholder="Tous les groupes"
          :options="groupeOptions"
        />

        <AppSelect
          id="status-filter"
          v-model="filtreStatut"
          placeholder="Tous les statuts"
          :options="statutOptions"
        />

      </div>

      <!-- CHARGEMENT -->
      <div v-if="loading" class="loading-state">
        <div class="spinner-large"></div>
        <p>Chargement des participations...</p>
      </div>

      <!-- TABLEAU -->
      <div v-else-if="participationsPaginees.length" class="participations-table-wrapper">
        <table class="participations-table">

          <thead>
            <tr>
              <th>Donneur</th>
              <th>Demande</th>
              <th>Groupe</th>
              <th>Date sollicitation</th>
              <th>Statut</th>
              <th>Date conf.</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in participationsPaginees" :key="item.id">

              <td>
                <div class="donor-cell">
                  <span class="donor-avatar">{{ item.donneur_initiales }}</span>
                  <div>
                    <strong>{{ item.donneur_prenom }} {{ item.donneur_nom }}</strong>
                    <span class="donor-reference">{{ item.donneur_ville }}</span>
                  </div>
                </div>
              </td>

              <td>
                <strong>{{ item.demande_reference }}</strong>
                <span v-if="item.demande_message" class="request-service">
                  {{ item.demande_message.slice(0, 30) }}{{ item.demande_message.length > 30 ? '...' : '' }}
                </span>
              </td>

              <td>
                <AppBadge variant="danger">{{ item.donneur_groupe_sanguin }}</AppBadge>
              </td>

              <td class="date-cell">
                {{ formaterDate(item.date_creation) }}
              </td>

              <td>
                <AppBadge :variant="statusVariant(item.statut_affiche)">
                  {{ statusLabel(item.statut_affiche) }}
                </AppBadge>
              </td>

              <td class="date-cell">
                {{ item.date_confirmation ? formaterDate(item.date_confirmation) : '—' }}
              </td>

              <td>
                <div class="actions-cell">

                  <AppButton
                    v-if="item.statut_affiche === 'pending' && item.statut === 'acceptee'"
                    variant="primary"
                    size="sm"
                    @click="confirmParticipation(item)"
                  >
                    Confirmer
                  </AppButton>

                  <span v-else class="no-action">—</span>

                </div>
              </td>

            </tr>
          </tbody>

        </table>
      </div>

      <!-- ÉTAT VIDE -->
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

        <AppButton variant="primary" to="/structure/demandes">
          <span class="drop-icon">🩸</span>
          Consulter vos demandes
        </AppButton>

      </div>

      <!-- PAGINATION -->
      <div v-if="participationsFiltrees.length > 0" class="participations-footer">
        <span>
          Affichage de <strong>{{ participationsPaginees.length }}</strong>
          sur <strong>{{ participationsFiltrees.length }}</strong>
          participation{{ participationsFiltrees.length > 1 ? 's' : '' }}
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


        <!-- ==========================================
         MODAL DE CONFIRMATION
    =========================================== -->
    <div
      v-if="confirmation"
      class="modal-overlay"
      @click.self="fermerConfirmation"
    >
      <div class="modal-box">

        <div class="modal-icon success">
          <CheckCircle :size="32" :stroke-width="3" />
        </div>

        <h3>Confirmer cette participation ?</h3>

        <p>
          Vous confirmez que
          <strong>{{ confirmation.donneurPrenom }} {{ confirmation.donneurNom }}</strong>
          s'est bien présenté et a effectué son don.
          <br><br>
          Cette action attribuera <strong>100 points</strong> au donneur
          et pourra clôturer la demande si le nombre de poches est atteint.
        </p>

        <div class="modal-actions">
          <AppButton
            variant="outline"
            :disabled="confirmationEnCours"
            @click="fermerConfirmation"
          >
            Annuler
          </AppButton>

          <AppButton
            variant="primary"
            :disabled="confirmationEnCours"
            @click="confirmerAction"
          >
            <template v-if="confirmationEnCours">
              <span class="spinner-small"></span>
              Confirmation...
            </template>
            <template v-else>
              Confirmer
            </template>
          </AppButton>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import api from '@/services/api'
import { CheckCircle } from 'lucide-vue-next'

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
const participations = ref([])

// ==========================================
// CHARGEMENT
// ==========================================

async function chargerParticipations() {
  loading.value = true
  try {
    const { data } = await api.get('/structure/participations/')
    participations.value = data
  } catch (e) {
    participations.value = []
  } finally {
    loading.value = false
  }
}

onMounted(chargerParticipations)

// ==========================================
// STATS
// ==========================================

const stats = computed(() => {
  const p = participations.value || []
  return {
    pending: p.filter(x => x.statut_affiche === 'pending').length,
    confirmed: p.filter(x => x.statut_affiche === 'confirmed').length,
    medicalRefusal: p.filter(x => x.statut_affiche === 'medical_refusal').length,
  }
})

// ==========================================
// FILTRES
// ==========================================

const recherche = ref('')
const filtreGroupe = ref('')
const filtreStatut = ref('')

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

const statutOptions = [
  { value: '', label: 'Tous les statuts' },
  { value: 'pending', label: 'En attente' },
  { value: 'confirmed', label: 'Confirmée' },
  { value: 'medical_refusal', label: 'Refus médical' },
  { value: 'cancelled', label: 'Annulée' },
]

// ==========================================
// FILTRAGE
// ==========================================

const participationsFiltrees = computed(() => {
  let resultat = participations.value || []

   // Recherche (nom, prénom, ville, référence demande, groupe sanguin)
  const r = recherche.value.trim().toLowerCase()
  if (r) {
    resultat = resultat.filter(p =>
      (p.donneur_nom || '').toLowerCase().includes(r) ||
      (p.donneur_prenom || '').toLowerCase().includes(r) ||
      (p.donneur_ville || '').toLowerCase().includes(r) ||
      (p.demande_reference || '').toLowerCase().includes(r) ||
      (p.demande_message || '').toLowerCase().includes(r) ||
      (p.donneur_groupe_sanguin || '').toLowerCase().includes(r)
    )
  }

  // Groupe (basé sur le groupe du donneur)
  if (filtreGroupe.value) {
    resultat = resultat.filter(p => p.donneur_groupe_sanguin === filtreGroupe.value)
  }

  // Statut
  if (filtreStatut.value) {
    resultat = resultat.filter(p => p.statut_affiche === filtreStatut.value)
  }

  return resultat
})

// ==========================================
// PAGINATION
// ==========================================

const pageActuelle = ref(1)
const elementsParPage = 10

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(participationsFiltrees.value.length / elementsParPage))
})

const participationsPaginees = computed(() => {
  const debut = (pageActuelle.value - 1) * elementsParPage
  return participationsFiltrees.value.slice(debut, debut + elementsParPage)
})

function changerPage(n) {
  if (n < 1 || n > totalPages.value) return
  pageActuelle.value = n
}

watch([recherche, filtreGroupe, filtreStatut], () => {
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
    return `Auj. ${h}:${m}`
  }

  const options = { day: '2-digit', month: 'short', year: 'numeric' }
  return date.toLocaleDateString('fr-FR', options)
}

function statusVariant(status) {
  if (status === 'pending') return 'warning'
  if (status === 'confirmed') return 'success'
  if (status === 'medical_refusal') return 'danger'
  return 'default'
}

function statusLabel(status) {
  if (status === 'pending') return 'En attente'
  if (status === 'confirmed') return 'Confirmée'
  if (status === 'medical_refusal') return 'Refus médical'
  if (status === 'cancelled') return 'Annulée'
  return status
}

// ==========================================
// ACTIONS
// ==========================================

// ==========================================
// MODAL DE CONFIRMATION
// ==========================================

const confirmation = ref(null)
const confirmationEnCours = ref(false)

function confirmParticipation(item) {
  confirmation.value = {
    sollicitationId: item.id,
    donneurPrenom: item.donneur_prenom,
    donneurNom: item.donneur_nom,
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
    await api.post(`/sollicitations/${confirmation.value.sollicitationId}/confirmer/`)
    await chargerParticipations()
    confirmation.value = null
  } catch (e) {
    // Silencieux
  } finally {
    confirmationEnCours.value = false
  }
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

/* STATS */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* FILTRES */
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

.filters-row :deep(.select-group) {
  min-width: 170px;
}

/* CHARGEMENT */
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

/* TABLE */
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

.request-service {
  display: block;
  margin-top: 2px;
  color: #8a94a3;
  font-size: 12.5px;
}

.date-cell {
  color: #4a5568;
  font-size: 13px;
  white-space: nowrap;
}

.actions-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.no-action {
  color: #c5cdd8;
}

/* ÉTAT VIDE */
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

/* FOOTER */
.participations-footer {
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
  max-width: 480px;
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

.modal-box p strong {
  color: var(--bloodsen-dark);
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

/* RESPONSIVE */
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