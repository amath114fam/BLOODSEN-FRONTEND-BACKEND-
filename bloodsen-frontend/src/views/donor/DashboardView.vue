<template>
  <div class="donor-dashboard-view">

    <div class="page-heading-row">
      <div class="page-heading">
        <h2>Bonjour {{ prenom }}</h2>
        <p>Merci de contribuer à sauver des vies.</p>
      </div>
    </div>

    <!-- Indicateurs -->
    <div class="stats-grid">

      <StatCard label="SOLLICITATIONS EN ATTENTE" :value="compteurs.sollicitations_en_attente">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M12 7V12L15 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="SOLLICITATIONS ACCEPTÉES" :value="compteurs.sollicitations_acceptees">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="PARTICIPATIONS" :value="compteurs.dons_effectues">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="DONS CONFIRMÉS" :value="compteurs.dons_effectues">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 21C12 21 4 15.5 4 9.5C4 6.46 6.46 4 9.5 4C11.24 4 12.78 4.81 12.78 4.81C12.78 4.81 14.32 4 16.06 4C19.1 4 21.56 6.46 21.56 9.5C21.56 15.5 12 21 12 21Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

    </div>

    <!-- Corps de page -->
    <div class="dashboard-grid">

      <!-- Sollicitations récentes -->
      <AppCard padding="0" class="requests-card">

        <div class="requests-header">
          <div class="requests-title">
            <span class="info-dot">i</span>
            <h3>Sollicitations récentes</h3>
          </div>
        </div>

        <div class="requests-table-wrapper">
          <table class="requests-table">

            <thead>
              <tr>
                <th>Demande</th>
                <th>Groupe</th>
                <th>Urgence</th>
                <th>Statut</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="request in requests" :key="request.id">

                <td>
                  <strong>{{ request.facility }}</strong>
                  <span class="request-location">{{ request.location }}</span>
                </td>

                <td>
                  <span class="group-text">{{ request.group }}</span>
                </td>

                <td>
                  <AppBadge :variant="urgencyVariant(request.urgency)">
                    {{ urgencyLabel(request.urgency) }}
                  </AppBadge>
                </td>

                <td>
                  <span class="status-text" :class="request.status">
                    {{ statusLabel(request.status) }}
                  </span>
                </td>

                <td>
                  <AppButton
                    v-if="request.status === 'pending'"
                    variant="outline"
                    size="sm"
                    to="/donneur/sollicitations"
                  >
                    Répondre
                  </AppButton>

                  <AppButton
                    v-else
                    variant="secondary"
                    size="sm"
                    to="/donneur/sollicitations"
                  >
                    Détails
                  </AppButton>
                </td>

              </tr>
            </tbody>

          </table>
        </div>

      </AppCard>

      <!-- Colonne droite -->
      <div class="side-column">

        <GamificationCard :profil="profil" />

        <!-- Conseils du donneur -->
        <div class="tips-card">

          <div class="tips-header">
            <span class="tips-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="12" width="4" height="8" rx="1" stroke="currentColor" stroke-width="2" />
                <rect x="10" y="8" width="4" height="12" rx="1" stroke="currentColor" stroke-width="2" />
                <rect x="17" y="4" width="4" height="16" rx="1" stroke="currentColor" stroke-width="2" />
              </svg>
            </span>
            <h3>Conseils du donneur</h3>
          </div>

          <ul class="tips-list">
            <li v-for="tip in tips" :key="tip.id">
              <span class="tip-emoji">{{ tip.emoji }}</span>
              <span>{{ tip.text }}</span>
            </li>
          </ul>

          <router-link to="/donneur/conseils" class="tips-link">
            En savoir plus →
          </router-link>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

import AppCard from '@/components/AppCard.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'
import StatCard from '@/components/StatCard.vue'
import GamificationCard from '@/components/GamificationCard.vue'

// ==========================================
// ÉTAT GLOBAL
// ==========================================

const auth = useAuthStore()

const loading = ref(true)
const erreur = ref('')
const dashboard = ref(null)

// ==========================================
// CHARGEMENT DES DONNÉES
// ==========================================

onMounted(async () => {
  try {
    const { data } = await api.get('/dashboard/donneur/')
    dashboard.value = data
  } catch (e) {
    erreur.value = 'Impossible de charger votre tableau de bord.'
  } finally {
    loading.value = false
  }
})

// ==========================================
// DONNÉES DÉRIVÉES
// ==========================================

const profil = computed(() => auth.user?.profil || {})

const compteurs = computed(() => dashboard.value?.compteurs || {
  sollicitations_en_attente: 0,
  sollicitations_acceptees: 0,
  dons_effectues: 0,
})

const requests = computed(() => {
  const sollicitations = dashboard.value?.dernieres_sollicitations || []
  return sollicitations.map(s => ({
    id: s.id,
    facility: s.structure_nom,
    location: `${s.structure_ville}, ${s.structure_region}`,
    group: s.groupe_sanguin,
    urgency: s.urgence === 'vitale' ? 'critical' : (s.urgence === 'urgent' ? 'high' : 'medium'),
    status: s.statut === 'en_attente' ? 'pending' : (s.statut === 'acceptee' ? 'accepted' : s.statut),
  }))
})

// ==========================================
// AFFICHAGE
// ==========================================

const prenom = computed(() => profil.value.prenom || 'Donneur')

// ==========================================
// HELPERS
// ==========================================

function urgencyVariant(urgency) {
  if (urgency === 'critical') return 'danger'
  return 'warning'
}

function urgencyLabel(urgency) {
  if (urgency === 'critical') return 'Critique'
  if (urgency === 'high') return 'Élevée'
  return 'Moyenne'
}

function statusLabel(status) {
  if (status === 'pending') return 'En attente'
  if (status === 'accepted') return 'Acceptée'
  if (status === 'refusee') return 'Refusée'
  if (status === 'expiree') return 'Expirée'
  return status
}

// ==========================================
// CONSEILS (statiques)
// ==========================================

const tips = ref([
  { id: 1, emoji: '💧', text: 'Buvez beaucoup d\'eau (au moins 500ml) avant votre don pour rester bien hydraté.' },
  { id: 2, emoji: '🍽️', text: 'Évitez les repas gras 2h avant le don. Privilégiez des aliments sains.' },
  { id: 3, emoji: '🌙', text: 'Reposez-vous bien après votre don et évitez les efforts physiques intenses.' },
])
</script>

<style scoped>
/* ========================================
   PAGE
======================================== */

.donor-dashboard-view {
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
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
}

/* ========================================
   GRILLE PRINCIPALE
======================================== */

.dashboard-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

/* ========================================
   SOLLICITATIONS RÉCENTES
======================================== */

.requests-card {
  min-width: 0;
}

.requests-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  padding: 18px 24px;
  border-bottom: 1px solid #e7e9ed;
}

.requests-title {
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

.requests-title h3 {
  margin: 0;
  color: var(--bloodsen-dark);
  font-size: 16px;
  font-weight: 700;
}

.requests-table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.requests-table {
  width: 100%;
  min-width: 600px;
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
  white-space: normal;
}

.request-location {
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

.status-text {
  font-size: 13px;
  font-weight: 700;
}

.status-text.pending {
  color: #2760d8;
}

.status-text.accepted {
  color: #1e9e5a;
}

/* ========================================
   COLONNE DROITE
======================================== */

.side-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

/* Conseils */

.tips-card {
  padding: 24px;
  border-radius: 12px;
  background-color: #10131a;
  color: #ffffff;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.tips-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--bloodsen-red);
}

.tips-icon svg {
  width: 18px;
  height: 18px;
}

.tips-header h3 {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 0 0 18px;
  padding: 0;
  list-style: none;
}

.tips-list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  color: rgba(255, 255, 255, 0.82);
  font-size: 13px;
  line-height: 1.5;
}

.tip-emoji {
  flex-shrink: 0;
  font-size: 15px;
}

.tips-link {
  color: var(--bloodsen-red);
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
}

.tips-link:hover {
  text-decoration: underline;
}

/* ========================================
   RESPONSIVE
======================================== */

/* Grands écrans (par défaut) : 4 stat-cards + 2 colonnes */

/* Écrans moyens : passage en 1 colonne pour le dashboard-grid */
@media (max-width: 1400px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .side-column {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
  }
}

/* Tablette : 2 stat-cards par ligne */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Petit écran : side-column en 1 colonne aussi */
@media (max-width: 900px) {
  .side-column {
    grid-template-columns: 1fr;
  }
}

/* Mobile : 1 stat-card par ligne */
@media (max-width: 700px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .page-heading h2 {
    font-size: 24px;
  }

  .requests-header {
    padding: 16px 20px;
  }

  .requests-table th,
  .requests-table td {
    padding: 12px 16px;
  }
}
</style>