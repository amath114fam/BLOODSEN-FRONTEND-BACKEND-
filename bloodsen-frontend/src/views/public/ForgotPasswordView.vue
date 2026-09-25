<template>
  <div class="forgot-password-view">

    <div class="forgot-card">

      <!-- Logo -->
      <router-link to="/" class="back-home">
        <ArrowLeft :size="16" />
        Retour à l'accueil
      </router-link>


      <!-- État 1 : formulaire -->
      <form
        v-if="!envoye"
        class="forgot-form"
        @submit.prevent="handleSubmit"
      >
        <AppInput
          id="email"
          v-model="email"
          type="email"
          label="Adresse email *"
          placeholder="nom@domaine.sn"
          required
          :error="erreur"
        />

        <div v-if="erreurGlobale" class="global-error">
          <AlertCircle :size="18" />
          <span>{{ erreurGlobale }}</span>
        </div>

        <AppButton
          type="submit"
          variant="primary"
          size="lg"
          :disabled="loading"
        >
          <template v-if="loading">
            <span class="spinner-small"></span>
            Envoi en cours...
          </template>
          <template v-else>
            Envoyer le lien de réinitialisation
          </template>
        </AppButton>

        <p class="back-to-login">
          Vous vous souvenez de votre mot de passe ?
          <router-link to="/connexion">Se connecter</router-link>
        </p>
      </form>

      <!-- État 2 : message de succès -->
      <div v-else class="success-state">
        <div class="success-icon">
          <CheckCircle :size="40" :stroke-width="2" />
        </div>
        <h3>Email envoyé !</h3>
        <p>
          Si un compte est associé à <strong>{{ email }}</strong>,
          vous recevrez un email avec un lien pour réinitialiser
          votre mot de passe.
        </p>
        <p class="hint">
          Pensez à vérifier vos <strong>spams</strong> si vous ne voyez
          rien dans votre boîte de réception.
        </p>
        <router-link to="/connexion" class="btn-back">
          Retour à la connexion
        </router-link>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'
import { ArrowLeft, Mail, AlertCircle, CheckCircle } from 'lucide-vue-next'

import AppInput from '@/components/AppInput.vue'
import AppButton from '@/components/AppButton.vue'

const email = ref('')
const loading = ref(false)
const erreur = ref('')
const erreurGlobale = ref('')
const envoye = ref(false)

async function handleSubmit() {
  erreur.value = ''
  erreurGlobale.value = ''

  if (!email.value) {
    erreur.value = "L'email est obligatoire."
    return
  }

  loading.value = true
  try {
    await api.post('/auth/mot-de-passe-oublie/', { email: email.value })
    envoye.value = true
  } catch (error) {
    if (error.response?.status === 400 && error.response.data.email) {
      erreur.value = error.response.data.email[0]
    } else {
      erreurGlobale.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.forgot-password-view {
  display: flex;
  align-items: center;
  justify-content: center;

  min-height: 100vh;
  padding: 24px;

  background: linear-gradient(135deg, #f7f9fb 0%, #e6eaf0 100%);
}

.forgot-card {
  max-width: 480px;
  width: 100%;

  padding: 40px 36px;

  background-color: #ffffff;
  border-radius: 16px;
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

/* En-tête */
.page-heading {
  text-align: center;
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

.page-heading h1 {
  margin: 0 0 12px;

  color: var(--bloodsen-dark);
  font-size: 26px;
  font-weight: 700;
}

.page-heading p {
  margin: 0;

  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

/* Formulaire */
.forgot-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

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
}

.back-to-login {
  margin: 8px 0 0;
  text-align: center;
  color: #6b7280;
  font-size: 13px;
}

.back-to-login a {
  color: var(--bloodsen-red);
  font-weight: 600;
  text-decoration: none;
}

.back-to-login a:hover {
  text-decoration: underline;
}

/* Succès */
.success-state {
  text-align: center;
}

.success-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 80px;
  height: 80px;
  margin-bottom: 20px;

  border-radius: 50%;
  background-color: #d1fae5;
  color: #059669;
}

.success-state h3 {
  margin: 0 0 12px;

  color: var(--bloodsen-dark);
  font-size: 22px;
  font-weight: 700;
}

.success-state p {
  margin: 0 0 16px;

  color: #6b7280;
  font-size: 14px;
  line-height: 1.6;
}

.success-state p strong {
  color: var(--bloodsen-dark);
}

.success-state .hint {
  font-size: 13px;
  color: #8a94a3;
}

.btn-back {
  display: inline-block;
  margin-top: 12px;
  padding: 12px 24px;

  background-color: var(--bloodsen-red);
  border-radius: 8px;

  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;

  transition: opacity 0.2s ease;
}

.btn-back:hover {
  opacity: 0.9;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>