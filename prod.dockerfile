# Build React front-end
FROM node:22 AS frontend
WORKDIR /app
COPY front .
# [D9] Build de production, sans source maps
RUN npm ci && npm run build && find dist -name "*.map" -delete

# Setup Flask back-end
FROM python:3

COPY --from=frontend /app/dist /var/www/html

# Install Apache
RUN apt update && apt install -y apache2 && a2enmod proxy proxy_http rewrite headers \
    && rm -rf /var/lib/apt/lists/*
COPY apache/apache-prod.conf /etc/apache2/sites-enabled/000-default.conf

# [D8] Pas de version dans l'en-tête Server ni dans les pages d'erreur
RUN printf "ServerTokens Prod\nServerSignature Off\nTraceEnable Off\n" > /etc/apache2/conf-enabled/zz-hardening.conf

# [D2] Utilisateur dédié sans privilèges pour le backend
RUN useradd --system --no-create-home --shell /usr/sbin/nologin hackbnb

# Start back-end
WORKDIR /app
COPY back .
RUN pip3 install --no-cache-dir -r requirements.txt \
    && chown -R root:root /app \
    && mkdir -p /app/instance \
    && chown hackbnb:hackbnb /app/instance
# Le code et les uploads restent en lecture seule pour hackbnb ; seule la base (instance/) est modifiable

COPY prod.entrypoint.sh /app/
RUN chmod 755 /app/prod.entrypoint.sh
ENTRYPOINT ["/app/prod.entrypoint.sh"]
