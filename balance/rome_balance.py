
import sys,q,logging,ba_config,os
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



logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='zmq.log',
                filemode='w')

logger = logging.getLogger('logger')
enable_asset_filter = False
# Process 5 updates
class zmqClient():
    def __init__(self, target):
        # self.qscript = ba_config.qscript
        cmd = 'nohup /home/sunqi/q/l32/q /home/sunqi/mysrc/kdbSync.qpy/src/qscript/contest.q -p %d -u /home/sunqi/qtest/pass > /dev/null 2>&1 &'%(ba_config.port)  
        logger.info(cmd)
        os.system('nohup /home/sunqi/q/l32/q /home/sunqi/mysrc/kdbSync.qpy/src/qscript/contest.q -p %d -u /home/sunqi/qtest/pass > /dev/null 2>&1 &'%(ba_config.port)  )
        time.sleep(3)
        self.qcon = q.q(host = 'localhost', port = ba_config.port, user = ba_config.user)
        zip_filter = u'bitsharzmq-accbalance'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(target)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
        self.filter_assets = []
    def update(self, j):
        try:
            self.qcon.k('json2k: ' + j +'; eleUpdate[json2k];')
        except:
            logger.error('failed to update json: ' + j)
    def run(self):
        date = None
        while 1:
            string = self.socket.recv_multipart()[0].decode('latin1').encode('utf8')
            try:
                obj = json.loads(string.split(' ')[1])
            except:
                logger.error('failed to load from recv: ' + string )
                continue
            logger.info('dealt object_id: ' + obj['object_id'] + ' ...')
            if enable_asset_filter and obj['asset_id'] not in self.filter_assets:
                continue
            obj['amount'] = float(obj['amount'] )
            j = json.dumps(json.dumps(obj))
            self.update(j)
   
    # obj = {u'asset_id': u'1.3.0', u'block_number': 434451, u'object_id': u'1.15.50', u'amount': u'125000000000', u'block_time': u'2018-03-13T08:18:45', u'owner': u'CYBDBpNEqZMiUtx7iJMK16dQXmX4bC3ZeUyx'}
    
if __name__ == '__main__':
    c = zmqClient('tcp://localhost:8084')
    c.run()
