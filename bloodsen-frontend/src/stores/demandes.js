import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

// ============================================
// STORE DES DEMANDES (côté structure)
// ============================================
// Centralise toutes les actions liées aux demandes :
//   - charger la liste
//   - créer une demande
//   - annuler une demande
//   - charger le détail d'une demande
// ============================================

export const useDemandesStore = defineStore('demandes', () => {

  // ==========================================
  // STATE
  // ==========================================

  // Liste des demandes de la structure connectée
  const demandes = ref([])

  // Indicateur de chargement global
  const loading = ref(false)

  // Message d'erreur global
  const erreur = ref('')

  // ==========================================
  // ACTIONS
  // ==========================================

  /**
   * Charge la liste des demandes de la structure connectée.
   * Met à jour `demandes.value`.
   */
  async function chargerDemandes() {
    loading.value = true
    erreur.value = ''
    try {
      const { data } = await api.get('/demandes/')
      demandes.value = data
      return data
    } catch (e) {
      erreur.value = 'Impossible de charger les demandes.'
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Crée une nouvelle demande.
   * Renvoie la demande créée.
   */
  async function creerDemande(donnees) {
    loading.value = true
    erreur.value = ''
    try {
      const { data } = await api.post('/creer-demandes/', donnees)

      // On ajoute la nouvelle demande en tête de la liste locale
      demandes.value.unshift(data)

      return data
    } catch (e) {
      erreur.value = 'Impossible de créer la demande.'
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Annule une demande existante (par son id).
   * Met à jour la demande dans la liste locale.
   */
  async function annulerDemande(id) {
    loading.value = true
    erreur.value = ''
    try {
      const { data } = await api.post(`/demandes/${id}/annuler/`)

      // On met à jour la demande dans la liste locale
      const index = demandes.value.findIndex(d => d.id === id)
      if (index !== -1) {
        demandes.value[index] = data
      }

      return data
    } catch (e) {
      erreur.value = "Impossible d'annuler la demande."
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Charge le détail d'une demande (par son id).
   * Renvoie la demande complète.
   */
  async function chargerDetail(id) {
    loading.value = true
    erreur.value = ''
    try {
      const { data } = await api.get(`/demandes/${id}/`)
      return data
    } catch (e) {
      erreur.value = 'Impossible de charger la demande.'
      throw e
    } finally {
      loading.value = false
    }
  }

  // ==========================================
  // EXPORT
  // ==========================================

  return {
    // State
    demandes,
    loading,
    erreur,

    // Actions
    chargerDemandes,
    creerDemande,
    annulerDemande,
    chargerDetail,
  }
})