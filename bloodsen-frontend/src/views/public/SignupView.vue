<template>
  <div class="signup-page">

    <!-- =========================
         PARTIE GAUCHE (visuel)
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
         PARTIE DROITE (formulaire)
    ========================== -->
    <div class="signup-form-section">
      <div class="signup-form-container">

        <!-- Logo -->
        <router-link to="/" class="signup-logo">
          <img src="@/assets/images/logo.png" alt="BloodSen" />
        </router-link>

        <!-- Retour accueil -->
        <router-link to="/" class="back-home">
          <span>←</span>
          Retour à l'accueil
        </router-link>

        <!-- ==========================================
             ÉCRAN DE SUCCÈS (après inscription)
        =========================================== -->
        <div v-if="inscriptionReussie" class="signup-success">
          <div class="success-icon">✓</div>
          <h1>Inscription réussie !</h1>
          <p>
            Un email de vérification a été envoyé à
            <strong>{{ emailInscrit }}</strong>.
          </p>
          <p>
            Cliquez sur le lien dans cet email pour activer votre compte,
            puis connectez-vous.
          </p>
          <router-link to="/connexion" class="btn-success">
            Aller à la connexion
          </router-link>
        </div>

        <!-- ==========================================
             FORMULAIRE D'INSCRIPTION
        =========================================== -->
        <div v-else>

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
            <p class="role-label">VOUS VOUS INSCRIVEZ EN TANT QUE :</p>
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

          <!-- Message d'erreur global (erreur réseau, 500, etc.) -->
          <div v-if="erreurGlobale" class="signup-error">
            {{ erreurGlobale }}
          </div>

          <!-- ==========================================
               FORMULAIRE DONNEUR
          =========================================== -->
          <form
            v-if="selectedRole === 'donor'"
            class="signup-form"
            @submit.prevent="handleSubmitDonneur"
          >
            <div class="form-row">
              <AppInput
                id="donor-nom"
                v-model="formDonneur.nom"
                label="Nom *"
                placeholder="Diop"
                required
                :error="erreursBackend.nom?.[0] || ''"
              />
              <AppInput
                id="donor-prenom"
                v-model="formDonneur.prenom"
                label="Prénom *"
                placeholder="Amadou"
                required
                :error="erreursBackend.prenom?.[0] || ''"
              />
            </div>

            <div class="form-row">
              <AppInput
                id="donor-email"
                v-model="formDonneur.email"
                label="Adresse email *"
                type="email"
                placeholder="nom@domaine.sn"
                required
                :error="erreursBackend.email?.[0] || ''"
              />
              <AppInput
                id="donor-telephone"
                v-model="formDonneur.telephone"
                label="Téléphone *"
                placeholder="+221 77 123 45 67"
                required
                :error="erreursBackend.telephone?.[0] || ''"
              />
            </div>

            <AppSelect
              id="donor-groupe-sanguin"
              v-model="formDonneur.groupe_sanguin"
              label="Groupe sanguin *"
              placeholder="Sélectionnez votre groupe sanguin"
              :options="groupesSanguinsOptions"
              :error="erreursBackend.groupe_sanguin?.[0] || ''"
              required
            />

            <AppSelect
              id="donor-region"
              v-model="formDonneur.region"
              label="Région *"
              placeholder="Sélectionnez une région"
              :options="regionsOptions"
              :error="erreursBackend.region?.[0] || ''"
              required
            />

            <div class="form-row">
              <AppInput
                id="donor-ville"
                v-model="formDonneur.ville"
                label="Ville *"
                placeholder="Dakar"
                required
                :error="erreursBackend.ville?.[0] || ''"
              />
              <AppInput
                id="donor-quartier"
                v-model="formDonneur.quartier"
                label="Quartier *"
                placeholder="Plateau"
                required
                :error="erreursBackend.quartier?.[0] || ''"
              />
            </div>

            <div class="form-row">
              <AppInput
                id="donor-password"
                v-model="formDonneur.mot_de_passe"
                label="Mot de passe *"
                type="password"
                placeholder="8 caractères minimum"
                required
                :error="erreursBackend.mot_de_passe?.[0] || ''"
              />
              <AppInput
                id="donor-password-confirmation"
                v-model="formDonneur.passwordConfirmation"
                label="Confirmation du mot de passe *"
                type="password"
                placeholder="Confirmez le mot de passe"
                required
                :error="erreurConfirmation"
              />
            </div>

            <label class="terms">
              <input v-model="formDonneur.acceptTerms" type="checkbox" required />
              <span>
                J'accepte sans réserve les
                <a href="#conditions">conditions d'utilisation</a>
                et la
                <a href="#confidentialite">politique de confidentialité</a>
                de la plateforme BloodSen relative aux données de santé.
              </span>
            </label>

            <AppButton
              type="submit"
              variant="primary"
              size="lg"
              :disabled="loading"
            >
              <template v-if="loading">
                <span class="spinner"></span>
                Chargement...
              </template>
              <template v-else>
                Créer mon compte
              </template>
            </AppButton>

            <p class="login-link">
              Déjà un compte ?
              <router-link to="/connexion">Se connecter</router-link>
            </p>
          </form>

          <!-- ==========================================
               FORMULAIRE STRUCTURE
          =========================================== -->
          <form
            v-else
            class="signup-form"
            @submit.prevent="handleSubmitStructure"
          >
            <AppInput
              id="structure-name"
              v-model="formStructure.nom_structure"
              label="Nom de la structure *"
              placeholder="Hôpital Principal de Dakar"
              required
              :error="erreursBackend.nom_structure?.[0] || ''"
            />

            <AppInput
              id="structure-adresse"
              v-model="formStructure.adresse"
              label="Adresse *"
              placeholder="Avenue Nelson Mandela, Dakar"
              required
              :error="erreursBackend.adresse?.[0] || ''"
            />

            <AppInput
              id="structure-email"
              v-model="formStructure.email"
              label="Adresse email professionnelle *"
              type="email"
              placeholder="contact@hopital.sn"
              required
              :error="erreursBackend.email?.[0] || ''"
            />

            <AppSelect
              id="structure-region"
              v-model="formStructure.region"
              label="Région *"
              placeholder="Sélectionnez une région"
              :options="regionsOptions"
              :error="erreursBackend.region?.[0] || ''"
              required
            />

            <div class="form-row">
              <AppInput
                id="structure-ville"
                v-model="formStructure.ville"
                label="Ville *"
                placeholder="Dakar"
                required
                :error="erreursBackend.ville?.[0] || ''"
              />
              <AppInput
                id="structure-quartier"
                v-model="formStructure.quartier"
                label="Quartier *"
                placeholder="Plateau"
                required
                :error="erreursBackend.quartier?.[0] || ''"
              />
            </div>

            <div class="form-row">
              <AppInput
                id="structure-password"
                v-model="formStructure.mot_de_passe"
                label="Mot de passe *"
                type="password"
                placeholder="8 caractères minimum"
                required
                :error="erreursBackend.mot_de_passe?.[0] || ''"
              />
              <AppInput
                id="structure-password-confirmation"
                v-model="formStructure.passwordConfirmation"
                label="Confirmation du mot de passe *"
                type="password"
                placeholder="Confirmez le mot de passe"
                required
                :error="erreurConfirmation"
              />
            </div>

            <label class="terms">
              <input v-model="formStructure.acceptTerms" type="checkbox" required />
              <span>
                J'accepte sans réserve les
                <a href="#conditions">conditions d'utilisation</a>
                et la
                <a href="#confidentialite">politique de confidentialité</a>
                de la plateforme BloodSen relative aux données de santé.
              </span>
            </label>

            <AppButton
              type="submit"
              variant="primary"
              size="lg"
              :disabled="loading"
            >
              <template v-if="loading">
                <span class="spinner"></span>
                Chargement...
              </template>
              <template v-else>
                Créer mon compte
              </template>
            </AppButton>

            <p class="login-link">
              Déjà un compte ?
              <router-link to="/connexion">Se connecter</router-link>
            </p>
          </form>

        </div>

        <!-- Footer gauche -->
        <div class="signup-footer">
          <p>© 2025 BloodSen Sénégal. Initiative civile et médicale.</p>
          <div>
            <a href="#assistance">Assistance</a>
            <a href="#securite">Sécurité des données</a>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

import AppButton from '@/components/AppButton.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import { useAuthStore } from '@/stores/auth'
import { REGIONS_SENEGAL, GROUPES_SANGUINS } from '@/constants/regions'

const router = useRouter()
const auth = useAuthStore()



// Options formatées pour le composant AppSelect
// (qui attend un tableau d'objets { value, label })
const regionsOptions = computed(() =>
  REGIONS_SENEGAL.map(r => ({ value: r, label: r }))
)

const groupesSanguinsOptions = computed(() =>
  GROUPES_SANGUINS.map(g => ({ value: g, label: g }))
)

// ==========================================
// ÉTAT GLOBAL DU FORMULAIRE
// ==========================================

// Rôle sélectionné : 'donor' ou 'structure'
const selectedRole = ref('donor')

// État de chargement pendant l'appel API
const loading = ref(false)

// Vrai quand l'inscription a réussi → affiche l'écran de succès
const inscriptionReussie = ref(false)

// Erreur globale (réseau, 500, etc.)
const erreurGlobale = ref('')

// Erreurs renvoyées par le backend, par champ
// Exemple : { email: ["Cet email est déjà utilisé."], nom: ["..."] }
const erreursBackend = ref({})

// Email utilisé lors de l'inscription réussie (pour l'afficher dans le message)
const emailInscrit = ref('')

// ==========================================
// FORMULAIRE DONNEUR
// ==========================================

const formDonneur = reactive({
  nom: '',
  prenom: '',
  email: '',
  telephone: '',
  groupe_sanguin: '',
  region: '',
  ville: '',
  quartier: '',
  mot_de_passe: '',
  passwordConfirmation: '',
  acceptTerms: false,
})

// ==========================================
// FORMULAIRE STRUCTURE
// ==========================================

const formStructure = reactive({
  nom_structure: '',
  adresse: '',
  email: '',
  region: '',
  ville: '',
  quartier: '',
  mot_de_passe: '',
  passwordConfirmation: '',
  acceptTerms: false,
})

// ==========================================
// VALIDATION DE LA CONFIRMATION
// ==========================================

// Erreur de confirmation de mot de passe (côté frontend uniquement)
const erreurConfirmation = computed(() => {
  const f = selectedRole.value === 'donor' ? formDonneur : formStructure
  if (f.passwordConfirmation && f.mot_de_passe !== f.passwordConfirmation) {
    return 'Les mots de passe ne correspondent pas.'
  }
  return ''
})

// ==========================================
// SOUMISSION DU FORMULAIRE DONNEUR
// ==========================================

async function handleSubmitDonneur() {
  erreurGlobale.value = ''
  erreursBackend.value = {}

  // 1. Vérifier la confirmation du mot de passe
  if (formDonneur.mot_de_passe !== formDonneur.passwordConfirmation) {
    erreurGlobale.value = 'Les mots de passe ne correspondent pas.'
    return
  }

  // 2. Construire les données à envoyer (sans passwordConfirmation ni acceptTerms)
  const donnees = {
    email: formDonneur.email,
    mot_de_passe: formDonneur.mot_de_passe,
    nom: formDonneur.nom,
    prenom: formDonneur.prenom,
    telephone: formDonneur.telephone,
    groupe_sanguin: formDonneur.groupe_sanguin,
    region: formDonneur.region,
    ville: formDonneur.ville,
    quartier: formDonneur.quartier,
  }

  // 3. Appel API
  loading.value = true
  try {
    await auth.inscrireDonneur(donnees)
    emailInscrit.value = donnees.email    
    inscriptionReussie.value = true
  } catch (error) {
    if (error.response?.status === 400) {
      // Erreurs de validation → afficher par champ
      erreursBackend.value = error.response.data
    } else {
      erreurGlobale.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    loading.value = false
  }
}

// ==========================================
// SOUMISSION DU FORMULAIRE STRUCTURE
// ==========================================

async function handleSubmitStructure() {
  erreurGlobale.value = ''
  erreursBackend.value = {}

  // 1. Vérifier la confirmation du mot de passe
  if (formStructure.mot_de_passe !== formStructure.passwordConfirmation) {
    erreurGlobale.value = 'Les mots de passe ne correspondent pas.'
    return
  }

  // 2. Construire les données
  const donnees = {
    email: formStructure.email,
    mot_de_passe: formStructure.mot_de_passe,
    nom_structure: formStructure.nom_structure,
    adresse: formStructure.adresse,
    region: formStructure.region,
    ville: formStructure.ville,
    quartier: formStructure.quartier,
  }

  // 3. Appel API
  loading.value = true
  try {
    await auth.inscrireStructure(donnees)
    emailInscrit.value = donnees.email   
    inscriptionReussie.value = true
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

/* ========================================
   LIGNE DE FORMULAIRE (2 colonnes)
======================================== */

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* ========================================
   MESSAGE D'ERREUR GLOBAL
======================================== */

.signup-error {
  padding: 12px 16px;
  margin-bottom: 16px;

  background-color: #fde8e8;
  border: 1px solid #f5c2c7;
  border-radius: 6px;

  color: #b42318;
  font-size: 14px;
  line-height: 1.4;
}

/* ========================================
   SPINNER
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
   ÉCRAN DE SUCCÈS
======================================== */

.signup-success {
  text-align: center;
  padding: 40px 20px;
}

.success-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 64px;
  height: 64px;
  margin-bottom: 24px;

  background-color: #d1fae5;
  border-radius: 50%;

  color: #059669;
  font-size: 32px;
  font-weight: 700;
}

.signup-success h1 {
  margin: 0 0 16px;

  color: #121a2c;
  font-size: 28px;
  font-weight: 700;
}

.signup-success p {
  margin: 0 0 12px;

  color: #60708a;
  font-size: 15px;
  line-height: 1.6;
}

.signup-success p strong {
  color: #121a2c;
}

.btn-success {
  display: inline-block;
  margin-top: 20px;
  padding: 14px 28px;

  background-color: var(--bloodsen-red);
  border-radius: 8px;

  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;

  transition: opacity 0.2s ease;
}

.btn-success:hover {
  opacity: 0.9;
}

/* ========================================
   RESPONSIVE — FORM ROW
======================================== */

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

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