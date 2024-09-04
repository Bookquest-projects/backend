# Utilise une image de base Python 3.11
FROM python:3.11-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    pkg-config \
    libzbar0 \
    libgl1 \
    libglib2.0-0 \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Définit le répertoire de travail dans le conteneur
WORKDIR /backend

# Copie uniquement le fichier requirements.txt
COPY requirements.txt /app

# Installe les dépendances du projet
RUN pip3 install --no-cache-dir -r requirements.txt

# Copie uniquement le contenu du dossier app dans le conteneur
<<<<<<< HEAD
COPY bookquest/app /app
COPY bookquest/tests /app
=======
COPY bookquest/app ./bookquest/app
COPY bookquest/tests ./bookquest/tests
>>>>>>> d17d4fde3b7ebd1ad5205da22745ade972d44ca3

# Expose le port 5000 (par défaut pour Flask)
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "/backend/bookquest/app/__init__.py"]
