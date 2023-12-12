from flask import Flask
from flask_jwt_extended import JWTManager 
from flask_restful import Api
from config import Config
from resources.movie import MovieListResource
from resources.user import  UserRegisterResource,UserLoginResource, UserLogoutResource

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

api = Api(app)

api.add_resource( UserRegisterResource, '/user/register')
api.add_resource( UserLoginResource, '/user/login')
api.add_resource( UserLogoutResource, '/user/logout')
api.add_resource (MovieListResource, '/movie')


if __name__ == '__main__':
    app.run()