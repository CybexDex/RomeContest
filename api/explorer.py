import datetime
import json
import urllib2
import psycopg2
# from services.bitshares_websocket_client import BitsharesWebsocketClient, client as bitshares_ws_client_factory
from services.cache import cache
import config
import logging
# from pymongo import MongoClient
import json
# from bson import json_util
# from bson.objectid import ObjectId
import q,traceback


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='mydebug.log',
                filemode='w')

logger = logging.getLogger('logger')
# client = MongoClient(config.MONGODB_DB_URL)
# db = client[config.MONGODB_DB_NAME]

# logger.info(config.MONGODB_DB_URL)
# logger.info(config.MONGODB_DB_NAME)
###################### Q functions ######################

@cache.memoize(timeout= 60 )    
def get_ex_rate(): 
    qconn = q.q(host = config.Q_HOST, port = config.Q_PORT, user = config.Q_USER)
    sql = '(usdt;eth;eos)'
    try:
        res = qconn.k(str(sql))
    except:
        res = []
        logger.error(traceback.format_exc())
        logger.error(sql)
    qconn.close()
    return res

@cache.memoize(timeout= 60 )    
def portfolio_ranking(algo, limit):
    # rates = get_ex_rate() # usdt, eth, eos
    qconn = q.q(host = config.Q_HOST, port = config.Q_PORT, user = config.Q_USER)
    if algo not in ('COMP','RV','VOT'):
        return []
    if limit > 50:
        return []
    sql = 'get_ranking[%d;%s]' % (limit, algo)
    # logger.info(sql)
    try:
        res = qconn.k(str(sql))
    except:
        res = []
        logger.error(traceback.format_exc())
        logger.error(sql)
    qconn.close()
    # return map(lambda x:{'account':x[0], 'value':x[1], 'cap':x[2]  } , list(res))
    if algo == 'COMP':
        return map(lambda x:{'account':x[0], 'rv':x[1], 'sharp':x[2], 'cap':x[3], 'comp':x[4]  } , list(res))
    else:
        return map(lambda x:{'account':x[0], 'rv':x[1], 'sharp':x[2], 'cap':x[3]  } , list(res))


@cache.memoize(timeout= 60 )    
def get_portfolio_account(account, slot): # sloc is minute
    if slot < 1:
        return ['error: slot must >0, please change your slot!']
    qconn = q.q(host = config.Q_HOST, port = config.Q_PORT, user = config.Q_USER)
    sql = 'getPortfolio["%s";%d]' % (account,slot)
    try:
        res = qconn.k(str(sql))
    except:
        res = []
        logger.error(traceback.format_exc())
        logger.error(sql)
    qconn.close()
    return map(lambda x:{'time':x[0], 'usdt':x[1], 'eth':x[2], 'eos':x[3], 'cap':x[4]  } , list(res))

