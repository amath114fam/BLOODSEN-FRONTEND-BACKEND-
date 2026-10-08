<template>
  <div class="location-selector">

    <!-- Select Région -->
    <AppSelect
      id="region-select"
      v-model="regionId"
      label="Région *"
      placeholder="Sélectionnez une région"
      :options="regionsOptions"
      :error="regionError"
      @update:modelValue="onRegionChange"
    />

    <!-- Select Ville (dépend de la région) -->
    <AppSelect
      id="ville-select"
      v-model="villeId"
      label="Ville *"
      :placeholder="regionId ? 'Sélectionnez une ville' : 'Choisissez d\'abord une région'"
      :options="villesOptions"
      :error="villeError"
      :disabled="!regionId"
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
import { watch } from 'vue'
import api from '@/services/api'
import AppSelect from '@/components/AppSelect.vue'

// Props : permet au parent de récupérer la région, la ville, lat, long
const props = defineProps({
  regionError: { type: String, default: '' },
  villeError: { type: String, default: '' },
})

const emit = defineEmits(['update:region', 'update:ville', 'update:coords'])

// ==========================================
// ÉTAT
// ==========================================

const regions = ref([])     // liste complète (avec villes imbriquées)
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
  } catch (e) {
    // Silencieux
  }
})

// ==========================================
// OPTIONS POUR LES SELECTS
// ==========================================

const regionsOptions = computed(() =>
  regions.value.map(r => ({ value: r.id, label: r.nom }))
)

const villesOptions = computed(() => {
  if (!regionId.value) return []
  const region = regions.value.find(r => r.id === regionId.value)
  if (!region) return []
  return region.villes.map(v => ({ value: v.id, label: v.nom }))
})

// ==========================================
// QUAND LA RÉGION CHANGE
// ==========================================

function onRegionChange() {
  // On reset la ville car elle n'appartient plus à la région
  villeId.value = null
  emit('update:region', regionId.value)
  emit('update:ville', null)
}

// On émet aussi quand la ville change
watch(villeId, (v) => emit('update:ville', v))
watch(regionId, (v) => emit('update:region', v))

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
      const lat = position.coords.latitude
      const lng = position.coords.longitude
      emit('update:coords', { latitude: lat, longitude: lng })
      geoMessage.value = 'Position enregistrée.'
      geoLoading.value = false
    },
    (error) => {
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