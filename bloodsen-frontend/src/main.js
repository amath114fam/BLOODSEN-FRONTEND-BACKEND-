import './style.css'

// Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Vue
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

// ============================================
// DÉMARRAGE DE L'APPLICATION
// ============================================
// On crée l'application Vue, puis on lui greffe :
//   1. Pinia  → pour gérer l'état global (stores)
//   2. Router → pour gérer la navigation entre pages


async function demarrerApplication() {
  const app = createApp(App)

  // On active Pinia AVANT le router (le router peut avoir besoin
  // d'accéder au store auth dans ses guards).
  app.use(createPinia())

  // Rechargement du profil si un token existe
  const auth = useAuthStore()

  if (localStorage.getItem('access_token')) {
    try {
      await auth.fetchMe()
    } catch (e) {
      // Token invalide ou expiré → on nettoie
      auth.logout()
    }
  }

  app.use(router)
  app.mount('#app')
}

demarrerApplication()