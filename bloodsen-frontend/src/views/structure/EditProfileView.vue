<template>
  <div class="edit-profile-view">

    <div class="page-heading">
      <h2>Mon profil</h2>
      <p>Gérez les informations de votre structure de santé.</p>
    </div>

    <form class="edit-form" @submit.prevent="handleSubmit">

      <!-- Informations de la structure -->
      <AppCard padding="28px" class="edit-card">

        <h3 class="card-title">Informations de la structure</h3>
        <div class="card-divider"></div>

        <div class="field-block">
          <AppInput
            id="structure-name"
            v-model="form.name"
            label="Nom de la structure de santé *"
            required
          >
            <template #trailing>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="8" r="3.5" stroke="currentColor" stroke-width="2" />
                <path d="M5 20C5 16.13 8.13 13 12 13C15.87 13 19 16.13 19 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              </svg>
            </template>
          </AppInput>
          <p class="field-hint">
            Nom légal répertorié sur le registre du Ministère de la Santé du Sénégal.
          </p>
        </div>

        <AppInput
          id="region"
          v-model="form.region"
          label="Région *"
          required
        />

        <AppInput
          id="city"
          v-model="form.city"
          label="Ville *"
          required
        />

        <AppInput
          id="district"
          v-model="form.district"
          label="Quartier *"
          required
        />

      </AppCard>

      <!-- Sécurité -->
      <AppCard padding="28px" class="edit-card">

        <AppInput
          id="current-password"
          v-model="form.currentPassword"
          type="password"
          label="Mot de passe actuel"
        />

        <AppInput
          id="confirm-password"
          v-model="form.confirmPassword"
          type="password"
          label="Confirmer le mot de passe"
          placeholder="Répéter le nouveau mot de passe"
        />

        <AppInput
          id="new-password"
          v-model="form.newPassword"
          type="password"
          label="Nouveau mot de passe"
          placeholder="Minimum 10 caractères"
        />

      </AppCard>

      <div class="form-actions">

        <AppButton
          type="button"
          variant="outline"
          to="/structure/profil"
        >
          Annuler
        </AppButton>

        <AppButton
          type="submit"
          variant="primary"
        >
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M5 4H16L19 7V19C19 19.55 18.55 20 18 20H5C4.45 20 4 19.55 4 19V5C4 4.45 4.45 4 5 4Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
            <path d="M8 4V9H15V4" stroke="currentColor" stroke-width="2" />
            <path d="M7 20V13H16V20" stroke="currentColor" stroke-width="2" />
          </svg>
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
  name: 'Centre Hospitalier National Universitaire de Fann (CHNU de Fann)',
  region: 'Dakar',
  city: 'Dakar',
  district: 'Dakar',
  currentPassword: '',
  confirmPassword: '',
  newPassword: '',
})

function handleSubmit() {
  console.log('Profil mis à jour :', form)

  // Plus tard : appel API PATCH /structure/profil
  router.push('/structure/profil')
}
</script>

<style scoped>
.edit-profile-view {
  max-width: 640px;
}

.page-heading {
  margin-bottom: 24px;
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

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.edit-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-title {
  margin: 0;
  color: var(--bloodsen-dark);
  font-size: 16px;
  font-weight: 700;
}

.card-divider {
  height: 1px;
  margin-top: -8px;
  background-color: #eef0f2;
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-hint {
  margin: 0;
  color: #8a94a3;
  font-size: 12px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@media (max-width: 700px) {

  .edit-profile-view {
    max-width: none;
  }

  .page-heading h2 {
    font-size: 24px;
  }

  .edit-card {
    padding: 20px !important;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions :deep(.app-button) {
    width: 100%;
  }

}
</style>