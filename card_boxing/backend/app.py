from flask import Flask
from flask_cors import CORS
from api.routes import api
from database.game_db import init_db

def create_app():
    app = Flask(__name__, static_folder='static')

    CORS(app)  # libera acesso do React

    init_db()

    app.register_blueprint(api, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
