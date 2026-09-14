<template>
  <div class="public-layout">
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
            <router-link to="/connexion" class="login-link">
                Connexion
            </router-link>

            <router-link to="/inscription" class="signup-button">
                Créer un compte
            </router-link>
            </div>

            <!-- Bouton hamburger mobile -->
            <button
            class="menu-button"
            @click="isMenuOpen = !isMenuOpen"
            :aria-label="isMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
            >
            {{ isMenuOpen ? '✕' : '☰' }}
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
        <img
          src="@/assets/images/logo.png"
          alt="BloodSen"
        />
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

        <a href="#comment-ca-marche">
          Comment ça marche
        </a>

        <a href="#pourquoi-donner">
          Pourquoi donner
        </a>

        <a href="#centres-collecte">
          Centres de collecte
        </a>
      </nav>

    </div>


    <!-- Colonne 3 : Informations -->
    <div class="footer-column">

      <h3>Informations & Aide</h3>

      <nav>
        <a href="#eligibilite">
          Critères d'éligibilité
        </a>

        <a href="#urgences">
          Urgences transfusionnelles
        </a>

        <a href="#contact">
          Nous contacter
        </a>

        <a href="#mentions-legales">
          Mentions légales
        </a>
      </nav>

    </div>


    <!-- Colonne 4 : Contact -->
    <div class="footer-column footer-contact">

      <h3>Contact Dakar</h3>

      <div class="footer-contact-item">

        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M20 10C20 15 12 21 12 21C12 21 4 15 4 10C4 5.58 7.58 2 12 2C16.42 2 20 5.58 20 10Z"
            stroke="currentColor"
            stroke-width="2"
          />

          <circle
            cx="12"
            cy="10"
            r="2.5"
            stroke="currentColor"
            stroke-width="2"
          />
        </svg>

        <span>
          Centre National de Transfusion Sanguine (CNTS),
          Fann Résidence, Dakar, Sénégal
        </span>

      </div>


      <div class="footer-contact-item">

        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M5 4H9L11 9L8.5 10.5C9.57 12.67 11.33 14.43 13.5 15.5L15 13L20 15V19C20 20.1 19.1 21 18 21C10.27 21 4 14.73 4 7C4 5.9 4.9 5 6 5"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        <span>
          +221 33 821 54 20
        </span>

      </div>


      <div class="footer-contact-item">

        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <rect
            x="3"
            y="5"
            width="18"
            height="14"
            rx="2"
            stroke="currentColor"
            stroke-width="2"
          />

          <path
            d="M3 7L12 13L21 7"
            stroke="currentColor"
            stroke-width="2"
            stroke-linejoin="round"
          />
        </svg>

        <span>
          contact@bloodsen.sn
        </span>

      </div>

    </div>

  </div>


  <!-- Ligne inférieure -->
  <div class="container footer-bottom">

    <p>
      © 2025 BloodSen Sénégal. Initiative civile et médicale d'intérêt public.
    </p>

    <nav>
      <a href="#mentions-legales">
        Mentions légales
      </a>

      <a href="#confidentialite">
        Politique de confidentialité
      </a>

      <a href="#accessibilite">
        Accessibilité
      </a>
    </nav>

  </div>

</footer>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { RouterView } from 'vue-router'

const isMenuOpen = ref(false)
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


/* ========================================
   CONTENU PRINCIPAL
======================================== */

.footer-main {
  display: grid;
  grid-template-columns: 1.35fr 1fr 1.1fr 1.15fr;
  gap: 60px;

  padding-bottom: 100px;
}


/* ========================================
   LOGO + DESCRIPTION
======================================== */

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


/* ========================================
   COLONNES
======================================== */

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


/* ========================================
   CONTACT
======================================== */

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


/* ========================================
   BAS DU FOOTER
======================================== */

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

/* =========================
   TABLETTE / MOBILE
========================= */

@media (max-width: 768px) {

  .header-content {
    min-height: 64px;
    gap: 16px;
  }

  .logo {
    width: 110px;
  }

  /* Cacher la navigation desktop */
  .main-nav,
  .header-actions {
    display: none;
  }

  /* Afficher le hamburger */
  .menu-button {
    display: block;
  }

  /* Afficher le menu uniquement lorsqu'il est ouvert */
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
}
</style>