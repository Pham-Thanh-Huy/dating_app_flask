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
    from app.apis.v1.interaction_api import interaction_api
    from app.apis.v1.conversation_api import conversation_api
    from app.apis.v1.block_api import block_api
    from app.apis.v1.notification_api import notification_api
    from app.apis.v1.location_api import location_api

    app.register_blueprint(authen_api,  url_prefix='/api/auth')
    app.register_blueprint(user_api, url_prefix='/api/user')
    app.register_blueprint(profile_api, url_prefix='/api/profiles')
    app.register_blueprint(interaction_api, url_prefix='/api/interactions')
    app.register_blueprint(conversation_api, url_prefix='/api/conversations')
    app.register_blueprint(block_api, url_prefix='/api/blocks')
    app.register_blueprint(notification_api, url_prefix='/api/notifications')
    app.register_blueprint(location_api, url_prefix='/api/locations')

    # CHECK LOGIN DATABASE AND IMPORT CLASS TO MIGRATE DATABASE
    from app.models import User, Profile, Notification, Interaction, ProfileImage, Block, Conversation, Message, Location
    with app.app_context():
        try:
            with db.engine.connect() as connect:
                connect.execute(text("SELECT 1"))
                logging.info("-----> CONNECT DATABASE SUCCESSFULL!")
        except Exception as e:
            logging.error(f"------> CONNECT DATABASE ERROR! ----- LOG: {e}")
    return app