from flask import Flask
from flask_cors import CORS
from api.routes import api  # ajuste o caminho conforme sua pasta

def create_app():
    app = Flask(__name__)
    CORS(app)  # libera acesso do React

    app.register_blueprint(api, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
