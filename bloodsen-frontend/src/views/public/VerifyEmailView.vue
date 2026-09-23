<template>
  <div class="verify-page">

    <div class="verify-card">

      <!-- ==========================================
           ÉTAT 1 : CHARGEMENT
      =========================================== -->
      <div v-if="etat === 'chargement'" class="verify-content">
        <div class="spinner-large"></div>
        <h1>Vérification en cours...</h1>
        <p>Nous validons votre adresse email, un instant.</p>
      </div>

      <!-- ==========================================
           ÉTAT 2 : SUCCÈS
      =========================================== -->
      <div v-else-if="etat === 'succes'" class="verify-content">
        <div class="icon-success">✓</div>
        <h1>Compte activé !</h1>
        <p>
          Votre adresse email a bien été vérifiée.
          Vous allez être redirigé vers votre espace...
        </p>
        <div class="spinner-small"></div>
      </div>

      <!-- ==========================================
           ÉTAT 3 : ERREUR
      =========================================== -->
      <div v-else-if="etat === 'erreur'" class="verify-content">
        <div class="icon-error">✕</div>
        <h1>Vérification impossible</h1>
        <p>{{ messageErreur }}</p>
        <router-link to="/inscription" class="btn-primary">
          Refaire une inscription
        </router-link>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

// États possibles : 'chargement' | 'succes' | 'erreur'
const etat = ref('chargement')
const messageErreur = ref('')

onMounted(async () => {
  // 1. Récupérer le token dans l'URL
  const token = route.query.token

  if (!token) {
    etat.value = 'erreur'
    messageErreur.value = "Aucun token n'a été fourni. Le lien est incomplet."
    return
  }

  // 2. Appeler l'API de vérification
  try {
    await auth.verifierEmail(token)

    // 3. Succès → afficher le message puis rediriger
    etat.value = 'succes'

    setTimeout(() => {
      if (auth.role === 'structure') {
        router.push('/structure/tableau-de-bord')
      } else if (auth.role === 'donneur') {
        router.push('/donneur/tableau-de-bord')
      } else {
        router.push('/')
      }
    }, 2000)

  } catch (error) {
    etat.value = 'erreur'

    if (error.response?.data?.detail) {
      messageErreur.value = error.response.data.detail
    } else {
      messageErreur.value = "Le lien est invalide ou a expiré."
    }
  }
})
</script>

<style scoped>
/* ========================================
   PAGE
======================================== */

.verify-page {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;
  height: 100vh;

  padding: 24px;

  box-sizing: border-box;

  background: linear-gradient(135deg, #f7f9fb 0%, #e6eaf0 100%);
}

/* ========================================
   CARTE CENTRALE
======================================== */

.verify-card {
  max-width: 480px;
  width: 100%;

  padding: 48px 40px;

  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);

  text-align: center;
}

.verify-content h1 {
  margin: 24px 0 16px;

  color: #121a2c;
  font-size: 26px;
  font-weight: 700;
}

.verify-content p {
  margin: 0 0 24px;

  color: #60708a;
  font-size: 15px;
  line-height: 1.6;
}

/* ========================================
   ICÔNES
======================================== */

.icon-success,
.icon-error {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 72px;
  height: 72px;

  border-radius: 50%;

  font-size: 36px;
  font-weight: 700;
}

.icon-success {
  background-color: #d1fae5;
  color: #059669;
}

.icon-error {
  background-color: #fee2e2;
  color: #dc2626;
}

/* ========================================
   SPINNERS
======================================== */

.spinner-large {
  display: inline-block;
  width: 56px;
  height: 56px;

  border: 4px solid #e6eaf0;
  border-top-color: var(--bloodsen-red);
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

.spinner-small {
  display: inline-block;
  width: 20px;
  height: 20px;
  margin-top: 8px;

  border: 2px solid #e6eaf0;
  border-top-color: var(--bloodsen-red);
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ========================================
   BOUTON
======================================== */

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
</style>