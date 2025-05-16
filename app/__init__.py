from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_restx import Api
from flask_migrate import Migrate
from pymysql import install_as_MySQLdb
import logging

# CONFIG LOGGING
logging.basicConfig(
    level=logging.INFO
)

# INSTALL MYSQL_DB
install_as_MySQLdb()

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

    #REGISTER BLUE_PRINT TO ROUTER
    from app.apis.v1.authen_api import authen_api
    from app.apis.v1.user_api import user_api
    from app.apis.v1.profile_api import profile_api
    app.register_blueprint(authen_api,  url_prefix='/api/auth')
    app.register_blueprint(user_api, url_prefix='/api/user')
    app.register_blueprint(profile_api, url_prefix='/api/profiles')

    # CHECK LOGIN DATABASE AND IMPORT CLASS TO MIGRATE DATABASE
    from app.models import User, Profile, Notification, Interaction, ProfileImage, Block, Conversation, Message
    with app.app_context():
        try:
            with db.engine.connect() as connect:
                connect.execute(text("SELECT 1"))
                logging.info("-----> CONNECT DATABASE SUCCESSFULL!")
        except Exception as e:
            logging.error(f"------> CONNECT DATABASE ERROR! ----- LOG: {e}")
    return app