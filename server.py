import json
import os
import time
import threading

from flask import Flask, request
from web3 import Web3
from contract import compiled_sol


class Storage:
    def __init__(self, file_name):
        self.file_name = file_name
        self.mutex = threading.Lock()
        self.web3 = Web3(Web3.HTTPProvider(ethereum_url))
        self.account = self.web3.eth.account.privateKeyToAccount(priv_key)
        self.bytecode = compiled_sol['contracts']['HashStorage.sol']['HashStorage']['evm']['bytecode']['object']
        self.abi = json.loads(compiled_sol['contracts']['HashStorage.sol']['HashStorage']['metadata'])['output']['abi']
        self.contract = self.web3.eth.contract(address=self.web3.toChecksumAddress(contract_address), abi=self.abi)
        self.threads = []

    def get_timestamp(self, h):
        self.mutex.acquire()
        if os.path.exists(self.file_name):
            data = json.loads(open(self.file_name).read())
        else:
            data = {}

        res = data.get(h)
        self.mutex.release()
        return res

    def set_timestamp(self, h, t):
        self.mutex.acquire()
        if os.path.exists(self.file_name):
            data = json.loads(open(self.file_name).read())
        else:
            data = {}

        data[h] = t

        open(self.file_name, 'w').write(json.dumps(data))
        self.threads.append(threading.Thread(target=self.contract.functions.registerHash(123456789).transact))
        self.threads[-1].run()
        self.mutex.release()

    def get_all_hashes(self):
        self.mutex.acquire()
        if os.path.exists(self.file_name):
            data = json.loads(open(self.file_name).read())
        else:
            data = {}

        res = list(data)
        self.mutex.release()
        return res


app = Flask(__name__)
storage = Storage('data.json')


@app.route('/registerHash', methods=['POST'])
def register_hash():
    req = request.get_json(force=True)

    if 'hash' not in req:
        return json.dumps({'error': 'no hash specified'}), 400

    h = req['hash']
    t = time.time()

    if storage.get_timestamp(h) is not None:
        return json.dumps({'error': 'hash has been already registered'}), 403
    storage.set_timestamp(h, t)

    return json.dumps({'timestamp': str(t)}), 200


@app.route('/checkHash', methods=['POST'])
def check_hash():
    req = request.get_json(force=True)

    if 'hash' not in req:
        return json.dumps({'error': 'no hash specified'}), 400

    h = req['hash']

    t = storage.get_timestamp(h)

    if t is not None:
        return json.dumps({'result': 'ok', 'timestamp': str(t)}), 200
    else:
        return json.dumps({'result': 'not found'}), 404


@app.route('/getAllHashes', methods=['GET'])
def get_all_hashes():
    hashes = list(map(str, storage.get_all_hashes()))
    return json.dumps({'hashes': hashes}), 200