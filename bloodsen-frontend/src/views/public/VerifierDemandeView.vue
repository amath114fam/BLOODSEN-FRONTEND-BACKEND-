<template>
  <div class="verifier-demande-view">
    <div class="card">

      <!-- Chargement -->
      <div v-if="etat === 'chargement'" class="state">
        <div class="spinner-large"></div>
        <h1>Vérification en cours...</h1>
      </div>

      <!-- Succès -->
      <!-- Succès -->
      <div v-else-if="etat === 'succes'" class="state">
        <CheckCircle :size="56" :stroke-width="1.5" class="icon success" />
        <h1>Demande vérifiée !</h1>
        <p>
          La recherche de donneurs a démarré.
          <strong>{{ sollicitationsCount }} donneur(s)</strong> ont été sollicités.
        </p>

        <!-- Code de suivi à conserver -->
        <div class="token-box">
          <span class="token-label">Votre code de suivi</span>
          <div class="token-value">{{ tokenAffiche }}</div>
          <button type="button" class="btn-copy" @click="copierToken">
            <template v-if="copie">✓ Copié</template>
            <template v-else>Copier le code</template>
          </button>
          <p class="token-hint">
            Conservez ce code. Il vous permettra de suivre l'état de votre
            demande à tout moment.
          </p>
        </div>

        <div class="actions">
          <router-link to="/suivi-demande" class="btn">
            Suivre ma demande
          </router-link>
          <router-link to="/" class="btn-outline">
            Retour à l'accueil
          </router-link>
        </div>
      </div>

      <!-- Erreur -->
      <div v-else class="state">
        <XCircle :size="56" :stroke-width="1.5" class="icon error" />
        <h1>Lien invalide</h1>
        <p>{{ erreur }}</p>
        <router-link to="/demande-urgente" class="btn">Nouvelle demande</router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { CheckCircle, XCircle } from 'lucide-vue-next'
import api from '@/services/api'

const route = useRoute()
const etat = ref('chargement')
const erreur = ref('')
const sollicitationsCount = ref(0)
const tokenAffiche = ref('')
const copie = ref(false)



onMounted(async () => {
  const token = route.query.token

  if (!token) {
    etat.value = 'erreur'
    erreur.value = "Aucun token fourni. Le lien est incomplet."
    return
  }

  try {
    const { data } = await api.get(`/demande-urgente/verifier/${token}/`)
    sollicitationsCount.value = data.nombre_sollicitations || 0
    tokenAffiche.value = token
    etat.value = 'succes'
  } catch (e) {
    etat.value = 'erreur'
    erreur.value = e.response?.data?.detail || "Le lien est invalide ou déjà utilisé."
  }
})

async function copierToken() {
  try {
    await navigator.clipboard.writeText(tokenAffiche.value)
    copie.value = true
    setTimeout(() => (copie.value = false), 2000)
  } catch (e) {
    // Silencieux
  }
}
</script>

<style scoped>
.verifier-demande-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background-color: #ffffff;
}

.card {
  max-width: 480px;
  width: 100%;
  padding: 48px 32px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.state { text-align: center; }

.state h1 {
  margin: 20px 0 12px;
  color: var(--bloodsen-dark);
  font-size: 24px;
  font-weight: 700;
}

.state p {
  margin: 0 0 12px;
  color: #5f6672;
  font-size: 15px;
  line-height: 1.6;
}

.state p.hint {
  font-size: 13px;
  color: #8a94a3;
}

.icon.success { color: #059669; }
.icon.error { color: #dc2626; }

.spinner-large {
  display: inline-block;
  width: 48px;
  height: 48px;
  border: 4px solid #e6eaf0;
  border-top-color: var(--bloodsen-red);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.btn {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 24px;
  background-color: var(--bloodsen-red);
  border-radius: 8px;
  color: #fff;
  text-decoration: none;
  font-weight: 600;
}
/* ========================================
   CODE DE SUIVI
======================================== */

.token-box {
  margin: 24px 0;
  padding: 20px;
  background-color: #f7f9fb;
  border: 1px dashed #c5cdd8;
  border-radius: 12px;
  text-align: left;
}

.token-label {
  display: block;
  margin-bottom: 8px;
  color: #8a94a3;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.token-value {
  padding: 12px;
  margin-bottom: 12px;
  background-color: #ffffff;
  border-radius: 6px;
  color: var(--bloodsen-dark);
  font-family: 'Courier New', monospace;
  font-size: 13px;
  word-break: break-all;
  user-select: all;
}

.btn-copy {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid var(--bloodsen-red);
  border-radius: 6px;
  background: transparent;
  color: var(--bloodsen-red);
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-copy:hover {
  background-color: #fdecec;
}

.token-hint {
  margin: 12px 0 0;
  color: #8a94a3;
  font-size: 12px;
  line-height: 1.5;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.btn-outline {
  display: inline-block;
  padding: 12px 24px;
  border: 1px solid #e0e4ea;
  border-radius: 8px;
  color: var(--bloodsen-dark);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.15s ease;
}

.btn-outline:hover {
  border-color: var(--bloodsen-red);
  color: var(--bloodsen-red);
}
</style>