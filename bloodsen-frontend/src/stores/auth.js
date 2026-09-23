import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

// ============================================
// STORE D'AUTHENTIFICATION
// ============================================
// Gère l'état global de l'authentification :
//   - l'utilisateur connecté (profil, rôle, infos)
//   - les actions de connexion/déconnexion
//   - l'inscription
//   - la vérification d'email
// ============================================

export const useAuthStore = defineStore('auth', () => {

  // ==========================================
  // STATE (données réactives)
  // ==========================================

  // L'utilisateur connecté. Contient :
  //   { id, email, role, profil: {...} }
  // Vaut null si personne n'est connecté.
  const user = ref(null)

  // Indicateur de chargement (utile pour désactiver les boutons).
  const loading = ref(false)

  // ==========================================
  // GETTERS (valeurs calculées)
  // ==========================================

  // Vrai si un access token existe dans le localStorage.
  const isAuthenticated = computed(() => {
    return !!user.value && !!localStorage.getItem('access_token')
  })

  // Rôle de l'utilisateur connecté ('donneur', 'structure', 'admin', ou null).
  const role = computed(() => user.value?.role || null)

  // Initiales de l'utilisateur (pour l'affichage dans la topbar).
  // Ex : "Amadou Diop" → "AD"
  const userInitiales = computed(() => {
    if (!user.value?.profil) return '?'
    const nom = user.value.profil.nom || user.value.profil.nom_structure || ''
    const prenom = user.value.profil.prenom || ''
    const p = (prenom[0] || '').toUpperCase()
    const n = (nom[0] || '').toUpperCase()
    return `${p}${n}` || '?'
  })

  // ==========================================
  // ACTIONS (méthodes)
  // ==========================================

  /**
   * Connexion : envoie email + password, stocke les tokens,
   * puis récupère les infos de l'utilisateur via /moi/.
   */
  async function login(email, password) {
    loading.value = true
    try {
      // 1. Appel à /connexion/ pour obtenir access + refresh
      const { data } = await api.post('/auth/connexion/', { email, password })

      // 2. Stocker les tokens dans le localStorage
      //    (api.js les utilisera automatiquement pour les prochaines requêtes)
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // 3. Récupérer les infos complètes de l'utilisateur
      await fetchMe()

      return { success: true }
    } catch (error) {
      // En cas d'erreur, on nettoie tout et on propage l'erreur
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      user.value = null
      throw error
    } finally {
      loading.value = false
    }
  }

  /**
   * Récupère les infos de l'utilisateur connecté via /moi/.
   */
  async function fetchMe() {
    const { data } = await api.get('/auth/moi/')
    user.value = data
    return data
  }

  /**
   * Déconnexion : supprime les tokens et vide l'utilisateur.
   */
  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
  }

  /**
   * Inscription d'un donneur.
   * Ne connecte PAS l'utilisateur (il doit d'abord vérifier son email).
   */
  async function inscrireDonneur(formData) {
    loading.value = true
    try {
      const { data } = await api.post('/auth/inscription/donneur/', formData)
      return data
    } finally {
      loading.value = false
    }
  }

  /**
   * Inscription d'une structure de santé.
   */
  async function inscrireStructure(formData) {
    loading.value = true
    try {
      const { data } = await api.post('/auth/inscription/structure/', formData)
      return data
    } finally {
      loading.value = false
    }
  }

  /**
   * Vérifie un token d'email reçu par lien.
   * Si le token est valide, le backend crée le compte et renvoie
   * les tokens JWT (l'utilisateur est alors connecté automatiquement).
   */
  async function verifierEmail(token) {
    loading.value = true
    try {
      const { data } = await api.post('/auth/verifier-email/', { token })

      // Le backend renvoie access + refresh : on les stocke
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // Puis on récupère les infos de l'utilisateur
      await fetchMe()

      return data
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // EXPORT : ce que le store expose au reste de l'app
  // ==========================================

  return {
    // State
    user,
    loading,

    // Getters
    isAuthenticated,
    role,
    userInitiales,

    // Actions
    login,
    logout,
    fetchMe,
    inscrireDonneur,
    inscrireStructure,
    verifierEmail,
  }
})