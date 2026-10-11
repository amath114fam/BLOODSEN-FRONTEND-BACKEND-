<template>
  <aside class="donor-sidebar">

    <router-link to="/" class="sidebar-logo">
      <img
        src="@/assets/images/logo.png"
        alt="BloodSen"
      />
    </router-link>

    <nav class="sidebar-nav">

      <router-link
        to="/donneur/tableau-de-bord"
        class="nav-item"
        active-class="active"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
            <rect x="13" y="3" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
            <rect x="3" y="13" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
            <rect x="13" y="13" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
          </svg>
        </span>
        Tableau de bord
      </router-link>

      <router-link
        to="/donneur/sollicitations"
        class="nav-item"
        active-class="active"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3C12 3 6 10 6 14.5C6 17.54 8.24 20 12 20C15.76 20 18 17.54 18 14.5C18 10 12 3 12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
          </svg>
        </span>
        Sollicitations
        <span v-if="pendingCount" class="nav-badge">{{ pendingCount }}</span>
      </router-link>

      <router-link
        to="/donneur/participations"
        class="nav-item"
        active-class="active"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
            <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>
        Participations
      </router-link>

    </nav>

    <div class="sidebar-bottom">

      <router-link
        to="/donneur/profil"
        class="nav-item"
        active-class="active"
      >
        <span class="nav-icon">
          <Settings :size="19" :stroke-width="2" />
        </span>
        Profil / Paramètres
      </router-link>
      <button
        type="button"
        class="nav-item logout"
        @click="handleLogout"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 21H5C4.44772 21 4 20.5523 4 20V4C4 3.44772 4.44772 3 5 3H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M16 17L21 12L16 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </span>
        Déconnexion
      </button>

    </div>

  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Settings } from 'lucide-vue-next'

defineProps({
  pendingCount: {
    type: [Number, String],
    default: null,
  },
})

const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
  // 1. Supprime les tokens et vide l'utilisateur du store
  auth.logout()

  // 2. Redirige vers la page de connexion
  router.push('/connexion')
}
</script>

<style scoped>
.donor-sidebar {
  display: flex;
  flex-direction: column;

  width: 260px;
  height: 100vh;

  padding: 24px 16px;
  box-sizing: border-box;

  background-color: #ffffff;
  border-right: 1px solid #e7e9ed;
}

.sidebar-logo {
  display: inline-block;
  margin-bottom: 28px;
  padding-left: 4px;
}

.sidebar-logo img {
  display: block;
  width: 100px;
  height: auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sidebar-bottom {
  display: flex;
  flex-direction: column;
  gap: 4px;

  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #edf0f4;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 11px 12px;

  border: none;
  border-radius: 8px;

  background: transparent;

  color: #4a5568;

  font-family: inherit;
  font-size: 14px;
  font-weight: 500;

  text-decoration: none;
  text-align: left;

  cursor: pointer;

  transition: background-color 0.15s ease, color 0.15s ease;
}

.nav-item:hover {
  background-color: #f4f6f8;
}

.nav-item.active {
  background-color: var(--bloodsen-red);
  color: #ffffff;
}

.nav-item.logout {
  color: var(--bloodsen-red);
}

.nav-item.logout:hover {
  background-color: #fdecec;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.nav-icon svg {
  width: 19px;
  height: 19px;
}

.nav-badge {
  margin-left: auto;

  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-width: 20px;
  height: 20px;
  padding: 0 6px;

  border-radius: 10px;

  background-color: var(--bloodsen-red);
  color: #ffffff;

  font-size: 11px;
  font-weight: 700;
}

.nav-item.active .nav-badge {
  background-color: #ffffff;
  color: var(--bloodsen-red);
}

@media (max-width: 768px) {
  .donor-sidebar {
    display: none;
  }
}
</style>