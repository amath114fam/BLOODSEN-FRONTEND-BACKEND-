<template>
  <AppCard padding="24px" class="gamification-card">

    <!-- Niveau -->
    <div class="gamif-header">
      <div class="gamif-level" :style="{ borderColor: couleur }">
        <Trophy :size="22" :stroke-width="2" :style="{ color: couleur }" />
        <div>
          <span class="gamif-label">NIVEAU</span>
          <strong class="gamif-name" :style="{ color: couleur }">
            {{ nomNiveau }}
          </strong>
        </div>
      </div>

      <div class="gamif-points">
        <strong>{{ points }}</strong>
        <span>pts</span>
      </div>
    </div>

    <!-- Récompense -->
    <p v-if="recompense" class="gamif-recompense">
      <Sparkles :size="13" :stroke-width="2" />
      {{ recompense }}
    </p>

    <div class="gamif-divider"></div>

    <!-- Progression -->
    <div class="gamif-progress">
      <div class="gamif-progress-row">
        <span>Progression</span>
        <strong>{{ points }} / {{ pointsSuivant }}</strong>
      </div>
      <div class="gamif-track">
        <div
          class="gamif-fill"
          :style="{ width: progression + '%', backgroundColor: couleur }"
        ></div>
      </div>
      <p class="gamif-next">
        <template v-if="nomNiveauSuivant">
          Prochain niveau : <strong>{{ nomNiveauSuivant }}</strong>
        </template>
        <template v-else>
          🎉 Vous avez atteint le niveau maximum !
        </template>
      </p>
    </div>

    <div class="gamif-divider"></div>

    <!-- Badges -->
    <div class="gamif-badges-row">
      <div class="gamif-badges-info">
        <Award :size="18" :stroke-width="2" />
        <span><strong>{{ nombreBadges }}</strong> badge(s) obtenu(s)</span>
      </div>
      <router-link to="/donneur/profil" class="gamif-link">
        Voir →
      </router-link>
    </div>

  </AppCard>
</template>

<script setup>
import { computed } from 'vue'
import { Trophy, Award, Sparkles } from 'lucide-vue-next'
import AppCard from '@/components/AppCard.vue'

const props = defineProps({
  // Objet profil complet renvoyé par /api/auth/moi/
  profil: {
    type: Object,
    default: () => ({}),
  },
})

// Couleur du niveau
const couleur = computed(() => props.profil.niveau?.couleur || '#CD7F32')

// Nom du niveau
const nomNiveau = computed(() => props.profil.niveau?.nom || 'Bronze')

// Récompense
const recompense = computed(() => props.profil.niveau?.recompense || '')

// Points actuels
const points = computed(() => props.profil.points_total || 0)

// Nombre de badges
const nombreBadges = computed(() => (props.profil.badges || []).length)

// ==========================================
// PROGRESSION VERS LE NIVEAU SUIVANT
// ==========================================
// Paliers (doivent correspondre au backend)
const PALIERS = [
  { nom: 'Bronze',  seuil: 0 },
  { nom: 'Argent',  seuil: 500 },
  { nom: 'Or',      seuil: 1500 },
  { nom: 'Platine', seuil: 3000 },
]

const indexNiveau = computed(() => {
  const i = PALIERS.findIndex(p => p.nom === nomNiveau.value)
  return i === -1 ? 0 : i
})

const pointsSuivant = computed(() => {
  const next = PALIERS[indexNiveau.value + 1]
  return next ? next.seuil : PALIERS[PALIERS.length - 1].seuil
})

const nomNiveauSuivant = computed(() => {
  const next = PALIERS[indexNiveau.value + 1]
  return next ? next.nom : null
})

const progression = computed(() => {
  if (!nomNiveauSuivant.value) return 100
  const seuilActuel = PALIERS[indexNiveau.value].seuil
  const seuilNext = PALIERS[indexNiveau.value + 1].seuil
  const range = seuilNext - seuilActuel
  if (range <= 0) return 0
  const pct = ((points.value - seuilActuel) / range) * 100
  return Math.min(Math.max(pct, 0), 100)
})
</script>

<style scoped>
.gamification-card {
  display: flex;
  flex-direction: column;
}

/* ========================================
   EN-TÊTE
======================================== */

.gamif-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.gamif-level {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 10px 14px;

  border: 2px solid;
  border-radius: 10px;

  background-color: #ffffff;
}

.gamif-label {
  display: block;
  color: #8a94a3;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
}

.gamif-name {
  display: block;
  margin-top: 1px;
  font-size: 17px;
  font-weight: 800;
}

.gamif-points {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.gamif-points strong {
  color: var(--bloodsen-dark);
  font-size: 24px;
  font-weight: 800;
  line-height: 1;
}

.gamif-points span {
  color: #8a94a3;
  font-size: 12px;
  font-weight: 600;
}

/* ========================================
   RÉCOMPENSE
======================================== */

.gamif-recompense {
  display: inline-flex;
  align-items: center;
  gap: 6px;

  margin: 14px 0 0;

  color: #8a94a3;
  font-size: 12.5px;
}

/* ========================================
   SÉPARATEUR
======================================== */

.gamif-divider {
  height: 1px;
  margin: 18px 0;
  background-color: #eef0f2;
}

/* ========================================
   PROGRESSION
======================================== */

.gamif-progress-row {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 8px;

  color: #8a94a3;
  font-size: 12px;
  font-weight: 600;
}

.gamif-progress-row strong {
  color: var(--bloodsen-dark);
}

.gamif-track {
  height: 8px;
  border-radius: 4px;
  background-color: #f1f3f5;
  overflow: hidden;
}

.gamif-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.4s ease;
}

.gamif-next {
  margin: 10px 0 0;
  color: #8a94a3;
  font-size: 12px;
}

.gamif-next strong {
  color: var(--bloodsen-dark);
}

/* ========================================
   BADGES
======================================== */

.gamif-badges-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.gamif-badges-info {
  display: flex;
  align-items: center;
  gap: 8px;

  color: #8a94a3;
  font-size: 13px;
}

.gamif-badges-info strong {
  color: var(--bloodsen-dark);
  font-weight: 700;
}

.gamif-link {
  color: var(--bloodsen-red);
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
}

.gamif-link:hover {
  text-decoration: underline;
}
</style>