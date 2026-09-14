<template>
  <div class="donor-edit-profile-view">

    <div class="page-heading">
      <h2>Mon profil</h2>
      <p>Gérez vos informations personnelles et vos préférences de don.</p>
    </div>

    <form class="edit-form" @submit.prevent="handleSubmit">

      <div class="edit-grid">

        <!-- Colonne gauche -->
        <div class="edit-column">

          <!-- Informations personnelles -->
          <AppCard padding="28px" class="edit-card">

            <div class="card-header">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="4" y="7" width="16" height="13" rx="2" stroke="currentColor" stroke-width="2" />
                  <path d="M9 7V5C9 3.9 9.9 3 11 3H13C14.1 3 15 3.9 15 5V7" stroke="currentColor" stroke-width="2" />
                </svg>
              </span>
              <h3>Informations personnelles</h3>
            </div>

            <div class="card-divider"></div>

            <div class="field-row two-cols">
              <AppInput
                id="last-name"
                v-model="form.lastName"
                label="Nom"
              />

              <AppInput
                id="first-name"
                v-model="form.firstName"
                label="Prénom"
              />
            </div>

            <div class="field-block">
              <span class="field-label">Téléphone de contact</span>
              <div class="phone-row">
                <AppInput
                  id="phone-prefix"
                  v-model="form.phonePrefix"
                  class="phone-prefix"
                  disabled
                />
                <AppInput
                  id="phone-number"
                  v-model="form.phoneNumber"
                  class="phone-number"
                />
              </div>
            </div>

            <AppInput
              id="region"
              v-model="form.region"
              label="Région"
            />

            <AppInput
              id="district"
              v-model="form.district"
              label="Quartier"
            />

            <AppInput
              id="city"
              v-model="form.city"
              label="Ville"
            />

          </AppCard>

          <!-- Informations de don -->
          <AppCard padding="28px" class="edit-card">

            <div class="card-header">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 3L19 6V11C19 15.5 16 19.5 12 21C8 19.5 5 15.5 5 11V6L12 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </span>
              <h3>Informations de don</h3>
            </div>

            <div class="card-divider"></div>

            <span class="field-label">Statut de disponibilité</span>

            <div class="availability-options">

              <label
                class="availability-option"
                :class="{ active: form.availability === 'available' }"
              >
                <input
                  v-model="form.availability"
                  type="radio"
                  value="available"
                  name="availability"
                />
                <div class="availability-content">
                  <span class="availability-title">
                    Disponible
                    <span class="dot success"></span>
                  </span>
                  <p>Vous recevez les alertes et sollicitations urgentes</p>
                </div>
              </label>

              <label
                class="availability-option"
                :class="{ active: form.availability === 'unavailable' }"
              >
                <input
                  v-model="form.availability"
                  type="radio"
                  value="unavailable"
                  name="availability"
                />
                <div class="availability-content">
                  <span class="availability-title">Indisponible</span>
                  <p>Mettre en pause les sollicitations et notifications</p>
                </div>
              </label>

            </div>

          </AppCard>

        </div>

        <!-- Colonne droite -->
        <div class="edit-column">

          <!-- Mon engagement citoyen -->
          <AppCard padding="28px" class="edit-card">

            <div class="card-header">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </span>
              <h3>Mon engagement citoyen</h3>
            </div>

            <div class="card-divider"></div>

            <div class="metrics-grid">

              <div class="metric-box">
                <span class="metric-label">Dons confirmés</span>
                <strong class="metric-value">{{ engagement.donations }} dons</strong>
              </div>

              <div class="metric-box">
                <span class="metric-label">Participations</span>
                <strong class="metric-value">{{ engagement.participations }}</strong>
              </div>

              <div class="metric-box">
                <span class="metric-label">Points d'engagement</span>
                <strong class="metric-value highlight">{{ engagement.points }} pts</strong>
              </div>

            </div>

          </AppCard>

          <!-- Informations du compte -->
          <AppCard padding="28px" class="edit-card">

            <div class="card-header">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="2" />
                  <path d="M3 19C3 15.69 5.69 13 9 13C12.31 13 15 15.69 15 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                  <path d="M17 8V14" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                  <path d="M14 11H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                </svg>
              </span>
              <h3>Informations du compte</h3>
            </div>

            <div class="card-divider"></div>

            <AppInput
              id="email"
              v-model="form.email"
              type="email"
              label="Adresse email"
            />

          </AppCard>

          <!-- Sécurité du compte -->
          <AppCard padding="28px" class="edit-card">

            <div class="card-header">
              <span class="card-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="5" y="11" width="14" height="9" rx="2" stroke="currentColor" stroke-width="2" />
                  <path d="M8 11V8C8 5.79 9.79 4 12 4C14.21 4 16 5.79 16 8V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                </svg>
              </span>
              <h3>Sécurité du compte</h3>
            </div>

            <div class="card-divider"></div>

            <AppInput
              id="current-password"
              v-model="form.currentPassword"
              type="password"
              label="Mot de passe actuel"
            />

            <AppInput
              id="new-password"
              v-model="form.newPassword"
              type="password"
              label="Nouveau mot de passe"
              placeholder="Minimum 8 caractères"
            />

            <AppButton
              type="button"
              variant="secondary"
              class="update-password-button"
              @click="updatePassword"
            >
              Mettre à jour le mot de passe
            </AppButton>

          </AppCard>

        </div>

      </div>

      <div class="form-actions">

        <AppButton
          type="button"
          variant="outline"
          to="/donneur/profil"
        >
          Annuler
        </AppButton>

        <AppButton
          type="submit"
          variant="primary"
        >
          Enregistrer les modifications
        </AppButton>

      </div>

    </form>

  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppButton from '@/components/AppButton.vue'

const router = useRouter()

const form = reactive({
  lastName: 'Sall',
  firstName: 'Abdoulaye',
  phonePrefix: '+221',
  phoneNumber: '77 452 18 90',
  region: 'Dakar',
  district: 'Dakar',
  city: 'Médina',
  availability: 'available',
  email: 'abdoulaye.sall@gmail.com',
  currentPassword: '',
  newPassword: '',
})

const engagement = reactive({
  donations: 6,
  participations: 8,
  points: 320,
})

function updatePassword() {
  console.log('Mise à jour du mot de passe...')
  // Plus tard : appel API PATCH /donneur/mot-de-passe
}

function handleSubmit() {
  console.log('Profil donneur mis à jour :', form)

  // Plus tard : appel API PATCH /donneur/profil
  router.push('/donneur/profil')
}
</script>

<style scoped>
.donor-edit-profile-view {
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

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   GRILLE 2 COLONNES
======================================== */

.edit-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: start;
}

.edit-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.edit-card {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* ========================================
   EN-TÊTE DE CARTE
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
  width: 19px;
  height: 19px;
}

.card-header h3 {
  margin: 0;

  color: var(--bloodsen-dark);

  font-size: 16px;
  font-weight: 700;
}

.card-divider {
  height: 1px;
  margin-top: -6px;

  background-color: #eef0f2;
}

/* ========================================
   CHAMPS
======================================== */

.field-row {
  display: grid;
  gap: 16px;
}

.field-row.two-cols {
  grid-template-columns: 1fr 1fr;
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  color: var(--bloodsen-dark);

  font-size: 13px;
  font-weight: 500;
}

.phone-row {
  display: grid;
  grid-template-columns: 76px 1fr;
  gap: 10px;
}

.phone-prefix :deep(input) {
  text-align: center;
  font-weight: 600;
}

/* ========================================
   DISPONIBILITÉ
======================================== */

.availability-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.availability-option {
  position: relative;

  display: flex;
  align-items: flex-start;
  gap: 10px;

  padding: 16px;

  border: 1px solid #e1e4e8;
  border-radius: 10px;

  cursor: pointer;

  transition: border-color 0.15s ease;
}

.availability-option.active {
  border-color: var(--bloodsen-red);
  border-width: 2px;
  padding: 15px;
}

.availability-option input {
  margin-top: 3px;

  accent-color: var(--bloodsen-red);

  cursor: pointer;
}

.availability-title {
  display: flex;
  align-items: center;
  gap: 6px;

  color: var(--bloodsen-dark);

  font-size: 14px;
  font-weight: 700;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.dot.success {
  background-color: #1e9e5a;
}

.availability-content p {
  margin: 4px 0 0;

  color: #8a94a3;

  font-size: 12.5px;
  line-height: 1.4;
}

/* ========================================
   MÉTRIQUES ENGAGEMENT
======================================== */

.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.metric-box {
  display: flex;
  flex-direction: column;
  gap: 8px;

  padding: 16px;

  border: 1px solid #eef0f2;
  border-radius: 10px;
}

.metric-label {
  color: #8a94a3;
  font-size: 12.5px;
}

.metric-value {
  color: var(--bloodsen-dark);

  font-size: 20px;
  font-weight: 700;
}

.metric-value.highlight {
  color: var(--bloodsen-red);
}

/* ========================================
   BOUTON MOT DE PASSE
======================================== */

.update-password-button {
  width: 100%;
}

/* ========================================
   ACTIONS BAS DE PAGE
======================================== */

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1100px) {
  .edit-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {

  .page-heading h2 {
    font-size: 24px;
  }

  .edit-card {
    padding: 20px !important;
  }

  .field-row.two-cols {
    grid-template-columns: 1fr;
  }

  .availability-options {
    grid-template-columns: 1fr;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions :deep(.app-button) {
    width: 100%;
  }

}
</style>