import datetime
import json
import urllib2
import psycopg2
# from services.bitshares_websocket_client import BitsharesWebsocketClient, client as bitshares_ws_client_factory
from services.cache import cache
import config
import logging
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId
import q,traceback


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='mydebug.log',
                filemode='w')

# client = MongoClient(config.MONGODB_DB_URL)
# db = client[config.MONGODB_DB_NAME]
logger.addHandler(logHandler)

# logger.info(config.MONGODB_DB_URL)
# logger.info(config.MONGODB_DB_NAME)
###################### Q functions ######################

@cache.memoize(timeout= 5 )    
def get_ex_rate(): # base as usdt
    return [1,1,1]
    pass
@cache.memoize(timeout= 5 )    
def portfolio_ranking(algo, limit):
    rates = get_ex_rate() # usdt, eth, eos
    qconn = q.q(host = config.Q_HOST, port = config.Q_PORT, user = config.Q_USER)
    if algo not in ('COMP','RV','VOT'):
        return []
    duration = str(duration)
    if limit > 100 :
        return []
    tbname = '_'.join(['top',algo])
    sql = 'get_ranking[%d;%s;%f;%f;%f]' % (limit, algo, rates[0], rates[1], rates[2])
    try:
        res = qconn.k(str(sql))
    except:
        re = []
        logger.error(traceback.format_exc())
        logger.error(sql)
    qconn.close()
    return map(lambda x:{'account':x[0], 'value':x[1]  } , list(res))


