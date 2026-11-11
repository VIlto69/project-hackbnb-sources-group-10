#!/bin/sh
set -e
# Apache démarre en root pour écouter le port 80, puis ses workers passent en www-data
apache2ctl -D FOREGROUND &

# [D2] Le backend tourne avec l'utilisateur non privilégié "hackbnb"
# [Bonus] gunicorn au lieu du serveur de développement Flask (pas de mode debug)
# [D8] Écoute uniquement en local : seul Apache est exposé
exec runuser -u hackbnb -- gunicorn --bind 127.0.0.1:9001 --workers 2 app:app
