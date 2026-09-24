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
    <div class="profile-grid">

      <!-- Informations personnelles -->
      <AppCard padding="28px" class="profile-card">

        <div class="card-header">
          <span class="card-icon">
            <User :size="20" :stroke-width="2" />
          </span>
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
          <span class="card-icon">
            <Heart :size="20" :stroke-width="2" />
          </span>
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
          <span class="card-icon">
            <MapPin :size="20" :stroke-width="2" />
          </span>
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

          <div class="info-row">
            <span class="info-label">Quartier</span>
            <strong class="info-value">{{ address.district }}</strong>
          </div>

        </div>

      </AppCard>

      <!-- Paramètres du compte -->
      <AppCard padding="28px" class="profile-card">

        <div class="card-header">
          <span class="card-icon">
            <Settings :size="20" :stroke-width="2" />
          </span>
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

          <div class="info-row">
            <span class="info-label">Dernière connexion</span>
            <strong class="info-value">{{ account.lastLogin }}</strong>
          </div>

        </div>

      </AppCard>

    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Settings, User, Heart, MapPin } from 'lucide-vue-next'

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
      // Silencieux : l'intercepteur gère la redirection
    }
  }
})

// ==========================================
// DONNÉES DÉRIVÉES
// ==========================================

const profil = computed(() => auth.user?.profil || {})

// Informations personnelles
const personal = computed(() => ({
  lastName: profil.value.nom || '—',
  firstName: profil.value.prenom || '—',
  phone: profil.value.telephone || '—',
}))

// Informations de don
const donation = computed(() => ({
  bloodGroup: profil.value.groupe_sanguin || '—',
  availability: profil.value.disponible ? 'Disponible' : 'Indisponible',
}))

// Adresse
const address = computed(() => ({
  region: profil.value.region || '—',
  city: profil.value.ville || '—',
  district: profil.value.quartier || '—',
}))

// Paramètres du compte
const account = computed(() => ({
  email: auth.user?.email || '—',
  createdAt: '—',
  lastLogin: '—',
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
   GRILLE DE CARTES
======================================== */

.profile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
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

/* ========================================
   LISTE D'INFOS
======================================== */

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

/* ========================================
   ACTIONS
======================================== */

.profile-actions {
  display: flex;
  justify-content: flex-end;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 900px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {

  .page-heading h2 {
    font-size: 24px;
  }

  .profile-card {
    padding: 20px !important;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .info-value {
    text-align: left;
  }

  .profile-actions {
    justify-content: stretch;
  }

  .profile-actions :deep(.app-button) {
    width: 100%;
  }

}
</style>