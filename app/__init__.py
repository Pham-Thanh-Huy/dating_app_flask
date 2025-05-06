from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_restx import Api
from flask_migrate import Migrate
from pymysql import install_as_MySQLdb
import logging

# INSTALL MYSQL_DB
install_as_MySQLdb()

# CONFIG log
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CONFIG DATABASE AND SWAGGER API
db = SQLAlchemy()
migrate = Migrate()
api = Api(title="API-APP-DATTING", version="1.0", description="API for app datting")


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)
    api.init_app(app)

    #MIGRATE DATABASE
    migrate.init_app(app, db)
    from app.models import User

    with app.app_context():
        try:
            with db.engine.connect() as connect:
                connect.execute(text("SELECT 1"))
                logger.info("-----> CONNECT DATABASE SUCCESSFULL!")
        except Exception as e:
            logger.error(f"------> CONNECT DATABASE ERROR! ----- LOG: {e}")
    return app
