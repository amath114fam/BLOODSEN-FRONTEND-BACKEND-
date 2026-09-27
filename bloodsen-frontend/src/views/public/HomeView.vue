<template>
  <div class="home-view">

    <!-- ==========================================
         HERO
    =========================================== -->
    <section class="hero">
      <div class="hero-bg"></div>
      <div class="hero-overlay"></div>

      <div class="container hero-content">
        <div class="hero-text glass-card">
         

          <h1>
            Des vies connectées
            grâce au <span class="highlight">don de sang</span>.
          </h1>

          <p>
            BloodSen facilite la mise en relation entre les structures
            de santé qui ont besoin de sang et les donneurs disponibles
            partout au Sénégal.
          </p>

          <div class="hero-actions">
            <AppButton variant="primary" size="lg" to="/inscription">
              Devenir donneur
            </AppButton>
            <AppButton variant="outline-light" size="lg" to="/inscription">
              Je suis une structure
            </AppButton>
          </div>

        </div>

        <div class="hero-image-wrapper">
          <img src="@/assets/images/connexion.jpg" alt="Don de sang" />
        </div>
      </div>
    </section>

    <!-- ==========================================
         STATS
    =========================================== -->
    <section class="stats">
      <div class="stats-bg"></div>
      <div class="container stats-content">
        <div class="stat glass-card">
          <strong>1 don</strong>
          <span>JUSQU'À 3 VIES SAUVÉES</span>
        </div>
        <div class="stat glass-card">
          <strong>&lt; 15 min</strong>
          <span>ALERTE DES DONNEURS PROCHES</span>
        </div>
        <div class="stat glass-card">
          <strong>14 Régions</strong>
          <span>COUVERTURE NATIONALE VISÉE</span>
        </div>
        <div class="stat glass-card">
          <strong>24h / 7j</strong>
          <span>COORDINATION D'URGENCE</span>
        </div>
      </div>
    </section>

    <!-- ==========================================
         COMMENT ÇA MARCHE
    =========================================== -->
    <section id="comment-ca-marche" class="how-it-works">
      <div class="container">
        <div class="section-heading reveal">
          <span class="section-label">Comment ça marche ?</span>
          <h2>Un parcours simple pour faciliter le don de sang.</h2>
          <p>
            BloodSen facilite la mise en relation entre les donneurs
            et les structures de santé qui ont besoin de sang.
          </p>
        </div>

        <div class="steps">
          <article class="step reveal" v-for="(step, index) in steps" :key="index">
            <div class="step-number">{{ String(index + 1).padStart(2, '0') }}</div>
            <div class="step-icon">
              <component :is="step.icon" :size="24" :stroke-width="2" />
            </div>
            <h3>{{ step.titre }}</h3>
            <p>{{ step.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ==========================================
         POURQUOI DONNER
    =========================================== -->
    <section id="pourquoi-donner" class="why-donate">
      <div class="why-donate-bg"></div>
      <div class="container why-donate-content">
        <div class="why-donate-image reveal">
          <img src="@/assets/images/medecine.jpg" alt="Don de sang" />
        </div>

        <div class="why-donate-text reveal">
          <span class="section-label">Pourquoi donner son sang ?</span>
          <h2>Un geste simple qui peut contribuer à sauver des vies.</h2>
          <p>
            Le don de sang joue un rôle essentiel dans la prise en charge
            des patients qui ont besoin de transfusions.
          </p>
          <p>
            En donnant votre sang, vous contribuez à rendre les réserves
            disponibles pour les personnes qui en ont besoin.
          </p>

          <div class="why-donate-highlight glass-card">
            <Droplet :size="24" :stroke-width="2" class="highlight-icon" />
            <div>
              <strong>Chaque don compte.</strong>
              <span>
                Votre disponibilité peut faire la différence lorsqu'une
                structure de santé doit répondre à un besoin de sang.
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================
         POURQUOI REJOINDRE
    =========================================== -->
    <section class="why-join">
      <div class="container">
        <div class="why-join-heading reveal">
          <h2>Pourquoi rejoindre BloodSen ?</h2>
          <p>
            Une infrastructure moderne conçue pour résorber les ruptures
            de stock sans submerger inutilement les citoyens.
          </p>
        </div>

        <div class="why-join-grid">
          <article class="join-card glass-card reveal" v-for="(card, i) in joinCards" :key="i">
            <div class="join-icon">
              <component :is="card.icon" :size="26" :stroke-width="2" />
            </div>
            <h3>{{ card.titre }}</h3>
            <p>{{ card.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <!-- ==========================================
         CONSEILS
    =========================================== -->
    <section class="registration-tips">
      <div class="registration-tips-bg"></div>
      <div class="container">
        <div class="registration-card glass-card reveal">
          <div class="registration-header">
            <div>
              <span class="registration-label">
                <Sparkles :size="14" :stroke-width="2.5" />
                RECOMMANDATIONS UTILES
              </span>
              <h2>Conseils pour bien s'inscrire</h2>
            </div>
            <p>Quelques précisions pour garantir une mobilisation rapide</p>
          </div>

          <div class="registration-divider"></div>

          <div class="tips-grid">
            <article class="tip" v-for="(tip, i) in tips" :key="i">
              <div class="tip-icon">
                <component :is="tip.icon" :size="20" :stroke-width="2" />
              </div>
              <div class="tip-content">
                <h3>{{ tip.titre }}</h3>
                <p>{{ tip.description }}</p>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>

    <!-- ==========================================
         CONTACT
    =========================================== -->
    <section id="contact" class="contact-section">
      <div class="container">
        <div class="contact-heading reveal">
          <span class="contact-label">ASSISTANCE & ÉCHANGE</span>
          <h2>Une question ? Parlons-nous.</h2>
          <p>
            Notre équipe de coordination et les relais de santé publique
            sont à votre écoute pour toute demande d'information,
            partenariat ou question médicale.
          </p>
        </div>

<div class="contact-content">
  <div class="contact-form-card glass-card reveal">

    <!-- Message de succès -->
    <div v-if="contactSucces" class="contact-success">
      <CheckCircle :size="20" :stroke-width="2.5" />
      <span>Votre message a bien été envoyé ! Nous vous répondrons rapidement.</span>
    </div>

    <!-- Message d'erreur global -->
    <div v-if="contactErreur" class="contact-error">
      <AlertCircle :size="20" :stroke-width="2.5" />
      <span>{{ contactErreur }}</span>
    </div>

            <form @submit.prevent="envoyerMessage">
              <div class="form-row">
                <AppInput
                  id="full-name"
                  v-model="formContact.nom_complet"
                  label="Nom complet *"
                  placeholder="Ex: Aminata Diop"
                  :error="contactErreursChamps.nom_complet?.[0] || ''"
                />
                <AppInput
                  id="email"
                  v-model="formContact.email"
                  label="Adresse email *"
                  type="email"
                  placeholder="Ex: aminata@exemple.sn"
                  :error="contactErreursChamps.email?.[0] || ''"
                />
              </div>

              <AppInput
                id="subject"
                v-model="formContact.sujet"
                label="Sujet de votre message *"
                placeholder="Ex: Question concernant le don"
                :error="contactErreursChamps.sujet?.[0] || ''"
              />

              <AppTextarea
                id="message"
                v-model="formContact.message"
                label="Votre message *"
                placeholder="Détaillez votre demande ici..."
                :rows="5"
                :error="contactErreursChamps.message?.[0] || ''"
              />

              <div class="form-footer">
                <AppButton
                  type="submit"
                  variant="primary"
                  :disabled="contactLoading"
                >
                  <template v-if="contactLoading">
                    <span class="spinner-small"></span>
                    Envoi...
                  </template>
                  <template v-else>
                    Envoyer le message
                  </template>
                </AppButton>
                <span>* Champs requis</span>
              </div>
            </form>
          </div>

          <div class="contact-side">
            <div class="institution-card glass-card reveal">
              <h3>Coordonnées institutionnelles</h3>

              <div class="institution-item" v-for="(info, i) in contactInfos" :key="i">
                <div class="institution-icon">
                  <component :is="info.icon" :size="20" :stroke-width="2" />
                </div>
                <div>
                  <strong>{{ info.titre }}</strong>
                  <p>{{ info.valeur }}</p>
                </div>
              </div>
            </div>

            <div class="emergency-card glass-card reveal">
              <div class="emergency-icon">
                <Phone :size="22" :stroke-width="2" />
              </div>
              <div class="emergency-content">
                <strong>Besoin transfusionnel urgent ?</strong>
                <p>Contactez en direct la permanence médicale du CNTS.</p>
              </div>
              <AppButton variant="light" size="sm">
                Appeler
              </AppButton>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, reactive, ref } from 'vue'
import api from '@/services/api'
import {
  Droplet,
  Bell,
  Hospital,
  Timer,
  Users,
  ClipboardList,
  UserPlus,
  Zap,
  Send,
  MapPin,
  Phone,
  Mail,
  Clock,
  Sparkles,
  UserCheck,
  RefreshCw,
  MessageCircle,
  AlertCircle,
  CheckCircle,
} from 'lucide-vue-next'

import AppButton from '@/components/AppButton.vue'
import AppInput from '@/components/AppInput.vue'
import AppTextarea from '@/components/AppTextarea.vue'

// ==========================================
// DONNÉES
// ==========================================

const steps = [
  {
    titre: 'Inscrivez-vous',
    description: 'Créez votre compte et renseignez les informations nécessaires à votre profil de donneur.',
    icon: UserPlus,
  },
  {
    titre: 'Une demande est créée',
    description: 'Une structure de santé peut créer une demande de sang en précisant ses besoins.',
    icon: ClipboardList,
  },
  {
    titre: 'Les donneurs sont identifiés',
    description: 'BloodSen identifie les donneurs potentiellement concernés selon les informations disponibles.',
    icon: Zap,
  },
  {
    titre: 'Participez',
    description: 'Les donneurs peuvent répondre aux sollicitations et participer au processus de don.',
    icon: Send,
  },
]

const joinCards = [
  {
    titre: 'Alertes ciblées',
    description: 'Recevez des notifications uniquement lorsqu\'un besoin urgent correspond précisément à votre groupe sanguin et à votre secteur géographique immédiat. Aucun spam, uniquement l\'essentiel.',
    icon: Bell,
  },
  {
    titre: 'Soutien aux structures',
    description: 'Permet aux banques de sang, centres hospitaliers et dispensaires régionaux de repérer et solliciter des donneurs disponibles et éligibles en temps réel sans appel public désorganisé.',
    icon: Hospital,
  },
  {
    titre: 'Gain de temps vital',
    description: 'Réduction drastique des délais critiques de recherche lors des urgences vitales absolues. Moins d\'intermédiaires, plus de réactivité médicale directe.',
    icon: Timer,
  },
  {
    titre: 'Communauté solidaire',
    description: 'Rejoignez un réseau engagé de citoyens, associations de jeunesse et professionnels de santé mobilisés activement pour la sécurité transfusionnelle au Sénégal.',
    icon: Users,
  },
]

const tips = [
  {
    titre: 'Renseigner précisément son groupe sanguin',
    description: 'Indiquez votre groupe avec son rhésus (A+, O−, B+, AB−, etc.). Si vous l\'ignorez, signalez-le : le centre effectuera un test de confirmation sur place.',
    icon: Droplet,
  },
  {
    titre: 'Indiquer sa disponibilité et sa ville',
    description: 'Précisez si vous résidez à Dakar (Plateau, Parcelles, Pikine, etc.), Thiès, Saint-Louis, Kaolack ou Ziguinchor pour recevoir des alertes de proximité directe.',
    icon: MapPin,
  },
  {
    titre: 'Garder ses coordonnées à jour',
    description: 'Vérifiez votre numéro de téléphone afin d\'être joignable immédiatement lorsqu\'une vie dépend d\'une transfusion d\'extrême urgence.',
    icon: UserCheck,
  },
  {
    titre: 'Répondre rapidement aux sollicitations',
    description: 'En cas d\'alerte, un simple oui ou non permet à l\'équipe médicale de savoir si elle doit immédiatement mobiliser un autre donneur de la même zone.',
    icon: RefreshCw,
  },
]

const contactInfos = [
  {
    titre: 'Siège & Référence',
    valeur: 'Centre National de Transfusion Sanguine (CNTS) / Point E, Dakar, Sénégal',
    icon: MapPin,
  },
  {
    titre: 'Ligne d\'assistance',
    valeur: '+221 33 800 00 00 / +221 77 000 00 00',
    icon: Phone,
  },
  {
    titre: 'Courriel officiel',
    valeur: 'contact@bloodsen.sn',
    icon: Mail,
  },
  {
    titre: 'Disponibilité',
    valeur: 'Accueil administratif : 08h00 – 17h00 — 24h/24 pour les urgences',
    icon: Clock,
  },
]

// ==========================================
// ANIMATIONS AU SCROLL
// ==========================================

// ==========================================
// FORMULAIRE DE CONTACT
// ==========================================

const formContact = reactive({
  nom_complet: '',
  email: '',
  sujet: '',
  message: '',
})

const contactLoading = ref(false)
const contactSucces = ref(false)
const contactErreur = ref('')
const contactErreursChamps = ref({})

async function envoyerMessage() {
  // Réinitialisation
  contactErreur.value = ''
  contactErreursChamps.value = {}
  contactSucces.value = false

  // Validation côté frontend
  if (!formContact.nom_complet || !formContact.email || !formContact.sujet || !formContact.message) {
    contactErreur.value = 'Tous les champs sont obligatoires.'
    return
  }

  contactLoading.value = true
  try {
    await api.post('/contact/', {
      nom_complet: formContact.nom_complet,
      email: formContact.email,
      sujet: formContact.sujet,
      message: formContact.message,
    })

    contactSucces.value = true

    // Vider le formulaire
    formContact.nom_complet = ''
    formContact.email = ''
    formContact.sujet = ''
    formContact.message = ''

    // Faire disparaître le message après 8 secondes
    setTimeout(() => {
      contactSucces.value = false
    }, 8000)
  } catch (error) {
    if (error.response?.status === 400) {
      contactErreursChamps.value = error.response.data
    } else {
      contactErreur.value = 'Une erreur est survenue. Veuillez réessayer.'
    }
  } finally {
    contactLoading.value = false
  }
}

let observer = null

onMounted(() => {
  // Vérifier que IntersectionObserver est supporté
  if (!('IntersectionObserver' in window)) {
    // Fallback : afficher tous les éléments directement
    document.querySelectorAll('.reveal').forEach((el) => {
      el.classList.add('visible')
    })
    return
  }

    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
            observer.unobserve(entry.target)
          }
        })
      },
      {
        rootMargin: '0px 0px 300px 0px', // déclenche bien avant que ce soit visible
        threshold: 0.01,
      }
    )

  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el))

  // Fallback de sécurité : après 1 seconde, forcer l'affichage
  // de tous les éléments encore invisibles (évite qu'ils restent cachés)
  setTimeout(() => {
    document.querySelectorAll('.reveal:not(.visible)').forEach((el) => {
      // On vérifie si l'élément est dans le viewport actuel
      const rect = el.getBoundingClientRect()
      const estDansLeViewport =
        rect.top < window.innerHeight && rect.bottom > 0

      if (estDansLeViewport) {
        el.classList.add('visible')
      }
    })
  }, 1000)
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.home-view {
  overflow-x: hidden;
}

/* ==========================================
   UTILITAIRE GLASSMORPHISM
========================================== */

.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* ==========================================
   HERO
========================================== */

.hero {
  position: relative;
  padding: 100px 0 80px;
  overflow: hidden;
  background: linear-gradient(135deg, #8b0000 0%, #c8102e 50%, #e63946 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
  background-image: url('@/assets/images/header.jpg');
  background-size: cover;
  background-position: center;
  opacity: 0.15;
  z-index: 0;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 20% 50%, rgba(200, 16, 46, 0.4), transparent 70%),
              radial-gradient(circle at 80% 80%, rgba(230, 57, 70, 0.3), transparent 60%);
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  align-items: center;
  gap: 60px;
}

.hero-text {
  padding: 40px;
  border-radius: 20px;
  color: #ffffff;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  margin-bottom: 20px;

  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 30px;

  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
}

.hero-text h1 {
  margin: 0 0 20px;
  font-size: 48px;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.hero-text h1 .highlight {
  color: #ffe5e5;
  position: relative;
}

.hero-text h1 .highlight::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 4px;
  height: 6px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  z-index: -1;
}

.hero-text p {
  margin: 0 0 32px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 17px;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-bottom: 32px;
}

.hero-trust {
  display: flex;
  align-items: center;
  gap: 14px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.trust-avatars {
  display: flex;
}

.trust-avatars span {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 36px;
  height: 36px;
  margin-left: -8px;

  border: 2px solid #c8102e;
  border-radius: 50%;

  background: #ffffff;
  color: #c8102e;

  font-size: 11px;
  font-weight: 700;
}

.trust-avatars span:first-child {
  margin-left: 0;
}

.trust-text {
  color: rgba(255, 255, 255, 0.95);
  font-size: 13px;
}

.trust-text strong {
  display: block;
  font-size: 15px;
  font-weight: 700;
}

.hero-image-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
}

.hero-image-wrapper::before {
  content: '';
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.2), transparent 70%);
  border-radius: 50%;
  filter: blur(40px);
}

.hero-image-wrapper img {
  position: relative;
  display: block;
  width: 100%;
  max-width: 480px;
  height: 480px;
  object-fit: cover;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

/* ==========================================
   STATS
========================================== */

.stats {
  position: relative;
  padding: 70px 0;
  background: linear-gradient(135deg, #1a0505 0%, #4a0808 100%);
  overflow: hidden;
}

.stats-bg {
  position: absolute;
  inset: 0;
  background-image: url('@/assets/images/medecin.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.25;
  z-index: 0;
}

/* Overlay sombre pour garantir la lisibilité du texte */
.stats::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(26, 5, 5, 0.7) 0%, rgba(74, 8, 8, 0.6) 100%);
  z-index: 1;
}

.stats-content {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat {
  padding: 24px 20px;
  border-radius: 16px;
  text-align: center;
  transition: transform 0.3s ease;
}

.stat:hover {
  transform: translateY(-4px);
}

.stat strong {
  display: block;
  margin-bottom: 8px;
  color: #ffffff;
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.stat span {
  display: block;
  color: rgba(255, 255, 255, 0.75);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
}

/* ==========================================
   COMMENT ÇA MARCHE
========================================== */

.how-it-works {
  padding: 100px 0;
  background-color: #ffffff;
}

.section-heading {
  max-width: 700px;
  margin: 0 auto 60px;
  text-align: center;
}

.section-label {
  display: inline-block;
  margin-bottom: 14px;
  color: var(--bloodsen-red);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.section-heading h2 {
  margin: 0 0 16px;
  color: var(--bloodsen-dark);
  font-size: 40px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.section-heading p {
  margin: 0;
  color: #5f6672;
  font-size: 16px;
  line-height: 1.7;
}

.steps {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.step {
  position: relative;
  padding: 32px 24px;
  background: linear-gradient(135deg, #fef2f2 0%, #fff1f2 100%);
  border: 1px solid #fee2e2;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.step:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(200, 16, 46, 0.1);
  border-color: var(--bloodsen-red);
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 44px;
  height: 44px;
  margin-bottom: 16px;

  border-radius: 12px;
  background: linear-gradient(135deg, #c8102e 0%, #8b0000 100%);
  color: #ffffff;

  font-size: 14px;
  font-weight: 800;
}

.step-icon {
  position: absolute;
  top: 32px;
  right: 24px;
  color: var(--bloodsen-red);
  opacity: 0.3;
}

.step h3 {
  margin: 0 0 10px;
  color: var(--bloodsen-dark);
  font-size: 18px;
  font-weight: 700;
}

.step p {
  margin: 0;
  color: #5f6672;
  font-size: 14px;
  line-height: 1.6;
}

/* ==========================================
   POURQUOI DONNER
========================================== */

.why-donate {
  position: relative;
  padding: 100px 0;
  background: linear-gradient(135deg, #fef2f2 0%, #fff1f2 50%, #fef2f2 100%);
  overflow: hidden;
}

.why-donate-bg {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 80% 20%, rgba(200, 16, 46, 0.08), transparent 40%),
    radial-gradient(circle at 20% 80%, rgba(230, 57, 70, 0.06), transparent 40%);
}

.why-donate-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 70px;
}

.why-donate-image img {
  display: block;
  width: 100%;
  height: 500px;
  object-fit: cover;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(200, 16, 46, 0.15);
}

.why-donate-text h2 {
  margin: 0 0 24px;
  color: var(--bloodsen-dark);
  font-size: 40px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.why-donate-text p {
  margin: 0 0 18px;
  color: #5f6672;
  font-size: 16px;
  line-height: 1.7;
}

.why-donate-highlight {
  display: flex;
  align-items: flex-start;
  gap: 16px;

  margin-top: 32px;
  padding: 20px 24px;

  background: linear-gradient(135deg, #c8102e 0%, #c8102e 100%);
  border-radius: 16px;
  color: #ffffff;
}

.highlight-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.why-donate-highlight strong {
  display: block;
  margin-bottom: 6px;
  font-size: 16px;
  font-weight: 700;
}

.why-donate-highlight span {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  line-height: 1.6;
}

/* ==========================================
   POURQUOI REJOINDRE
========================================== */

.why-join {
  padding: 100px 0;
  background-color: #ffffff;
}

.why-join-heading {
  max-width: 650px;
  margin-bottom: 56px;
}

.why-join-heading h2 {
  margin: 0 0 12px;
  color: var(--bloodsen-dark);
  font-size: 40px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.why-join-heading p {
  margin: 0;
  color: #5f6672;
  font-size: 16px;
  line-height: 1.6;
}

.why-join-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.join-card {
  position: relative;
  padding: 36px 32px;
  border-radius: 20px;
  background: linear-gradient(135deg, #ffffff 0%, #fef9f9 100%);
  border: 1px solid #fee2e2;
  box-shadow: 0 4px 16px rgba(200, 16, 46, 0.05);
  transition: all 0.3s ease;
  overflow: hidden;
}

.join-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #c8102e 0%, #e63946 100%);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.join-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 40px rgba(200, 16, 46, 0.12);
}

.join-card:hover::before {
  transform: scaleX(1);
}

.join-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  width: 56px;
  height: 56px;
  margin-bottom: 24px;

  background: linear-gradient(135deg, #fde8e8 0%, #fef2f2 100%);
  border-radius: 14px;
  color: var(--bloodsen-red);
}

.join-card h3 {
  margin: 0 0 12px;
  color: var(--bloodsen-dark);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.join-card p {
  margin: 0;
  color: #5f6672;
  font-size: 15px;
  line-height: 1.6;
}

/* ==========================================
   CONSEILS
========================================== */

.registration-tips {
  position: relative;
  padding: 100px 0;
  background: linear-gradient(135deg, #1a0505 0%, #4a0808 100%);
  overflow: hidden;
}

.registration-tips-bg {
  position: absolute;
  inset: 0;
  background-image: url('@/assets/images/header2.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.2;
  z-index: 0;
}

/* Overlay sombre pour garantir la lisibilité du texte */
.registration-tips::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(26, 5, 5, 0.75) 0%, rgba(74, 8, 8, 0.65) 100%);
  z-index: 1;
}

.registration-card {
  position: relative;
  z-index: 1;
  padding: 48px;
  border-radius: 24px;
  color: #ffffff;
}

.registration-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: end;
  gap: 40px;
}

.registration-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;

  color: #ffe5e5;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.registration-header h2 {
  margin: 0;
  color: #ffffff;
  font-size: 32px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.registration-header > p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 15px;
  text-align: right;
}

.registration-divider {
  height: 1px;
  margin: 24px 0 36px;
  background: rgba(255, 255, 255, 0.15);
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 48px;
  row-gap: 32px;
}

.tip {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.tip-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;

  width: 44px;
  height: 44px;

  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;

  color: #ffe5e5;
}

.tip-content h3 {
  margin: 4px 0 8px;
  color: #ffffff;
  font-size: 17px;
  font-weight: 700;
}

.tip-content p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  line-height: 1.6;
}

/* ==========================================
   CONTACT
========================================== */

.contact-section {
  padding: 100px 0;
  background-color: #f7f9fb;
}

.contact-heading {
  max-width: 620px;
  margin-bottom: 56px;
}

.contact-label {
  display: block;
  margin-bottom: 10px;
  color: var(--bloodsen-red);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.contact-heading h2 {
  margin: 0 0 12px;
  color: var(--bloodsen-dark);
  font-size: 40px;
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.contact-heading p {
  margin: 0;
  color: #5f6672;
  font-size: 16px;
  line-height: 1.6;
}

.contact-content {
  display: grid;
  grid-template-columns: 1.35fr 0.95fr;
  gap: 32px;
  align-items: start;
}

.contact-form-card {
  padding: 36px;
  border-radius: 20px;
  background: #ffffff;
  border: 1px solid #e6eaf0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.contact-form-card form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.form-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-top: 8px;
}

.form-footer span {
  color: #8a94a3;
  font-size: 13px;
}

/* Colonne droite */
.contact-side {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.institution-card {
  padding: 32px 28px;
  border-radius: 20px;
  background: #ffffff;
  border: 1px solid #e6eaf0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.institution-card h3 {
  margin: 0 0 24px;
  color: var(--bloodsen-dark);
  font-size: 19px;
  font-weight: 700;
}

.institution-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 20px;
}

.institution-item:last-child {
  margin-bottom: 0;
}

.institution-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;

  width: 36px;
  height: 36px;

  background: #fef2f2;
  border-radius: 10px;
  color: var(--bloodsen-red);
}

.institution-item strong {
  display: block;
  margin-bottom: 4px;
  color: var(--bloodsen-dark);
  font-size: 13px;
  font-weight: 700;
}

.institution-item p {
  margin: 0;
  color: #5f6672;
  font-size: 13.5px;
  line-height: 1.5;
}

/* Carte urgence */
.emergency-card {
  display: flex;
  align-items: center;
  gap: 16px;

  padding: 24px;

  background: linear-gradient(135deg, #c8102e 0%, #c8102e 100%);
  border-radius: 20px;
  color: #ffffff;
  box-shadow: 0 10px 30px rgba(200, 16, 46, 0.25);
}

.emergency-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;

  width: 48px;
  height: 48px;

  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 12px;
}

.emergency-content {
  flex: 1;
}

.emergency-content strong {
  display: block;
  margin-bottom: 4px;
  font-size: 14px;
  font-weight: 700;
}

.emergency-content p {
  margin: 0;
  color: rgba(255, 255, 255, 0.85);
  font-size: 12.5px;
  line-height: 1.4;
}

/* ==========================================
   ANIMATIONS AU SCROLL
========================================== */

.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ==========================================
   MESSAGES DU FORMULAIRE DE CONTACT
========================================== */

.contact-success,
.contact-error {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 14px 18px;
  margin-bottom: 20px;

  border-radius: 10px;

  font-size: 14px;
  line-height: 1.4;
}

.contact-success {
  background-color: #d1fae5;
  border: 1px solid #a7f3d0;
  color: #059669;
}

.contact-error {
  background-color: #fde8e8;
  border: 1px solid #f5c2c7;
  color: #b42318;
}

.spinner-small {
  display: inline-block;
  width: 14px;
  height: 14px;

  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: #ffffff;
  border-radius: 50%;

  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
/* ==========================================
   RESPONSIVE
========================================== */

@media (max-width: 992px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .hero-image-wrapper {
    order: -1;
  }

  .hero-image-wrapper img {
    height: 380px;
  }

  .stats-content {
    grid-template-columns: repeat(2, 1fr);
  }

  .steps {
    grid-template-columns: repeat(2, 1fr);
  }

  .why-donate-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .why-donate-image img {
    height: 400px;
  }

  .contact-content {
    grid-template-columns: 1fr;
  }

  .registration-header {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .registration-header > p {
    text-align: left;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 60px 0;
  }

  .hero-text {
    padding: 28px;
  }

  .hero-text h1 {
    font-size: 34px;
  }

  .hero-text p {
    font-size: 15px;
  }

  .section-heading h2,
  .why-donate-text h2,
  .why-join-heading h2,
  .contact-heading h2,
  .registration-header h2 {
    font-size: 30px;
  }

  .why-join-grid {
    grid-template-columns: 1fr;
  }

  .tips-grid {
    grid-template-columns: 1fr;
    row-gap: 24px;
  }

  .registration-card {
    padding: 32px 24px;
  }
}

@media (max-width: 576px) {
  .hero-text h1 {
    font-size: 28px;
  }

  .hero-actions {
    flex-direction: column;
  }

  .hero-actions :deep(button) {
    width: 100%;
  }

  .stats-content,
  .steps {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .emergency-card {
    flex-wrap: wrap;
  }

  .emergency-card :deep(button) {
    margin-left: 0;
    width: 100%;
  }
}
</style>