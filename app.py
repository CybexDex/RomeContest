import connexion

options = {'swagger_url': '/apidocs'}
app = connexion.FlaskApp('bitshares-explorer-api', options=options)

from flask_cors import CORS
CORS(app.app)

from services.cache import cache
cache.init_app(app.app)

app.add_api('api.yaml')

import services.profiler
services.profiler.init_app(app.app)

application = app.app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 8082, use_reloader=True)


