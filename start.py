import os
from gunicorn.app.wsgiapp import WSGIApplication

if __name__ == "__main__":
    port = os.getenv("PORT", "8000")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doxcela.settings")  # Replace if your settings file path is different
    app = WSGIApplication()
    app.run(bind=f"0.0.0.0:{port}", args=["gunicorn", "doxcela.wsgi:application"])
