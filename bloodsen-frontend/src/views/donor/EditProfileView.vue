<template>
  <div class="donor-edit-profile-view">

    <div class="page-heading">
      <h2>Mon profil</h2>
      <p>Gérez vos informations personnelles et vos préférences de don.</p>
    </div>

    <form class="edit-form" @submit.prevent="handleSubmit">
      <div v-if="erreurGlobale" class="form-error">
        {{ erreurGlobale }}
      </div>

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
                  model-value="+221"
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

            <AppSelect
              id="region"
              v-model="form.region"
              label="Région"
              placeholder="Sélectionnez une région"
              :options="regionsOptions"
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
                  <span class="metric-label">Groupe sanguin</span>
                  <strong class="metric-value">{{ groupeSanguin }}</strong>
                </div>

                <div class="metric-box">
                  <span class="metric-label">Points d'engagement</span>
                  <strong class="metric-value highlight">{{ pointsEngagement }} pts</strong>
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
                :model-value="emailUtilisateur"
                type="email"
                label="Adresse email"
                disabled
                hint="L'email ne peut pas être modifié."
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

            <!-- Messages d'erreur / succès -->
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
  lastName: '',
  firstName: '',
  phoneNumber: '',   // partie locale du numéro (sans +221)
  region: '',
  district: '',
  city: '',
  availability: 'available',
})

// ==========================================
// PRÉ-REMPLISSAGE
// ==========================================

onMounted(async () => {
  // S'assurer que le profil est chargé
  if (!auth.user) {
    try {
      await auth.fetchMe()
    } catch (e) {
      // Silencieux
    }
  }

  const profil = auth.user?.profil || {}

  form.lastName = profil.nom || ''
  form.firstName = profil.prenom || ''
  form.region = profil.region || ''
  form.city = profil.ville || ''
  form.district = profil.quartier || ''
  form.availability = profil.disponible ? 'available' : 'unavailable'

  // Extraire la partie locale du téléphone (sans +221)
  if (profil.telephone) {
    form.phoneNumber = profil.telephone.replace('+221', '')
  }
})

// ==========================================
// DONNÉES DÉRIVÉES
// ==========================================

const emailUtilisateur = computed(() => auth.user?.email || '—')

const regionsOptions = computed(() =>
  REGIONS_SENEGAL.map(r => ({ value: r, label: r }))
)

const groupeSanguin = computed(() => auth.user?.profil?.groupe_sanguin || '—')

const pointsEngagement = computed(() => auth.user?.profil?.points_total || 0)

// ==========================================
// SOUMISSION
// ==========================================

async function handleSubmit() {
  erreurGlobale.value = ''
  erreursBackend.value = {}

  // Construire les données à envoyer
  // On envoie seulement les champs modifiés (PATCH)
  const donnees = {
    nom: form.lastName,
    prenom: form.firstName,
    telephone: form.phoneNumber,
    region: form.region,
    ville: form.city,
    quartier: form.district,
    disponible: form.availability === 'available',
  }

  loading.value = true
  try {
    await api.patch('/auth/moi/', donnees)

    // Recharger le profil dans le store pour refléter les changements
    await auth.fetchMe()

    // Rediriger vers la page de profil
    router.push('/donneur/profil')
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

// État local pour les 3 champs du formulaire de mot de passe
const passwordForm = reactive({
  actuel: '',
  nouveau: '',
  confirmation: '',
})

async function updatePassword() {
  passwordErreur.value = ''
  passwordSucces.value = ''

  // Vérifications côté frontend
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

    // Vider les champs
    passwordForm.actuel = ''
    passwordForm.nouveau = ''
    passwordForm.confirmation = ''

    // Faire disparaître le message après 5 secondes
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