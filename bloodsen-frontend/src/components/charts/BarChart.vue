<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  labels: { type: Array, required: true },
  values: { type: Array, required: true },
  peakIndex: { type: Number, default: -1 },
})

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: 'Demandes',
      data: props.values,
      backgroundColor: props.values.map((_, i) =>
        i === props.peakIndex ? '#d32f2f' : '#1e293b'
      ),
      borderRadius: 4,
      barThickness: 28,
    },
  ],
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => `${ctx.parsed.y} demande(s)`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: '#6b7280', font: { size: 12 } },
    },
    y: {
      beginAtZero: true,
      grid: { color: '#f0f1f3' },
      ticks: {
        color: '#6b7280',
        font: { size: 12 },
        stepSize: 1,
        precision: 0,
      },
    },
  },
}))
</script>