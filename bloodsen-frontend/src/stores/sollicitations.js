import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

// ============================================
// STORE DES SOLLICITATIONS (côté donneur)
// ============================================
// Centralise toutes les actions liées aux sollicitations
// reçues par un donneur :
//   - charger la liste
//   - accepter une sollicitation
//   - refuser une sollicitation
// ============================================

export const useSollicitationsStore = defineStore('sollicitations', () => {

  // ==========================================
  // STATE
  // ==========================================

  const sollicitations = ref([])
  const loading = ref(false)
  const erreur = ref('')

  // ==========================================
  // ACTIONS
  // ==========================================

  /**
   * Charge toutes les sollicitations du donneur connecté.
   */
  async function charger() {
    loading.value = true
    erreur.value = ''
    try {
      const { data } = await api.get('/sollicitations/')
      sollicitations.value = data
      return data
    } catch (e) {
      erreur.value = 'Impossible de charger vos sollicitations.'
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Accepte une sollicitation (par son id).
   * Met à jour la sollicitation dans la liste locale.
   */

  async function accepter(id) {
    erreur.value = ''
    try {
      await api.post(`/sollicitations/${id}/accepter/`)
      // On recharge toute la liste pour être sûr d'être synchro avec le backend
      await charger()
    } catch (e) {
      erreur.value = "Impossible d'accepter la sollicitation."
      throw e
    }
  }

  /**
   * Refuse une sollicitation (par son id).
   * Recharge la liste complète après succès.
   */
  async function refuser(id) {
    erreur.value = ''
    try {
      await api.post(`/sollicitations/${id}/refuser/`)
      // On recharge toute la liste pour être sûr d'être synchro avec le backend
      await charger()
    } catch (e) {
      erreur.value = 'Impossible de refuser la sollicitation.'
      throw e
    }
  }

  // ==========================================
  // EXPORT
  // ==========================================

  return {
    // State
    sollicitations,
    loading,
    erreur,

    // Actions
    charger,
    accepter,
    refuser,
  }
})