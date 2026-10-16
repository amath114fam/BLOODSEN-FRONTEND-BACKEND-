<template>
  <div class="suivi-demande-view">
    <div class="container">

      <router-link to="/" class="back-home">
        <ArrowLeft :size="18" :stroke-width="2" />
        Retour à l'accueil
      </router-link>

      <div class="page-header">
        <span class="page-badge">
          <Search :size="14" />
          SUIVI DE DEMANDE
        </span>
        <h1>Suivre votre demande</h1>
        <p>
          Saisissez le code reçu par email pour consulter l'état
          de votre demande.
        </p>
      </div>

      <!-- Formulaire de saisie -->
      <div v-if="!demande" class="search-card">
        <form @submit.prevent="rechercher">
          <AppInput
            id="token"
            v-model="token"
            label="Code de suivi *"
            placeholder="Collez le code reçu par email"
            required
            :error="erreur"
          />
          <AppButton
            type="submit"
            variant="primary"
            size="lg"
            :disabled="loading"
          >
            <template v-if="loading">
              <span class="spinner"></span>
              Recherche...
            </template>
            <template v-else>
              Rechercher
            </template>
          </AppButton>
        </form>
      </div>

      <!-- Résultat -->
      <div v-else class="result-card">

        <div class="result-header">
          <div class="group-pill">{{ demande.groupe_sanguin }}</div>
          <div>
            <h2>{{ demande.lieu_prise_en_charge }}</h2>
            <p class="location">{{ demande.ville }}</p>
          </div>
          <AppBadge :variant="statutVariant">{{ statutLabel }}</AppBadge>
        </div>

        <div class="stats-grid">
          <div class="stat">
            <span class="stat-label">Donneurs sollicités</span>
            <strong class="stat-value">{{ demande.sollicitations_envoyees }}</strong>
          </div>
          <div class="stat">
            <span class="stat-label">Ont accepté</span>
            <strong class="stat-value success">{{ demande.sollicitations_acceptees }}</strong>
          </div>
          <div class="stat">
            <span class="stat-label">Dons confirmés</span>
            <strong class="stat-value success">{{ demande.participations_confirmees }}</strong>
          </div>
        </div>

        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Patient</span>
            <strong>{{ demande.nom_patient }}</strong>
          </div>
          <div class="info-item">
            <span class="info-label">Quantité demandée</span>
            <strong>{{ demande.quantite }} poche(s)</strong>
          </div>
          <div class="info-item">
            <span class="info-label">Urgence</span>
            <strong>{{ demande.urgence }}</strong>
          </div>
          <div class="info-item">
            <span class="info-label">Demande créée le</span>
            <strong>{{ formaterDate(demande.date_creation) }}</strong>
          </div>
        </div>

        <button type="button" class="btn-reset" @click="reset">
          Suivre une autre demande
        </button>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search, ArrowLeft } from 'lucide-vue-next'
import api from '@/services/api'
import AppInput from '@/components/AppInput.vue'
import AppButton from '@/components/AppButton.vue'
import AppBadge from '@/components/AppBadge.vue'

const token = ref('')
const loading = ref(false)
const erreur = ref('')
const demande = ref(null)

// ==========================================
// RECHERCHE
// ==========================================

async function rechercher() {
  erreur.value = ''
  loading.value = true
  try {
    const { data } = await api.get(`/demande-urgente/${token.value.trim()}/`)
    demande.value = data
  } catch (e) {
    if (e.response?.status === 404) {
      erreur.value = "Code invalide. Vérifiez le code reçu par email."
    } else {
      erreur.value = "Une erreur est survenue."
    }
  } finally {
    loading.value = false
  }
}

function reset() {
  token.value = ''
  demande.value = null
}

// ==========================================
// HELPERS
// ==========================================

const statutLabel = computed(() => {
  const s = demande.value?.statut
  if (s === 'en_verification') return 'En attente de vérification'
  if (s === 'en_cours') return 'En cours'
  if (s === 'terminee') return 'Terminée'
  if (s === 'expiree') return 'Expirée'
  if (s === 'annulee') return 'Annulée'
  return s
})

const statutVariant = computed(() => {
  const s = demande.value?.statut
  if (s === 'en_verification') return 'warning'
  if (s === 'en_cours') return 'info'
  if (s === 'terminee') return 'success'
  if (s === 'annulee' || s === 'expiree') return 'danger'
  return 'default'
})

function formaterDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'long', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}
</script>

<style scoped>
.suivi-demande-view {
  min-height: 100vh;
  padding: 40px 0 60px;
  background-color: #ffffff;
}

/* ========================================
   LIEN RETOUR (simple, sans bouton)
======================================== */

.back-home {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  margin-bottom: 32px;

  color: #60708a;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;

  transition: color 0.15s ease;
}

.back-home:hover {
  color: var(--bloodsen-red);
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
  background-color: #fdecec;
  border-radius: 20px;
  color: var(--bloodsen-red);
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

/* Carte de recherche */
.search-card {
  max-width: 480px;
  margin: 0 auto;
  padding: 32px;
  background-color: #fff;
  border: 1px solid #e6eaf0;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.search-card form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Carte résultat */
.result-card {
  max-width: 700px;
  margin: 0 auto;
  padding: 32px;
  background-color: #fff;
  border: 1px solid #e6eaf0;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eef0f2;
  margin-bottom: 24px;
}

.group-pill {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background-color: #fdecec;
  color: var(--bloodsen-red);
  font-size: 20px;
  font-weight: 800;
}

.result-header h2 {
  margin: 0 0 4px;
  color: var(--bloodsen-dark);
  font-size: 18px;
  font-weight: 700;
}

.result-header .location {
  margin: 0;
  color: #8a94a3;
  font-size: 13px;
}

.result-header > :last-child {
  margin-left: auto;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 16px;
  background-color: #f7f9fb;
  border-radius: 10px;
  text-align: center;
}

.stat-label {
  color: #8a94a3;
  font-size: 12px;
}

.stat-value {
  color: var(--bloodsen-dark);
  font-size: 26px;
  font-weight: 800;
}

.stat-value.success {
  color: #059669;
}

/* Infos */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  color: #8a94a3;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.info-item strong {
  color: var(--bloodsen-dark);
  font-size: 15px;
}

/* Bouton reset */
.btn-reset {
  display: block;
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e4ea;
  border-radius: 8px;
  background: transparent;
  color: var(--bloodsen-dark);
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-reset:hover {
  border-color: var(--bloodsen-red);
  color: var(--bloodsen-red);
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

@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 700px) {
  .page-header h1 { font-size: 28px; }
  .stats-grid { grid-template-columns: 1fr; }
  .info-grid { grid-template-columns: 1fr; }
}
</style>