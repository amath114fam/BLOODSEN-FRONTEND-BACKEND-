import axios from 'axios'

// ============================================
// CLIENT HTTP CENTRALISÉ
// ============================================
// Toutes les requêtes vers le backend Django passent par ce client.
// Il gère automatiquement :
//   - l'URL de base (http://localhost:8000/api)
//   - l'ajout du token JWT dans les headers
//   - le rafraîchissement automatique du token expiré
// ============================================

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// ============================================
// Intercepteur de REQUÊTE
// ============================================
// Avant chaque requête, on ajoute le token d'accès s'il existe.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// ============================================
// Intercepteur de RÉPONSE
// ============================================
// Si le serveur répond 401 (token expiré), on tente de rafraîchir
// le token une fois. Si ça échoue aussi, on déconnecte l'utilisateur.
let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Si l'erreur n'est pas un 401, ou si c'est déjà un retry, on rejette
    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error)
    }

    // Si on est déjà en train de rafraîchir, on met la requête en file d'attente
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      })
        .then((token) => {
          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        })
        .catch((err) => Promise.reject(err))
    }

    originalRequest._retry = true
    isRefreshing = true

    const refreshToken = localStorage.getItem('refresh_token')

    if (!refreshToken) {
      // Pas de refresh token → déconnexion
      isRefreshing = false
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')

          // on ne redirige QUE si l'erreur ne vient PAS
      // de l'endpoint de connexion lui-même. Sinon, un mauvais mot de passe
      // déclencherait une redirection en boucle.
      const urlAppelee = originalRequest.url || ''

      if (!urlAppelee.includes('/auth/connexion/')) {
        window.location.href = '/connexion'
      }
      return Promise.reject(error)
    }

    try {
      // Appel direct (sans passer par api pour éviter la boucle infinie)
      const { data } = await axios.post(
        'http://localhost:8000/api/auth/connexion/rafraichir/',
        { refresh: refreshToken },
      )

      const newAccess = data.access
      localStorage.setItem('access_token', newAccess)

      processQueue(null, newAccess)

      originalRequest.headers.Authorization = `Bearer ${newAccess}`
      return api(originalRequest)
    } catch (refreshError) {
      processQueue(refreshError, null)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/connexion'
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export default api