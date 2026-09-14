<template>
  <div class="donor-dashboard-view">

    <div class="page-heading-row">
      <div class="page-heading">
        <h2>Bonjour Moussa</h2>
        <p>Merci de contribuer à sauver des vies.</p>
      </div>

      <AppButton variant="primary" to="/donneur/sollicitations">
        Voir mes sollicitations
      </AppButton>
    </div>

    <!-- Indicateurs -->
    <div class="stats-grid">

      <StatCard label="SOLLICITATIONS EN ATTENTE" value="03">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M12 7V12L15 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="SOLLICITATIONS ACCEPTÉES" :value="12">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="PARTICIPATIONS" :value="28">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </template>
      </StatCard>

      <StatCard label="DONS CONFIRMÉS" :value="24">
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
          <span class="requests-updated">Actualisé il y a 5 min</span>
        </div>

        <div class="requests-table-wrapper">
          <table class="requests-table">

            <thead>
              <tr>
                <th>Demande</th>
                <th>Groupe</th>
                <th>Distance</th>
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

                <td class="distance-cell">
                  {{ request.distance }}
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
                    :to="`/donneur/sollicitations/${request.id}`"
                  >
                    Répondre
                  </AppButton>

                  <AppButton
                    v-else
                    variant="secondary"
                    size="sm"
                    :to="`/donneur/sollicitations/${request.id}`"
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

        <EngagementCard
            level="Donneur Élite"
            :current="engagement.donations"
            :target="engagement.target"
            :low-tier-label="`NIVEAU ${engagement.currentLevel}`"
            :high-tier-label="`NIVEAU ${engagement.nextLevel} (HÉROS)`"
            :participations="engagement.participations"
            :points="engagement.points"
        />

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
import { computed, ref } from 'vue'

import AppCard from '@/components/AppCard.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'
import StatCard from '@/components/StatCard.vue'
import EngagementCard from '@/components/EngagementCard.vue'

const requests = ref([
  {
    id: 'req-1',
    facility: 'Hôpital Principal',
    location: 'Dakar, Plateau',
    group: 'O+',
    distance: '2.4 km',
    urgency: 'critical',
    status: 'pending',
  },
  {
    id: 'req-2',
    facility: 'Hôpital Dalal Jamm',
    location: 'Guédiawaye',
    group: 'A+',
    distance: '12.1 km',
    urgency: 'medium',
    status: 'accepted',
  },
  {
    id: 'req-3',
    facility: 'Centre de Santé Phillippe',
    location: 'Yoff',
    group: 'O+',
    distance: '5.8 km',
    urgency: 'high',
    status: 'pending',
  },
])

function urgencyVariant(urgency) {
  if (urgency === 'critical') return 'danger'
  return 'warning' // medium & high
}

function urgencyLabel(urgency) {
  if (urgency === 'critical') return 'Critique'
  if (urgency === 'medium') return 'Moyenne'
  return 'Élevée'
}

function statusLabel(status) {
  return status === 'pending' ? 'En attente' : 'Acceptée'
}

const engagement = ref({
  level: 'Donneur Élite',
  donations: 24,
  target: 30,
  currentLevel: 3,
  nextLevel: 4,
  participations: 28,
  points: 1420,
})

const engagementPercent = computed(() =>
  Math.round((engagement.value.donations / engagement.value.target) * 100)
)

const tips = ref([
  { id: 1, emoji: '💧', text: 'Buvez beaucoup d\'eau (au moins 500ml) avant votre don pour rester bien hydraté.' },
  { id: 2, emoji: '🍽️', text: 'Évitez les repas gras 2h avant le don. Privilégiez des aliments sains.' },
  { id: 3, emoji: '🌙', text: 'Reposez-vous bien après votre don et évitez les efforts physiques intenses.' },
])

// TODO : remplacer requests/engagement/tips par un appel API réel
</script>

<style scoped>
.donor-dashboard-view {
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
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

/* ========================================
   GRILLE PRINCIPALE
======================================== */

.dashboard-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 20px;
  align-items: start;
}

/* ========================================
   SOLLICITATIONS RÉCENTES
======================================== */

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

.requests-updated {
  color: #8a94a3;
  font-size: 12.5px;
}

.requests-table-wrapper {
  overflow-x: auto;
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

  white-space: nowrap;
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

.distance-cell {
  color: #4a5568;
  font-size: 13px;
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
}

/* Engagement */

.engagement-header {
  display: flex;
  align-items: center;
  gap: 12px;

  margin-bottom: 20px;
}

.engagement-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 36px;
  height: 36px;

  border-radius: 50%;

  background-color: #eafaf0;
  color: #1e9e5a;
}

.engagement-icon svg {
  width: 18px;
  height: 18px;
}

.engagement-header h3 {
  margin: 0 0 2px;

  color: var(--bloodsen-dark);

  font-size: 15px;
  font-weight: 700;
}

.engagement-header p {
  margin: 0;

  color: #6b7280;

  font-size: 12.5px;
}

.engagement-progress-row {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 8px;

  color: var(--bloodsen-dark);
  font-size: 13px;
}

.engagement-progress-row strong {
  color: var(--bloodsen-dark);
}

.progress-track {
  height: 8px;
  margin-bottom: 8px;

  border-radius: 4px;

  background-color: #f1f3f5;
  overflow: hidden;
}

.progress-fill {
  height: 100%;

  border-radius: 4px;

  background-color: #1e9e5a;
}

.progress-levels {
  display: flex;
  align-items: center;
  justify-content: space-between;

  color: #8a94a3;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.engagement-divider {
  height: 1px;
  margin: 20px 0;

  background-color: #eef0f2;
}

.engagement-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.engagement-metric {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.engagement-metric span {
  color: #8a94a3;

  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.engagement-metric strong {
  color: var(--bloodsen-dark);
  font-size: 17px;
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

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .dashboard-grid {
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

  .page-heading-row :deep(button) {
    width: 100%;
  }
}
</style>