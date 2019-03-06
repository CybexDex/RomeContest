from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId

import sys,logging,ba_config,os
import zmq,time


#  Socket to talk to server
# socket.connect("tcp://localhost:"+ sys.argv[1])
#socket.connect(sys.argv[1])

# Subscribe to zipcode, default is NYC, 10001
# zip_filter = 'bitsharzmq-balance'
# zip_filter = zip_filter.decode('utf8')
# socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
import json, datetime
from datetime import datetime

client = MongoClient(ba_config.MONGODB_DB_URL)
db = client[ba_config.MONGODB_DB_NAME]

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='mongo.log',
                filemode='w')

enable_asset_filter = False
# Process 5 updates
class zmq2mongoObjectCommonClient():
    def __init__(self, target, topic):
        # self.qscript = ba_config.qscript
        # os.system('nohup /home/sunqi/q/l32/q /home/sunqi/mysrc/kdbSync.qpy/src/qscript/contest.q -p %d -u /home/sunqi/qtest/pass > /dev/null 2>&1 &'%(ba_config.port)  )
        self.zip_filter = topic
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(target)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.zip_filter)
        self.filter_assets = []
        self.logger = logging.getLogger('zmq2mongoObjecsClients')
    def update(self, j):
        try:
            if self.zip_filter == 'bitsharzmq-limitorder':
                db.limitorders.insert_one(j)
            if self.zip_filter == 'bitsharzmq-account':
                db.accounts.insert_one(j)
            if self.zip_filter == 'bitsharzmq-asset':
                db.assets.insert_one(j)
            if self.zip_filter == 'bitsharzmq-accbalance':
                _k = j['object_id']
                db.accbalances.update_one( { "object_id" : _k }, {'$set':j}, upsert = True)
        except:
            self.logger.error('failed to update json: ' + str(j) )
    def run(self):
        while 1:
            string = self.socket.recv_multipart()[0].decode('latin1').encode('utf8')
            try:
                obj = json.loads(string.split(' ')[1])
            except:
                self.logger.error('failed to load from recv: ' + string )
                continue
            self.logger.info('dealt object_id: ' + obj['object_id'] + ' ...')
            if enable_asset_filter and obj.get('asset_id','null') not in self.filter_assets:
                continue
            if self.zip_filter == 'bitsharzmq-accbalance':
                obj['amount'] = float(obj['amount'] )
            self.update(obj)

   
class zmq2mongoObjecsClient():
    def __init__(self, target):
        # self.qscript = ba_config.qscript
        # os.system('nohup /home/sunqi/q/l32/q /home/sunqi/mysrc/kdbSync.qpy/src/qscript/contest.q -p %d -u /home/sunqi/qtest/pass > /dev/null 2>&1 &'%(ba_config.port)  )
        zip_filter = u'bitsharzmq-accbalance'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(target)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
        self.filter_assets = []
        self.logger = logging.getLogger('zmq2mongoObjecsClient')
    def update(self, j):
        try:
            db.objects.insert_one(j)
        except:
            self.logger.error('failed to update json: ' + j)
    def run(self):
        while 1:
            string = self.socket.recv_multipart()[0].decode('latin1').encode('utf8')
            try:
                obj = json.loads(string.split(' ')[1])
            except:
                self.logger.error('failed to load from recv: ' + string )
                continue
            self.logger.info('dealt object_id: ' + obj['object_id'] + ' ...')
            if enable_asset_filter and obj['asset_id'] not in self.filter_assets:
                continue
            obj['amount'] = float(obj['amount'] )
            self.update(obj)

class zmq2mongoHistoryClient():
    def __init__(self, target, op = 4):
        # self.qscript = ba_config.qscript
        # os.system('nohup /home/sunqi/q/l32/q /home/sunqi/mysrc/kdbSync.qpy/src/qscript/contest.q -p %d -u /home/sunqi/qtest/pass > /dev/null 2>&1 &'%(ba_config.port)  )
        zip_filter = u'history'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(target)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
        self.filter_assets = []
        self.logger = logging.getLogger('zmq2mongoHistoryClient')
        self.op = op
    def update_contest(self, j):
        try:
            db.contest_history.insert_one(j)
        except:
            self.logger.error('failed to update json: ' + j)
    def update(self, j):
        try:
            db.history.insert_one(j)
        except:
            self.logger.error('failed to update json: ' + j)
    def run(self):
        while 1:
            string = self.socket.recv_multipart()[0].decode('latin1').encode('utf8')
            try:
                obj = json.loads(string.split(' ')[1])
                if self.op != None and obj['bulk']['operation_type'] != self.op:
                    continue
                obj['op'] = json.loads(obj['op'])
                obj['result'] = json.loads(obj['result'])
            except:
                self.logger.error('failed to load from recv: ' + string )
                continue
            self.logger.info('dealt object_id: ' + obj['object_id'] + '...')
            if enable_asset_filter and (obj['op']['fill_price']['base']['asset_id'] not in self.filter_assets or obj['op']['fill_price']['quote']['asset_id'] not in self.filter_assets):
                continue
            # obj['amount'] = float(obj['amount'] )
            self.update_contest(obj)

