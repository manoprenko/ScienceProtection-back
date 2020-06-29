import json
import os
import threading


class HashStorage:
    def __init__(self, file_name):
        self.file_name = file_name
        self.mutex = threading.Lock()

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
