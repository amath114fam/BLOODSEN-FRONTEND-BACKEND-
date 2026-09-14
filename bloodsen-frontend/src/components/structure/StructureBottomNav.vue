<template>
  <nav class="bottom-nav">

    <router-link
      to="/structure/tableau-de-bord"
      class="bottom-nav-item"
      active-class="active"
    >
      <span class="bottom-nav-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="3" y="3" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
          <rect x="13" y="3" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
          <rect x="3" y="13" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
          <rect x="13" y="13" width="8" height="8" rx="1.5" stroke="currentColor" stroke-width="2" />
        </svg>
      </span>
      <span class="bottom-nav-label">Accueil</span>
    </router-link>

    <router-link
      to="/structure/demandes"
      class="bottom-nav-item"
      active-class="active"
    >
      <span class="bottom-nav-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M13 2L4 14H12L11 22L20 10H12L13 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <span v-if="demandesCount" class="bottom-nav-badge">{{ demandesCount }}</span>
      </span>
      <span class="bottom-nav-label">Demandes</span>
    </router-link>

    <!-- Bouton central surélevé -->
    <router-link
      to="/structure/demandes/creer"
      class="bottom-nav-cta"
      aria-label="Créer une demande"
    >
      <span class="cta-plus">+</span>
    </router-link>

    <router-link
      to="/structure/donneurs"
      class="bottom-nav-item"
      active-class="active"
    >
      <span class="bottom-nav-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="9" cy="8" r="3" stroke="currentColor" stroke-width="2" />
          <circle cx="17" cy="9" r="2.3" stroke="currentColor" stroke-width="2" />
          <path d="M3 19C3 15.69 5.69 13 9 13C12.31 13 15 15.69 15 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          <path d="M14 14C14.83 13.37 15.86 13 17 13C19.76 13 22 15.24 22 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
      </span>
      <span class="bottom-nav-label">Donneurs</span>
    </router-link>

    <router-link
      to="/structure/participations"
      class="bottom-nav-item"
      active-class="active"
    >
      <span class="bottom-nav-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
          <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </span>
      <span class="bottom-nav-label">Suivi</span>
    </router-link>

  </nav>
</template>

<script setup>
defineProps({
  demandesCount: {
    type: [Number, String],
    default: null,
  },
})
</script>

<style scoped>
.bottom-nav {
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

  background-color: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);

  border-top: 1px solid #e7e9ed;

  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.04);
}

.bottom-nav-item {
  position: relative;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  gap: 3px;

  flex: 1;
  height: 100%;

  color: #8a94a3;
  text-decoration: none;

  transition: color 0.15s ease;
}

.bottom-nav-item.active {
  color: var(--bloodsen-red);
}

.bottom-nav-icon {
  position: relative;

  display: flex;
  align-items: center;
  justify-content: center;
}

.bottom-nav-icon svg {
  width: 22px;
  height: 22px;
}

.bottom-nav-label {
  font-size: 10.5px;
  font-weight: 600;
}

.bottom-nav-badge {
  position: absolute;
  top: -5px;
  right: -9px;

  display: flex;
  align-items: center;
  justify-content: center;

  min-width: 16px;
  height: 16px;
  padding: 0 4px;

  border-radius: 8px;

  background-color: var(--bloodsen-red);
  color: #ffffff;

  font-size: 9.5px;
  font-weight: 700;
}

/* ========================================
   BOUTON CENTRAL (CTA)
======================================== */

.bottom-nav-cta {
  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  width: 52px;
  height: 52px;
  margin-top: -26px;

  border-radius: 50%;

  background-color: var(--bloodsen-red);
  color: #ffffff;

  box-shadow: 0 6px 16px rgba(217, 48, 48, 0.35);

  text-decoration: none;
}

.cta-plus {
  font-size: 26px;
  font-weight: 400;
  line-height: 1;

  margin-top: -2px;
}

/* Visible uniquement sur mobile */

@media (min-width: 769px) {
  .bottom-nav {
    display: none;
  }
}
</style>