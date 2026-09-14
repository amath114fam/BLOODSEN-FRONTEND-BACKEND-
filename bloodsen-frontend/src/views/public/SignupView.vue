<template>
  <div class="signup-page">

    <!-- =========================
         PARTIE GAUCHE
    ========================== -->
    <div class="signup-visual">

      <div class="visual-overlay"></div>

      <div class="visual-content">

            <blockquote>
            « Chaque minute compte
            lorsqu'une vie est en jeu. »
            </blockquote>

            <p>
            BloodSen connecte en temps réel les banques de sang et
            hôpitaux de Dakar et des régions avec des donneurs volontaires
            certifiés, réduisant drastiquement les délais critiques
            d'approvisionnement.
            </p>

      </div>

    </div>
    <!-- =========================
         PARTIE DROITE
    ========================== -->

     <div class="signup-form-section">

      <div class="signup-form-container">

        <!-- Logo -->
        <router-link to="/" class="signup-logo">
          <img
            src="@/assets/images/logo.png"
            alt="BloodSen"
          />
        </router-link>


        <!-- Retour accueil -->
        <router-link to="/" class="back-home">
          <span>←</span>
          Retour à l'accueil
        </router-link>


        <!-- Introduction -->
        <div class="signup-heading">

          <h1>Créer votre compte</h1>

          <p>
            Rejoignez BloodSen et contribuez à faciliter le don de sang au
            Sénégal.
          </p>

        </div>


        <!-- Choix du rôle -->
        <div class="role-section">

          <p class="role-label">
            VOUS VOUS INSCRIVEZ EN TANT QUE :
          </p>

          <div class="role-switch">

            <button
              type="button"
              class="role-option"
              :class="{ active: selectedRole === 'donor' }"
              @click="selectedRole = 'donor'"
            >
              <span class="role-icon">♡</span>
              Donneur bénévole
            </button>

            <button
              type="button"
              class="role-option"
              :class="{ active: selectedRole === 'structure' }"
              @click="selectedRole = 'structure'"
            >
              <span class="role-icon">♜</span>
              Structure de santé
            </button>

          </div>

        </div>


        <!-- Formulaire structure -->
        <form
          class="signup-form"
          @submit.prevent="handleSubmit"
        >

          <!-- Nom -->
          <AppInput
            id="structure-name"
            v-model="form.structureName"
            label="Nom de la structure*"
            placeholder="Poste de santé Unité 22"
            required
          />


          <!-- Région -->
          <AppSelect
            id="region"
            v-model="form.region"
            label="Région *"
            required
          >
            <option value="">
              Sélectionnez une région
            </option>

            <option value="Dakar">
              Dakar
            </option>

            <option value="Thiès">
              Thiès
            </option>

            <option value="Saint-Louis">
              Saint-Louis
            </option>

            <option value="Diourbel">
              Diourbel
            </option>

            <option value="Kaolack">
              Kaolack
            </option>
          </AppSelect>


          <!-- Ville -->
          <AppSelect
            id="city"
            v-model="form.city"
            label="Ville *"
            required
          >
            <option value="">
              Sélectionnez une ville
            </option>

            <option value="Dakar">
              Dakar
            </option>

            <option value="Thiès">
              Thiès
            </option>

            <option value="Saint-Louis">
              Saint-Louis
            </option>
          </AppSelect>


          <!-- Quartier -->
          <AppSelect
            id="district"
            v-model="form.district"
            label="Quartier *"
            required
          >
            <option value="">
              Sélectionnez un quartier
            </option>

            <option value="Médina">
              Médina
            </option>

            <option value="Plateau">
              Plateau
            </option>

            <option value="Pikine">
              Pikine
            </option>

            <option value="Parcelles Assainies">
              Parcelles Assainies
            </option>
          </AppSelect>


          <!-- Email -->
          <AppInput
            id="email"
            v-model="form.email"
            label="Adresse email professionnelle ou personnelle *"
            type="email"
            placeholder="nom@domaine.sn"
            required
          />


          <!-- Mot de passe -->
          <div class="password-row">

            <AppInput
              id="password"
              v-model="form.password"
              label="Mot de passe *"
              type="password"
              placeholder="8 caractères minimum"
              required
            />

            <AppInput
              id="password-confirmation"
              v-model="form.passwordConfirmation"
              label="Confirmation du mot de passe *"
              type="password"
              placeholder="Confirmez le mot de passe"
              required
            />

          </div>


          <!-- Conditions -->
          <label class="terms">

            <input
              v-model="form.acceptTerms"
              type="checkbox"
              required
            />

            <span>
              J'accepte sans réserve les
              <a href="#conditions">
                conditions d'utilisation
              </a>
              et la
              <a href="#confidentialite">
                politique de confidentialité
              </a>
              de la plateforme BloodSen relative aux données de santé.
            </span>

          </label>


          <!-- Bouton -->
          <AppButton
            type="submit"
            variant="primary"
            size="lg"
          >
            Créer mon compte
            <span class="button-arrow">→</span>
          </AppButton>


          <!-- Connexion -->
          <p class="login-link">
            Déjà un compte ?

            <router-link to="/connexion">
              Se connecter
            </router-link>
          </p>

        </form>


        <!-- Footer gauche -->
        <div class="signup-footer">

          <p>
            © 2025 BloodSen Sénégal. Initiative civile et médicale.
          </p>

          <div>
            <a href="#assistance">
              Assistance
            </a>

            <a href="#securite">
              Sécurité des données
            </a>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>


<script setup>
import { reactive, ref } from 'vue'

import AppButton from '@/components/AppButton.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'


const selectedRole = ref('structure')


const form = reactive({
  structureName: '',
  region: '',
  city: '',
  district: '',
  email: '',
  password: '',
  passwordConfirmation: '',
  acceptTerms: false,
})


function handleSubmit() {
  if (form.password !== form.passwordConfirmation) {
    alert('Les mots de passe ne correspondent pas.')
    return
  }

  console.log('Données du formulaire :', form)

  // Plus tard :
  // appel API Django/DRF pour créer le compte.
}
</script>


<style scoped>

/* ========================================
   PAGE
======================================== */

.signup-page {
  display: grid;
  grid-template-columns: 50% 50%;

  max-height: 100%;

  background-color: #ffffff;
}


/* ========================================
   FORMULAIRE - GAUCHE
======================================== */

.signup-form-section {
  display: flex;
  justify-content: center;

  background-color: #ffffff;
}

.signup-form-container {
  width: 100%;
  max-width: 640px;

  padding: 32px 64px 24px;
}


/* ========================================
   LOGO
======================================== */

.signup-logo {
  display: inline-block;

  margin-bottom: 24px;
}

.signup-logo img {
  display: block;

  width: 42px;
  height: auto;
}


/* ========================================
   RETOUR
======================================== */

.back-home {
  display: flex;
  align-items: center;
  gap: 8px;

  margin-bottom: 62px;

  color: #60708a;

  font-size: 14px;
  font-weight: 500;

  text-decoration: none;
}

.back-home span {
  font-size: 22px;
  line-height: 1;
}

.back-home:hover {
  color: var(--bloodsen-red);
}


/* ========================================
   TITRE
======================================== */

.signup-heading {
  margin-bottom: 30px;
}

.signup-heading h1 {
  margin: 0 0 8px;

  color: #121a2c;

  font-size: 32px;
  line-height: 1.2;
  font-weight: 700;
}

.signup-heading p {
  max-width: 530px;

  margin: 0;

  color: #60708a;

  font-size: 16px;
  line-height: 1.55;
}


/* ========================================
   RÔLE
======================================== */

.role-section {
  margin-bottom: 30px;
}

.role-label {
  margin: 0 0 10px;

  color: #30415e;

  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.role-switch {
  display: grid;
  grid-template-columns: 1fr 1fr;

  gap: 12px;

  padding: 6px;

  background-color: #f3f6fa;
  border: 1px solid #dce4ee;
  border-radius: 10px;
}

.role-option {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  min-height: 44px;

  padding: 10px 14px;

  border: 1px solid transparent;
  border-radius: 7px;

  background-color: transparent;

  color: #50617b;

  font-family: inherit;
  font-size: 14px;
  font-weight: 600;

  cursor: pointer;

  transition:
    background-color 0.2s ease,
    border-color 0.2s ease,
    color 0.2s ease;
}

.role-option.active {
  background-color: #ffffff;
  border-color: #d8e1ec;
  color: #1d293d;
}

.role-icon {
  color: var(--bloodsen-red);

  font-size: 19px;
  line-height: 1;
}


/* ========================================
   FORMULAIRE
======================================== */

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.password-row {
  display: grid;
  grid-template-columns: 1fr 1fr;

  gap: 16px;
}


/* ========================================
   CONDITIONS
======================================== */

.terms {
  display: flex;
  align-items: flex-start;
  gap: 10px;

  margin-top: 2px;

  color: #50617b;

  font-size: 12px;
  line-height: 1.5;

  cursor: pointer;
}

.terms input {
  flex-shrink: 0;

  width: 14px;
  height: 14px;

  margin-top: 2px;

  accent-color: var(--bloodsen-red);

  cursor: pointer;
}

.terms a {
  color: #25344c;
  font-weight: 600;
  text-decoration: underline;
}


/* ========================================
   BOUTON
======================================== */

.button-arrow {
  margin-left: 8px;

  font-size: 20px;
  line-height: 1;
}


/* ========================================
   CONNEXION
======================================== */

.login-link {
  margin: 10px 0 0;

  color: #60708a;

  font-size: 14px;
  text-align: center;
}

.login-link a {
  margin-left: 4px;

  color: var(--bloodsen-red);

  font-weight: 700;
  text-decoration: none;
}


/* ========================================
   FOOTER GAUCHE
======================================== */

.signup-footer {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;

  gap: 24px;

  margin-top: 32px;
  padding-top: 18px;

  border-top: 1px solid #edf0f4;
}

.signup-footer p {
  max-width: 270px;

  margin: 0;

  color: #8a98ad;

  font-size: 11px;
  line-height: 1.4;
}

.signup-footer div {
  display: flex;
  gap: 20px;
}

.signup-footer a {
  color: #8a98ad;

  font-size: 11px;
  text-decoration: none;
}


/* ========================================
   VISUEL DROITE
======================================== */

.signup-visual {
  position: relative;

  min-height: 100vh;

  background-image: url('@/assets/images/inscription.jpg');
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;

  overflow: hidden;
}

.visual-overlay {
  position: absolute;
  inset: 0;

  background: url("src/assets/images/Inscription.png") 50% 50%;
}

.visual-content {
  position: absolute;

  right: 64px;
  bottom: 72px;
  left: 64px;

  max-width: 580px;

  color: #ffffff;
}

.visual-content blockquote {
  margin: 0 0 18px;

  font-size: 34px;
  line-height: 1.12;
  font-weight: 700;
}

.visual-content p {
  margin: 0;

  color: rgba(255, 255, 255, 0.86);

  font-size: 16px;
  line-height: 1.5;
}


/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1100px) {

  .signup-form-container {
    padding-right: 40px;
    padding-left: 40px;
  }

  .visual-content {
    right: 40px;
    bottom: 50px;
    left: 40px;
  }

  .visual-content blockquote {
    font-size: 30px;
  }

}


@media (max-width: 900px) {

  .signup-page {
    grid-template-columns: 1fr;
  }

  .signup-form-container {
    max-width: 680px;

    padding: 32px 40px 24px;
  }

  .signup-visual {
    min-height: 450px;
  }

}


@media (max-width: 600px) {

  .signup-form-container {
    padding: 24px 20px;
  }

  .back-home {
    margin-bottom: 40px;
  }

  .signup-heading h1 {
    font-size: 28px;
  }

  .role-switch {
    grid-template-columns: 1fr;
  }

  .password-row {
    grid-template-columns: 1fr;
  }

  .signup-footer {
    flex-direction: column;
  }

  .signup-footer div {
    flex-wrap: wrap;
  }

  .signup-visual {
    min-height: 380px;
  }

  .visual-content {
    right: 24px;
    bottom: 32px;
    left: 24px;
  }

  .visual-content blockquote {
    font-size: 27px;
  }

  .visual-content p {
    font-size: 14px;
  }

}
</style>