# Imports 
from flask import Flask, render_template
from backend.api.routes import api
from backend.database.operations import *

app = Flask(__name__)

setup_database()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)