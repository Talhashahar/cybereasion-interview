import app_utils
from app_utils import config
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    users = app_utils.get_manipulate_docs()
    return render_template('index.html', users=users)


if __name__ == '__main__':
    app_utils.run_mongo_docker()
    app.run(host=config['flask']['hostname'], port=config['flask']['port'], threaded=True)


