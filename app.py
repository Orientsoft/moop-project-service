from flask import Flask
from optparse import OptionParser
import yaml


def import_config():
    parser = OptionParser()
    parser.add_option('-f', '--file', action='store', type='string', dest='filename')
    option, args = parser.parse_args()
    f = open(option.filename)
    data = yaml.load(f)
    f.close()
    config = data['config']
    cfg = {
        'HOST': config['HOST'],
        'PORT': config['PORT'],
        'DEBUG': config['DEBUG'],
        'SECRET_KEY': config['SECRET_KEY'],
        'MONGODB_URL': config['MONGODB_URL'],
        'LOG_FORMAT': config['LOG_FORMAT'],
        'MOOP_TENANT_SERVICE_URL': config['MOOP_TENANT_SERVICE_URL'],
        'MOOP_PROJECT_SERVICE_URL': config['MOOP_PROJECT_SERVICE_URL']
    }
    return cfg


app = Flask('moop-project-service')
config = import_config()
for cfg in config:
    app.config[cfg] = config[cfg]


def register_blueprint():
    from application.project import projects
    app.register_blueprint(projects, url_prefix='/service/v1')


register_blueprint()


@app.route('/')
def index():
    from auth import raise_status
    return raise_status(200)
