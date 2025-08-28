from flask import Flask


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #
    # Importa e registra Blueprints
    from app.routes.route_main import main_bp
    app.register_blueprint(main_bp)
    
    return app