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
              v-model="form.bloodGroup"
              label="Groupe sanguin recherché *"
              placeholder="Sélectionner un groupe"
              :options="bloodGroupOptions"
            />
            <p v-if="selectedBloodGroupHint" class="field-hint">
              {{ selectedBloodGroupHint }}
            </p>
          </div>

          <div class="field-block">
            <AppSelect
              id="urgency-level"
              v-model="form.urgency"
              label="Niveau d'urgence clinique *"
              placeholder="Sélectionner un niveau"
              :options="urgencyOptions"
            />
            <p v-if="selectedUrgencyHint" class="field-hint">
              {{ selectedUrgencyHint }}
            </p>
          </div>

        </div>

      </AppCard>

      <!-- ============================
           ÉTAPE 2 — LIEU DE COLLECTE
      ============================= -->
      <AppCard padding="24px" class="form-section">

        <div class="section-header">
          <span class="step-number">2</span>
          <div>
            <h3>Lieu de collecte &amp; Périmètre</h3>
            <p>Localisation de la banque de sang et ciblage kilométrique des donneurs.</p>
          </div>
        </div>

        <div class="section-divider"></div>

        <div class="section-grid two-cols">

          <AppInput
            id="requesting-facility"
            v-model="form.facility"
            label="Établissement demandeur"
            disabled
            hint="Structure certifiée sous contrat national CNTS"
          >
            <template #icon>
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="5" y="11" width="14" height="9" rx="2" stroke="currentColor" stroke-width="2" />
                <path d="M8 11V8C8 5.79 9.79 4 12 4C14.21 4 16 5.79 16 8V11" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              </svg>
            </template>
          </AppInput>

          <AppSelect
            id="requesting-service"
            v-model="form.service"
            label="Service / Unité de soins *"
            placeholder="Sélectionner un service"
            :options="serviceOptions"
          />

        </div>

        <div class="map-block">

          <div class="map-block-header">
            <span>Point d'orientation &amp; Commune</span>
            <span class="map-location-label">{{ form.commune }}</span>
          </div>

          <!--
            ⚠️ Placeholder visuel pour l'instant (pas de carte interactive branchée).
            À remplacer plus tard par une vraie intégration (Leaflet / Google Maps).
          -->
          <div class="map-placeholder">
            <div class="map-pin">📍</div>

            <div class="map-address-card">
              <span class="map-pin-small">📍</span>
              <div>
                <strong>{{ form.address }}</strong>
                <span class="map-address-detail">{{ form.addressDetail }}</span>
              </div>
              <span class="map-active-dot">
                <span class="dot"></span>
                Point d'accueil actif
              </span>
            </div>
          </div>

        </div>

      </AppCard>

      <!-- ============================
           ÉTAPE 3 — INFOS & MESSAGE
      ============================= -->
      <AppCard padding="24px" class="form-section">

        <div class="section-header">
          <span class="step-number">3</span>
          <div>
            <h3>Informations &amp; Message d'alerte</h3>
            <p>Délai opérationnel et communication directe transmise aux donneurs.</p>
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
          />

          <AppInput
            id="deadline-time"
            v-model="form.deadlineTime"
            type="time"
            label="Heure limite impérative *"
            required
          />

        </div>

        <div class="field-block textarea-block">
          <AppTextarea
            id="alert-message"
            v-model="form.message"
            label="Message notifié aux donneurs"
            :rows="4"
            :maxlength="messageMaxLength"
          />
          <span class="char-counter">
            {{ form.message.length }} / {{ messageMaxLength }} caractères
          </span>
        </div>

      </AppCard>

      <!-- ============================
           ACTIONS
      ============================= -->
      <div class="form-actions">
        <AppButton
          type="button"
          variant="outline"
          @click="handleCancel"
        >
          Annuler
        </AppButton>

        <AppButton
          type="submit"
          variant="primary"
        >
          Créer la demande
        </AppButton>
      </div>

    </form>

  </div>
</template>
<script setup>
import { computed, reactive } from 'vue'
import { useRouter } from 'vue-router'

import AppCard from '@/components/AppCard.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppTextarea from '@/components/AppTextarea.vue'
import AppButton from '@/components/AppButton.vue'

const router = useRouter()

const messageMaxLength = 280

const form = reactive({
  bloodGroup: 'O-',
  urgency: 'vitale',
  facility: 'CHNU de Fann — Dakar',
  service: '',
  commune: 'Dakar-Plateau / Fann-Point E',
  address: 'Avenue Cheikh Anta Diop, Dakar',
  addressDetail: 'Pavillon Maternité • Coordonnées GPS enregistrées',
  deadlineDate: '',
  deadlineTime: '16:00',
  message: '',
})

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

const urgencyDescriptions = {
  vitale: 'Alerte SMS instantanée & push prioritaire direct.',
  urgent: 'Intervention chirurgicale imminente.',
  programme: 'Mobilisation planifiée sous 24 à 72 heures.',
}

const serviceOptions = [
  { value: 'maternite', label: 'Maternité & Néonatologie (Bloc obstétrical)' },
  { value: 'reanimation', label: 'Service Réanimation' },
  { value: 'chirurgie', label: 'Chirurgie Cardiovasculaire' },
  { value: 'urgences', label: "Service d'Urgences" },
]

const selectedBloodGroupHint = computed(() => {
  const option = bloodGroupOptions.find((o) => o.value === form.bloodGroup)
  return option ? `Groupe sélectionné : ${option.label}` : ''
})

const selectedUrgencyHint = computed(() => {
  return urgencyDescriptions[form.urgency] || ''
})

function handleCancel() {
  router.push('/structure/demandes')
}

function handleSubmit() {
  console.log('Nouvelle demande de sang :', form)

  // Plus tard : appel API POST /demandes puis redirection
  // router.push('/structure/demandes')
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