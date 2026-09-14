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
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="8" r="3.5" stroke="currentColor" stroke-width="2" />
              <path d="M5 20C5 16.13 8.13 13 12 13C15.87 13 19 16.13 19 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
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
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21C12 21 4 15.5 4 9.5C4 6.46 6.46 4 9.5 4C11.24 4 12.78 4.81 12.78 4.81C12.78 4.81 14.32 4 16.06 4C19.1 4 21.56 6.46 21.56 9.5C21.56 15.5 12 21 12 21Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
            </svg>
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
            <AppBadge variant="success">{{ donation.availability }}</AppBadge>
          </div>

        </div>

      </AppCard>

      <!-- Adresse -->
      <AppCard padding="28px" class="profile-card">

        <div class="card-header">
          <span class="card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 10C20 15 12 21 12 21C12 21 4 15 4 10C4 5.58 7.58 2 12 2C16.42 2 20 5.58 20 10Z" stroke="currentColor" stroke-width="2" />
              <circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="2" />
            </svg>
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
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" />
              <path d="M19.4 15C19.13 15.6 19.2 16.3 19.6 16.83L19.66 16.91C19.99 17.33 20 17.92 19.66 18.34C19.33 18.75 18.76 18.87 18.29 18.62L18.2 18.57C17.62 18.25 16.92 18.28 16.36 18.65C15.81 19.01 15.48 19.63 15.5 20.29V20.4C15.51 20.99 15.05 21.47 14.47 21.48H14.4C13.83 21.5 13.34 21.05 13.31 20.47V20.36C13.29 19.7 12.9 19.11 12.31 18.83C11.71 18.53 11 18.6 10.47 19L10.4 19.06C9.93 19.4 9.28 19.33 8.9 18.9C8.53 18.48 8.53 17.85 8.9 17.43L8.96 17.34C9.33 16.87 9.4 16.24 9.15 15.7C8.9 15.16 8.38 14.79 7.79 14.71H7.68C7.09 14.65 6.66 14.13 6.72 13.54C6.78 12.97 7.27 12.53 7.85 12.54H7.96C8.62 12.53 9.22 12.16 9.51 11.57C9.8 10.98 9.75 10.27 9.37 9.73L9.31 9.65C8.96 9.19 9.04 8.55 9.46 8.19C9.87 7.83 10.49 7.83 10.9 8.19L10.98 8.25C11.46 8.62 12.09 8.68 12.62 8.41C13.16 8.14 13.51 7.61 13.53 7.01V6.9C13.5 6.32 13.94 5.83 14.51 5.79C15.09 5.75 15.6 6.17 15.66 6.75V6.86C15.68 7.52 16.07 8.11 16.66 8.39C17.26 8.68 17.97 8.61 18.5 8.21L18.57 8.16C19.03 7.81 19.68 7.87 20.06 8.29C20.44 8.71 20.44 9.35 20.06 9.77L20 9.86C19.62 10.32 19.55 10.96 19.79 11.5C20.05 12.03 20.56 12.4 21.16 12.48H21.27C21.85 12.53 22.28 13.05 22.22 13.63C22.17 14.2 21.68 14.65 21.1 14.63H20.99C20.33 14.65 19.73 15.03 19.44 15.62" stroke="currentColor" stroke-width="1.3" />
            </svg>
          </span>
          <h3>Paramètres du compte</h3>
        </div>

        <div class="card-divider"></div>

        <div class="info-list">

          <div class="info-row">
            <span class="info-label">Email</span>
            <strong class="info-value">{{ account.maskedEmail }}</strong>
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
import { ref } from 'vue'

import AppCard from '@/components/AppCard.vue'
import AppBadge from '@/components/AppBadge.vue'
import AppButton from '@/components/AppButton.vue'

const personal = ref({
  lastName: 'Diop',
  firstName: 'Moussa',
  phone: '+221 77 *** ** 45',
})

const donation = ref({
  bloodGroup: 'AB+',
  availability: 'Disponible',
})

const address = ref({
  region: 'Dakar',
  city: 'Dakar',
  district: 'Médina',
})

const account = ref({
  maskedEmail: 'm*****p@gmail.com',
  createdAt: '15 Jan 2023',
  lastLogin: "Aujourd'hui, 14:32",
})

// TODO : remplacer par un appel API GET /donneur/profil
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

.card-icon svg {
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