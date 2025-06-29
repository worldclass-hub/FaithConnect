import os
from doxcela.wsgi import application
from gunicorn.app.wsgiapp import run

if __name__ == '__main__':
    port = os.environ.get("PORT", "8000")
    run(["gunicorn", "doxcela.wsgi:application", "--bind", f"0.0.0.0:{port}"])
