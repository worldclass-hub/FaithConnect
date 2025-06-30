import os
import sys
from gunicorn.app.wsgiapp import run

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doxcela.settings")
    port = os.environ.get("PORT", "8000")
    sys.argv = [
        "gunicorn",
        "doxcela.wsgi:application",  # ← Make sure this matches your project folder
        "--bind",
        f"0.0.0.0:{port}"
    ]
    run()
