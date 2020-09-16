import argparse
import logging
import time

import falcon
from falcon_cors import CORS
import json
import waitress
import lawa

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
args = parser.parse_args()
model_config = args.config_file


class TorchResource:

    def __init__(self):
        logger.info("...")
        self.cut = lawa.cut_for_search
        logger.info("###")

    def process_context(self, line):
        start = time.process_time_ns()
        words = self.cut(line)
        words = [{'word':word} for word in words]
        logger.info("cut:{}ns".format(time.process_time_ns() - start))
        return {'data':words}

    def on_get(self, req, resp):
        logger.info("...")
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        line = req.get_param('text', True)
        resp.media = self.process_context(line)
        logger.info("###")

    def on_post(self, req, resp):
        """Handles POST requests"""
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Allow-Credentials', 'true')
        resp.set_header("Cache-Control", "no-cache")
        start = time.process_time_ns()
        jsondata = json.loads(req.stream.read(req.content_length))
        line=jsondata['text']
        resp.media = self.process_context(line)
        logger.info("tot:{}ns".format(time.process_time_ns() - start))
        logger.info("###")


if __name__ == "__main__":
    api = falcon.API(middleware=[cors_allow_all.middleware])
    api.req_options.auto_parse_form_urlencoded = True
    api.add_route('/z', TorchResource())
    waitress.serve(api, port=58086, threads=48, url_scheme='http')
