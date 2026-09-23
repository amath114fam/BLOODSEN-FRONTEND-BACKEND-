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

      <router-link
        to="/donneur/historique"
        class="nav-item"
        active-class="active"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3V8H8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M3.5 13C4.4 18 8.8 21.5 13.5 21C18.7 20.5 22.5 15.8 22 10.5C21.5 5.3 16.8 1.5 11.5 2C7.9 2.4 4.9 4.8 3.5 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M12 7V12L15.5 14.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>
        Historique
      </router-link>

    </nav>

    <div class="sidebar-bottom">

      <router-link
        to="/donneur/profil"
        class="nav-item"
        active-class="active"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" />
            <path d="M19.4 15C19.13 15.6 19.2 16.3 19.6 16.83L19.66 16.91C19.99 17.33 20 17.92 19.66 18.34C19.33 18.75 18.76 18.87 18.29 18.62L18.2 18.57C17.62 18.25 16.92 18.28 16.36 18.65C15.81 19.01 15.48 19.63 15.5 20.29V20.4C15.51 20.99 15.05 21.47 14.47 21.48H14.4C13.83 21.5 13.34 21.05 13.31 20.47V20.36C13.29 19.7 12.9 19.11 12.31 18.83C11.71 18.53 11 18.6 10.47 19L10.4 19.06C9.93 19.4 9.28 19.33 8.9 18.9C8.53 18.48 8.53 17.85 8.9 17.43L8.96 17.34C9.33 16.87 9.4 16.24 9.15 15.7C8.9 15.16 8.38 14.79 7.79 14.71H7.68C7.09 14.65 6.66 14.13 6.72 13.54C6.78 12.97 7.27 12.53 7.85 12.54H7.96C8.62 12.53 9.22 12.16 9.51 11.57C9.8 10.98 9.75 10.27 9.37 9.73L9.31 9.65C8.96 9.19 9.04 8.55 9.46 8.19C9.87 7.83 10.49 7.83 10.9 8.19L10.98 8.25C11.46 8.62 12.09 8.68 12.62 8.41C13.16 8.14 13.51 7.61 13.53 7.01V6.9C13.5 6.32 13.94 5.83 14.51 5.79C15.09 5.75 15.6 6.17 15.66 6.75V6.86C15.68 7.52 16.07 8.11 16.66 8.39C17.26 8.68 17.97 8.61 18.5 8.21L18.57 8.16C19.03 7.81 19.68 7.87 20.06 8.29C20.44 8.71 20.44 9.35 20.06 9.77L20 9.86C19.62 10.32 19.55 10.96 19.79 11.5C20.05 12.03 20.56 12.4 21.16 12.48H21.27C21.85 12.53 22.28 13.05 22.22 13.63C22.17 14.2 21.68 14.65 21.1 14.63H20.99C20.33 14.65 19.73 15.03 19.44 15.62" stroke="currentColor" stroke-width="1.3" />
          </svg>
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