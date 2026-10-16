<template>
  <div class="public-layout">

    <!-- ==========================================
         BANDEAU D'URGENCE (au-dessus de la navbar)
    =========================================== -->
    <router-link to="/demande-urgente" class="urgent-banner">
      <div class="container urgent-banner-content">
        <span class="urgent-dot"></span>
        <span class="urgent-banner-text">
          Un proche a besoin de sang en urgence ?
          <strong>Faites une demande maintenant →</strong>
        </span>
      </div>
    </router-link>

    <header class="site-header">
      <div class="container header-content">

        <!-- Logo -->
        <router-link to="/" class="logo-link">
          <img
            src="@/assets/images/logo.png"
            alt="BloodSen"
            class="logo"
          />
        </router-link>

        <!-- Navigation desktop -->
        <nav class="main-nav">
          <router-link to="/">Accueil</router-link>
          <a href="#comment-ca-marche">Comment ça marche</a>
          <a href="#pourquoi-donner">Pourquoi donner</a>
          <a href="#contact">Contact</a>
        </nav>

        <!-- Actions desktop -->
        <div class="header-actions">

          <!-- Si NON connecté -->
          <template v-if="!estConnecte">
            <router-link to="/connexion" class="login-link">
              Connexion
            </router-link>

            <router-link to="/inscription" class="signup-button">
              Créer un compte
            </router-link>
          </template>

          <!-- Si connecté -->
          <template v-else>
            <router-link :to="lienTableauDeBord" class="dashboard-link">
              <LayoutDashboard :size="16" />
              Tableau de bord
            </router-link>

            <button type="button" class="logout-button" @click="ouvrirModalLogout">
              <LogOut :size="16" />
              Déconnexion
            </button>
          </template>

        </div>

        <!-- Bouton hamburger mobile -->
        <button
          class="menu-button"
          @click="isMenuOpen = !isMenuOpen"
          :aria-label="isMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
        >
          <X v-if="isMenuOpen" :size="24" :stroke-width="2" />
          <Menu v-else :size="24" :stroke-width="2" />
        </button>

      </div>

      <!-- Menu mobile -->
      <div v-if="isMenuOpen" class="mobile-menu">

        <router-link to="/" @click="isMenuOpen = false">
          Accueil
        </router-link>

        <a href="#comment-ca-marche" @click="isMenuOpen = false">
          Comment ça marche
        </a>

        <a href="#pourquoi-donner" @click="isMenuOpen = false">
          Pourquoi donner
        </a>

        <a href="#contact" @click="isMenuOpen = false">
          Contact
        </a>

        <template v-if="!estConnecte">
          <router-link
            to="/connexion"
            class="mobile-login"
            @click="isMenuOpen = false"
          >
            Connexion
          </router-link>

          <router-link
            to="/inscription"
            class="mobile-signup"
            @click="isMenuOpen = false"
          >
            Créer un compte
          </router-link>
        </template>

        <template v-else>
          <router-link
            :to="lienTableauDeBord"
            class="mobile-signup"
            @click="isMenuOpen = false"
          >
            Tableau de bord
          </router-link>

          <button
            type="button"
            class="mobile-logout"
            @click="ouvrirModalLogout"
          >
            Déconnexion
          </button>
        </template>

      </div>
    </header>

    <main>
      <RouterView />
    </main>

    <footer class="site-footer">

      <div class="container footer-main">

        <!-- Colonne 1 : Présentation -->
        <div class="footer-brand">

          <div class="footer-logo">
            <img src="@/assets/images/logo.png" alt="BloodSen" />
          </div>

          <p>
            Plateforme nationale de coordination et de sensibilisation
            au don de sang au Sénégal. Relier les donneurs volontaires
            aux structures hospitalières de Dakar et des régions.
          </p>

        </div>

        <!-- Colonne 2 : Plateforme -->
        <div class="footer-column">
          <h3>Plateforme</h3>
          <nav>
            <a href="#accueil">Accueil</a>
            <a href="#comment-ca-marche">Comment ça marche</a>
            <a href="#pourquoi-donner">Pourquoi donner</a>
            <a href="#centres-collecte">Centres de collecte</a>
          </nav>
        </div>

        <!-- Colonne 3 : Informations -->
        <div class="footer-column">
          <h3>Informations & Aide</h3>
          <nav>
            <a href="#eligibilite">Critères d'éligibilité</a>
            <a href="#urgences">Urgences transfusionnelles</a>
            <a href="#contact">Nous contacter</a>
            <a href="#mentions-legales">Mentions légales</a>
          </nav>
        </div>

        <!-- Colonne 4 : Contact -->
        <div class="footer-column footer-contact">
          <h3>Contact Dakar</h3>

          <div class="footer-contact-item">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 10C20 15 12 21 12 21C12 21 4 15 4 10C4 5.58 7.58 2 12 2C16.42 2 20 5.58 20 10Z" stroke="currentColor" stroke-width="2" />
              <circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="2" />
            </svg>
            <span>
              Centre National de Transfusion Sanguine (CNTS),
              Fann Résidence, Dakar, Sénégal
            </span>
          </div>

          <div class="footer-contact-item">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 4H9L11 9L8.5 10.5C9.57 12.67 11.33 14.43 13.5 15.5L15 13L20 15V19C20 20.1 19.1 21 18 21C10.27 21 4 14.73 4 7C4 5.9 4.9 5 6 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <span>+221 33 821 54 20</span>
          </div>

          <div class="footer-contact-item">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="2" />
              <path d="M3 7L12 13L21 7" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
            </svg>
            <span>contact@bloodsen.sn</span>
          </div>

        </div>

      </div>

      <!-- Ligne inférieure -->
      <div class="container footer-bottom">
        <p>
          © 2025 BloodSen Sénégal. Initiative civile et médicale d'intérêt public.
        </p>
        <nav>
          <a href="#mentions-legales">Mentions légales</a>
          <a href="#confidentialite">Politique de confidentialité</a>
          <a href="#accessibilite">Accessibilité</a>
        </nav>
      </div>

    </footer>

    <ChatWidget />

    <LogoutModal
      :visible="afficherModalLogout"
      :chargement="deconnexionEnCours"
      @annuler="fermerModalLogout"
      @confirmer="confirmerLogout"
    />

        <!-- Bottom nav mobile (remplace le burger) -->
    <PublicBottomNav />

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { X, Menu, LayoutDashboard, LogOut } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import ChatWidget from '@/components/ChatWidget.vue'
import LogoutModal from '@/components/LogoutModal.vue'
import PublicBottomNav from '@/views/public/PublicBottomNav.vue'

const router = useRouter()
const auth = useAuthStore()

const isMenuOpen = ref(false)

// ==========================================
// MODAL DE DÉCONNEXION
// ==========================================

const afficherModalLogout = ref(false)
const deconnexionEnCours = ref(false)

function ouvrirModalLogout() {
  afficherModalLogout.value = true
  isMenuOpen.value = false
}

function fermerModalLogout() {
  if (deconnexionEnCours.value) return
  afficherModalLogout.value = false
}

function confirmerLogout() {
  deconnexionEnCours.value = true
  auth.logout()
  isMenuOpen.value = false
  router.push('/connexion')
}

// Vrai si l'utilisateur est connecté
const estConnecte = computed(() => auth.isAuthenticated)

// Lien vers le bon tableau de bord selon le rôle
// On utilise ?. pour éviter un crash si user est null
const lienTableauDeBord = computed(() => {
  if (auth.user?.role === 'structure') return '/structure/tableau-de-bord'
  if (auth.user?.role === 'donneur') return '/donneur/tableau-de-bord'
  return '/'
})

</script>

<style scoped>
.public-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* ========================================
   BANDEAU D'URGENCE
======================================== */

.urgent-banner {
  display: block;

  background: linear-gradient(90deg, #8b0000 0%, #c8102e 50%, #8b0000 100%);
  color: #ffffff;

  text-decoration: none;

  transition: opacity 0.2s ease;
}

.urgent-banner:hover {
  opacity: 0.92;
}

.urgent-banner-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;

  min-height: 42px;
  padding: 8px 0;
}

.urgent-banner-text {
  font-size: 13.5px;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.urgent-banner-text strong {
  font-weight: 700;
  text-decoration: underline;
  text-underline-offset: 3px;
}

/* Point pulsant */
.urgent-dot {
  position: relative;
  flex-shrink: 0;

  display: inline-block;
  width: 8px;
  height: 8px;

  border-radius: 50%;
  background-color: #ffffff;
}

.urgent-dot::after {
  content: '';
  position: absolute;
  inset: 0;

  border-radius: 50%;
  background-color: #ffffff;

  animation: urgent-pulse 1.8s ease-out infinite;
}

@keyframes urgent-pulse {
  0%   { transform: scale(1);   opacity: 0.9; }
  100% { transform: scale(2.5); opacity: 0; }
}

/* ========================================
   HEADER
======================================== */

.site-header {
  background: #fff;
  border-bottom: 1px solid var(--bloodsen-border);
}

.header-content {
  min-height: 76px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
}

.logo {
  width: 130px;
  height: auto;
}

/* =========================
   NAVIGATION DESKTOP
========================= */

.main-nav {
  display: flex;
  align-items: center;
  gap: 28px;
}

.main-nav a,
.login-link {
  color: var(--bloodsen-dark);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.main-nav a:hover,
.login-link:hover {
  color: var(--bloodsen-red);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.signup-button {
  padding: 10px 18px;
  border-radius: 8px;
  background: var(--bloodsen-red);
  color: #fff;
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}

/* Lien vers le tableau de bord (quand connecté) */
.dashboard-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;

  padding: 10px 18px;
  border-radius: 8px;

  background: var(--bloodsen-red);
  color: #fff;

  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
}

.dashboard-link:hover {
  opacity: 0.9;
}

/* Bouton de déconnexion */
.logout-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;

  padding: 10px 16px;
  border: 1px solid #e0e4ea;
  border-radius: 8px;

  background: transparent;
  color: var(--bloodsen-dark);

  font-family: inherit;
  font-size: 14px;
  font-weight: 500;

  cursor: pointer;
  transition: all 0.15s ease;
}

.logout-button:hover {
  border-color: var(--bloodsen-red);
  color: var(--bloodsen-red);
}

/* =========================
   BOUTON HAMBURGER
========================= */

.menu-button {
  display: none;
  border: none;
  background: transparent;
  font-size: 28px;
  cursor: pointer;
  color: var(--bloodsen-dark);
}

/* Menu mobile caché par défaut */
.mobile-menu {
  display: none;
}

/* ========================================
   FOOTER
======================================== */

.site-footer {
  padding-top: 42px;
  background-color: #f1f3f5;
  color: #5f6672;
}

.footer-main {
  display: grid;
  grid-template-columns: 1.35fr 1fr 1.1fr 1.15fr;
  gap: 60px;

  padding-bottom: 100px;
}

.footer-brand {
  max-width: 270px;
}

.footer-logo {
  margin-bottom: 28px;
}

.footer-logo img {
  display: block;
  width: 48px;
  height: auto;
}

.footer-brand p {
  margin: 0;
  color: #6a5960;
  font-size: 14px;
  line-height: 1.5;
}

.footer-column h3 {
  margin: 0 0 14px;
  color: #202428;
  font-size: 14px;
  font-weight: 700;
}

.footer-column nav {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.footer-column a {
  color: #66585d;
  font-size: 14px;
  line-height: 1.4;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-column a:hover {
  color: var(--bloodsen-red);
}

.footer-contact {
  max-width: 280px;
}

.footer-contact-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 12px;
}

.footer-contact-item:last-child {
  margin-bottom: 0;
}

.footer-contact-item svg {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  margin-top: 1px;
  color: #5c687b;
}

.footer-contact-item span {
  color: #66585d;
  font-size: 14px;
  line-height: 1.4;
}

.footer-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 58px;
  border-top: 1px solid #d9dde2;
}

.footer-bottom p {
  margin: 0;
  color: #697386;
  font-size: 12px;
}

.footer-bottom nav {
  display: flex;
  align-items: center;
  gap: 22px;
}

.footer-bottom a {
  color: #697386;
  font-size: 12px;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-bottom a:hover {
  color: var(--bloodsen-red);
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 992px) {
  .footer-main {
    grid-template-columns: repeat(2, 1fr);
    gap: 40px;
    padding-bottom: 60px;
  }

  .footer-brand {
    max-width: 320px;
  }
}

@media (max-width: 768px) {
  .site-footer {
    padding-top: 40px;
  }

  .footer-main {
    grid-template-columns: 1fr 1fr;
    gap: 36px 24px;
  }

  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    gap: 12px;
    padding: 18px 0;
  }

  .footer-bottom nav {
    flex-wrap: wrap;
    gap: 12px 20px;
  }

  /* Bandeau d'urgence en mobile */
  .urgent-banner-content {
    justify-content: flex-start;
    padding: 10px 16px;
  }

  .urgent-banner-text {
    font-size: 12.5px;
  }

  /* Header en mobile */
  .header-content {
    min-height: 64px;
    gap: 16px;
  }

  .logo {
    width: 110px;
  }

  .main-nav,
  .header-actions {
    display: none;
  }

  .menu-button {
    display: none;
  }

    .mobile-menu {
    display: none !important;
  }

  .mobile-menu {
    display: flex;
    flex-direction: column;
    gap: 18px;
    padding: 20px;
    border-top: 1px solid var(--bloodsen-border);
    background: #fff;
  }

  .mobile-menu a {
    color: var(--bloodsen-dark);
    text-decoration: none;
    font-size: 15px;
    font-weight: 500;
  }

  .mobile-menu a:hover {
    color: var(--bloodsen-red);
  }

  .mobile-login {
    padding-top: 10px;
  }

  .mobile-signup {
    padding: 12px 16px;
    border-radius: 8px;
    background: var(--bloodsen-red);
    color: #fff !important;
    text-align: center;
  }

  .mobile-logout {
    padding: 12px 16px;
    border: 1px solid #e0e4ea;
    border-radius: 8px;
    background: transparent;
    color: var(--bloodsen-dark);
    font-family: inherit;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
  }

  .mobile-logout:hover {
    border-color: var(--bloodsen-red);
    color: var(--bloodsen-red);
  }
}

@media (max-width: 576px) {
  .footer-main {
    grid-template-columns: 1fr;
    gap: 32px;
    padding-bottom: 40px;
  }

  .footer-brand,
  .footer-contact {
    max-width: none;
  }

  .footer-logo {
    margin-bottom: 20px;
  }
}
</style>