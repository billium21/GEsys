"""
Wrapper around the redis hash datatype to behave like a dict.
"""
import redis

class Rdict:
    """
    Wraps a single redis hash datatype to provide a dict-like access pattern.
    """
    def __init__(self, rediskey, rhost='localhost', rport=6379, rdb=0):
        self.rediskey = rediskey
        self.rinstance = redis.StrictRedis(host=rhost, port=rport, db=rdb)

    def __getitem__(self, key):
        val = self.rinstance.hget(self.rediskey, key)
        if val is not None:
            return val
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        ret = self.rinstance.hset(self.rediskey, key, value)

    def keys(self):
        return self.rinstance.hkeys(self.rediskey)

    def values(self):
        return self.rinstance.hvals(self.rediskey)

    def items(self):
        return self.rinstance.hgetall(self.rediskey).items()

    def delete(self):
        self.rinstance.delete(self.rediskey)


if __name__ == "__main__":
    pass
