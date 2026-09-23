<template>
  <Doughnut :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
  labels: { type: Array, required: true },
  values: { type: Array, required: true },
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      data: props.values,
      backgroundColor: [
        '#d32f2f',
        '#1e293b',
        '#f59e0b',
        '#10b981',
        '#6366f1',
        '#ec4899',
        '#0ea5e9',
        '#84cc16',
      ],
      borderWidth: 2,
      borderColor: '#ffffff',
    },
  ],
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#4a5568',
        font: { size: 12 },
        padding: 12,
      },
    },
    tooltip: {
      callbacks: {
        label: (ctx) => {
          const value = ctx.parsed
          const total = ctx.dataset.data.reduce((a, b) => a + b, 0)
          const percent = total ? Math.round((value / total) * 100) : 0
          return `${value} don(s) (${percent}%)`
        },
      },
    },
  },
}))
</script>