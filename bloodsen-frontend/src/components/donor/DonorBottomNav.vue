<template>
  <nav class="bottom-nav">

    <router-link
      to="/donneur/tableau-de-bord"
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
      to="/donneur/sollicitations"
      class="bottom-nav-item"
      active-class="active"
    >
      <span class="bottom-nav-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 3C12 3 6 10 6 14.5C6 17.54 8.24 20 12 20C15.76 20 18 17.54 18 14.5C18 10 12 3 12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
        </svg>
        <span v-if="pendingCount" class="bottom-nav-badge">{{ pendingCount }}</span>
      </span>
      <span class="bottom-nav-label">Sollic.</span>
    </router-link>

    <router-link
      to="/donneur/participations"
      class="bottom-nav-item"
      active-class="active"
    >
      <span class="bottom-nav-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" stroke-width="2" />
          <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </span>
      <span class="bottom-nav-label">Particip.</span>
    </router-link>

  </nav>
</template>

<script setup>
defineProps({
  pendingCount: {
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

@media (min-width: 769px) {
  .bottom-nav {
    display: none;
  }
}
</style>