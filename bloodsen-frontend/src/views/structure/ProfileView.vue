<template>
  <div class="profile-view">

    <div class="page-heading-row">

      <div class="page-heading">
        <h2>Mon profil</h2>
        <p>Gérez les informations de votre structure.</p>
      </div>

      <AppButton v-if="!afficherMessageSucces" variant="primary" to="/structure/profil/modifier">
        Modifier mon profil
      </AppButton>

      <div v-if="afficherMessageSucces" class="success-banner">
        <CheckCircle :size="20" :stroke-width="2.5" class="success-icon" />
        <span>Votre profil a été mis à jour avec succès.</span>
      </div>

    </div>

    <!-- Informations de la structure -->
    <AppCard padding="28px" class="profile-card">

      <div class="card-header">
        <span class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" />
            <path d="M12 8H12.01" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" />
            <path d="M11 12H12V16H13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>

        <h3>Informations de la structure</h3>
      </div>

      <div class="card-divider"></div>

      <div class="info-list">

        <div class="info-item">
          <span class="info-label">Nom de l'établissement</span>
          <strong class="info-value">{{ structure.name }}</strong>
        </div>

        <div class="info-item">
          <span class="info-label">Région</span>
          <strong class="info-value">{{ structure.region }}</strong>
        </div>

        <div class="info-item">
          <span class="info-label">Ville</span>
          <strong class="info-value">{{ structure.city }}</strong>
        </div>

        <div class="info-item">
          <span class="info-label">Quartier</span>
          <strong class="info-value">{{ structure.district }}</strong>
        </div>

      </div>

    </AppCard>

    <!-- Sécurité et accès -->
    <AppCard padding="28px" class="profile-card">

      <div class="card-header">
        <span class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3L19 6V11C19 15.5 16 19.5 12 21C8 19.5 5 15.5 5 11V6L12 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>

        <h3>Email</h3>
      </div>

      <div class="card-divider"></div>

      <div class="info-grid">

        <div class="info-item">
          <span class="info-label">Adresse email</span>
          <div class="info-value-row">
            <strong class="info-value">{{ account.email }}</strong>
          </div>
        </div>

      </div>

    </AppCard>

  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { CheckCircle } from 'lucide-vue-next'

import AppCard from '@/components/AppCard.vue'
import AppButton from '@/components/AppButton.vue'

const auth = useAuthStore()

const route = useRoute()
const router = useRouter()

// Affiche le message de succès si on vient de la page de modification
const afficherMessageSucces = ref(route.query.updated === '1')

// Cache le message après 5 secondes et retire le paramètre de l'URL
onMounted(() => {
  if (afficherMessageSucces.value) {
    setTimeout(() => {
      afficherMessageSucces.value = false
      router.replace({ query: {} })   // retire le ?updated=1
    }, 5000)
  }
})

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

// Informations de la structure
const structure = computed(() => ({
  name: profil.value.nom_structure || '—',
  region: profil.value.region || '—',
  city: profil.value.ville || '—',
  district: profil.value.quartier || '—',
}))

// Informations du compte
const account = computed(() => ({
  email: auth.user?.email || '—',
  createdAt: '—',        // pas encore disponible dans l'API
  lastLogin: '—',        // pas encore disponible dans l'API
}))
</script>

<style scoped>
.profile-view {
  display: flex;
  flex-direction: column;
  gap: 24px;

  max-width: 640px;
}

/* ========================================
   EN-TÊTE
======================================== */

.page-heading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;

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

/* ========================================
   CARTES
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

  width: 26px;
  height: 26px;

  border-radius: 50%;

  background-color: var(--bloodsen-red);
  color: #ffffff;
}

.card-icon svg {
  width: 15px;
  height: 15px;
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
   LISTE D'INFOS
======================================== */

.info-list {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

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

  font-size: 16px;
  font-weight: 600;
}

.info-value-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
/* ========================================
   BANDEAU DE SUCCÈS
======================================== */

.success-banner {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 14px 18px;

  background-color: #d1fae5;
  border: 1px solid #a7f3d0;
  border-radius: 8px;

  color: #059669;
  font-size: 14px;
  font-weight: 600;

  animation: slideDown 0.3s ease;
}

.success-icon {
  flex-shrink: 0;
  color: #059669;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 700px) {

  .profile-view {
    max-width: none;
  }

  .page-heading-row {
    flex-direction: column;
    align-items: stretch;
  }

  .page-heading-row :deep(button) {
    width: 100%;
  }

  .page-heading h2 {
    font-size: 24px;
  }

  .profile-card {
    padding: 20px !important;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

}
</style>