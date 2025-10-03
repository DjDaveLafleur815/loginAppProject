# Stage 1 : build Flutter Web
FROM debian:latest AS build-env

# Installer les dépendances de base
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    unzip \
    gdb \
    libstdc++6 \
    libglu1-mesa \
    fonts-droid-fallback \
    lib32stdc++6 \
    python3 \
    && apt-get clean

# Installer Flutter
RUN git clone https://github.com/flutter/flutter.git /usr/local/flutter
ENV PATH="/usr/local/flutter/bin:/usr/local/flutter/bin/cache/dart-sdk/bin:${PATH}"

# Configurer Flutter
RUN flutter doctor -v
RUN flutter channel master
RUN flutter upgrade
RUN flutter config --enable-web

# Build de l'application
WORKDIR /app
COPY . /app
RUN flutter pub get
RUN flutter build web

# Stage 2 : serveur Nginx
FROM nginx:latest
COPY --from=build-env /app/build/web /usr/share/nginx/html

# sudo docker build -t GUI . && sudo docker run --rm -p 1200:80 GUI