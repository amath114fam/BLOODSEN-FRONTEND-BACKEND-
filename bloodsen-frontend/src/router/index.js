import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/public/HomeView.vue'
import PublicLayout from '@/layouts/PublicLayout.vue'
import SignupView from '@/views/public/SignupView.vue'
import LoginView from '@/views/public/LoginView.vue'
import StructureLayout from '@/layouts/StructureLayout.vue'
import DashboardView from '@/views/structure/DashboardView.vue'
import RequestsView from '@/views/structure/RequestsView.vue'
import CreateDemandeView from '@/views/structure/CreateDemandeView.vue'
import DonorsView from '@/views/structure/DonorsView.vue'
import ParticipationsView from '@/views/structure/ParticipationsView.vue'
import ProfileView from '@/views/structure/ProfileView.vue'
import EditProfileView from '@/views/structure/EditProfileView.vue'
import DonorLayout from '@/layouts/DonorLayout.vue'
import DonorDashboardView from '@/views/donor/DashboardView.vue'
import SollicitationsView from '@/views/donor/SollicitationsView.vue'
import DonorParticipationsView from '@/views/donor/ParticipationsView.vue'
import HistoriqueView from '@/views/donor/HistoriqueView.vue'
import DonorProfileView from '@/views/donor/ProfileView.vue'
import DonorEditProfileView from '@/views/donor/EditProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      component: PublicLayout,
      children: [
        {
          path: '',
          component: HomeView,
        },
      ],
    },

    {
      path: '/inscription',
      component: SignupView,
    },
    {
      path: '/connexion',
      component: LoginView,
    },

    {
      path: '/structure',
      component: StructureLayout,
      children: [
        {
          path: 'tableau-de-bord',
          component: DashboardView,
        },
        {
          path: 'demandes',
          component: RequestsView,
        },
        {
          path: 'demandes/creer',
          component: CreateDemandeView,
        },
        {
          path: 'donneurs',
          component: DonorsView,
        },
        { path: 'participations', 
          component: ParticipationsView 
        },
        {
          path: 'profil',
          component: ProfileView,
          meta: { topbarVariant: 'search' },
        },
        {
          path: 'profil/modifier',
          component: EditProfileView,
          meta: { topbarVariant: 'search' },
        },
      ],
    },
    {
      path: '/donneur',
      component: DonorLayout,
      children: [
        {
          path: 'tableau-de-bord',
          component: DonorDashboardView,
        },
        { path: 'sollicitations', 
          component: SollicitationsView 
        },
        { path: 'participations',
          component: DonorParticipationsView,
          meta: { searchPlaceholder: 'Rechercher sur BloodSen...' },
        },
        { path: 'historique',
          component: HistoriqueView,
          meta: { searchPlaceholder: 'Rechercher une participation...' },
        },
        { path: 'profil',
          component: DonorProfileView,
          meta: { searchPlaceholder: 'Rechercher sur BloodSen...' },
        },
        {
          path: 'profil/modifier',
          component: DonorEditProfileView,
          meta: { searchPlaceholder: 'Rechercher sur BloodSen...' },
        },
      ],
    },

  ],
})

export default router