<template>
  <div class="edit-profile-view">

    <div class="page-heading">
      <h2>Mon profil</h2>
      <p>Gérez les informations de votre structure de santé.</p>
    </div>

    <form class="edit-form" @submit.prevent="handleSubmit">
      <div v-if="erreurGlobale" class="form-error">
        {{ erreurGlobale }}
      </div>

      <!-- Informations de la structure -->
      <AppCard padding="28px" class="edit-card">

        <h3 class="card-title">Informations de la structure</h3>
        <div class="card-divider"></div>

        <div class="field-block">
          <AppInput
            id="structure-name"
            v-model="form.nom_structure"
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
          id="structure-address"
          v-model="form.adresse"
          label="Adresse *"
          placeholder="Avenue Nelson Mandela, Dakar"
          required
        />

        <AppSelect
          id="region"
          v-model="form.region"
          label="Région *"
          placeholder="Sélectionnez une région"
          :options="regionsOptions"
          required
        />

        <AppInput
          id="city"
          v-model="form.ville"
          label="Ville *"
          required
        />

        <AppInput
          id="district"
          v-model="form.quartier"
          label="Quartier *"
          required
        />

      </AppCard>

      <!-- Sécurité -->
       <!-- Sécurité -->
      <AppCard padding="28px" class="edit-card">

        <h3 class="card-title">Sécurité du compte</h3>
        <div class="card-divider"></div>

        <AppInput
          id="current-password"
          v-model="passwordForm.actuel"
          type="password"
          label="Mot de passe actuel"
        />

        <AppInput
          id="new-password"
          v-model="passwordForm.nouveau"
          type="password"
          label="Nouveau mot de passe"
          placeholder="Minimum 8 caractères"
        />

        <AppInput
          id="confirm-password"
          v-model="passwordForm.confirmation"
          type="password"
          label="Confirmer le nouveau mot de passe"
          placeholder="Répéter le nouveau mot de passe"
        />

        <div v-if="passwordErreur" class="password-message error">
          <AlertCircle :size="18" :stroke-width="2" />
          <span>{{ passwordErreur }}</span>
        </div>

        <div v-if="passwordSucces" class="password-message success">
          <CheckCircle :size="18" :stroke-width="2" />
          <span>{{ passwordSucces }}</span>
        </div>

        <AppButton
          type="button"
          variant="secondary"
          class="update-password-button"
          :disabled="passwordLoading"
          @click="updatePassword"
        >
          <template v-if="passwordLoading">
            <span class="spinner-small"></span>
            Mise à jour...
          </template>
          <template v-else>
            Mettre à jour le mot de passe
          </template>
        </AppButton>

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
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { CheckCircle, AlertCircle } from 'lucide-vue-next'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppButton from '@/components/AppButton.vue'
import { REGIONS_SENEGAL } from '@/constants/regions'

const router = useRouter()
const auth = useAuthStore()

// ==========================================
// ÉTAT GLOBAL
// ==========================================

const loading = ref(false)
const erreurGlobale = ref('')
const erreursBackend = ref({})

// ==========================================
// FORMULAIRE
// ==========================================

const form = reactive({
  nom_structure: '',
  adresse: '',
  region: '',
  ville: '',
  quartier: '',
})

// ==========================================
// OPTIONS
// ==========================================

const regionsOptions = computed(() =>
  REGIONS_SENEGAL.map(r => ({ value: r, label: r }))
)

// ==========================================
// PRÉ-REMPLISSAGE
// ==========================================

onMounted(async () => {
  if (!auth.user) {
    try {
      await auth.fetchMe()
    } catch (e) {
      // Silencieux
    }
  }

  const profil = auth.user?.profil || {}

  form.nom_structure = profil.nom_structure || ''
  form.adresse = profil.adresse || ''
  form.region = profil.region || ''
  form.ville = profil.ville || ''
  form.quartier = profil.quartier || ''
})

// ==========================================
// SOUMISSION
// ==========================================

async function handleSubmit() {
  erreurGlobale.value = ''
  erreursBackend.value = {}

  const donnees = {
    nom_structure: form.nom_structure,
    adresse: form.adresse,
    region: form.region,
    ville: form.ville,
    quartier: form.quartier,
  }

  loading.value = true
  try {
    await api.patch('/auth/moi/', donnees)
    await auth.fetchMe()
    // On redirige avec un paramètre de succès
    router.push('/structure/profil?updated=1')
  } catch (error) {
    if (error.response?.status === 400) {
      erreursBackend.value = error.response.data
    } else {
      erreurGlobale.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    loading.value = false
  }
}

// ==========================================
// CHANGEMENT DE MOT DE PASSE
// ==========================================

const passwordLoading = ref(false)
const passwordErreur = ref('')
const passwordSucces = ref('')

const passwordForm = reactive({
  actuel: '',
  nouveau: '',
  confirmation: '',
})

async function updatePassword() {
  passwordErreur.value = ''
  passwordSucces.value = ''

  if (!passwordForm.actuel || !passwordForm.nouveau || !passwordForm.confirmation) {
    passwordErreur.value = 'Tous les champs sont obligatoires.'
    return
  }

  if (passwordForm.nouveau !== passwordForm.confirmation) {
    passwordErreur.value = 'Les deux nouveaux mots de passe ne correspondent pas.'
    return
  }

  if (passwordForm.nouveau.length < 8) {
    passwordErreur.value = 'Le nouveau mot de passe doit contenir au moins 8 caractères.'
    return
  }

  passwordLoading.value = true
  try {
    await api.post('/auth/changer-mot-de-passe/', {
      mot_de_passe_actuel: passwordForm.actuel,
      nouveau_mot_de_passe: passwordForm.nouveau,
    })

    passwordSucces.value = 'Mot de passe mis à jour avec succès.'

    passwordForm.actuel = ''
    passwordForm.nouveau = ''
    passwordForm.confirmation = ''

    setTimeout(() => {
      passwordSucces.value = ''
    }, 5000)
  } catch (error) {
    if (error.response?.status === 400) {
      const data = error.response.data
      if (data.mot_de_passe_actuel) {
        passwordErreur.value = data.mot_de_passe_actuel[0]
      } else if (data.nouveau_mot_de_passe) {
        passwordErreur.value = data.nouveau_mot_de_passe[0]
      } else {
        passwordErreur.value = 'Une erreur est survenue.'
      }
    } else {
      passwordErreur.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    passwordLoading.value = false
  }
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
.form-error {
  padding: 12px 16px;
  margin-bottom: 16px;

  background-color: #fde8e8;
  border: 1px solid #f5c2c7;
  border-radius: 6px;

  color: #b42318;
  font-size: 14px;
}

.password-message {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 10px 14px;

  border-radius: 6px;

  font-size: 13px;
  line-height: 1.4;
}

.password-message.error {
  background-color: #fde8e8;
  border: 1px solid #f5c2c7;
  color: #b42318;
}

.password-message.success {
  background-color: #d1fae5;
  border: 1px solid #a7f3d0;
  color: #059669;
}

.update-password-button {
  width: 100%;
}

.spinner-small {
  display: inline-block;
  width: 14px;
  height: 14px;

  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: currentColor;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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