<template>
  <div class="donors-view">

    <div class="page-heading-row">
      <div class="page-heading">
        <h2>Donneurs</h2>
        <p>Suivez les donneurs ayant répondu à vos demandes.</p>
      </div>

    </div>

    <!-- Indicateurs -->
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

    <!-- Filtres + Table -->
    <AppCard padding="20px 24px" class="donors-card">

      <div class="filters-row">

        <AppInput
          id="search-donor"
          v-model="filters.search"
          placeholder="Rechercher par identifiant donneur, zone géographique, référence demande..."
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
          v-model="filters.group"
          placeholder="Tous les groupes"
          :options="groupOptions"
        />

        <AppSelect
          id="status-filter"
          v-model="filters.status"
          placeholder="Tous statuts"
          :options="statusOptions"
        />

        <AppSelect
          id="participation-filter"
          v-model="filters.participation"
          placeholder="Toutes participations"
          :options="participationOptions"
        />

        <AppSelect
          id="request-filter"
          v-model="filters.request"
          placeholder="Toutes demandes"
          :options="requestOptions"
        />

      </div>

      <div v-if="donors.length" class="donors-table-wrapper">
        <table class="donors-table">

          <thead>
            <tr>
              <th>Donneur</th>
              <th>Téléphone</th>
              <th>Groupe sanguin</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="donor in donors" :key="donor.id">

              <td>
                <div class="donor-cell">
                  <span class="donor-avatar">{{ donor.initials }}</span>
                  <div>
                    <strong>{{ donor.name }}</strong>
                    <span class="donor-reference">
                      {{ donor.reference }} • {{ donor.location }}
                    </span>
                  </div>
                </div>
              </td>

              <td>{{ donor.phone }}</td>

              <td>
                <AppBadge variant="danger">{{ donor.bloodGroup }}</AppBadge>
              </td>

            </tr>
          </tbody>

        </table>
      </div>

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
          <AppButton variant="outline" @click="goToRequests">
            <span class="drop-icon">🩸</span>
            Consulter vos demandes en cours
          </AppButton>

          <AppButton variant="primary" @click="goToCreateRequest">
            <span class="plus-icon">+</span>
            Créer une demande
          </AppButton>
        </div>

      </div>

      <div v-if="donors.length" class="donors-footer">
        <span>
          Affichage de <strong>{{ pagination.from }} à {{ pagination.to }}</strong>
          sur {{ pagination.total }} donneurs mobilisés
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
  solicited: 148,
  positiveResponses: 38,
  completedDonations: 24,
})

const filters = reactive({
  search: '',
  group: '',
  status: '',
  participation: '',
  request: '',
})

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
  { value: 'active', label: 'Actif' },
  { value: 'inactive', label: 'Inactif' },
]

const participationOptions = [
  { value: 'confirmed', label: 'Confirmée' },
  { value: 'pending', label: 'En attente' },
]

const requestOptions = [
  { value: 'DS-2025-142', label: '#DS-2025-142' },
  { value: 'DS-2025-141', label: '#DS-2025-141' },
]

const donors = ref([
  { id: 1, initials: 'AS', name: 'Abdoulaye Sall', reference: 'DON-SN-8492', location: 'Dakar-Fann', phone: '+221 77 654 21 89', bloodGroup: 'O-' },
  { id: 2, initials: 'MD', name: 'Mamadou Diop', reference: 'DON-SN-7319', location: 'Grand Yoff', phone: '+221 78 412 90 33', bloodGroup: 'B+' },
  { id: 3, initials: 'FF', name: 'Fatou Fall', reference: 'DON-SN-9022', location: 'Mermoz', phone: '+221 76 890 14 55', bloodGroup: 'A+' },
  { id: 4, initials: 'IB', name: 'Ibrahima Ba', reference: 'DON-SN-6105', location: 'Médina', phone: '+221 77 321 09 87', bloodGroup: 'O+' },
  { id: 5, initials: 'PK', name: 'Papa Kane', reference: 'DON-SN-5120', location: 'Ouakam', phone: '+221 70 543 88 12', bloodGroup: 'AB+' },
  { id: 6, initials: 'SN', name: 'Seynabou Ndiaye', reference: 'DON-SN-3904', location: 'Almadies', phone: '+221 77 234 56 78', bloodGroup: 'A-' },
])

const pagination = reactive({
  page: 1,
  from: 1,
  to: 6,
  total: 38,
  totalPages: 3,
})

function goToPage(page) {
  if (page < 1 || page > pagination.totalPages) return
  pagination.page = page
  // Plus tard : appel API paginé GET /donneurs?page=...
}

function goToCreateRequest() {
  router.push('/structure/demandes/creer')
}

function goToRequests() {
  router.push('/structure/demandes')
}
</script>

<style scoped>
.donors-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-heading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
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
  min-width: 150px;
}

/* ========================================
   TABLE
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

.plus-icon {
  margin-right: 6px;
  font-size: 16px;
}

.drop-icon {
  margin-right: 6px;
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