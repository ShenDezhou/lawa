import argparse
import logging
import sys
import time

import falcon
from falcon_cors import CORS
import json
import waitress
import lawa

if sys.hexversion < 0x03070000:
    ft = time.process_time
else:
    ft = time.process_time_ns
    
logging.basicConfig(level=logging.INFO, format='%(asctime)-18s %(message)s')
logger = logging.getLogger()
cors_allow_all = CORS(allow_all_origins=True,
                      allow_origins_list=['*'],
                      allow_all_headers=True,
                      allow_all_methods=True,
                      allow_credentials_all_origins=True
                      )

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', '--config_file', default='config/bert_config.json',
    help='model config file')
parser.add_argument(
    '-p', '--port', default=58086,
    help='falcon server port')
parser.add_argument(
    '-m', '--for_search', default=1,
    help='falcon server port')
args = parser.parse_args()
model_config = args.config_file


class TorchResource:

    def __init__(self):
        logger.info("...")
        self.cut = lawa.cut
        self.cut_search = lawa.cut_for_search
        #早加载
        logger.info(list(self.cut_search("中国人民")))
        logger.info("###")

    def process_context(self, line):
        start = ft()
        if int(args.for_search):
            words = self.cut_search(line)
        else:
            words = self.cut(line)
        words = [{'word':word} for word in words]
        logger.info("cut:{}ns".format(ft() - start))
        return {'data':words}

    def on_get(self, req, resp):
        logger.info("...")
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        line = req.get_param('text', True)
        # mode = req.get_param('mode', default=0)
        resp.media = self.process_context(line)
        logger.info("###")

    def on_post(self, req, resp):
        """Handles POST requests"""
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        resp.set_header("Cache-Control", "no-cache")
        start = ft()
        jsondata = json.loads(req.stream.read(req.content_length))
        line=jsondata['text']
        # mode = jsondata.get('mode', 0)
        resp.media = self.process_context(line)
        logger.info("tot:{}ns".format(ft() - start))
        logger.info("###")


if __name__ == "__main__":
    api = falcon.API(middleware=[cors_allow_all.middleware])
    api.req_options.auto_parse_form_urlencoded = True
    api.add_route('/z', TorchResource())
    waitress.serve(api, port=args.port, threads=48, url_scheme='http')
