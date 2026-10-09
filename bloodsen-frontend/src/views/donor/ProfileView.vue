<template>
  <div class="donor-profile-view">

    <div class="page-heading">
      <h2>Mon profil</h2>
      <p>Gérez vos informations de donneur.</p>
    </div>

    <div class="profile-actions">
      <AppButton variant="primary" to="/donneur/profil/modifier">
        Modifier mon profil
      </AppButton>
    </div>

    <!-- ==========================================
         CARTE GAMIFICATION (niveau + badges)
    =========================================== -->
    <AppCard padding="28px" class="gamification-card">
      <div class="gamif-header">
        <div class="gamif-level" :style="{ borderColor: niveauCouleur }">
          <Trophy :size="24" :stroke-width="2" :style="{ color: niveauCouleur }" />
          <div>
            <span class="gamif-level-label">NIVEAU</span>
            <strong class="gamif-level-name" :style="{ color: niveauCouleur }">
              {{ niveauNom }}
            </strong>
          </div>
        </div>

        <div class="gamif-points">
          <span class="gamif-points-value">{{ pointsTotal }}</span>
          <span class="gamif-points-label">points</span>
        </div>
      </div>

      <p v-if="niveauRecompense" class="gamif-recompense">
        <Sparkles :size="14" :stroke-width="2" />
        {{ niveauRecompense }}
      </p>

      <div class="card-divider"></div>

      <h3 class="badges-title">
        <Award :size="18" :stroke-width="2" />
        Badges obtenus ({{ badges.length }})
      </h3>

      <div v-if="badges.length" class="badges-grid">
        <div
          v-for="badge in badges"
          :key="badge.nom"
          class="badge-item"
          :title="badge.description"
        >
          <component :is="iconeBadge(badge.icone)" :size="20" :stroke-width="2" />
          <span>{{ badge.nom }}</span>
        </div>
      </div>

      <p v-else class="badges-empty">
        Aucun badge pour le moment. Continuez à donner !
      </p>
    </AppCard>

    <div class="profile-grid">

      <!-- Informations personnelles -->
      <AppCard padding="28px" class="profile-card">
        <div class="card-header">
          <span class="card-icon"><User :size="20" :stroke-width="2" /></span>
          <h3>Informations personnelles</h3>
        </div>

        <div class="card-divider"></div>

        <div class="info-list">
          <div class="info-row">
            <span class="info-label">Nom</span>
            <strong class="info-value">{{ personal.lastName }}</strong>
          </div>
          <div class="info-row">
            <span class="info-label">Prénom</span>
            <strong class="info-value">{{ personal.firstName }}</strong>
          </div>
          <div class="info-row">
            <span class="info-label">Téléphone</span>
            <strong class="info-value">{{ personal.phone }}</strong>
          </div>
        </div>
      </AppCard>

      <!-- Informations de don -->
      <AppCard padding="28px" class="profile-card">
        <div class="card-header">
          <span class="card-icon"><Heart :size="20" :stroke-width="2" /></span>
          <h3>Informations de don</h3>
        </div>

        <div class="card-divider"></div>

        <div class="info-list">
          <div class="info-row">
            <span class="info-label">Groupe sanguin</span>
            <AppBadge variant="danger">{{ donation.bloodGroup }}</AppBadge>
          </div>
          <div class="info-row">
            <span class="info-label">Disponibilité</span>
            <AppBadge :variant="profil.disponible ? 'success' : 'warning'">
              {{ donation.availability }}
            </AppBadge>
          </div>
        </div>
      </AppCard>

      <!-- Adresse -->
      <AppCard padding="28px" class="profile-card">
        <div class="card-header">
          <span class="card-icon"><MapPin :size="20" :stroke-width="2" /></span>
          <h3>Adresse</h3>
        </div>

        <div class="card-divider"></div>

        <div class="info-list">
          <div class="info-row">
            <span class="info-label">Région</span>
            <strong class="info-value">{{ address.region }}</strong>
          </div>
          <div class="info-row">
            <span class="info-label">Ville</span>
            <strong class="info-value">{{ address.city }}</strong>
          </div>
        </div>
      </AppCard>

      <!-- Paramètres du compte -->
      <AppCard padding="28px" class="profile-card">
        <div class="card-header">
          <span class="card-icon"><Settings :size="20" :stroke-width="2" /></span>
          <h3>Paramètres du compte</h3>
        </div>

        <div class="card-divider"></div>

        <div class="info-list">
          <div class="info-row">
            <span class="info-label">Email</span>
            <strong class="info-value">{{ account.email }}</strong>
          </div>
          <div class="info-row">
            <span class="info-label">Date de création</span>
            <strong class="info-value">{{ account.createdAt }}</strong>
          </div>
        </div>
      </AppCard>

    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import {
  Settings, User, Heart, MapPin,
  Trophy, Award, Sparkles,
  Droplet, Star, Zap, Calendar, Check, Gem, Crown,
} from 'lucide-vue-next'

import AppCard from '@/components/AppCard.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'

const auth = useAuthStore()

// ==========================================
// CHARGEMENT DU PROFIL
// ==========================================

onMounted(async () => {
  if (!auth.user) {
    try {
      await auth.fetchMe()
    } catch (e) {
      // Silencieux
    }
  }
})

// ==========================================
// DONNÉES DÉRIVÉES
// ==========================================

const profil = computed(() => auth.user?.profil || {})

// ==========================================
// GAMIFICATION
// ==========================================

const pointsTotal = computed(() => profil.value.points_total || 0)

const niveauNom = computed(() => profil.value.niveau?.nom || '—')
const niveauCouleur = computed(() => profil.value.niveau?.couleur || '#CD7F32')
const niveauRecompense = computed(() => profil.value.niveau?.recompense || '')

const badges = computed(() => profil.value.badges || [])

// Map : nom d'icône (backend) → composant Lucide
const ICONES = {
  droplet: Droplet,
  award: Award,
  star: Star,
  zap: Zap,
  calendar: Calendar,
  check: Check,
  gem: Gem,
  trophy: Trophy,
  crown: Crown,
}

function iconeBadge(nom) {
  return ICONES[nom] || Award
}

// ==========================================
// AUTRES INFOS
// ==========================================

const personal = computed(() => ({
  lastName: profil.value.nom || '—',
  firstName: profil.value.prenom || '—',
  phone: profil.value.telephone || '—',
}))

const donation = computed(() => ({
  bloodGroup: profil.value.groupe_sanguin || '—',
  availability: profil.value.disponible ? 'Disponible' : 'Indisponible',
}))

const address = computed(() => ({
  region: profil.value.ville?.region || '—',
  city: profil.value.ville?.nom || '—',
}))

const account = computed(() => ({
  email: auth.user?.email || '—',
  createdAt: '—',
}))
</script>

<style scoped>
.donor-profile-view {
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
  color: #6b7280;
  font-size: 14px;
}

/* ========================================
   CARTE GAMIFICATION
======================================== */

.gamification-card {
  display: flex;
  flex-direction: column;
}

.gamif-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.gamif-level {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 14px 20px;

  border: 2px solid;
  border-radius: 12px;

  background-color: #ffffff;
}

.gamif-level-label {
  display: block;
  color: #8a94a3;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.gamif-level-name {
  display: block;
  margin-top: 2px;
  font-size: 20px;
  font-weight: 800;
}

.gamif-points {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.gamif-points-value {
  color: var(--bloodsen-dark);
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
}

.gamif-points-label {
  color: #8a94a3;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.gamif-recompense {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  margin: 16px 0 0;

  color: #8a94a3;
  font-size: 13px;
}

/* Badges */

.badges-title {
  display: flex;
  align-items: center;
  gap: 8px;

  margin: 0 0 16px;

  color: var(--bloodsen-dark);
  font-size: 15px;
  font-weight: 700;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.badge-item {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 12px 14px;

  background: linear-gradient(135deg, #fef2f2 0%, #fff1f2 100%);
  border: 1px solid #fee2e2;
  border-radius: 10px;

  color: var(--bloodsen-red);
  font-size: 13px;
  font-weight: 600;

  transition: transform 0.15s ease;
}

.badge-item:hover {
  transform: translateY(-2px);
}

.badges-empty {
  margin: 0;
  color: #8a94a3;
  font-size: 13px;
  font-style: italic;
}

/* ========================================
   GRILLE DE CARTES
======================================== */

.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

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

.card-icon :deep(svg) {
  width: 20px;
  height: 20px;
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

.info-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.info-label {
  color: #6b7280;
  font-size: 14px;
}

.info-value {
  color: var(--bloodsen-dark);
  font-size: 15px;
  font-weight: 600;
  text-align: right;
}

.profile-actions {
  display: flex;
  justify-content: flex-end;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 900px) {
  .profile-grid { grid-template-columns: 1fr; }
}

@media (max-width: 700px) {
  .page-heading h2 { font-size: 24px; }
  .profile-card, .gamification-card { padding: 20px !important; }
  .info-row { flex-direction: column; align-items: flex-start; gap: 4px; }
  .info-value { text-align: left; }
  .profile-actions { justify-content: stretch; }
  .profile-actions :deep(.app-button) { width: 100%; }
}
</style>