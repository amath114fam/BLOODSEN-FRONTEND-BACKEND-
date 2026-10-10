<template>
  <div class="predictions-view">

    <div class="page-heading">
      <h2>Prédictions & Analyse</h2>
      <p>
        Analyse intelligente de vos demandes et des donneurs disponibles
        pour cibler vos actions de mobilisation.
      </p>
    </div>

    <!-- Chargement -->
    <div v-if="loading" class="loading-state">
      <div class="spinner-large"></div>
      <p>Analyse en cours...</p>
    </div>

    <!-- Erreur -->
    <div v-else-if="erreur" class="error-state">
      <AlertCircle :size="48" :stroke-width="1.5" />
      <h3>Impossible de charger l'analyse</h3>
      <p>{{ erreur }}</p>
    </div>

    <!-- Contenu -->
    <div v-else-if="data" class="content-stack">

      <!-- Stats globales -->
      <div class="stats-grid">
        <StatCard label="TOTAL DEMANDES" :value="data.stats_globales.total_demandes" icon-tone="neutral">
          <template #icon>
            <ClipboardList :size="20" :stroke-width="2" />
          </template>
        </StatCard>

        <StatCard label="DONS CONFIRMÉS" :value="data.stats_globales.total_dons" icon-tone="success">
          <template #icon>
            <CheckCircle :size="20" :stroke-width="2" />
          </template>
        </StatCard>

        <StatCard
          label="TAUX SATISFACTION"
          :value="`${data.stats_globales.taux_satisfaction}%`"
          icon-tone="danger"
        >
          <template #icon>
            <TrendingUp :size="20" :stroke-width="2" />
          </template>
        </StatCard>
      </div>

      <!-- Recommandations IA -->
      <AppCard padding="32px" class="ia-card">
        <div class="ia-header">
          <div class="ia-icon">
            <Sparkles :size="22" :stroke-width="2" />
          </div>
          <div>
            <h3>Recommandations de l'assistant IA</h3>
            <p>Générées par analyse intelligente de vos données</p>
          </div>
        </div>

        <div class="ia-divider"></div>

        <div v-if="data.recommandations_ia" class="ia-content">
          <p
            v-for="(paragraphe, index) in paragraphesIA"
            :key="index"
            class="ia-paragraphe"
          >
            {{ paragraphe }}
          </p>
        </div>
        <p v-else class="ia-empty">
          Les recommandations ne sont pas disponibles pour le moment.
        </p>
      </AppCard>

      <!-- Zones critiques -->
      <AppCard v-if="data.zones_critiques.length" padding="28px" class="alert-card">
        <div class="card-header">
          <span class="card-icon danger">
            <AlertTriangle :size="20" :stroke-width="2" />
          </span>
          <h3>Zones critiques</h3>
        </div>

        <div class="card-divider"></div>

        <div class="alerts-list">
          <div
            v-for="(zone, index) in data.zones_critiques"
            :key="index"
            class="alert-item"
          >
            <div class="alert-region">{{ zone.region }}</div>
            <div class="alert-raison">{{ zone.raison }}</div>
            <div class="alert-demandes">{{ zone.demandes }} demande(s)</div>
          </div>
        </div>
      </AppCard>

      <!-- Analyse par région -->
      <AppCard padding="28px" class="analysis-card">
        <div class="card-header">
          <span class="card-icon"><MapPin :size="20" :stroke-width="2" /></span>
          <h3>Répartition par région</h3>
        </div>

        <div class="card-divider"></div>

        <div v-if="data.par_region.length" class="analysis-grid">
          <div
            v-for="(region, index) in data.par_region"
            :key="index"
            class="analysis-item"
          >
            <div class="analysis-row">
              <strong class="analysis-label">{{ region.region }}</strong>
              <span class="analysis-ratio" :class="ratioClass(region.ratio)">
                {{ region.ratio !== null ? `Ratio ${region.ratio}` : 'Aucun donneur' }}
              </span>
            </div>
            <div class="analysis-details">
              <span>{{ region.demandes }} demande(s)</span>
              <span>•</span>
              <span>{{ region.donneurs_disponibles }} donneur(s)</span>
            </div>
            <div class="analysis-bar">
              <div
                class="analysis-bar-fill"
                :style="{ width: barWidth(region) + '%' }"
                :class="ratioClass(region.ratio)"
              ></div>
            </div>
          </div>
        </div>
        <p v-else class="analysis-empty">Aucune donnée régionale.</p>
      </AppCard>

      <!-- Analyse par groupe sanguin -->
      <AppCard padding="28px" class="analysis-card">
        <div class="card-header">
          <span class="card-icon"><Droplet :size="20" :stroke-width="2" /></span>
          <h3>Répartition par groupe sanguin</h3>
        </div>

        <div class="card-divider"></div>

        <div v-if="data.par_groupe.length" class="analysis-grid">
          <div
            v-for="(groupe, index) in data.par_groupe"
            :key="index"
            class="analysis-item"
          >
            <div class="analysis-row">
              <div class="group-badge">
                <strong>{{ groupe.groupe }}</strong>
              </div>
              <span
                v-if="groupe.alerte"
                class="alert-pill"
              >
                <AlertTriangle :size="12" :stroke-width="2.5" />
                Déficit
              </span>
              <span v-else class="ok-pill">OK</span>
            </div>
            <div class="analysis-details">
              <span>{{ groupe.demandes }} demande(s)</span>
              <span>•</span>
              <span>{{ groupe.donneurs }} donneur(s)</span>
            </div>
          </div>
        </div>
        <p v-else class="analysis-empty">Aucune donnée par groupe.</p>
      </AppCard>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Sparkles,
  AlertTriangle,
  AlertCircle,
  MapPin,
  Droplet,
  ClipboardList,
  CheckCircle,
  TrendingUp,
} from 'lucide-vue-next'
import api from '@/services/api'

import AppCard from '@/components/AppCard.vue'
import StatCard from '@/components/StatCard.vue'

// ==========================================
// ÉTAT
// ==========================================

const loading = ref(true)
const erreur = ref('')
const data = ref(null)

// ==========================================
// CHARGEMENT
// ==========================================

onMounted(async () => {
  try {
    const { data: reponse } = await api.get('/dashboard/structure/predictions/')
    data.value = reponse
  } catch (e) {
    erreur.value = e.response?.data?.detail || 'Une erreur est survenue.'
  } finally {
    loading.value = false
  }
})

// ==========================================
// PARAGRAPHES IA
// ==========================================

const paragraphesIA = computed(() => {
  const texte = data.value?.recommandations_ia
  if (!texte) return []

  return texte
    .split('\n')
    .map(p => p.trim())
    .filter(p => p.length > 0)
})

// ==========================================
// HELPERS
// ==========================================

function ratioClass(ratio) {
  if (ratio === null || ratio === undefined) return 'danger'
  if (ratio >= 3) return 'danger'
  if (ratio >= 1) return 'warning'
  return 'success'
}

function barWidth(region) {
  if (!region.ratio) return 100
  return Math.min(region.ratio * 30, 100)
}
</script>

<style scoped>
.predictions-view {
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

/* ========================================
   STACK DE CONTENU (espacement vertical)
======================================== */

.content-stack {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========================================
   ÉTATS
======================================== */

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80px 24px;
  text-align: center;
  color: #6b7280;
}

.spinner-large {
  display: inline-block;
  width: 40px;
  height: 40px;
  margin-bottom: 16px;
  border: 3px solid #e6eaf0;
  border-top-color: var(--bloodsen-red);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  color: var(--bloodsen-red);
}

.error-state h3 {
  margin: 16px 0 8px;
  color: var(--bloodsen-dark);
  font-size: 18px;
}

/* ========================================
   STATS
======================================== */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

/* ========================================
   CARTE IA (même fond que le dashboard)
======================================== */

.ia-card {
  background-color: #ffffff;
}

.ia-header {
  display: flex;
  align-items: center;
  gap: 14px;
}

.ia-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 48px;
  height: 48px;

  border-radius: 12px;
  background-color: var(--bloodsen-red);
  color: #ffffff;
}

.ia-header h3 {
  margin: 0 0 2px;
  color: var(--bloodsen-dark);
  font-size: 17px;
  font-weight: 700;
}

.ia-header p {
  margin: 0;
  color: #8a94a3;
  font-size: 13px;
}

.ia-divider {
  height: 1px;
  margin: 20px 0;
  background-color: #eef0f2;
}

.ia-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ia-paragraphe {
  margin: 0;
  color: #4a5568;
  font-size: 14.5px;
  line-height: 1.7;
}

.ia-empty {
  margin: 0;
  color: #8a94a3;
  font-size: 14px;
  font-style: italic;
}

/* ========================================
   CARTE GÉNÉRIQUE
======================================== */

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--bloodsen-red);
}

.card-icon.danger {
  color: #dc2626;
}

.card-header h3 {
  margin: 0;
  color: var(--bloodsen-dark);
  font-size: 17px;
  font-weight: 700;
}

.card-divider {
  height: 1px;
  margin: 18px 0 22px;
  background-color: #eef0f2;
}

/* ========================================
   ZONES CRITIQUES
======================================== */

.alert-card {
  border-left: 4px solid #dc2626;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  padding: 16px;
  background-color: #fef2f2;
  border-radius: 10px;
}

.alert-region {
  margin-bottom: 4px;
  color: var(--bloodsen-dark);
  font-size: 15px;
  font-weight: 700;
}

.alert-raison {
  margin-bottom: 4px;
  color: #6b7280;
  font-size: 13.5px;
}

.alert-demandes {
  color: #dc2626;
  font-size: 12px;
  font-weight: 600;
}

/* ========================================
   ANALYSE
======================================== */

.analysis-grid {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.analysis-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.analysis-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.analysis-label {
  color: var(--bloodsen-dark);
  font-size: 15px;
  font-weight: 700;
}

.analysis-ratio {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
}

.analysis-ratio.success { background-color: #d1fae5; color: #059669; }
.analysis-ratio.warning { background-color: #fef3c7; color: #92400e; }
.analysis-ratio.danger  { background-color: #fee2e2; color: #dc2626; }

.analysis-details {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #8a94a3;
  font-size: 13px;
}

.analysis-bar {
  height: 6px;
  border-radius: 3px;
  background-color: #f1f3f5;
  overflow: hidden;
}

.analysis-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

.analysis-bar-fill.success { background-color: #059669; }
.analysis-bar-fill.warning { background-color: #f59e0b; }
.analysis-bar-fill.danger  { background-color: #dc2626; }

.analysis-empty {
  margin: 0;
  color: #8a94a3;
  font-size: 13px;
  font-style: italic;
}

/* ========================================
   BADGE GROUPE
======================================== */

.group-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  padding: 6px 14px;

  background-color: #fdecec;
  border-radius: 20px;

  color: var(--bloodsen-red);
  font-size: 14px;
  font-weight: 800;
}

.alert-pill,
.ok-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;

  padding: 4px 10px;
  border-radius: 20px;

  font-size: 11.5px;
  font-weight: 700;
}

.alert-pill {
  background-color: #fee2e2;
  color: #dc2626;
}

.ok-pill {
  background-color: #d1fae5;
  color: #059669;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 900px) {
  .stats-grid { grid-template-columns: 1fr; }
  .page-heading h2 { font-size: 24px; }
}
</style>