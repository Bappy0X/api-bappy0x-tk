from flask import Flask, jsonify, request
from flask_cors import CORS
from flaskext.markdown import Markdown

from os.path import join

from dotenv import load_dotenv
load_dotenv(override=True)
from os import getenv

from db.models import *

def create_app():
    app = Flask(__name__)

    app.jinja_env.globals.update(len=len)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)
    Markdown(app)

    from views.notifications import blueprint as notifications_blueprint
    app.register_blueprint(notifications_blueprint)

    from views.docs import auto_docs, blueprint as docs_blueprint
    auto_docs.init_app(app)
    app.register_blueprint(docs_blueprint)

    @app.route("/")
    def index():
        return jsonify({"success": True})

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=80, debug=True)