# Utilise une image Node.js version 20, basée sur Alpine Linux.
# Alpine est une distribution Linux légère, ce qui permet d'avoir une image Docker moins volumineuse.
FROM node:20-alpine


# Définit le dossier de travail à l'intérieur du conteneur.
# Toutes les commandes suivantes seront exécutées depuis /app.
WORKDIR /app


# Copie les fichiers package.json et package-lock.json
# depuis le projet local vers le dossier /app du conteneur.
#
# Le symbole * permet de copier :
# - package.json
# - package-lock.json, s'il existe
COPY package*.json ./


# Installe les dépendances Node.js du projet.
# Les dépendances sont définies dans package.json.
# Le résultat est généralement placé dans le dossier node_modules.
RUN npm install


# Copie tous les fichiers du projet local
# vers le dossier /app du conteneur.
#
# Le premier "." représente le dossier actuel sur la machine.
# Le deuxième "." représente le dossier /app dans le conteneur.
COPY . .


# Indique que l'application utilise le port 5173.
# Ce port est généralement utilisé par Vite pour le serveur de développement.
#
# EXPOSE ne publie pas réellement le port.
# Il sert principalement à documenter le port utilisé par le conteneur.
EXPOSE 5173


# Commande exécutée automatiquement lorsque le conteneur démarre.
#
# npm run dev :
# Lance le serveur de développement défini dans package.json.
#
# -- :
# Indique que les arguments suivants doivent être transmis à la commande npm.
#
# --host 0.0.0.0 :
# Rend le serveur accessible depuis l'extérieur du conteneur.
# Sans cette option, Vite peut écouter uniquement sur localhost
# à l'intérieur du conteneur, ce qui empêcherait l'accès depuis le navigateur.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]