from app import app
import logging

if __name__ == '__main__':
    logging.basicConfig(format=app.config['LOG_FORMAT'], level=logging.DEBUG)
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'], threaded=True)
