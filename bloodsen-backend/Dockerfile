# Utilise une image officielle contenant Python 3.12.
# "slim" signifie que l'image est allégée pour prendre moins de place.
FROM python:3.12-slim


# Définit le dossier de travail à l'intérieur du conteneur.
# Toutes les commandes suivantes seront exécutées depuis /app.
WORKDIR /app


# Empêche Python de créer des fichiers .pyc
# (fichiers contenant du bytecode Python).
ENV PYTHONDONTWRITEBYTECODE=1 \

    # Force Python à afficher immédiatement les logs
    # dans le terminal, sans les mettre en mémoire tampon.
    PYTHONUNBUFFERED=1


# Met à jour la liste des paquets disponibles dans Debian.
# Puis installe les dépendances système nécessaires.
RUN apt-get update && apt-get install -y --no-install-recommends \

    # libpq-dev : bibliothèque nécessaire pour certaines
    # connexions Python à PostgreSQL, notamment avec psycopg.
    # gcc : compilateur nécessaire pour compiler certains
    # paquets Python lors de leur installation.
    libpq-dev gcc \

    # Supprime les listes de paquets téléchargées par apt.
    # Cela permet de réduire la taille finale de l'image.
    && rm -rf /var/lib/apt/lists/*


# Copie le fichier requirements.txt depuis ton ordinateur
# vers le dossier /app du conteneur.
COPY requirements.txt .


# Installe toutes les dépendances Python
# listées dans requirements.txt.
# --no-cache-dir évite de conserver le cache de pip,
# ce qui permet de réduire la taille de l'image.
RUN pip install --no-cache-dir -r requirements.txt


# Copie tous les fichiers du projet actuel
# dans le dossier /app du conteneur.
# Exemple : manage.py, config/, apps/, etc.
COPY . .


# Indique que l'application utilise le port 8000.
# Cela sert principalement de documentation pour Docker.
EXPOSE 8000


# Commande exécutée automatiquement lorsque le conteneur démarre.
# Lance le serveur de développement Django.
# 0.0.0.0 permet au serveur d'être accessible depuis l'extérieur
# du conteneur, notamment via le port publié par Docker.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]