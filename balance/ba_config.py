
import os

port=8085
user='sunqi:sunqi123'

MONGODB_DB_URL_READ = os.environ.get('MONGO_WRAPPER', "mongodb://yoyo:yoyo123@127.0.0.1:27017/cybex") # clockwork
MONGODB_DB_URL = os.environ.get('MONGO_WRAPPER', "mongodb://sunqi:sunqi123@127.0.0.1:27017/cybex") # clockwork
MONGODB_DB_NAME = os.environ.get('MONGO_DB_NAME', 'cybex')



