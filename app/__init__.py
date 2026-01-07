from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config.from_prefixed_env()  # opcional, si usas variables de entorno

    # Registrar rutas
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
