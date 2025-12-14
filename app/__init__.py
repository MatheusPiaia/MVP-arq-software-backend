from flask_openapi3 import OpenAPI, Info
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    info = Info(title="Minha API", version="1.0.0")
    app = OpenAPI(__name__, info=info)
    app.url_map.strict_slashes = False

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@db:5432/mydb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)

    from app.routes.main_routes import main_bp
    from app.routes.product_routes import product_bp
    from app.routes.stock_routes import stock_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.conditional_routes import conditional_bp

    app.register_api(main_bp)
    app.register_api(product_bp)
    app.register_api(stock_bp)
    app.register_api(customer_bp)
    app.register_api(conditional_bp)

    from app.models import(
        user, role, product,
        product_stock, customer,
        conditional, conditional_item,
        api_products_cache
    )  # importa models

    return app