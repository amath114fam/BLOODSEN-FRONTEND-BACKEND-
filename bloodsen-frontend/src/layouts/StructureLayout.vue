<template>
  <div class="structure-layout">

    <StructureSidebar :demandes-count="pendingRequestsCount" />

    <div class="structure-main">

      <header class="structure-topbar">

        <!-- Variante recherche (ex: page Profil) -->
        <AppInput
          v-if="topbarVariant === 'search'"
          id="topbar-search"
          v-model="searchQuery"
          placeholder="Rechercher..."
          class="topbar-search"
        >
          <template #icon>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2" />
              <path d="M21 21L16.5 16.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
          </template>
        </AppInput>

        <!-- Variante par défaut -->
        <div v-else class="structure-identity">
          <h1>{{ structureName }}</h1>
          <p>{{ structureSubtitle }}</p>
        </div>

        <div class="structure-actions">

          <template v-if="topbarVariant !== 'search'">

            <router-link to="/structure/demandes/creer" class="create-request-button">
              <span class="plus-icon">+</span>
              <span class="create-request-label">Créer une demande</span>
            </router-link>

            <button type="button" class="icon-button" aria-label="Notifications">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 8C18 5.79 16.21 4 14 4H10C7.79 4 6 5.79 6 8C6 12.5 4 14 4 16H20C20 14 18 12.5 18 8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M10 20H14" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              </svg>
              <span v-if="hasNotifications" class="notification-dot"></span>
            </button>

          </template>

          <router-link to="/structure/profil" class="user-block">
            <span class="user-avatar">{{ userInitials }}</span>

            <div class="user-info">
              <strong>{{ userName }}</strong>
              <span>{{ userRole }}</span>
            </div>
          </router-link>

        </div>

      </header>

      <main class="structure-content">
        <RouterView />
      </main>

    </div>

    <StructureBottomNav :demandes-count="pendingRequestsCount" />

  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import StructureSidebar from '@/components/structure/StructureSidebar.vue'
import StructureBottomNav from '@/components/structure/StructureBottomNav.vue'
import AppInput from '@/components/AppInput.vue'

defineProps({
  structureName: {
    type: String,
    default: 'CHNU de Fann',
  },
  structureSubtitle: {
    type: String,
    default: 'Centre Hospitalier National Universitaire • Dakar, Sénégal',
  },
  userInitials: {
    type: String,
    default: 'MD',
  },
  userName: {
    type: String,
    default: 'Dr. M. Diop',
  },
  userRole: {
    type: String,
    default: 'Banque de Sang',
  },
  pendingRequestsCount: {
    type: [Number, String],
    default: 6,
  },
  hasNotifications: {
    type: Boolean,
    default: true,
  },
})

const route = useRoute()

// Une route peut déclarer `meta: { topbarVariant: 'search' }`
// pour afficher la barre de recherche à la place de l'identité + actions.
const topbarVariant = computed(() => route.meta.topbarVariant || 'default')

const searchQuery = ref('')
</script>

<style scoped>

/* ========================================
   LAYOUT GLOBAL
======================================== */

.structure-layout {
  display: flex;

  height: 100vh;
  overflow: hidden;

  background-color: #f6f7f9;
}

.structure-main {
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

.structure-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 16px;

  padding: 22px 40px;

  background-color: #ffffff;
  border-bottom: 1px solid #e7e9ed;

  flex-shrink: 0;
}

.structure-identity h1 {
  margin: 0 0 2px;

  color: var(--bloodsen-dark);

  font-size: 20px;
  font-weight: 700;
}

.structure-identity p {
  margin: 0;

  color: #6b7280;

  font-size: 13px;
}

.topbar-search {
  flex: 1;
  max-width: 420px;
  margin: 0;
}

.structure-actions {
  display: flex;
  align-items: center;
  gap: 18px;

  flex-shrink: 0;
}

.create-request-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;

  padding: 10px 18px;

  border-radius: 8px;

  background-color: var(--bloodsen-red);
  color: #ffffff;

  font-size: 14px;
  font-weight: 600;

  text-decoration: none;

  white-space: nowrap;
}

.plus-icon {
  font-size: 16px;
  line-height: 1;
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

  flex-shrink: 0;
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

.user-avatar {
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

.structure-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;

  padding: 32px 40px 48px;
}

/* ========================================
   TABLETTE
======================================== */

@media (max-width: 992px) {
  .structure-content {
    padding: 24px;
  }

  .structure-topbar {
    padding: 18px 24px;
  }

  .user-info {
    display: none;
  }
}

/* ========================================
   MOBILE : sidebar → bottom nav
======================================== */

@media (max-width: 768px) {

  .structure-topbar {
    padding: 16px 20px;
    gap: 10px;
  }

  .structure-identity h1 {
    font-size: 16px;
  }

  .structure-identity p {
    font-size: 11.5px;
  }

  .create-request-button {
    display: none;
  }

  .structure-content {
    padding: 20px 16px 96px;
  }

}

@media (max-width: 380px) {
  .structure-identity p {
    display: none;
  }
}

</style>