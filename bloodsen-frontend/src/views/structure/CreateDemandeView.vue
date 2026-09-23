<template>
  <div class="create-request-view">

    <!-- Fil d'ariane -->
    <div class="breadcrumb">
      <router-link to="/structure/demandes">
        <span class="drop-icon">🩸</span>
        Demandes
      </router-link>
      <span class="separator">/</span>
      <span class="current">Nouvelle demande</span>
    </div>

    <div class="page-heading">
      <h2>Créer une demande de sang</h2>
      <p>
        Renseignez les informations cliniques nécessaires pour mobiliser les
        donneurs compatibles en temps réel.
      </p>
    </div>

    <form class="request-form" @submit.prevent="handleSubmit">

      <!-- ============================
           ÉTAPE 1 — BESOIN DE SANG
      ============================= -->
      <AppCard padding="24px" class="form-section">

        <div class="section-header">
          <span class="step-number">1</span>
          <div>
            <h3>Besoin de sang</h3>
            <p>Définissez le groupe immunohématologique et le degré de criticité.</p>
          </div>
        </div>

        <div class="section-divider"></div>

        <div class="section-grid two-cols">

          <div class="field-block">
            <AppSelect
              id="blood-group"
              v-model="form.groupe_sanguin"
              label="Groupe sanguin recherché *"
              placeholder="Sélectionner un groupe"
              :options="bloodGroupOptions"
              :error="erreursBackend.groupe_sanguin?.[0] || ''"
            />
            <p v-if="selectedBloodGroupHint" class="field-hint">
              {{ selectedBloodGroupHint }}
            </p>
          </div>

          <div class="field-block">
            <AppSelect
              id="urgency-level"
              v-model="form.urgence"
              label="Niveau d'urgence clinique *"
              placeholder="Sélectionner un niveau"
              :options="urgencyOptions"
              :error="erreursBackend.urgence?.[0] || ''"
            />
          </div>

          <AppInput
            id="quantite"
            v-model.number="form.quantite"
            type="number"
            label="Nombre de poches *"
            placeholder="1"
            :min="1"
            required
            :error="erreursBackend.quantite?.[0] || ''"
          />

        </div>

      </AppCard>

      <!-- ============================
           ÉTAPE 2 — DATE LIMITE
      ============================= -->
      <AppCard padding="24px" class="form-section">

        <div class="section-header">
          <span class="step-number">2</span>
          <div>
            <h3>Délai opérationnel</h3>
            <p>Date et heure limites avant lesquelles la demande doit être satisfaite.</p>
          </div>
        </div>

        <div class="section-divider"></div>

        <div class="section-grid two-cols">

          <AppInput
            id="deadline-date"
            v-model="form.deadlineDate"
            type="date"
            label="Date limite *"
            required
            :error="erreursBackend.date_limite?.[0] || ''"
          />

          <AppInput
            id="deadline-time"
            v-model="form.deadlineTime"
            type="time"
            label="Heure limite *"
            required
          />

        </div>

      </AppCard>

      <!-- ============================
           ÉTAPE 3 — MESSAGE
      ============================= -->
      <AppCard padding="24px" class="form-section">

        <div class="section-header">
          <span class="step-number">3</span>
          <div>
            <h3>Message aux donneurs</h3>
            <p>Communication directe transmise aux donneurs sollicités.</p>
          </div>
        </div>

        <div class="section-divider"></div>

        <div class="field-block textarea-block">
          <AppTextarea
            id="alert-message"
            v-model="form.message"
            label="Message notifié aux donneurs"
            :rows="4"
            :maxlength="messageMaxLength"
            :error="erreursBackend.message?.[0] || ''"
          />
          <span class="char-counter">
            {{ form.message.length }} / {{ messageMaxLength }} caractères
          </span>
        </div>

      </AppCard>

      <!-- ============================
           ACTIONS
      ============================= -->
      <div v-if="erreurGlobale" class="form-error">
        {{ erreurGlobale }}
      </div>

      <div class="form-actions">
        <AppButton
          type="button"
          variant="outline"
          :disabled="loading"
          @click="handleCancel"
        >
          Annuler
        </AppButton>

        <AppButton
          type="submit"
          variant="primary"
          :disabled="loading"
        >
          <template v-if="loading">
            <span class="spinner"></span>
            Création...
          </template>
          <template v-else>
            Créer la demande
          </template>
        </AppButton>
      </div>

    </form>

  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDemandesStore } from '@/stores/demandes'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppTextarea from '@/components/AppTextarea.vue'
import AppButton from '@/components/AppButton.vue'

const router = useRouter()
const demandesStore = useDemandesStore()

const messageMaxLength = 280

// ==========================================
// ÉTAT DU FORMULAIRE
// ==========================================

const form = reactive({
  groupe_sanguin: '',
  urgence: 'urgent',
  quantite: 1,
  deadlineDate: '',
  deadlineTime: '16:00',
  message: '',
})

const loading = ref(false)
const erreurGlobale = ref('')
const erreursBackend = ref({})

// ==========================================
// OPTIONS
// ==========================================

const bloodGroupOptions = [
  { value: 'O-', label: 'O- — Universel' },
  { value: 'O+', label: 'O+ — Courant' },
  { value: 'A+', label: 'A+ — Standard' },
  { value: 'A-', label: 'A- — Rare' },
  { value: 'B+', label: 'B+ — Standard' },
  { value: 'B-', label: 'B- — Rare' },
  { value: 'AB+', label: 'AB+ — Receveur' },
  { value: 'AB-', label: 'AB- — Très rare' },
]

const urgencyOptions = [
  { value: 'vitale', label: 'Urgence vitale' },
  { value: 'urgent', label: 'Urgent' },
  { value: 'programme', label: 'Programmé' },
]

// ==========================================
// SOUMISSION
// ==========================================

async function handleSubmit() {
  erreurGlobale.value = ''
  erreursBackend.value = {}

  // 1. Vérifier que la date et l'heure sont remplies
  if (!form.deadlineDate || !form.deadlineTime) {
    erreurGlobale.value = 'La date et l\'heure limites sont obligatoires.'
    return
  }

  // 2. Construire la date_limite au format ISO (YYYY-MM-DDTHH:MM:SS)
  const dateLimiteISO = `${form.deadlineDate}T${form.deadlineTime}:00`

  // 3. Construire les données à envoyer
  const donnees = {
    groupe_sanguin: form.groupe_sanguin,
    urgence: form.urgence,
    quantite: form.quantite,
    date_limite: dateLimiteISO,
    message: form.message,
  }

  // 4. Appel API via le store
  loading.value = true
  try {
    await demandesStore.creerDemande(donnees)
    // Succès → redirection vers la liste des demandes
    router.push('/structure/demandes')
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

function handleCancel() {
  router.push('/structure/demandes')
}
</script>

<style scoped>
.create-request-view {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* ========================================
   FIL D'ARIANE
======================================== */

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;

  margin-bottom: 6px;

  color: #8a94a3;
  font-size: 13px;
}

.breadcrumb a {
  display: flex;
  align-items: center;
  gap: 6px;

  color: #8a94a3;
  text-decoration: none;
}

.breadcrumb a:hover {
  color: var(--bloodsen-red);
}

.breadcrumb .current {
  color: var(--bloodsen-dark);
  font-weight: 600;
}

/* ========================================
   FORMULAIRE
======================================== */

.request-form {
  display: flex;
  flex-direction: column;
  gap: 20px;

  margin-top: 20px;
}

.form-section {
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 28px;
  height: 28px;

  border-radius: 6px;

  background-color: var(--bloodsen-dark);
  color: #ffffff;

  font-size: 13px;
  font-weight: 700;
}

.section-header h3 {
  margin: 0 0 4px;

  color: var(--bloodsen-dark);

  font-size: 17px;
  font-weight: 700;
}

.section-header p {
  margin: 0;

  color: #6b7280;
  font-size: 13px;
}

.section-divider {
  height: 1px;
  margin: 18px 0 22px;

  background-color: #eef0f2;
}

.section-grid {
  display: grid;
  gap: 20px;
}

.section-grid.two-cols {
  grid-template-columns: 1fr 1fr;
}

.field-block {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-hint {
  margin: 0;
  color: #6b7280;
  font-size: 12px;
}

/* ========================================
   BLOC CARTE (placeholder)
======================================== */

.map-block {
  margin-top: 22px;
}

.map-block-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 10px;

  color: var(--bloodsen-dark);
  font-size: 13px;
  font-weight: 600;
}

.map-location-label {
  color: #8a94a3;
  font-weight: 500;
}

.map-placeholder {
  position: relative;

  height: 220px;

  border-radius: 10px;
  overflow: hidden;

  background: linear-gradient(135deg, #cdeef7 0%, #e7f6fb 60%, #f3f6f2 100%);
}

.map-pin {
  position: absolute;
  top: 40%;
  left: 55%;

  font-size: 22px;
  transform: translate(-50%, -50%);
}

.map-address-card {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 12px;

  display: flex;
  align-items: center;
  gap: 10px;

  padding: 12px 14px;

  border-radius: 8px;

  background-color: #ffffff;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
}

.map-pin-small {
  font-size: 16px;
}

.map-address-card strong {
  display: block;
  color: var(--bloodsen-dark);
  font-size: 13px;
}

.map-address-detail {
  display: block;
  margin-top: 2px;

  color: #8a94a3;
  font-size: 12px;
}

.map-active-dot {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-left: auto;

  color: #1e9e5a;
  font-size: 12px;
  font-weight: 600;

  white-space: nowrap;
}

.map-active-dot .dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: #1e9e5a;
}

/* ========================================
   MESSAGE + COMPTEUR
======================================== */

.textarea-block {
  position: relative;
  margin-top: 22px;
}

.char-counter {
  align-self: flex-end;

  color: #8a94a3;
  font-size: 12px;
}

/* ========================================
   ACTIONS
======================================== */

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* ========================================
   RESPONSIVE
======================================== */
/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 900px) {
  .section-grid.two-cols {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {

  .page-heading h2 {
    font-size: 24px;
  }

  .page-heading p {
    font-size: 13px;
  }

  .breadcrumb {
    font-size: 12px;
  }

  .form-section {
    padding: 20px !important;
  }

  .section-header {
    gap: 10px;
  }

  .section-header h3 {
    font-size: 15px;
  }

  .map-placeholder {
    height: 180px;
  }

  .map-address-card {
    flex-wrap: wrap;
    gap: 8px;
  }

  .map-active-dot {
    margin-left: 0;
    width: 100%;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions :deep(button) {
    width: 100%;
  }

}
</style>