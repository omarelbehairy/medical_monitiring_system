import redis
import json
class RedisMaster():
    def __init__(self, host='localhost', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connection = None

    def connect(self):
        self.connection = redis.Redis(host=self.host, port=self.port, db=self.db)    

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def set_key_value(self, key, value):
        if self.connection:
            self.connection.set(key, value)

    def get_key_value(self, key):
     if self.connection:
        data = self.connection.get(key)
        if data:
            data = json.loads(data.decode('utf-8'))
            if isinstance(data, dict):
                return [data]  # Convert single dictionary to list
            elif isinstance(data, list):
                return data
        else:
            return None


