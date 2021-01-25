import logging, sys
from flask_restful import Api
from logging.handlers import RotatingFileHandler
from cachelib import SimpleCache
from blueprints import app, manager
from data.seeder import seeder

cache = SimpleCache()
api = Api(app, catch_all_404s=True)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'db':
            manager.run()

        # To seed
        elif sys.argv[1] == 'seed':
            seeder()

    # define log format and create a rotating log with max size of 10MB and max backup to 10 files 
    except Exception as e:
        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

        log_handler = RotatingFileHandler("%s/%s" % (app.root_path, '../storage/log/app.log'), maxBytes=1000000000, backupCount=10)

        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)

        app.run(debug=False, host='0.0.0.0', port=9000)