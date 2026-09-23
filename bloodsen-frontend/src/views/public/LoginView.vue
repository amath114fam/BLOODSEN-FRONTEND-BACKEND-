<template>
  <div class="login-page">

        <!-- =========================
         PARTIE DROITE
    ========================== -->

    <div class="login-visual">

      <div class="visual-overlay"></div>

      <div class="visual-content">

        <blockquote>
          « Chaque minute compte
          lorsqu'une vie est en jeu. »
        </blockquote>

        <p>
          BloodSen connecte en temps réel les banques de sang et
          hôpitaux du Sénégal avec des donneurs volontaires certifiés,
          réduisant drastiquement les délais critiques
          d'approvisionnement.
        </p>

      </div>

    </div>


    <!-- =========================
         PARTIE GAUCHE
    ========================== -->

    <div class="login-form-section">

      <div class="login-form-container">

        <!-- Logo + retour accueil -->
        <div class="login-top">

          <router-link to="/" class="back-home">
            <span>←</span>
            Retour à l'accueil
          </router-link>

          <router-link to="/" class="login-logo">
            <img
              src="@/assets/images/logo.png"
              alt="BloodSen"
            />
          </router-link>

        </div>

        <!-- Introduction -->
        <div class="login-heading">

          <h1>Bienvenue sur BloodSen</h1>

          <p>
            Connectez-vous pour accéder à votre espace.
          </p>

        </div>

        <!-- Formulaire -->
        <form
          class="login-form"
          @submit.prevent="handleSubmit"
        >

          <AppInput
            id="email"
            v-model="form.email"
            label="Adresse email *"
            type="email"
            placeholder="nom@domaine.sn"
            required
          >
            <template #icon>
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect
                  x="3"
                  y="5"
                  width="18"
                  height="14"
                  rx="2"
                  stroke="currentColor"
                  stroke-width="2"
                />
                <path
                  d="M3 7L12 13L21 7"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linejoin="round"
                />
              </svg>
            </template>
          </AppInput>

          <AppInput
            id="password"
            v-model="form.password"
            label="Mot de passe *"
            type="password"
            placeholder="Votre mot de passe"
            required
          >
            <template #icon>
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect
                  x="5"
                  y="11"
                  width="14"
                  height="9"
                  rx="2"
                  stroke="currentColor"
                  stroke-width="2"
                />
                <path
                  d="M8 11V8C8 5.79 9.79 4 12 4C14.21 4 16 5.79 16 8V11"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </template>
          </AppInput>
          <div v-if="erreur" class="login-error">
            {{ erreur }}
          </div>
          <div class="login-options">

            <label class="remember-me">
              <input
                v-model="form.rememberMe"
                type="checkbox"
              />
              <span>Se souvenir de moi</span>
            </label>

            <router-link to="/mot-de-passe-oublie" class="forgot-password">
              Mot de passe oublié ?
            </router-link>

          </div>

          <AppButton
            type="submit"
            variant="primary"
            size="lg"
            :disabled="auth.loading"
          >
            <template v-if="auth.loading">
              <span class="spinner"></span>
              Chargement...
            </template>
            <template v-else>
              Se connecter
            </template>
          </AppButton>

          <div class="login-divider"></div>

          <p class="signup-link">
            Vous n'avez pas encore de compte ?

            <router-link to="/inscription">
              S'inscrire
            </router-link>
          </p>

          <div class="secure-access">

            <div class="secure-icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 3L19 6V11C19 15.5 16 19.5 12 21C8 19.5 5 15.5 5 11V6L12 3Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
                <path
                  d="M9 12L11 14L15 10"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>

            <div>
              <strong>Accès réservé aux membres agréés</strong>
              <p>
                Donneurs volontaires et structures hospitalières
                accréditées au Sénégal.
              </p>
            </div>

          </div>

        </form>

      </div>

    </div>

  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import AppButton from '@/components/AppButton.vue'
import AppInput from '@/components/AppInput.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

// Au montage du composant, on vérifie si un email a été mémorisé
onMounted(() => {
  const emailSauvegarde = localStorage.getItem('remembered_email')
  if (emailSauvegarde) {
    form.email = emailSauvegarde
    form.rememberMe = true
  }
})

const form = reactive({
  email: '',
  password: '',
  rememberMe: false,
})

// Message d'erreur affiché à l'utilisateur en cas d'échec de connexion.
const erreur = ref('')

async function handleSubmit() {
  // Réinitialiser l'erreur précédente
  erreur.value = ''

  try {
    // 1. Appel au store qui fait l'appel API et stocke les tokens
    await auth.login(form.email, form.password)

    // 2. Gestion du "Se souvenir de moi" : sauvegarder l'email
    if (form.rememberMe) {
      localStorage.setItem('remembered_email', form.email)
    } else {
      localStorage.removeItem('remembered_email')
    }

    // 3. Redirection selon le rôle
    if (auth.role === 'structure') {
      router.push('/structure/tableau-de-bord')
    } else if (auth.role === 'donneur') {
      router.push('/donneur/tableau-de-bord')
    } else {
      router.push('/')
    }
  } catch (error) {
    // 4. Gestion des erreurs
    if (error.response?.status === 401) {
      erreur.value = 'Email ou mot de passe incorrect.'
    } else if (error.response?.data?.detail) {
      erreur.value = error.response.data.detail
    } else {
      erreur.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  }
}
</script>

<style scoped>

/* ========================================
   PAGE
======================================== */

.login-page {
  display: grid;
  grid-template-columns: 50% 50%;

  width: 100%;
  height: 100vh;

  overflow: hidden;

  background-color: #ffffff;
}
/* ========================================
   FORMULAIRE - GAUCHE
======================================== */

.login-form-section {
  display: flex;
  justify-content: center;

  height: 100%;

  background-color: #ffffff;
}

.login-form-container {
  display: flex;
  flex-direction: column;
  justify-content: center;

  width: 100%;
  max-width: 560px;
  height: 100%;

  box-sizing: border-box;

  padding: 32px 64px;
  overflow-y: auto;
}
/* ========================================
   HAUT DE PAGE
======================================== */

.login-top {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 40px;   /* ← était 60px */
}

.login-logo img {
  display: block;

  width: 42px;
  height: auto;
}

.back-home {
  display: flex;
  align-items: center;
  gap: 8px;

  color: #60708a;

  font-size: 14px;
  font-weight: 500;

  text-decoration: none;
}

.back-home span {
  font-size: 18px;
  line-height: 1;
}

.back-home:hover {
  color: var(--bloodsen-red);
}

/* ========================================
   TITRE
======================================== */

.login-heading {
  margin-bottom: 26px;
}

.login-heading h1 {
  margin: 0 0 8px;

  color: #121a2c;

  font-size: 30px;
  line-height: 1.2;
  font-weight: 700;
}

.login-heading p {
  margin: 0;

  color: #60708a;

  font-size: 16px;
  line-height: 1.5;
}

/* ========================================
   FORMULAIRE
======================================== */

.login-form {
  display: flex;
  flex-direction: column;

  gap: 16px;
}

/* ========================================
   OPTIONS (checkbox + mot de passe oublié)
======================================== */

.login-options {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-top: -4px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;

  color: #50617b;

  font-size: 13px;

  cursor: pointer;
}

.remember-me input {
  width: 14px;
  height: 14px;

  accent-color: var(--bloodsen-red);

  cursor: pointer;
}

.forgot-password {
  color: var(--bloodsen-red);

  font-size: 13px;
  font-weight: 700;

  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}



/* ========================================
   SPINNER DE CHARGEMENT
======================================== */

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;

  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;

  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ========================================
   SÉPARATEUR
======================================== */

.login-divider {
  height: 1px;
  margin: 6px 0;

  background-color: #edf0f4;
}

/* ========================================
   LIEN INSCRIPTION
======================================== */

.signup-link {
  margin: 0;

  color: #60708a;

  font-size: 14px;
  text-align: center;
}

.signup-link a {
  margin-left: 4px;

  color: var(--bloodsen-red);

  font-weight: 700;
  text-decoration: none;
}

.signup-link a:hover {
  text-decoration: underline;
}

/* ========================================
   ENCART SÉCURITÉ
======================================== */

.secure-access {
  display: flex;
  align-items: flex-start;
  gap: 14px;

  margin-top: 6px;
  padding: 18px;

  background-color: #f7f9fb;
  border: 1px solid #e6eaf0;
  border-radius: 8px;
}

.secure-icon {
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 34px;
  height: 34px;

  background-color: #fde8e8;
  border-radius: 50%;

  color: var(--bloodsen-red);
}

.secure-icon svg {
  width: 18px;
  height: 18px;
}

.secure-access strong {
  display: block;
  margin-bottom: 4px;

  color: #202428;

  font-size: 13px;
  font-weight: 700;
}

.secure-access p {
  margin: 0;

  color: #60708a;

  font-size: 12px;
  line-height: 1.5;
}

/* ========================================
   FOOTER GAUCHE
======================================== */

.login-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 24px;

  margin-top: 20px;
  padding-top: 16px;

  border-top: 1px solid #edf0f4;
}

.login-footer p {
  margin: 0;

  color: #8a98ad;

  font-size: 11px;
}

.login-footer div {
  display: flex;
  gap: 16px;
}

.login-footer a {
  color: #8a98ad;

  font-size: 11px;
  text-decoration: none;
}

.login-footer a:hover {
  color: var(--bloodsen-red);
}

/* ========================================
   VISUEL DROITE
======================================== */

/* ========================================
   VISUEL DROITE
======================================== */

.login-visual {
  position: relative;

  display: flex;
  align-items: flex-end;       /* colle le contenu en bas */
  justify-content: center;

  width: 100%;
  height: 100%;

  overflow: hidden;

  background-image: url('@/assets/images/Connexion.png');
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.visual-overlay {
  position: absolute;
  inset: 0;

  background-color: rgba(11, 25, 43, 0.58);
}

.visual-content {
  position: relative;          /* ← plus "absolute" */
  z-index: 1;                  /* passe au-dessus de l'overlay */

  width: 100%;
  max-width: 580px;

  padding: 0 64px 64px;        /* marge interne : 64px en bas et sur les côtés */

  color: #ffffff;
}

.visual-content blockquote {
  margin: 0 0 14px;

  font-size: 28px;
  line-height: 1.15;
  font-weight: 700;
}

.visual-content p {
  margin: 0;

  color: rgba(255, 255, 255, 0.86);

  font-size: 15px;
  line-height: 1.5;
}
/* ========================================
   MESSAGE D'ERREUR
======================================== */

.login-error {
  padding: 12px 16px;

  background-color: #fde8e8;
  border: 1px solid #f5c2c7;
  border-radius: 6px;

  color: #b42318;

  font-size: 14px;
  line-height: 1.4;
}
/* ========================================
   TABLETTE
======================================== */

@media (max-width: 1100px) {

  .login-form-container {
    padding-right: 40px;
    padding-left: 40px;
  }

  .visual-content {
    padding: 0 40px 40px;
  }

  .visual-content blockquote {
    font-size: 24px;
  }

  .visual-content p {
    font-size: 14px;
  }

}
/* ========================================
   ÉCRANS PLUS PETITS
======================================== */

@media (max-width: 900px) {

  .login-page {
    grid-template-columns: 1fr;

    height: auto;
    min-height: 100vh;

    overflow: visible;
  }

  .login-form-container {
    height: auto;

    max-width: 680px;

    padding: 32px 40px 24px;
  }

  .login-visual {
    height: 420px;
    min-height: 420px;
  }

}

/* ========================================
   MOBILE
======================================== */

@media (max-width: 600px) {

  .login-form-container {
    padding: 24px 20px;
  }

  .login-top {
    margin-bottom: 40px;
  }

  .login-heading h1 {
    font-size: 26px;
  }

  .login-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .login-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .login-visual {
    height: 340px;
    min-height: 340px;
  }

  .visual-content {
    padding: 0 24px 32px;
  }

  .visual-content blockquote {
    font-size: 20px;
  }

  .visual-content p {
    font-size: 13px;
  }

}

</style>