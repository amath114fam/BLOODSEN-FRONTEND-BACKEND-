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
import SollicitationDetailView from '@/views/donor/SollicitationDetailView.vue'
import DonorParticipationsView from '@/views/donor/ParticipationsView.vue'
import DonorProfileView from '@/views/donor/ProfileView.vue'
import DonorEditProfileView from '@/views/donor/EditProfileView.vue'
import VerifyEmailView from '@/views/public/VerifyEmailView.vue'
import { useAuthStore } from '@/stores/auth'
import ForgotPasswordView from '@/views/public/ForgotPasswordView.vue'
import ResetPasswordView from '@/views/public/ResetPasswordView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // ==========================================
    // ROUTES PUBLIQUES
    // ==========================================
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
      meta: { guestOnly: true },  // ← redirige si déjà connecté
    },

    {
      path: '/verification-email',
      component: VerifyEmailView,
    },
    {
      path: '/mot-de-passe-oublie',
      component: ForgotPasswordView,
    },
    {
      path: '/reinitialiser-mot-de-passe',
      component: ResetPasswordView,
    },

    // ==========================================
    // ROUTES STRUCTURE (authentification + rôle requis)
    // ==========================================
    {
      path: '/structure',
      component: StructureLayout,
      meta: { requiresAuth: true, role: 'structure' },
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
        {
          path: 'participations',
          component: ParticipationsView,
        },
        {
          path: 'profil',
          component: ProfileView,
        },
        {
          path: 'profil/modifier',
          component: EditProfileView,
        },
      ],
    },

    // ==========================================
    // ROUTES DONNEUR (authentification + rôle requis)
    // ==========================================
    {
      path: '/donneur',
      component: DonorLayout,
      meta: { requiresAuth: true, role: 'donneur' },
      children: [
        {
          path: 'tableau-de-bord',
          component: DonorDashboardView,
        },
        {
          path: 'sollicitations',
          component: SollicitationsView,
        },
        {
          path: 'sollicitations/:id',
          component: SollicitationDetailView,
        },
        {
          path: 'participations',
          component: DonorParticipationsView,
          meta: { searchPlaceholder: 'Rechercher sur BloodSen...' },
        },
        {
          path: 'profil',
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

// ============================================
// GUARDS DE NAVIGATION
// ============================================
// Fonction exécutée AVANT chaque navigation.
// Elle vérifie les règles d'accès selon les meta de la route ciblée.

router.beforeEach(async (to, from) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth) {
  
    const tokenExiste = !!localStorage.getItem('access_token')

    if (!tokenExiste) {
      return '/connexion'
    }

    // Si le token existe mais que l'utilisateur n'est pas chargé en mémoire
    // (cas d'un F5), on le recharge.
    if (!auth.user) {
      try {
        await auth.fetchMe()
      } catch (e) {
        // Le token est invalide ou expiré → déconnexion
        auth.logout()
        return '/connexion'
      }
    }

    // Vérification du rôle (si la route en exige un)
    if (to.meta.role && auth.role !== to.meta.role) {
      if (auth.role === 'structure') {
        return '/structure/tableau-de-bord'
      } else if (auth.role === 'donneur') {
        return '/donneur/tableau-de-bord'
      } else {
        return '/'
      }
    }
  }


  if (to.meta.guestOnly) {
    const tokenExiste = !!localStorage.getItem('access_token')

    if (tokenExiste) {
      // Si pas d'user en mémoire, on le charge
      if (!auth.user) {
        try {
          await auth.fetchMe()
        } catch (e) {
          // Token invalide → laisser passer vers /connexion
          auth.logout()
          return
        }
      }

      // Redirection vers le bon espace
      if (auth.role === 'structure') {
        return '/structure/tableau-de-bord'
      } else if (auth.role === 'donneur') {
        return '/donneur/tableau-de-bord'
      }
      return '/'
    }
  }

  // Tout est OK, on laisse passer
})

export default router