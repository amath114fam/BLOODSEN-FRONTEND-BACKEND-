<template>
  <div class="donor-layout">

    <DonorSidebar :pending-count="pendingSollicitationsCount" />

    <div class="donor-main">

      <header class="donor-topbar">

        <div class="donor-topbar-title">
          <h2>Tableau de bord</h2>
        </div>


        <div class="donor-actions">

          <button type="button" class="icon-button" aria-label="Notifications">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 8C18 5.79 16.21 4 14 4H10C7.79 4 6 5.79 6 8C6 12.5 4 14 4 16H20C20 14 18 12.5 18 8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              <path d="M10 20H14" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
            <span v-if="hasNotifications" class="notification-dot"></span>
          </button>

          <router-link to="/donneur/profil" class="user-block">

            <img
              v-if="userAvatarUrl"
              :src="userAvatarUrl"
              :alt="userName"
              class="user-avatar-photo"
            />
            <span v-else class="user-avatar-fallback">{{ userInitials }}</span>

            <div class="user-info">
              <strong>{{ userName }}</strong>
              <span>{{ userRole }}</span>
            </div>

          </router-link>

        </div>

      </header>

      <main class="donor-content">
        <RouterView />
      </main>

    </div>

    <DonorBottomNav :pending-count="pendingSollicitationsCount" />

  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import DonorSidebar from '@/components/donor/DonorSidebar.vue'
import DonorBottomNav from '@/components/donor/DonorBottomNav.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const auth = useAuthStore()

// ==========================================
// INFOS UTILISATEUR (depuis le store auth)
// ==========================================

// ==========================================
// INFOS UTILISATEUR (depuis le store auth)
// ==========================================

// On force le chargement du profil si ce n'est pas déjà fait
onMounted(async () => {
  if (!auth.user) {
    try {
      await auth.fetchMe()
    } catch (e) {
      // Si le fetch échoue, l'intercepteur de api.js gère la redirection
    }
  }
})

// Nom complet de l'utilisateur
const userName = computed(() => {
  const p = auth.user?.profil
  if (!p) return 'Donneur'
  return `${p.prenom || ''} ${p.nom || ''}`.trim()
})

// Rôle affiché ("Donneur A+")
const userRole = computed(() => {
  const p = auth.user?.profil
  if (!p) return 'Donneur'
  return `Donneur ${p.groupe_sanguin || ''}`.trim()
})

// Initiales (pour la fallback sans photo)
const userInitials = computed(() => {
  const p = auth.user?.profil
  if (!p) return '?'
  const prenomInitial = (p.prenom || '')[0] || ''
  const nomInitial = (p.nom || '')[0] || ''
  return `${prenomInitial}${nomInitial}`.toUpperCase() || '?'
})

// Photo de profil (pas encore implémentée côté backend)
const userAvatarUrl = computed(() => null)

// ==========================================
// NOTIFICATIONS / SOLLICITATIONS EN ATTENTE
// ==========================================

const pendingSollicitationsCount = ref(0)

async function chargerCompteurs() {
  try {
    const { data } = await api.get('/sollicitations/', {
      params: { statut: 'en_attente' },
    })
    pendingSollicitationsCount.value = Array.isArray(data) ? data.length : 0
  } catch (e) {
    // Silencieux : si ça échoue, on laisse 0
    pendingSollicitationsCount.value = 0
  }
}

onMounted(chargerCompteurs)

// Vrai si l'utilisateur a au moins une sollicitation en attente
const hasNotifications = computed(() => pendingSollicitationsCount.value > 0)
</script>

<style scoped>

/* ========================================
   LAYOUT GLOBAL
======================================== */

.donor-layout {
  display: flex;

  height: 100vh;
  overflow: hidden;

  background-color: #f6f7f9;
}

.donor-main {
  display: flex;
  flex-direction: column;

  flex: 1;
  min-width: 0;
  height: 100%;

  overflow: hidden;
}

/* ========================================
   TOPBAR
======================================== */

.donor-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 16px;

  padding: 22px 40px;

  background-color: #ffffff;
  border-bottom: 1px solid #e7e9ed;

  flex-shrink: 0;
}

.donor-topbar-title h2 {
  margin: 0;

  color: var(--bloodsen-dark);

  font-size: 30px;
  font-weight: bold;
}

.donor-actions {
  display: flex;
  align-items: center;
  gap: 18px;

  flex-shrink: 0;
}

.icon-button {
  position: relative;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 36px;
  height: 36px;

  border: none;
  border-radius: 8px;

  background-color: transparent;
  color: #4a5568;

  cursor: pointer;
}

.icon-button:hover {
  background-color: #f4f6f8;
}

.icon-button svg {
  width: 19px;
  height: 19px;
}

.notification-dot {
  position: absolute;
  top: 6px;
  right: 7px;

  width: 8px;
  height: 8px;

  border-radius: 50%;

  background-color: var(--bloodsen-red);
  border: 2px solid #ffffff;
}

.user-block {
  display: flex;
  align-items: center;
  gap: 10px;

  padding-left: 4px;

  text-decoration: none;

  flex-shrink: 0;
}

.user-avatar-photo {
  width: 36px;
  height: 36px;

  border-radius: 50%;

  object-fit: cover;

  flex-shrink: 0;
}

.user-avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 36px;
  height: 36px;

  border-radius: 50%;

  background-color: #fdecec;
  color: var(--bloodsen-red);

  font-size: 13px;
  font-weight: 700;

  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  line-height: 1.3;
}

.user-info strong {
  color: var(--bloodsen-dark);
  font-size: 13px;
}

.user-info span {
  color: #6b7280;
  font-size: 12px;
}

/* ========================================
   CONTENU SCROLLABLE
======================================== */

.donor-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;

  padding: 32px 40px 48px;
}

/* ========================================
   TABLETTE
======================================== */

@media (max-width: 992px) {
  .donor-content {
    padding: 24px;
  }

  .donor-topbar {
    padding: 18px 24px;
  }

  .user-info {
    display: none;
  }
}

/* ========================================
   MOBILE
======================================== */

@media (max-width: 768px) {

  .donor-topbar {
    padding: 16px 20px;
    gap: 12px;
  }

  .topbar-search {
    max-width: none;
  }

  .donor-content {
    padding: 20px 16px 96px;
  }

}
</style>