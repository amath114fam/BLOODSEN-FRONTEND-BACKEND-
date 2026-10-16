<template>
  <nav class="public-bottom-nav">

    <!-- Accueil -->
    <router-link
      to="/"
      class="nav-item"
      :class="{ active: route.path === '/' }"
      aria-label="Accueil"
      @click="fermer"
    >
      <Home :size="24" :stroke-width="2" />
    </router-link>

    <!-- Menu -->
    <button
      type="button"
      class="nav-item"
      :class="{ active: menuOuvert }"
      aria-label="Menu"
      @click="toggleMenu"
    >
      <!-- Icône custom : 3 points + 3 lignes -->
      <svg
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        class="custom-menu-icon"
      >
        <circle cx="3.5" cy="6" r="1.8" fill="currentColor" />
        <rect x="8" y="5" width="14" height="2" rx="1" fill="currentColor" />

        <circle cx="3.5" cy="12" r="1.8" fill="currentColor" />
        <rect x="8" y="11" width="14" height="2" rx="1" fill="currentColor" />

        <circle cx="3.5" cy="18" r="1.8" fill="currentColor" />
        <rect x="8" y="17" width="14" height="2" rx="1" fill="currentColor" />
      </svg>
    </button>

    <!-- Connexion -->
    <router-link
      to="/connexion"
      class="nav-item"
      :class="{ active: route.path === '/connexion' }"
      aria-label="Connexion"
      @click="fermer"
    >
      <LogIn :size="24" :stroke-width="2" />
    </router-link>

    <!-- Créer un compte -->
    <router-link
      to="/inscription"
      class="nav-item nav-item-accent"
      :class="{ active: route.path === '/inscription' }"
      aria-label="Créer un compte"
      @click="fermer"
    >
      <UserPlus :size="24" :stroke-width="2" />
    </router-link>

  </nav>

  <!-- Panneau qui descend quand on clique sur Menu -->
  <transition name="slide-up">
    <div v-if="menuOuvert" class="menu-panel">

      <div class="menu-header">
        <h3>Menu</h3>
        <button type="button" class="menu-close" @click="fermer">
          <X :size="20" :stroke-width="2" />
        </button>
      </div>

      <nav class="menu-links">
        <router-link to="/demande-urgente" class="menu-link urgent" @click="fermer">
          <AlertCircle :size="18" :stroke-width="2" />
          Demande urgente
        </router-link>

        <a href="/#comment-ca-marche" class="menu-link" @click="fermer">
          <Info :size="18" :stroke-width="2" />
          Comment ça marche
        </a>

        <a href="/#pourquoi-donner" class="menu-link" @click="fermer">
          <Heart :size="18" :stroke-width="2" />
          Pourquoi donner
        </a>

        <a href="/#contact" class="menu-link" @click="fermer">
          <Mail :size="18" :stroke-width="2" />
          Contact
        </a>
      </nav>

    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  Home, LogIn, UserPlus,
  X, AlertCircle, Info, Heart, Mail,
} from 'lucide-vue-next'

const route = useRoute()

const menuOuvert = ref(false)

function toggleMenu() {
  menuOuvert.value = !menuOuvert.value
}

function fermer() {
  menuOuvert.value = false
}
</script>

<style scoped>
/* ========================================
   BOTTOM NAV
======================================== */

.public-bottom-nav {
  position: fixed;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 100;

  display: flex;
  align-items: center;
  justify-content: space-around;

  height: 64px;
  padding-bottom: env(safe-area-inset-bottom, 0px);

  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);

  border-top: 1px solid #e7e9ed;

  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.04);
}

.nav-item {
  display: flex;
  align-items: center;
  justify-content: center;

  flex: 1;
  height: 100%;

  border: none;
  background: transparent;

  color: #8a94a3;
  text-decoration: none;

  cursor: pointer;

  transition: color 0.15s ease;
}

.nav-item.active {
  color: var(--bloodsen-red);
}

.nav-item-accent {
  color: var(--bloodsen-red);
}

.custom-menu-icon {
  display: block;
}

/* ========================================
   PANNEAU MENU (glisse vers le haut)
======================================== */

.menu-panel {
  position: fixed;
  right: 0;
  bottom: 64px;
  left: 0;
  z-index: 99;

  background-color: #ffffff;
  border-top: 1px solid #e7e9ed;
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;

  box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.08);
}

.menu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 16px 20px;
  border-bottom: 1px solid #eef0f2;
}

.menu-header h3 {
  margin: 0;
  color: var(--bloodsen-dark);
  font-size: 15px;
  font-weight: 700;
}

.menu-close {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 32px;
  height: 32px;

  border: none;
  border-radius: 8px;

  background: transparent;
  color: #6b7280;

  cursor: pointer;
}

.menu-close:hover {
  background-color: #f4f6f8;
}

.menu-links {
  display: flex;
  flex-direction: column;

  padding: 8px 0;
}

.menu-link {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 14px 20px;

  color: #4a5568;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;

  transition: background-color 0.15s ease;
}

.menu-link:hover {
  background-color: #f7f9fb;
}

.menu-link.urgent {
  color: var(--bloodsen-red);
  font-weight: 700;
}

/* ========================================
   TRANSITION
======================================== */

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(20px);
  opacity: 0;
}

/* ========================================
   CACHÉ SUR DESKTOP
======================================== */

@media (min-width: 769px) {
  .public-bottom-nav {
    display: none;
  }
}
</style>