import os

# Q_HOST = os.environ.get('Q_HOST_ADDR','localhost')
Q_HOST = os.environ.get('Q_HOST_ADDR','39.105.55.115')
Q_PORT = os.environ.get('Q_PORT', 8085)
Q_USER= os.environ.get('Q_USER', 'sunqi:sunqi123')


#WEBSOCKET_URL = os.environ.get('WEBSOCKET_URL', "ws://47.75.208.12:8090/")
# WEBSOCKET_URL2 = os.environ.get('WEBSOCKET_URL', "ws://47.75.208.12:8090/")
# FULL_WEBSOCKET_URL = os.environ.get('FULL_WEBSOCKET_URL', "ws://47.75.208.12:8090/")

# MONGODB_DB_URL = os.environ.get('MONGO_WRAPPER', "mongodb://yoyo:yoyo123@127.0.0.1:27017/cybex") # clockwork
# MONGODB_DB_NAME = os.environ.get('MONGO_DB_NAME', 'cybex')

# Cache: see https://flask-caching.readthedocs.io/en/latest/#configuring-flask-caching
CACHE = {
    'CACHE_TYPE': os.environ.get('CACHE_TYPE', 'simple'),
    'CACHE_DEFAULT_TIMEOUT': int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 600)) # 10 min
}

# Configure profiler: see https://github.com/muatik/flask-profiler
PROFILER = {
    'enabled': os.environ.get('PROFILER_ENABLED', False),
    'username': os.environ.get('PROFILER_USERNAME', None),
    'password': os.environ.get('PROFILER_PASSWORD', None),
}

# CORE_ASSET_SYMBOL = 'BTS'
CORE_ASSET_SYMBOL = 'CYB'
CORE_ASSET_ID = '1.3.0'

TESTNET = 0 # 0 = not in the testnet, 1 = testnet
CORE_ASSET_SYMBOL_TESTNET = 'TEST'
