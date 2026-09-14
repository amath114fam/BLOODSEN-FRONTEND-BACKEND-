<template>
  <AppCard padding="24px" class="engagement-card">

    <div class="engagement-header">
      <span class="engagement-icon">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </span>
      <div>
        <h3>Mon Engagement</h3>
        <p>Niveau: {{ level }}</p>
      </div>
    </div>

    <div class="engagement-progress-row">
      <span>{{ progressLabel }}</span>
      <strong>{{ current }} / {{ target }}</strong>
    </div>

    <div class="progress-track">
      <div
        class="progress-fill"
        :style="{ width: percent + '%' }"
      ></div>
    </div>

    <div class="progress-levels">
      <span>{{ lowTierLabel }}</span>
      <span>{{ highTierLabel }}</span>
    </div>

    <div class="engagement-divider"></div>

    <div class="engagement-metrics">
      <div class="engagement-metric">
        <span>PARTICIPATIONS</span>
        <strong>{{ participations }}</strong>
      </div>

      <div class="engagement-metric">
        <span>POINTS ACQUIS</span>
        <strong>{{ points.toLocaleString('fr-FR') }} pts</strong>
      </div>
    </div>

  </AppCard>
</template>

<script setup>
import { computed } from 'vue'

import AppCard from '@/components/AppCard.vue'

const props = defineProps({
  level: { type: String, required: true },
  progressLabel: { type: String, default: 'Dons confirmés' },
  current: { type: Number, required: true },
  target: { type: Number, required: true },
  lowTierLabel: { type: String, required: true },
  highTierLabel: { type: String, required: true },
  participations: { type: Number, required: true },
  points: { type: Number, required: true },
})

const percent = computed(() =>
  Math.min(100, Math.round((props.current / props.target) * 100))
)
</script>

<style scoped>
.engagement-header {
  display: flex;
  align-items: center;
  gap: 12px;

  margin-bottom: 20px;
}

.engagement-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  width: 36px;
  height: 36px;

  border-radius: 50%;

  background-color: #eafaf0;
  color: #1e9e5a;
}

.engagement-icon svg {
  width: 18px;
  height: 18px;
}

.engagement-header h3 {
  margin: 0 0 2px;

  color: var(--bloodsen-dark);

  font-size: 15px;
  font-weight: 700;
}

.engagement-header p {
  margin: 0;

  color: #6b7280;

  font-size: 12.5px;
}

.engagement-progress-row {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 8px;

  color: var(--bloodsen-dark);
  font-size: 13px;
}

.engagement-progress-row strong {
  color: var(--bloodsen-dark);
}

.progress-track {
  height: 8px;
  margin-bottom: 8px;

  border-radius: 4px;

  background-color: #f1f3f5;
  overflow: hidden;
}

.progress-fill {
  height: 100%;

  border-radius: 4px;

  background-color: #1e9e5a;
}

.progress-levels {
  display: flex;
  align-items: center;
  justify-content: space-between;

  color: #8a94a3;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.engagement-divider {
  height: 1px;
  margin: 20px 0;

  background-color: #eef0f2;
}

.engagement-metrics {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.engagement-metric {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.engagement-metric span {
  color: #8a94a3;

  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.engagement-metric strong {
  color: var(--bloodsen-dark);
  font-size: 17px;
}
</style>