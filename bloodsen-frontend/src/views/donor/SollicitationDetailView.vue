<template>
  <div class="sollicitation-detail-view">

    <!-- ==========================================
         CHARGEMENT
    =========================================== -->
    <div v-if="loading" class="loading-state">
      <div class="spinner-large"></div>
      <p>Chargement de la sollicitation...</p>
    </div>

    <!-- ==========================================
         ERREUR
    =========================================== -->
    <div v-else-if="erreur" class="error-state">
      <AlertCircle :size="48" :stroke-width="1.5" />
      <h3>Impossible de charger la sollicitation</h3>
      <p>{{ erreur }}</p>
      <AppButton variant="primary" to="/donneur/sollicitations">
        Retour aux sollicitations
      </AppButton>
    </div>

    <!-- ==========================================
         CONTENU
    =========================================== -->
    <div v-else-if="sollicitation">

      <!-- Fil d'ariane -->
      <div class="breadcrumb">
        <router-link to="/donneur/sollicitations">
          <ArrowLeft :size="16" />
          Mes sollicitations
        </router-link>
        <span class="separator">/</span>
        <span class="current">Détail #{{ sollicitation.id }}</span>
      </div>

      <!-- Carte principale -->
      <div class="detail-grid">

        <!-- Colonne gauche : infos principales -->
        <div class="main-column">

          <!-- En-tête avec groupe sanguin -->
          <AppCard padding="0" class="hero-card">
            <div class="hero-content">
              <div class="hero-group">
                <strong>{{ sollicitation.groupe_sanguin }}</strong>
                <span>GROUPE RECHERCHÉ</span>
              </div>

              <div class="hero-info">
                <h1>{{ sollicitation.structure_nom }}</h1>
                <p class="hero-location">
                  <MapPin :size="14" />
                  {{ sollicitation.structure_ville }}, {{ sollicitation.structure_region }}
                </p>

                <div class="hero-badges">
                  <AppBadge :variant="urgenceVariant">
                    {{ urgenceLabel }}
                  </AppBadge>

                  <AppBadge :variant="statutVariant">
                    {{ statutLabel }}
                  </AppBadge>
                </div>
              </div>
            </div>
          </AppCard>

          <!-- Message de la structure -->
          <AppCard padding="28px" class="message-card">
            <div class="card-header">
              <span class="card-icon">
                <MessageSquare :size="20" :stroke-width="2" />
              </span>
              <h3>Message de la structure</h3>
            </div>

            <div class="card-divider"></div>

            <blockquote v-if="sollicitation.message" class="message-quote">
              « {{ sollicitation.message }} »
            </blockquote>
            <p v-else class="empty-message">
              Aucun message particulier n'a été ajouté à cette demande.
            </p>
          </AppCard>

          <!-- Détails de la demande -->
          <AppCard padding="28px" class="details-card">
            <div class="card-header">
              <span class="card-icon">
                <FileText :size="20" :stroke-width="2" />
              </span>
              <h3>Détails de la demande</h3>
            </div>

            <div class="card-divider"></div>

            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">Référence</span>
                <strong class="info-value">#DS-{{ sollicitation.demande_id.toString().padStart(4, '0') }}</strong>
              </div>

              <div class="info-item">
                <span class="info-label">Groupe sanguin</span>
                <strong class="info-value red">{{ sollicitation.groupe_sanguin }}</strong>
              </div>

              <div class="info-item">
                <span class="info-label">Urgence</span>
                <strong class="info-value">{{ urgenceLabel }}</strong>
              </div>

              <div class="info-item">
                <span class="info-label">Date de sollicitation</span>
                <strong class="info-value">{{ formaterDate(sollicitation.date_creation) }}</strong>
              </div>
            </div>
          </AppCard>

        </div>

        <!-- Colonne droite : actions -->
        <div class="side-column">

          <!-- Actions -->
          <AppCard padding="28px" class="actions-card">
            <div class="card-header">
              <span class="card-icon">
                <Zap :size="20" :stroke-width="2" />
              </span>
              <h3>Actions</h3>
            </div>

            <div class="card-divider"></div>

            <!-- Si la sollicitation est en attente, on propose d'accepter ou refuser -->
            <template v-if="sollicitation.statut === 'en_attente'">
              <p class="action-hint">
                Vous pouvez accepter ou décliner cette sollicitation.
              </p>

              <div class="action-buttons">
                <AppButton
                  variant="primary"
                  class="action-button"
                  @click="accepter"
                >
                  <Check :size="18" />
                  Accepter le don
                </AppButton>

                <AppButton
                  variant="outline"
                  class="action-button"
                  @click="refuser"
                >
                  <X :size="18" />
                  Décliner
                </AppButton>
              </div>
            </template>

            <!-- Si déjà traitée -->
            <template v-else>
              <div class="status-info" :class="sollicitation.statut">
                <component :is="statutIcon" :size="20" :stroke-width="2" />
                <div>
                  <strong>Sollicitation {{ statutLabel.toLowerCase() }}</strong>
                  <p v-if="sollicitation.date_reponse">
                    Le {{ formaterDate(sollicitation.date_reponse) }}
                  </p>
                </div>
              </div>
            </template>
          </AppCard>

          <!-- Timeline -->
          <AppCard padding="28px" class="timeline-card">
            <div class="card-header">
              <span class="card-icon">
                <Clock :size="20" :stroke-width="2" />
              </span>
              <h3>Chronologie</h3>
            </div>

            <div class="card-divider"></div>

            <div class="timeline">
              <div class="timeline-item active">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <strong>Sollicitation reçue</strong>
                  <span>{{ formaterDate(sollicitation.date_creation) }}</span>
                </div>
              </div>

              <div v-if="sollicitation.date_reponse" class="timeline-item active">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <strong>Réponse envoyée</strong>
                  <span>{{ formaterDate(sollicitation.date_reponse) }}</span>
                </div>
              </div>
            </div>
          </AppCard>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import {
  ArrowLeft,
  MapPin,
  MessageSquare,
  FileText,
  Zap,
  Clock,
  Check,
  X,
  AlertCircle,
  CheckCircle,
  XCircle,
  Clock as ClockIcon,
} from 'lucide-vue-next'

import AppCard from '@/components/AppCard.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const erreur = ref('')
const sollicitation = ref(null)

// ==========================================
// CHARGEMENT
// ==========================================

onMounted(async () => {
  const id = route.params.id
  try {
    const { data } = await api.get(`/sollicitations/${id}/`)
    sollicitation.value = data
  } catch (e) {
    if (e.response?.status === 404) {
      erreur.value = "Cette sollicitation n'existe pas ou ne vous est pas adressée."
    } else {
      erreur.value = "Une erreur est survenue lors du chargement."
    }
  } finally {
    loading.value = false
  }
})

// ==========================================
// COMPUTED
// ==========================================

const urgenceVariant = computed(() => {
  const u = sollicitation.value?.urgence
  if (u === 'vitale') return 'danger'
  if (u === 'urgent') return 'warning'
  return 'default'
})

const urgenceLabel = computed(() => {
  const u = sollicitation.value?.urgence
  if (u === 'vitale') return 'Urgence vitale'
  if (u === 'urgent') return 'Urgent'
  if (u === 'programme') return 'Programmé'
  return u
})

const statutVariant = computed(() => {
  const s = sollicitation.value?.statut
  if (s === 'en_attente') return 'warning'
  if (s === 'acceptee') return 'success'
  if (s === 'refusee') return 'danger'
  return 'default'
})

const statutLabel = computed(() => {
  const s = sollicitation.value?.statut
  if (s === 'en_attente') return 'En attente'
  if (s === 'acceptee') return 'Acceptée'
  if (s === 'refusee') return 'Refusée'
  if (s === 'expiree') return 'Expirée'
  return s
})

const statutIcon = computed(() => {
  const s = sollicitation.value?.statut
  if (s === 'acceptee') return CheckCircle
  if (s === 'refusee') return XCircle
  return ClockIcon
})

// ==========================================
// ACTIONS
// ==========================================

async function accepter() {
  try {
    await api.post(`/sollicitations/${sollicitation.value.id}/accepter/`)
    router.push('/donneur/sollicitations')
  } catch (e) {
    // Silencieux
  }
}

async function refuser() {
  try {
    await api.post(`/sollicitations/${sollicitation.value.id}/refuser/`)
    router.push('/donneur/sollicitations')
  } catch (e) {
    // Silencieux
  }
}

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

  const options = {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }
  return date.toLocaleDateString('fr-FR', options)
}
</script>

<style scoped>
.sollicitation-detail-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   CHARGEMENT
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

.error-state p {
  margin: 0 0 24px;
  color: #6b7280;
}

/* ========================================
   FIL D'ARIANE
======================================== */

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #8a94a3;
  font-size: 13px;
}

.breadcrumb a {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #8a94a3;
  text-decoration: none;
  transition: color 0.15s ease;
}

.breadcrumb a:hover {
  color: var(--bloodsen-red);
}

.breadcrumb .separator {
  color: #c5cdd8;
}

.breadcrumb .current {
  color: var(--bloodsen-dark);
  font-weight: 600;
}

/* ========================================
   GRILLE
======================================== */

.detail-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
  align-items: start;
}

.main-column,
.side-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   CARTE HERO
======================================== */

.hero-card {
  overflow: hidden;
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
  background: #ffffff;
}

.hero-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 100px;
  height: 100px;

  border-radius: 16px;
  background-color: #ffffff;
}

.hero-group strong {
  color: var(--bloodsen-red);
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
}

.hero-group span {
  margin-top: 6px;
  color: var(--bloodsen-red);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.hero-info {
  flex: 1;
  min-width: 0;
}

.hero-info h1 {
  margin: 0 0 8px;
  color: var(--bloodsen-dark);
  font-size: 22px;
  font-weight: 700;
  line-height: 1.3;
}

.hero-location {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 12px;
  color: #6b7280;
  font-size: 14px;
}

.hero-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* ========================================
   CARTE MESSAGE
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

.card-header h3 {
  margin: 0;
  color: var(--bloodsen-dark);
  font-size: 16px;
  font-weight: 700;
}

.card-divider {
  height: 1px;
  margin: 18px 0 22px;
  background-color: #eef0f2;
}

.message-quote {
  margin: 0;
  padding: 16px 20px;
  border-left: 3px solid var(--bloodsen-red);
  background-color: #fef9f9;
  border-radius: 0 8px 8px 0;
  color: #4a5568;
  font-size: 14px;
  font-style: italic;
  line-height: 1.6;
}

.empty-message {
  margin: 0;
  color: #8a94a3;
  font-size: 14px;
  font-style: italic;
}

/* ========================================
   GRILLE D'INFOS
======================================== */

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-label {
  color: #8a94a3;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.info-value {
  color: var(--bloodsen-dark);
  font-size: 15px;
  font-weight: 600;
}

.info-value.red {
  color: var(--bloodsen-red);
}

/* ========================================
   CARTE ACTIONS
======================================== */

.action-hint {
  margin: 0 0 20px;
  color: #6b7280;
  font-size: 14px;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-button {
  width: 100%;
  justify-content: center;
}

.status-info {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-radius: 10px;
}

.status-info.en_attente {
  background-color: #fef3c7;
  color: #92400e;
}

.status-info.acceptee {
  background-color: #d1fae5;
  color: #059669;
}

.status-info.refusee {
  background-color: #fee2e2;
  color: #dc2626;
}

.status-info strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
}

.status-info p {
  margin: 4px 0 0;
  font-size: 12.5px;
  opacity: 0.85;
}

/* ========================================
   TIMELINE
======================================== */

.timeline {
  position: relative;
  padding-left: 24px;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 6px;
  bottom: 6px;
  left: 5px;
  width: 2px;
  background-color: #eef0f2;
}

.timeline-item {
  position: relative;
  padding-bottom: 20px;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-dot {
  position: absolute;
  left: -24px;
  top: 4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #c5cdd8;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px #eef0f2;
}

.timeline-item.active .timeline-dot {
  background-color: var(--bloodsen-red);
  box-shadow: 0 0 0 2px #fde8e8;
}

.timeline-content strong {
  display: block;
  color: var(--bloodsen-dark);
  font-size: 13px;
  font-weight: 700;
}

.timeline-content span {
  display: block;
  margin-top: 2px;
  color: #8a94a3;
  font-size: 12px;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1100px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .hero-content {
    flex-direction: column;
    align-items: stretch;
    padding: 24px;
  }

  .hero-group {
    width: 100%;
    height: 80px;
    flex-direction: row;
    gap: 12px;
  }

  .hero-group strong {
    font-size: 28px;
  }

  .hero-info h1 {
    font-size: 18px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>