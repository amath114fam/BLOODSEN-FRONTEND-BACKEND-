<template>
  <div class="demande-urgente-view">
    <div class="container">

      <div class="page-header">
        <span class="page-badge">
          <AlertCircle :size="14" />
          URGENCE VITALE
        </span>
        <h1>Demande urgente de sang</h1>
        <p>
          Un proche a besoin de sang ? Remplissez ce formulaire pour
          mobiliser les donneurs compatibles autour de vous.
          <strong>Aucun compte n'est requis.</strong>
        </p>
      </div>

      <!-- Message succès -->
      <div v-if="succes" class="success-state">
        <CheckCircle :size="48" :stroke-width="1.5" />
        <h2>Demande enregistrée</h2>
        <p>
          Un email de vérification a été envoyé à
          <strong>{{ form.email_demandeur }}</strong>.
        </p>
        <p>
          Cliquez sur le lien reçu pour lancer la recherche de donneurs.
          Vous pourrez ensuite suivre votre demande avec ce même lien.
        </p>
        <router-link to="/" class="btn-back">Retour à l'accueil</router-link>
      </div>

      <!-- Formulaire -->
      <form v-else class="demande-form" @submit.prevent="soumettre">

        <AppCard padding="28px">
          <h2 class="section-title">1. Besoin de sang</h2>

          <div class="form-row">
            <AppSelect
              id="groupe-sanguin"
              v-model="form.groupe_sanguin"
              label="Groupe sanguin recherché *"
              placeholder="Sélectionnez"
              :options="groupesOptions"
              :error="erreurs.groupe_sanguin?.[0]"
              required
            />
            <AppInput
              id="quantite"
              v-model.number="form.quantite"
              type="number"
              label="Nombre de poches *"
              :min="1"
              :error="erreurs.quantite?.[0]"
              required
            />
          </div>

          <AppSelect
            id="urgence"
            v-model="form.urgence"
            label="Niveau d'urgence *"
            placeholder="Sélectionnez"
            :options="urgencesOptions"
            :error="erreurs.urgence?.[0]"
            required
          />
        </AppCard>

        <AppCard padding="28px">
          <h2 class="section-title">2. Localisation</h2>

          <LocationSelector
            :region-error="erreurs.region?.[0]"
            :ville-error="erreurs.ville_id?.[0]"
            @update:region="form.region = $event"
            @update:ville="form.ville_id = $event"
            @update:coords="onCoords"
          />
        </AppCard>

        <AppCard padding="28px">
          <h2 class="section-title">3. Patient concerné</h2>

          <div class="form-row">
            <AppInput
              id="nom-patient"
              v-model="form.nom_patient"
              label="Nom du patient *"
              placeholder="Ex: Moussa Ndiaye"
              :error="erreurs.nom_patient?.[0]"
              required
            />
            <AppInput
              id="lieu"
              v-model="form.lieu_prise_en_charge"
              label="Hôpital / Structure *"
              placeholder="Ex: Hôpital Fann"
              :error="erreurs.lieu_prise_en_charge?.[0]"
              required
            />
          </div>

          <AppTextarea
            id="message"
            v-model="form.message"
            label="Message aux donneurs (optionnel)"
            placeholder="Précisez tout ce qui peut aider les donneurs..."
            :rows="3"
            :error="erreurs.message?.[0]"
          />
        </AppCard>

        <AppCard padding="28px">
          <h2 class="section-title">4. Vos coordonnées</h2>

          <AppInput
            id="nom-demandeur"
            v-model="form.nom_demandeur"
            label="Votre nom complet *"
            :error="erreurs.nom_demandeur?.[0]"
            required
          />

          <div class="form-row">
            <AppInput
              id="telephone"
              v-model="form.telephone_demandeur"
              label="Téléphone *"
              placeholder="+221 77 123 45 67"
              :error="erreurs.telephone_demandeur?.[0]"
              required
            />
            <AppInput
              id="email"
              v-model="form.email_demandeur"
              type="email"
              label="Email *"
              placeholder="vous@exemple.com"
              :error="erreurs.email_demandeur?.[0]"
              required
            />
          </div>
        </AppCard>

        <div v-if="erreurGlobale" class="form-error">
          {{ erreurGlobale }}
        </div>

        <div class="actions">
          <AppButton
            type="submit"
            variant="primary"
            size="lg"
            :disabled="loading"
          >
            <template v-if="loading">
              <span class="spinner"></span>
              Envoi...
            </template>
            <template v-else>
              Envoyer la demande
            </template>
          </AppButton>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { AlertCircle, CheckCircle } from 'lucide-vue-next'
import api from '@/services/api'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppTextarea from '@/components/AppTextarea.vue'
import AppButton from '@/components/AppButton.vue'
import LocationSelector from '@/components/LocationSelector.vue'
import { GROUPES_SANGUINS } from '@/constants/regions'

// ==========================================
// ÉTAT
// ==========================================

const form = reactive({
  groupe_sanguin: '',
  quantite: 1,
  urgence: 'vitale',
  region: null,
  ville_id: null,
  latitude_urgence: null,
  longitude_urgence: null,
  nom_patient: '',
  lieu_prise_en_charge: '',
  message: '',
  nom_demandeur: '',
  telephone_demandeur: '',
  email_demandeur: '',
})

const loading = ref(false)
const succes = ref(false)
const erreurGlobale = ref('')
const erreurs = ref({})

// ==========================================
// OPTIONS
// ==========================================

const groupesOptions = computed(() =>
  GROUPES_SANGUINS.map(g => ({ value: g, label: g }))
)

const urgencesOptions = [
  { value: 'vitale', label: 'Urgence vitale' },
  { value: 'urgent', label: 'Urgent' },
  { value: 'programme', label: 'Programmé' },
]

// ==========================================
// COORDONNÉES GPS
// ==========================================

function onCoords({ latitude, longitude }) {
  form.latitude_urgence = latitude
  form.longitude_urgence = longitude
}

// ==========================================
// SOUMISSION
// ==========================================

async function soumettre() {
  erreurGlobale.value = ''
  erreurs.value = {}

  if (!form.ville_id) {
    erreurGlobale.value = 'Veuillez sélectionner une ville.'
    return
  }

  loading.value = true
  try {
    await api.post('/demande-urgente/', {
      groupe_sanguin: form.groupe_sanguin,
      quantite: form.quantite,
      urgence: form.urgence,
      ville_id: form.ville_id,
      latitude_urgence: form.latitude_urgence,
      longitude_urgence: form.longitude_urgence,
      nom_patient: form.nom_patient,
      lieu_prise_en_charge: form.lieu_prise_en_charge,
      message: form.message,
      nom_demandeur: form.nom_demandeur,
      telephone_demandeur: form.telephone_demandeur,
      email_demandeur: form.email_demandeur,
    })
    succes.value = true
  } catch (error) {
    if (error.response?.status === 400) {
      erreurs.value = error.response.data
    } else {
      erreurGlobale.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.demande-urgente-view {
  min-height: 100vh;
  padding: 60px 0;
  background: linear-gradient(135deg, #fef2f2 0%, #fff1f2 100%);
}

.page-header {
  max-width: 700px;
  margin: 0 auto 40px;
  text-align: center;
}

.page-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  margin-bottom: 16px;
  background-color: #fee2e2;
  border-radius: 20px;
  color: #dc2626;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
}

.page-header h1 {
  margin: 0 0 12px;
  color: var(--bloodsen-dark);
  font-size: 38px;
  font-weight: 800;
}

.page-header p {
  margin: 0;
  color: #5f6672;
  font-size: 16px;
  line-height: 1.6;
}

.demande-form {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  margin: 0 0 16px;
  color: var(--bloodsen-dark);
  font-size: 17px;
  font-weight: 700;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.form-error {
  padding: 14px 18px;
  background-color: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #b42318;
  font-size: 14px;
}

.actions {
  display: flex;
  justify-content: center;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Succès */
.success-state {
  max-width: 600px;
  margin: 60px auto;
  padding: 48px 32px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  text-align: center;
  color: #059669;
}

.success-state h2 {
  margin: 16px 0 12px;
  color: var(--bloodsen-dark);
  font-size: 26px;
}

.success-state p {
  margin: 0 0 12px;
  color: #5f6672;
  font-size: 15px;
  line-height: 1.6;
}

.btn-back {
  display: inline-block;
  margin-top: 16px;
  padding: 12px 24px;
  background-color: var(--bloodsen-red);
  border-radius: 8px;
  color: #fff;
  text-decoration: none;
  font-weight: 600;
}

@media (max-width: 700px) {
  .page-header h1 { font-size: 28px; }
  .form-row { grid-template-columns: 1fr; }
}
</style>