<template>
  <div class="reset-password-view">

    <div class="reset-card">

      <!-- Logo -->
      <router-link to="/" class="back-home">
        <ArrowLeft :size="16" />
        Retour à l'accueil
      </router-link>

      <!-- ==========================================
           ÉTAT 1 : CHARGEMENT DE LA VÉRIFICATION
      =========================================== -->
      <div v-if="etat === 'verification'" class="state-content">
        <div class="spinner-large"></div>
        <h1>Vérification du lien...</h1>
        <p>Un instant, nous validons votre lien de réinitialisation.</p>
      </div>

      <!-- ==========================================
           ÉTAT 2 : FORMULAIRE DE NOUVEAU MOT DE PASSE
      =========================================== -->
      <div v-else-if="etat === 'formulaire'" class="state-content">
        <div class="page-heading">
          <div class="icon-wrapper">
            <Lock :size="32" :stroke-width="1.8" />
          </div>
          <h1>Nouveau mot de passe</h1>
          <p>
            Choisissez un nouveau mot de passe sécurisé pour votre compte.
          </p>
        </div>

        <form class="reset-form" @submit.prevent="handleSubmit">
          <AppInput
            id="password"
            v-model="password"
            type="password"
            label="Nouveau mot de passe *"
            placeholder="8 caractères minimum"
            required
            :error="erreurPassword"
          />

          <AppInput
            id="password-confirmation"
            v-model="passwordConfirmation"
            type="password"
            label="Confirmation du mot de passe *"
            placeholder="Répétez le mot de passe"
            required
            :error="erreurConfirmation"
          />

          <div v-if="erreurGlobale" class="global-error">
            <AlertCircle :size="18" />
            <span>{{ erreurGlobale }}</span>
          </div>

          <div class="password-hints">
            <p><strong>Règles de sécurité :</strong></p>
            <ul>
              <li :class="{ valid: password.length >= 8 }">
                Au moins 8 caractères
              </li>
              <li :class="{ valid: /[A-Z]/.test(password) }">
                Une majuscule
              </li>
              <li :class="{ valid: /[a-z]/.test(password) }">
                Une minuscule
              </li>
              <li :class="{ valid: /\d/.test(password) }">
                Un chiffre
              </li>
            </ul>
          </div>

          <AppButton
            type="submit"
            variant="primary"
            size="lg"
            :disabled="loading"
          >
            <template v-if="loading">
              <span class="spinner-small"></span>
              Réinitialisation...
            </template>
            <template v-else>
              Réinitialiser mon mot de passe
            </template>
          </AppButton>
        </form>
      </div>

      <!-- ==========================================
           ÉTAT 3 : SUCCÈS
      =========================================== -->
      <div v-else-if="etat === 'succes'" class="state-content">
        <div class="success-icon">
          <CheckCircle :size="40" :stroke-width="2" />
        </div>
        <h3>Mot de passe réinitialisé !</h3>
        <p>
          Votre mot de passe a été modifié avec succès.
          Vous allez être redirigé vers la page de connexion...
        </p>
        <div class="spinner-small dark"></div>
      </div>

      <!-- ==========================================
           ÉTAT 4 : ERREUR (token invalide/expiré)
      =========================================== -->
      <div v-else-if="etat === 'erreur'" class="state-content">
        <div class="error-icon">
          <XCircle :size="40" :stroke-width="2" />
        </div>
        <h3>Lien invalide ou expiré</h3>
        <p>{{ erreurGlobale }}</p>
        <router-link to="/mot-de-passe-oublie" class="btn-primary">
          Demander un nouveau lien
        </router-link>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import {
  ArrowLeft,
  Lock,
  AlertCircle,
  CheckCircle,
  XCircle,
} from 'lucide-vue-next'

import AppInput from '@/components/AppInput.vue'
import AppButton from '@/components/AppButton.vue'

const route = useRoute()
const router = useRouter()

// États : 'verification' | 'formulaire' | 'succes' | 'erreur'
const etat = ref('verification')

const token = ref('')
const password = ref('')
const passwordConfirmation = ref('')

const loading = ref(false)
const erreurGlobale = ref('')
const erreurPassword = ref('')
const erreurConfirmation = ref('')

// ==========================================
// AU CHARGEMENT DE LA PAGE
// ==========================================

onMounted(() => {
  // Récupérer le token dans l'URL
  const tokenUrl = route.query.token

  if (!tokenUrl) {
    etat.value = 'erreur'
    erreurGlobale.value = "Aucun token n'a été fourni. Le lien est incomplet."
    return
  }

  token.value = tokenUrl
  etat.value = 'formulaire'
})

// ==========================================
// VALIDATION
// ==========================================

function validerFormulaire() {
  erreurPassword.value = ''
  erreurConfirmation.value = ''
  erreurGlobale.value = ''

  // Vérifier la longueur
  if (password.value.length < 8) {
    erreurPassword.value = 'Le mot de passe doit contenir au moins 8 caractères.'
    return false
  }

  // Vérifier la correspondance
  if (password.value !== passwordConfirmation.value) {
    erreurConfirmation.value = 'Les deux mots de passe ne correspondent pas.'
    return false
  }

  return true
}

// ==========================================
// SOUMISSION
// ==========================================

async function handleSubmit() {
  if (!validerFormulaire()) return

  loading.value = true
  try {
    await api.post('/auth/reinitialiser-mot-de-passe/', {
      token: token.value,
      nouveau_mot_de_passe: password.value,
    })

    etat.value = 'succes'

    // Redirection après 3 secondes
    setTimeout(() => {
      router.push('/connexion')
    }, 3000)
  } catch (error) {
    if (error.response?.status === 400) {
      const data = error.response.data

      if (data.token) {
        // Token invalide ou expiré
        etat.value = 'erreur'
        erreurGlobale.value = data.token[0]
      } else if (data.nouveau_mot_de_passe) {
        erreurPassword.value = data.nouveau_mot_de_passe[0]
      } else {
        erreurGlobale.value = 'Une erreur est survenue. Veuillez réessayer.'
      }
    } else {
      erreurGlobale.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reset-password-view {
  display: flex;
  align-items: center;
  justify-content: center;

  min-height: 100vh;
  padding: 24px;

  background: linear-gradient(135deg, #f7f9fb 0%, #e6eaf0 100%);
}

.reset-card {
  max-width: 480px;
  width: 100%;

  padding: 40px 36px;

  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.back-home {
  display: inline-flex;
  align-items: center;
  gap: 6px;

  margin-bottom: 24px;

  color: #60708a;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
}

.back-home:hover {
  color: var(--bloodsen-red);
}

/* États */
.state-content {
  text-align: center;
}

.state-content h1 {
  margin: 0 0 12px;

  color: var(--bloodsen-dark);
  font-size: 24px;
  font-weight: 700;
}

.state-content h3 {
  margin: 0 0 12px;

  color: var(--bloodsen-dark);
  font-size: 22px;
  font-weight: 700;
}

.state-content p {
  margin: 0 0 16px;

  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

/* En-tête */
.page-heading {
  margin-bottom: 32px;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 64px;
  height: 64px;
  margin-bottom: 20px;

  border-radius: 50%;
  background-color: #fdecec;
  color: var(--bloodsen-red);
}

/* Formulaire */
.reset-form {
  display: flex;
  flex-direction: column;
  gap: 20px;

  text-align: left;
}

/* Hints de mot de passe */
.password-hints {
  padding: 14px 16px;

  background-color: #f7f9fb;
  border: 1px solid #e6eaf0;
  border-radius: 8px;
}

.password-hints p {
  margin: 0 0 10px;
  color: var(--bloodsen-dark);
  font-size: 13px;
}

.password-hints ul {
  margin: 0;
  padding: 0;
  list-style: none;

  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
}

.password-hints li {
  color: #8a94a3;
  font-size: 12.5px;
  transition: color 0.15s ease;
}

.password-hints li::before {
  content: '○ ';
}

.password-hints li.valid {
  color: #059669;
  font-weight: 600;
}

.password-hints li.valid::before {
  content: '✓ ';
}

/* Erreurs / Spinner */
.global-error {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 12px 16px;

  background-color: #fde8e8;
  border: 1px solid #f5c2c7;
  border-radius: 6px;

  color: #b42318;
  font-size: 13px;

  text-align: left;
}

.spinner-large {
  display: inline-block;
  width: 48px;
  height: 48px;
  margin-bottom: 20px;

  border: 4px solid #e6eaf0;
  border-top-color: var(--bloodsen-red);
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

.spinner-small {
  display: inline-block;
  width: 14px;
  height: 14px;

  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

.spinner-small.dark {
  border-color: rgba(200, 16, 46, 0.2);
  border-top-color: var(--bloodsen-red);
  margin-top: 12px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Icônes de succès / erreur */
.success-icon,
.error-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 80px;
  height: 80px;
  margin-bottom: 20px;

  border-radius: 50%;
}

.success-icon {
  background-color: #d1fae5;
  color: #059669;
}

.error-icon {
  background-color: #fee2e2;
  color: #dc2626;
}

/* Bouton primaire */
.btn-primary {
  display: inline-block;
  margin-top: 8px;
  padding: 14px 28px;

  background-color: var(--bloodsen-red);
  border-radius: 8px;

  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;

  transition: opacity 0.2s ease;
}

.btn-primary:hover {
  opacity: 0.9;
}

@media (max-width: 480px) {
  .reset-card {
    padding: 32px 24px;
  }

  .password-hints ul {
    grid-template-columns: 1fr;
  }
}
</style>