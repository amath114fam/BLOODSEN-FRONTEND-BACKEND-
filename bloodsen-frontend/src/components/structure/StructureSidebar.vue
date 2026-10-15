<template>
  <aside class="structure-sidebar">

    <router-link to="/" class="sidebar-logo">
      <img
        src="@/assets/images/logo.png"
        alt="BloodSen"
      />
    </router-link>

    <nav class="sidebar-nav">

      <router-link
        to="/structure/tableau-de-bord"
        class="nav-item"
        :class="{ active: isDashboardActive }"
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
        to="/structure/demandes"
        class="nav-item"
        :class="{ active: isRequestsActive }"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M13 2L4 14H12L11 22L20 10H12L13 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>
        Demandes
        <span v-if="demandesCount" class="nav-badge">{{ demandesCount }}</span>
      </router-link>

      <router-link
        to="/structure/donneurs"
        class="nav-item"
        :class="{ active: isDonorsActive }"
      >
        <span class="nav-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="2" />
            <circle cx="17" cy="9" r="2.3" stroke="currentColor" stroke-width="2" />
            <path d="M3 19C3 15.69 5.69 13 9 13C12.31 13 15 15.69 15 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            <path d="M14 14C14.83 13.37 15.86 13 17 13C19.76 13 22 15.24 22 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </span>
        Donneurs
      </router-link>

      <router-link
        to="/structure/participations"
        class="nav-item"
        :class="{ active: isParticipationsActive }"
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
          to="/structure/predictions"
          class="nav-item"
          active-class="active"
        >
          <span class="nav-icon">
            <Sparkles :size="18" :stroke-width="2" />
          </span>
          Prédictions IA
      </router-link>

    </nav>

    <div class="sidebar-bottom">

      <router-link
        to="/structure/profil"
        class="nav-item"
        :class="{ active: isProfileActive }"
      >
        <span class="nav-icon">
          <Settings :size="19" :stroke-width="2" />
        </span>
        Profil / Paramètres
      </router-link>

      <button
        type="button"
        class="nav-item logout"
        @click="ouvrirModalLogout"
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

  <LogoutModal
    :visible="afficherModalLogout"
    :chargement="deconnexionEnCours"
    @annuler="fermerModalLogout"
    @confirmer="confirmerLogout"
  />
  
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Sparkles, Settings } from 'lucide-vue-next'
import LogoutModal from '@/components/LogoutModal.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

// ==========================================
// MODAL DE DÉCONNEXION
// ==========================================

const afficherModalLogout = ref(false)
const deconnexionEnCours = ref(false)

function ouvrirModalLogout() {
  afficherModalLogout.value = true
}

function fermerModalLogout() {
  if (deconnexionEnCours.value) return
  afficherModalLogout.value = false
}

function confirmerLogout() {
  deconnexionEnCours.value = true
  auth.logout()
  router.push('/connexion')
}

// ==========================================
// DÉTECTION DE LA SECTION ACTIVE
// ==========================================

function isSectionActive(basePath) {
  return route.path === basePath || route.path.startsWith(`${basePath}/`)
}

const isDashboardActive = computed(() => isSectionActive('/structure/tableau-de-bord'))
const isRequestsActive = computed(() => isSectionActive('/structure/demandes'))
const isDonorsActive = computed(() => isSectionActive('/structure/donneurs'))
const isParticipationsActive = computed(() => isSectionActive('/structure/participations'))
const isProfileActive = computed(() => isSectionActive('/structure/profil'))

// ==========================================
// PROPS
// ==========================================

defineProps({
  demandesCount: {
    type: [Number, String],
    default: null,
  },
})

</script>

<style scoped>
.structure-sidebar {
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
/* Caché sur mobile, remplacé par StructureBottomNav */
@media (max-width: 768px) {
  .structure-sidebar {
    display: none;
  }
}
</style>