from flask import Flask
from copy import deepcopy
import logging
import traceback
import yaml


def import_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    config = data['config']
    cfg = deepcopy(config)
    return cfg


app = Flask('moop-project-service')
config = import_config()
for cfg in config:
    app.config[cfg] = config[cfg]


def register_blueprint():
    from application.project import projects
    app.register_blueprint(projects)


register_blueprint()


@app.route('/')
def index():
    from auth import raise_status
    return raise_status(200)


@app.errorhandler(Exception)
def error_handler(error):
    logging.error('Request Error: {}\nStack: {}\n'.format(error, traceback.format_exc()))
    return 'PROJECT-SERVICE 未知错误', 500
