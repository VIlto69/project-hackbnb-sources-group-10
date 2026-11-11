import os
import re
from flask import Blueprint, request, send_from_directory, abort

uploads_api = Blueprint('uploads', __name__)

# [D2] Dossier absolu des uploads + format de nom strict
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')
SAFE_FILENAME = re.compile(r'^[A-Za-z0-9_-]{1,64}\.(jpg|jpeg|png|webp)$')


@uploads_api.route('/')
def get_upload():
   name = request.args.get("name", "")

   # [D2] Refus de tout nom qui ne respecte pas le format attendu (pas de "/", pas de "..")
   if not SAFE_FILENAME.fullmatch(name):
      abort(404)

   # [D2] send_from_directory refuse en plus toute sortie du dossier (safe_join)
   return send_from_directory(os.path.realpath(UPLOADS_DIR), name)
