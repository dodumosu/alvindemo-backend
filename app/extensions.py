# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_security import Security
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

api = Api()
cors = CORS()
csrf = CSRFProtect()
# don't automatically flush SQLAlchemy sessions
db = SQLAlchemy(session_options={"autoflush": False})
jwt_manager = JWTManager()
limiter = Limiter(key_func=get_remote_address)
security = Security()
talisman = Talisman()
