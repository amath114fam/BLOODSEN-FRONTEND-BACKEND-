<template>
  <section class="hero">
    <div class="container hero-content">

      <div class="hero-text">
        <h1>Des vies connectées grâce au don de sang.</h1>

        <p>
          BloodSen facilite la mise en relation entre les structures de santé
          qui ont besoin de sang et les donneurs disponibles.
        </p>

        <div class="hero-actions">
          <AppButton variant="primary" size="lg">
            Devenir donneur
          </AppButton>

          <AppButton variant="outline" size="lg">
            Je suis une structure de santé
          </AppButton>
        </div>
      </div>

      <div class="hero-image">
        <img
          src="@/assets/images/header.png"
          alt="Don de sang"
        />
      </div>

    </div>
  </section>
  <section class="stats">
  <div class="container stats-content">

    <div class="stat">
      <strong>1 don</strong>
      <span>JUSQU'À 3 VIES SAUVÉES</span>
    </div>

    <div class="stat">
      <strong>&lt; 15 min</strong>
      <span>ALERTE DES DONNEURS PROCHES</span>
    </div>

    <div class="stat">
      <strong>14 Régions</strong>
      <span>COUVERTURE NATIONALE VISÉE</span>
    </div>

    <div class="stat">
      <strong>24h / 7j</strong>
      <span>COORDINATION D’URGENCE</span>
    </div>

  </div>
</section>
  <section id="comment-ca-marche" class="how-it-works">
  <div class="container">

    <div class="section-heading">
      <span class="section-label">Comment ça marche ?</span>

      <h2>
        Un parcours simple pour faciliter le don de sang.
      </h2>

      <p>
        BloodSen facilite la mise en relation entre les donneurs
        et les structures de santé qui ont besoin de sang.
      </p>
    </div>

    <div class="steps">

      <article class="step">
        <div class="step-number">01</div>

        <div class="step-content">
          <h3>Inscrivez-vous</h3>

          <p>
            Créez votre compte et renseignez les informations
            nécessaires à votre profil de donneur.
          </p>
        </div>
      </article>

      <article class="step">
        <div class="step-number">02</div>

        <div class="step-content">
          <h3>Une demande est créée</h3>

          <p>
            Une structure de santé peut créer une demande
            de sang en précisant ses besoins.
          </p>
        </div>
      </article>

      <article class="step">
        <div class="step-number">03</div>

        <div class="step-content">
          <h3>Les donneurs sont identifiés</h3>

          <p>
            BloodSen identifie les donneurs potentiellement
            concernés selon les informations disponibles.
          </p>
        </div>
      </article>

      <article class="step">
        <div class="step-number">04</div>

        <div class="step-content">
          <h3>Participez</h3>

          <p>
            Les donneurs peuvent répondre aux sollicitations
            et participer au processus de don.
          </p>
        </div>
      </article>

    </div>

  </div>
</section>
<section id="pourquoi-donner" class="why-donate">
  <div class="container why-donate-content">

    <div class="why-donate-image">
      <img
        src="@/assets/images/medecin.png"
        alt="Don de sang"
      />
    </div>

    <div class="why-donate-text">
      <span class="section-label">Pourquoi donner son sang ?</span>

      <h2>
        Un geste simple qui peut contribuer à sauver des vies.
      </h2>

      <p>
        Le don de sang joue un rôle essentiel dans la prise en charge
        des patients qui ont besoin de transfusions.
      </p>

      <p>
        En donnant votre sang, vous contribuez à rendre les réserves
        disponibles pour les personnes qui en ont besoin.
      </p>

      <div class="why-donate-highlight">
        <strong>Chaque don compte.</strong>

        <span>
          Votre disponibilité peut faire la différence lorsqu'une
          structure de santé doit répondre à un besoin de sang.
        </span>
      </div>
    </div>

  </div>
</section>
<section class="why-join">
  <div class="container">

    <div class="why-join-heading">
      <h2>Pourquoi rejoindre BloodSen ?</h2>

      <p>
        Une infrastructure moderne conçue pour résorber les ruptures de stock
        sans submerger inutilement les citoyens.
      </p>
    </div>

    <div class="why-join-grid">

      <!-- Carte 1 -->
      <article class="join-card">
        <div class="join-icon">
          <!-- Icône cloche -->
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M18 8C18 5.79 16.21 4 14 4H10C7.79 4 6 5.79 6 8C6 12.5 4 14 4 16H20C20 14 18 12.5 18 8Z"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M10 20H14"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </div>

        <h3>Alertes ciblées</h3>

        <p>
          Recevez des notifications uniquement lorsqu'un besoin urgent
          correspond précisément à votre groupe sanguin et à votre secteur
          géographique immédiat. Aucun spam, uniquement l'essentiel.
        </p>
      </article>

      <!-- Carte 2 -->
      <article class="join-card">
        <div class="join-icon">
          <!-- Icône structure de santé -->
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <rect
              x="5"
              y="5"
              width="14"
              height="14"
              rx="1"
              stroke="currentColor"
              stroke-width="2"
            />
            <path
              d="M12 8V16"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
            <path
              d="M8 12H16"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </div>

        <h3>Soutien aux structures</h3>

        <p>
          Permet aux banques de sang, centres hospitaliers et dispensaires
          régionaux de repérer et solliciter des donneurs disponibles et
          éligibles en temps réel sans appel public désorganisé.
        </p>
      </article>

      <!-- Carte 3 -->
      <article class="join-card">
        <div class="join-icon">
          <!-- Icône chronomètre -->
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="12"
              cy="13"
              r="7"
              stroke="currentColor"
              stroke-width="2"
            />
            <path
              d="M12 9V13L14 15"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M9 3H15"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
            <path
              d="M12 3V5"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </div>

        <h3>Gain de temps vital</h3>

        <p>
          Réduction drastique des délais critiques de recherche lors des
          urgences vitales absolues. Moins d'intermédiaires, plus de
          réactivité médicale directe.
        </p>
      </article>

      <!-- Carte 4 -->
      <article class="join-card">
        <div class="join-icon">
          <!-- Icône communauté -->
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="9"
              cy="9"
              r="3"
              stroke="currentColor"
              stroke-width="2"
            />
            <circle
              cx="17"
              cy="10"
              r="2.5"
              stroke="currentColor"
              stroke-width="2"
            />
            <path
              d="M3 19C3 15.69 5.69 13 9 13C12.31 13 15 15.69 15 19"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
            <path
              d="M14 14C14.83 13.37 15.86 13 17 13C19.76 13 22 15.24 22 18"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </div>

        <h3>Communauté solidaire</h3>

        <p>
          Rejoignez un réseau engagé de citoyens, associations de jeunesse
          et professionnels de santé mobilisés activement pour la sécurité
          transfusionnelle au Sénégal.
        </p>
      </article>

    </div>
  </div>
</section>
<section class="registration-tips">
  <div class="container">

    <div class="registration-card">

      <!-- En-tête -->
      <div class="registration-header">

        <div>
          <span class="registration-label">
            ▣ RECOMMANDATIONS UTILES
          </span>

          <h2>Conseils pour bien s'inscrire</h2>
        </div>

        <p>
          Quelques précisions pour garantir une mobilisation rapide
        </p>

      </div>

      <div class="registration-divider"></div>

      <!-- Conseils -->
      <div class="tips-grid">

        <!-- Conseil 1 -->
        <article class="tip">

          <div class="tip-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="12"
                cy="12"
                r="8"
                stroke="currentColor"
                stroke-width="2"
              />

              <path
                d="M12 8V16"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />

              <path
                d="M9 12H15"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </div>

          <div class="tip-content">
            <h3>Renseigner précisément son groupe sanguin</h3>

            <p>
              Indiquez votre groupe avec son rhésus (A+, O−, B+, AB−, etc.).
              Si vous l'ignorez, signalez-le : le centre effectuera un test
              de confirmation sur place.
            </p>
          </div>

        </article>

        <!-- Conseil 2 -->
        <article class="tip">

          <div class="tip-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect
                x="5"
                y="4"
                width="14"
                height="16"
                rx="2"
                stroke="currentColor"
                stroke-width="2"
              />

              <path
                d="M9 8H15"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />

              <path
                d="M9 12H15"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />

              <path
                d="M9 16H12"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </div>

          <div class="tip-content">
            <h3>Indiquer sa disponibilité et sa ville</h3>

            <p>
              Précisez si vous résidez à Dakar (Plateau, Parcelles, Pikine,
              etc.), Thiès, Saint-Louis, Kaolack ou Ziguinchor pour recevoir
              des alertes de proximité directe.
            </p>
          </div>

        </article>

        <!-- Conseil 3 -->
        <article class="tip">

          <div class="tip-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect
                x="4"
                y="6"
                width="16"
                height="14"
                rx="2"
                stroke="currentColor"
                stroke-width="2"
              />

              <circle
                cx="9"
                cy="11"
                r="2"
                stroke="currentColor"
                stroke-width="2"
              />

              <path
                d="M7 17C7.5 15.5 8.5 15 10 15C11.5 15 12.5 15.5 13 17"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />

              <path
                d="M15 10H18"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </div>

          <div class="tip-content">
            <h3>Garder ses coordonnées à jour</h3>

            <p>
              Vérifiez votre numéro de téléphone afin d'être joignable
              immédiatement lorsqu'une vie dépend d'une transfusion
              d'extrême urgence.
            </p>
          </div>

        </article>

        <!-- Conseil 4 -->
        <article class="tip">

          <div class="tip-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M19 12H5"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />

              <path
                d="M9 8L5 12L9 16"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </div>

          <div class="tip-content">
            <h3>Répondre rapidement aux sollicitations</h3>

            <p>
              En cas d'alerte, un simple oui ou non permet à l'équipe médicale
              de savoir si elle doit immédiatement mobiliser un autre donneur
              de la même zone.
            </p>
          </div>

        </article>

      </div>

    </div>

  </div>
</section>
<section id="contact" class="contact-section">
  <div class="container">

    <!-- En-tête -->
    <div class="contact-heading">
      <span class="contact-label">ASSISTANCE & ÉCHANGE</span>

      <h2>Une question ? Parlons-nous.</h2>

      <p>
        Notre équipe de coordination et les relais de santé publique sont à
        votre écoute pour toute demande d'information, partenariat ou question
        médicale.
      </p>
    </div>


    <!-- Contenu -->
    <div class="contact-content">

      <!-- Formulaire -->
      <div class="contact-form-card">

        <form @submit.prevent>

          <div class="form-row">

            <AppInput
              id="full-name"
              label="Nom complet *"
              placeholder="Ex: Aminata Diop"
            />

            <AppInput
              id="email"
              label="Adresse email *"
              type="email"
              placeholder="Ex: aminata@exemple.sn"
            />

          </div>


          <AppInput
            id="subject"
            label="Sujet de votre message *"
            placeholder="Ex: Question concernant le don"
          >
            <option value="">
              Sélectionnez un sujet...
            </option>

            <option value="information">
              Demande d'information
            </option>

            <option value="partenariat">
              Partenariat
            </option>

            <option value="medical">
              Question médicale
            </option>

            <option value="other">
              Autre
            </option>
          </AppInput>


          <AppTextarea
            id="message"
            label="Votre message *"
            placeholder="Détaillez votre demande ici..."
            :rows="5"
          />


          <div class="form-footer">

            <AppButton
              type="submit"
              variant="primary"
            >
              Envoyer le message
            </AppButton>

            <span>* Champs requis</span>

          </div>

        </form>

      </div>


      <!-- Colonne droite -->
      <div class="contact-side">

        <!-- Coordonnées -->
        <div class="institution-card">

          <h3>Coordonnées institutionnelles</h3>


          <div class="institution-item">

            <div class="institution-icon">
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
            </div>

            <div>
              <strong>Siège & Référence</strong>

              <p>
                Centre National de Transfusion Sanguine (CNTS) /
                Point E, Dakar, Sénégal
              </p>
            </div>

          </div>


          <div class="institution-item">

            <div class="institution-icon">
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
            </div>

            <div>
              <strong>Ligne d'assistance</strong>

              <p>
                +221 33 800 00 00 / +221 77 000 00 00
              </p>
            </div>

          </div>


          <div class="institution-item">

            <div class="institution-icon">
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
            </div>

            <div>
              <strong>Courriel officiel</strong>

              <p>
                contact@bloodsen.sn
              </p>
            </div>

          </div>


          <div class="institution-item">

            <div class="institution-icon">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="12"
                  cy="12"
                  r="9"
                  stroke="currentColor"
                  stroke-width="2"
                />

                <path
                  d="M12 7V12L15 14"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>

            <div>
              <strong>Disponibilité</strong>

              <p>
                Accueil administratif : 08h00 – 17h00
                <br />

                <span class="emergency-text">
                  24h/24
                </span>

                pour les urgences médicales et hospitalières
              </p>
            </div>

          </div>

        </div>


        <!-- Urgence -->
        <div class="emergency-card">

          <div class="emergency-icon">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                cx="12"
                cy="12"
                r="8"
                stroke="currentColor"
                stroke-width="2"
              />

              <path
                d="M12 8V16"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />

              <path
                d="M8 12H16"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </div>

          <div class="emergency-content">

            <strong>
              Besoin transfusionnel urgent ?
            </strong>

            <p>
              Contactez en direct la permanence médicale du CNTS.
            </p>

          </div>

          <AppButton
            variant="outline"
            size="sm"
          >
            Appeler
          </AppButton>

        </div>

      </div>

    </div>

  </div>
</section>
</template>

<script setup>
import AppButton from '@/components/AppButton.vue'
import AppInput from '@/components/AppInput.vue'
import AppSelect from '@/components/AppSelect.vue'
import AppTextarea from '@/components/AppTextarea.vue'
</script>

<style scoped>
.hero {
  padding: 80px 0;
  background-color: #fff;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 60px;
}

.hero-text {
  max-width: 600px;
}

.hero-text h1 {
  margin: 0 0 24px;
  color: var(--bloodsen-dark);
  font-size: 48px;
  line-height: 1.15;
  font-weight: 700;
}

.hero-text p {
  margin: 0 0 32px;
  color: #5f6672;
  font-size: 17px;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.hero-image {
  width: 100%;
}

.hero-image img {
  display: block;
  width: 100%;
  height: 420px;
  object-fit: cover;
  border-radius: 12px;
}
.how-it-works {
  padding: 80px 0;
  background-color: #f8f9fb;
}

.section-heading {
  max-width: 700px;
  margin: 0 auto 50px;
  text-align: center;
}

.section-label {
  display: inline-block;
  margin-bottom: 12px;
  color: var(--bloodsen-red);
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.section-heading h2 {
  margin: 0 0 16px;
  color: var(--bloodsen-dark);
  font-size: 36px;
  line-height: 1.2;
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
  padding: 28px;
  background-color: #fff;
  border: 1px solid #e7e9ed;
  border-radius: 12px;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 48px;
  height: 48px;
  margin-bottom: 20px;

  border-radius: 50%;
  background-color: var(--bloodsen-red);
  color: #fff;

  font-size: 14px;
  font-weight: 700;
}

.step-content h3 {
  margin: 0 0 12px;
  color: var(--bloodsen-dark);
  font-size: 19px;
}

.step-content p {
  margin: 0;
  color: #5f6672;
  font-size: 15px;
  line-height: 1.6;
}
.stats {
  padding: 24px 0;
  background-color: #f1f3f5;
}

.stats-content {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
}

.stat {
  padding: 16px 12px;
  background-color: #fff;
  border: 1px solid #d9dde2;
  border-radius: 4px;
}

.stat strong {
  display: block;
  margin-bottom: 2px;

  color: var(--bloodsen-red);
  font-size: 28px;
  line-height: 1.2;
  font-weight: 700;
}

.stat span {
  display: block;

  color: #50596a;
  font-size: 12px;
  line-height: 1.4;
  font-weight: 500;
  letter-spacing: 0.04em;
}
.why-donate {
  padding: 90px 0;
  background-color: #fff;
}

.why-donate-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: 70px;
}

.why-donate-image img {
  display: block;
  width: 100%;
  height: 480px;
  object-fit: cover;
  border-radius: 12px;
}

.why-donate-text {
  max-width: 560px;
}

.why-donate-text h2 {
  margin: 0 0 24px;

  color: var(--bloodsen-dark);
  font-size: 38px;
  line-height: 1.2;
  font-weight: 700;
}

.why-donate-text p {
  margin: 0 0 18px;

  color: #5f6672;
  font-size: 16px;
  line-height: 1.7;
}

.why-donate-highlight {
  display: flex;
  flex-direction: column;
  gap: 8px;

  margin-top: 30px;
  padding-left: 20px;

  border-left: 3px solid var(--bloodsen-red);
}

.why-donate-highlight strong {
  color: var(--bloodsen-dark);
  font-size: 18px;
}

.why-donate-highlight span {
  color: #5f6672;
  font-size: 15px;
  line-height: 1.6;
}

/* ========================================
   POURQUOI REJOINDRE BLOODSEN
======================================== */

.why-join {
  padding: 80px 0;
  background-color: #ffffff;
}

.why-join-heading {
  max-width: 650px;
  margin-bottom: 48px;
}

.why-join-heading h2 {
  margin: 0 0 10px;
  color: var(--bloodsen-dark);
  font-size: 38px;
  line-height: 1.2;
  font-weight: 700;
}

.why-join-heading p {
  margin: 0;
  color: #5f6672;
  font-size: 16px;
  line-height: 1.5;
}

/* Grille 2 x 2 */

.why-join-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

/* Carte */

.join-card {
  min-height: 260px;
  padding: 32px;
  background-color: #f8f9fb;
  border: 1px solid #dfe3e8;
  border-radius: 4px;
}

/* Icône */

.join-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 48px;
  height: 48px;
  margin-bottom: 20px;

  background-color: #e9ecef;
  border-radius: 4px;

  color: var(--bloodsen-red);
}

.join-icon svg {
  width: 26px;
  height: 26px;
}

/* Titre */

.join-card h3 {
  margin: 0 0 10px;

  color: #202428;
  font-size: 19px;
  line-height: 1.3;
  font-weight: 700;
}

/* Texte */

.join-card p {
  margin: 0;

  color: #5f6672;
  font-size: 16px;
  line-height: 1.5;
}
/* ========================================
   CONSEILS POUR BIEN S'INSCRIRE
======================================== */

.registration-tips {
  padding: 72px 0;
  background-color: #f4f6f8;
}

.registration-card {
  padding: 48px;
  background-color: #ffffff;
  border: 1px solid #dfe3e8;
  border-radius: 8px;
}


/* ========================================
   EN-TÊTE
======================================== */

.registration-header {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: end;
  gap: 40px;
}

.registration-label {
  display: block;
  margin-bottom: 8px;

  color: var(--bloodsen-red);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.registration-header h2 {
  margin: 0;

  color: #202428;
  font-size: 30px;
  line-height: 1.2;
  font-weight: 700;
}

.registration-header > p {
  margin: 0 0 3px;

  color: #5f6672;
  font-size: 15px;
  line-height: 1.5;
  text-align: right;
}


/* ========================================
   SÉPARATION
======================================== */

.registration-divider {
  height: 1px;
  margin: 18px 0 30px;

  background-color: #dfe3e8;
}


/* ========================================
   GRILLE DES CONSEILS
======================================== */

.tips-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  column-gap: 48px;
  row-gap: 24px;
}


/* ========================================
   CONSEIL
======================================== */

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

  width: 32px;
  height: 32px;

  background-color: #e9ecef;
  border-radius: 4px;

  color: var(--bloodsen-red);
}

.tip-icon svg {
  width: 19px;
  height: 19px;
}

.tip-content {
  flex: 1;
}

.tip-content h3 {
  margin: 1px 0 6px;

  color: #202428;
  font-size: 18px;
  line-height: 1.35;
  font-weight: 600;
}

.tip-content p {
  margin: 0;

  color: #5f6672;
  font-size: 14px;
  line-height: 1.55;
}

/* ========================================
   CONTACT
======================================== */

.contact-section {
  padding: 80px 0;
  background-color: #ffffff;
}


/* ========================================
   EN-TÊTE
======================================== */

.contact-heading {
  max-width: 620px;
  margin-bottom: 48px;
}

.contact-label {
  display: block;
  margin-bottom: 8px;

  color: var(--bloodsen-red);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.08em;
}

.contact-heading h2 {
  margin: 0 0 10px;

  color: var(--bloodsen-dark);
  font-size: 38px;
  line-height: 1.2;
  font-weight: 700;
}

.contact-heading p {
  margin: 0;

  color: #5f6672;
  font-size: 16px;
  line-height: 1.5;
}


/* ========================================
   CONTENU
======================================== */

.contact-content {
  display: grid;
  grid-template-columns: 1.35fr 0.95fr;
  gap: 32px;
  align-items: start;
}


/* ========================================
   FORMULAIRE
======================================== */

.contact-form-card {
  padding: 32px;

  background-color: #f8f9fb;
  border: 1px solid #dfe3e8;
  border-radius: 8px;
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

  margin-top: 4px;
}

.form-footer span {
  color: #5f6672;
  font-size: 13px;
}


/* ========================================
   COLONNE DROITE
======================================== */

.contact-side {
  display: flex;
  flex-direction: column;
  gap: 24px;
}


/* ========================================
   COORDONNÉES
======================================== */

.institution-card {
  padding: 28px 24px;

  background-color: #f8f9fb;
  border: 1px solid #dfe3e8;
  border-radius: 8px;
}

.institution-card h3 {
  margin: 0 0 20px;

  color: #202428;
  font-size: 20px;
  line-height: 1.3;
  font-weight: 700;
}

.institution-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;

  margin-bottom: 18px;
}

.institution-item:last-child {
  margin-bottom: 0;
}

.institution-icon {
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 22px;
  height: 22px;

  color: var(--bloodsen-red);
}

.institution-icon svg {
  width: 20px;
  height: 20px;
}

.institution-item strong {
  display: block;
  margin-bottom: 2px;

  color: #202428;
  font-size: 13px;
  font-weight: 600;
}

.institution-item p {
  margin: 0;

  color: #5f6672;
  font-size: 14px;
  line-height: 1.45;
}

.emergency-text {
  color: var(--bloodsen-red);
}


/* ========================================
   ENCADRÉ URGENCE
======================================== */

.emergency-card {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 24px;

  background-color: #f8f9fb;
  border: 1px solid #dfe3e8;
  border-radius: 8px;
}

.emergency-icon {
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 40px;
  height: 40px;

  background-color: var(--bloodsen-red);
  border-radius: 4px;

  color: #ffffff;
}

.emergency-icon svg {
  width: 22px;
  height: 22px;
}

.emergency-content {
  flex: 1;
}

.emergency-content strong {
  display: block;
  margin-bottom: 2px;

  color: #202428;
  font-size: 14px;
  font-weight: 700;
}

.emergency-content p {
  margin: 0;

  color: #5f6672;
  font-size: 12px;
  line-height: 1.4;
}


/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 992px) {

  .contact-content {
    grid-template-columns: 1fr;
  }

  .contact-side {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

}


@media (max-width: 768px) {

  .contact-section {
    padding: 60px 0;
  }

  .contact-heading h2 {
    font-size: 32px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .contact-side {
    display: flex;
  }

}


@media (max-width: 576px) {

  .contact-heading h2 {
    font-size: 28px;
  }

  .contact-form-card {
    padding: 24px 20px;
  }

  .form-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .emergency-card {
    flex-wrap: wrap;
  }

  .emergency-card :deep(button) {
    margin-left: 52px;
  }

}
/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 768px) {

  .registration-tips {
    padding: 60px 0;
  }

  .registration-card {
    padding: 32px 24px;
  }

  .registration-header {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .registration-header h2 {
    font-size: 28px;
  }

  .registration-header > p {
    text-align: left;
  }

  .tips-grid {
    grid-template-columns: 1fr;
    row-gap: 28px;
  }
}


@media (max-width: 576px) {

  .registration-card {
    padding: 24px 20px;
  }

  .registration-label {
    font-size: 12px;
  }

  .registration-header h2 {
    font-size: 25px;
  }

  .tip-content h3 {
    font-size: 17px;
  }

  .tip-content p {
    font-size: 14px;
  }
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 768px) {

  .why-join {
    padding: 60px 0;
  }

  .why-join-heading {
    margin-bottom: 36px;
  }

  .why-join-heading h2 {
    font-size: 32px;
  }

  .why-join-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .join-card {
    min-height: auto;
    padding: 28px;
  }
}


@media (max-width: 576px) {

  .why-join-heading h2 {
    font-size: 28px;
  }

  .join-card {
    padding: 24px;
  }

  .join-card p {
    font-size: 15px;
  }
}

@media (max-width: 768px) {
  .why-donate {
    padding: 60px 0;
  }

  .why-donate-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .why-donate-image img {
    height: 350px;
  }

  .why-donate-text h2 {
    font-size: 32px;
  }
}
@media (max-width: 992px) {
  .stats-content {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .stats {
    padding: 16px 0;
  }

  .stats-content {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .stat {
    padding: 14px 16px;
  }

  .stat strong {
    font-size: 24px;
  }
}
@media (max-width: 992px) {
  .steps {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .how-it-works {
    padding: 60px 0;
  }

  .section-heading h2 {
    font-size: 30px;
  }

  .steps {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .hero {
    padding: 50px 0;
  }

  .hero-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .hero-text h1 {
    font-size: 36px;
  }

  .hero-text p {
    font-size: 16px;
  }

  .hero-image img {
    height: 300px;
  }
}

@media (max-width: 576px) {
  .hero-text h1 {
    font-size: 30px;
  }

  .hero-actions {
    flex-direction: column;
  }

  .hero-actions :deep(button) {
    width: 100%;
  }
}
</style>