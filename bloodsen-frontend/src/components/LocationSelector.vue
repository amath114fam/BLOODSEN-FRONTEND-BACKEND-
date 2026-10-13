<template>
  <div class="location-selector">

    <!-- Select Région -->
    <AppSelect
      id="region-select"
      :model-value="regionId"
      label="Région *"
      placeholder="Sélectionnez une région"
      :options="regionsOptions"
      :error="regionError"
      @update:model-value="onRegionChange"
    />

    <!-- Select Ville (dépend de la région) -->
    <AppSelect
      id="ville-select"
      :model-value="villeId"
      label="Ville *"
      :placeholder="regionId ? 'Sélectionnez une ville' : 'Choisissez d\'abord une région'"
      :options="villesOptions"
      :error="villeError"
      :disabled="!regionId"
      @update:model-value="onVilleChange"
    />

    <!-- Bouton de géolocalisation -->
    <button
      type="button"
      class="geo-button"
      :disabled="geoLoading"
      @click="mePositionner"
    >
      <MapPin :size="16" :stroke-width="2" />
      <template v-if="geoLoading">Localisation...</template>
      <template v-else>Me positionner</template>
    </button>

    <p v-if="geoMessage" class="geo-message">{{ geoMessage }}</p>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { MapPin } from 'lucide-vue-next'
import api from '@/services/api'
import AppSelect from '@/components/AppSelect.vue'

const props = defineProps({
  regionError: { type: String, default: '' },
  villeError: { type: String, default: '' },
  // Valeurs initiales (pré-remplissage depuis le profil existant)
  initialRegionId: { type: [Number, String], default: null },
  initialVilleId: { type: [Number, String], default: null },
})

const emit = defineEmits(['update:region', 'update:ville', 'update:coords'])

// ==========================================
// ÉTAT
// ==========================================

const regions = ref([])
const regionId = ref(null)
const villeId = ref(null)
const geoLoading = ref(false)
const geoMessage = ref('')

// ==========================================
// CHARGEMENT DES RÉGIONS
// ==========================================

onMounted(async () => {
  try {
    const { data } = await api.get('/auth/regions/')
    regions.value = data

    // Pré-sélectionner la région et la ville si fournies
    if (props.initialRegionId) {
      regionId.value = Number(props.initialRegionId)
    }
    if (props.initialVilleId) {
      villeId.value = Number(props.initialVilleId)
      // Informer le parent pour qu'il ait la valeur
      emit('update:ville', villeId.value)
    }
  } catch (e) {
    // Silencieux
  }
})

// ==========================================
// OPTIONS
// ==========================================

const regionsOptions = computed(() =>
  regions.value.map(r => ({ value: r.id, label: r.nom }))
)

const villesOptions = computed(() => {
  if (!regionId.value) return []

  const id = Number(regionId.value)

  const region = regions.value.find(r => r.id === id)
  if (!region) return []

  return region.villes.map(v => ({ value: v.id, label: v.nom }))
})

// ==========================================
// CHANGEMENT DE RÉGION
// ==========================================

function onRegionChange(value) {
  // On convertit explicitement en nombre (AppSelect renvoie une string)
  regionId.value = value ? Number(value) : null

  // On reset la ville car elle n'appartient plus à la région
  villeId.value = null

  emit('update:region', regionId.value)
  emit('update:ville', null)
}

// ==========================================
// CHANGEMENT DE VILLE
// ==========================================

function onVilleChange(value) {
  villeId.value = value ? Number(value) : null
  emit('update:ville', villeId.value)
}

// ==========================================
// GÉOLOCALISATION
// ==========================================

function mePositionner() {
  if (!navigator.geolocation) {
    geoMessage.value = "La géolocalisation n'est pas supportée par votre navigateur."
    return
  }

  geoLoading.value = true
  geoMessage.value = ''

  navigator.geolocation.getCurrentPosition(
    (position) => {
      emit('update:coords', {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
      })
      geoMessage.value = 'Position enregistrée.'
      geoLoading.value = false
    },
    () => {
      geoMessage.value = 'Impossible de récupérer votre position.'
      geoLoading.value = false
    },
    { enableHighAccuracy: true, timeout: 10000 },
  )
}
</script>

<style scoped>
.location-selector {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.geo-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;

  align-self: flex-start;

  padding: 10px 18px;

  border: 1px solid var(--bloodsen-red);
  border-radius: 8px;

  background-color: transparent;
  color: var(--bloodsen-red);

  font-family: inherit;
  font-size: 14px;
  font-weight: 600;

  cursor: pointer;
  transition: all 0.15s ease;
}

.geo-button:hover:not(:disabled) {
  background-color: #fdecec;
}

.geo-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.geo-message {
  margin: 0;
  color: #059669;
  font-size: 12px;
}
</style>