import './style.css'

// Bootstrap
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

// Vue
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// ============================================
// DÉMARRAGE DE L'APPLICATION
// ============================================
// On crée l'application Vue, puis on lui greffe :
//   1. Pinia  → pour gérer l'état global (stores)
//   2. Router → pour gérer la navigation entre pages
// ============================================

const app = createApp(App)

// On active Pinia AVANT le router (le router peut avoir besoin
// d'accéder au store auth dans ses guards).
app.use(createPinia())

app.use(router)

app.mount('#app')