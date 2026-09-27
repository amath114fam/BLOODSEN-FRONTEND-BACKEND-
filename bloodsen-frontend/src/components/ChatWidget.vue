<template>
  <!-- ==========================================
       BULLE FLOTTANTE (bouton)
  =========================================== -->
  <button
    v-if="!estOuvert"
    type="button"
    class="chat-bubble"
    aria-label="Ouvrir l'assistant BloodSen"
    @click="ouvrirChat"
  >
    <MessageCircle :size="26" :stroke-width="2" />
    <span class="chat-bubble-pulse"></span>
  </button>

  <!-- ==========================================
       FENÊTRE DE CHAT
  =========================================== -->
  <div v-else class="chat-window">

    <!-- En-tête -->
    <div class="chat-header">
      <div class="chat-header-info">
        <div class="chat-avatar">
          <Bot :size="20" :stroke-width="2" />
        </div>
        <div>
          <strong>Assistant BloodSen</strong>
          <span>Posez vos questions sur le don de sang</span>
        </div>
      </div>
      <button
        type="button"
        class="chat-close"
        aria-label="Fermer le chat"
        @click="fermerChat"
      >
        <X :size="20" :stroke-width="2" />
      </button>
    </div>

    <!-- Zone des messages -->
    <div ref="messagesContainer" class="chat-messages">

      <!-- Message d'accueil (toujours présent) -->
      <div class="message assistant">
        <div class="message-bubble">
          👋 Bonjour ! Je suis l'assistant BloodSen.
          <br><br>
          Posez-moi une question sur le don de sang
          (conditions, durée, groupes sanguins, etc.).
        </div>
      </div>

      <!-- Historique des messages -->
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message"
        :class="msg.role === 'user' ? 'user' : 'assistant'"
      >
        <div class="message-bubble">
          <span v-if="msg.role === 'assistant' && msg.enCours" class="message-loading">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </span>
          <template v-else>
            {{ msg.contenu }}
          </template>
        </div>
        <div v-if="msg.sources && msg.sources.length" class="message-sources">
          <span class="sources-label">Sources :</span>
          <span v-for="(src, i) in msg.sources" :key="i" class="source-tag">
            {{ src }}
          </span>
        </div>
      </div>

    </div>

    <!-- Zone de saisie -->
    <div class="chat-input">
      <input
        v-model="questionActuelle"
        type="text"
        placeholder="Écrivez votre question..."
        :disabled="chargement"
        @keydown.enter.prevent="envoyerQuestion"
      />
      <button
        type="button"
        class="chat-send"
        :disabled="!questionActuelle.trim() || chargement"
        aria-label="Envoyer"
        @click="envoyerQuestion"
      >
        <Send :size="18" :stroke-width="2" />
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import api from '@/services/api'
import { MessageCircle, Bot, X, Send } from 'lucide-vue-next'

// ==========================================
// ÉTAT
// ==========================================

const estOuvert = ref(false)
const questionActuelle = ref('')
const chargement = ref(false)
const messages = ref([])
const messagesContainer = ref(null)

// ==========================================
// OUVERTURE / FERMETURE
// ==========================================

function ouvrirChat() {
  estOuvert.value = true
  scrollEnBas()
}

function fermerChat() {
  estOuvert.value = false
}

// ==========================================
// ENVOI DE LA QUESTION
// ==========================================

async function envoyerQuestion() {
  const question = questionActuelle.value.trim()
  if (!question || chargement.value) return

  // 1. Ajouter le message de l'utilisateur
  messages.value.push({
    role: 'user',
    contenu: question,
  })

  questionActuelle.value = ''
  chargement.value = true
  scrollEnBas()

  // 2. Ajouter un message assistant "en cours" (placeholder)
  const indexAssistant = messages.value.length
  messages.value.push({
    role: 'assistant',
    contenu: '',
    enCours: true,
  })

  scrollEnBas()

  try {
    const { data } = await api.post('/rag/chat/', { question })

    // 3. Remplacer le placeholder par la vraie réponse
    messages.value[indexAssistant] = {
      role: 'assistant',
      contenu: data.reponse,
      sources: data.sources || [],
      enCours: false,
    }
  } catch (error) {
    messages.value[indexAssistant] = {
      role: 'assistant',
      contenu: "Désolé, une erreur est survenue. Veuillez réessayer.",
      enCours: false,
    }
  } finally {
    chargement.value = false
    scrollEnBas()
  }
}

// ==========================================
// SCROLL AUTOMATIQUE
// ==========================================

function scrollEnBas() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// ==========================================
// SCROLL QUAND LE CHAT S'OUVRE
// ==========================================

watch(estOuvert, (valeur) => {
  if (valeur) scrollEnBas()
})
</script>

<style scoped>
/* ==========================================
   BULLE FLOTTANTE
========================================== */

.chat-bubble {
  position: fixed;
  bottom: 24px;
  right: 24px;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 60px;
  height: 60px;

  border: none;
  border-radius: 50%;

  background: linear-gradient(135deg, #c8102e 0%, #8b0000 100%);
  color: #ffffff;

  box-shadow: 0 8px 24px rgba(200, 16, 46, 0.4);

  cursor: pointer;
  z-index: 9998;

  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chat-bubble:hover {
  transform: scale(1.08);
  box-shadow: 0 12px 32px rgba(200, 16, 46, 0.5);
}

.chat-bubble-pulse {
  position: absolute;
  inset: 0;

  border-radius: 50%;
  background-color: rgba(200, 16, 46, 0.4);

  animation: pulse 2s ease-out infinite;
  z-index: -1;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 0.7; }
  100% { transform: scale(1.6); opacity: 0; }
}

/* ==========================================
   FENÊTRE DE CHAT
========================================== */

.chat-window {
  position: fixed;
  bottom: 24px;
  right: 24px;

  display: flex;
  flex-direction: column;

  width: 380px;
  height: 560px;
  max-height: calc(100vh - 48px);

  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);

  overflow: hidden;
  z-index: 9999;

  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* En-tête */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 16px 18px;

  background: linear-gradient(135deg, #c8102e 0%, #8b0000 100%);
  color: #ffffff;
}

.chat-header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 40px;
  height: 40px;

  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
}

.chat-header-info strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
}

.chat-header-info span {
  display: block;
  margin-top: 2px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 11px;
}

.chat-close {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 32px;
  height: 32px;

  border: none;
  border-radius: 8px;

  background: transparent;
  color: #ffffff;

  cursor: pointer;

  transition: background-color 0.15s ease;
}

.chat-close:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

/* Zone des messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;

  padding: 18px;

  background-color: #f7f9fb;

  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
  align-items: flex-end;
}

.message.assistant {
  align-self: flex-start;
  align-items: flex-start;
}

.message-bubble {
  padding: 10px 14px;

  border-radius: 14px;

  font-size: 14px;
  line-height: 1.5;

  word-wrap: break-word;
}

.message.assistant .message-bubble {
  background-color: #ffffff;
  color: #1a1a1a;
  border: 1px solid #e6eaf0;
  border-bottom-left-radius: 4px;
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #c8102e 0%, #8b0000 100%);
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

/* Sources */
.message-sources {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  padding-left: 4px;
}

.sources-label {
  color: #8a94a3;
  font-size: 11px;
  font-style: italic;
}

.source-tag {
  display: inline-block;
  padding: 2px 8px;

  background-color: #fdecec;
  border-radius: 10px;

  color: var(--bloodsen-red);
  font-size: 10.5px;
  font-weight: 600;
}

/* Loading (3 points qui pulsent) */
.message-loading {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.dot {
  display: inline-block;
  width: 6px;
  height: 6px;

  border-radius: 50%;
  background-color: #c8102e;

  animation: bounce 1.2s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.15s; }
.dot:nth-child(3) { animation-delay: 0.3s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
  30% { transform: translateY(-6px); opacity: 1; }
}

/* Zone de saisie */
.chat-input {
  display: flex;
  align-items: center;
  gap: 8px;

  padding: 12px 14px;

  background-color: #ffffff;
  border-top: 1px solid #e6eaf0;
}

.chat-input input {
  flex: 1;

  padding: 10px 14px;

  border: 1px solid #e0e4ea;
  border-radius: 20px;

  background-color: #f7f9fb;
  color: #1a1a1a;

  font-family: inherit;
  font-size: 14px;

  outline: none;
  transition: border-color 0.15s ease;
}

.chat-input input:focus {
  border-color: var(--bloodsen-red);
}

.chat-input input:disabled {
  opacity: 0.6;
}

.chat-send {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 40px;
  height: 40px;

  border: none;
  border-radius: 50%;

  background: linear-gradient(135deg, #c8102e 0%, #8b0000 100%);
  color: #ffffff;

  cursor: pointer;

  transition: opacity 0.15s ease;
}

.chat-send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.chat-send:not(:disabled):hover {
  opacity: 0.9;
}

/* ==========================================
   RESPONSIVE (mobile)
========================================== */

@media (max-width: 480px) {
  .chat-window {
    bottom: 0;
    right: 0;
    left: 0;

    width: 100%;
    height: 100vh;
    max-height: 100vh;

    border-radius: 0;
  }

  .chat-bubble {
    bottom: 20px;
    right: 20px;
  }
}
</style>