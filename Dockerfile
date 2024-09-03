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
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définit le répertoire de travail dans le conteneur
WORKDIR /bookquest

# Copie uniquement le fichier requirements.txt
COPY requirements.txt .

# Installe les dépendances du projet
RUN pip3 install --no-cache-dir -r requirements.txt

# Copie uniquement le contenu du dossier app dans le conteneur
COPY bookquest/app ./app
COPY bookquest/images ./images

COPY bookquest/tests ./tests

# Expose le port 5000 (par défaut pour Flask)
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "app/__init__.py"]
