import redis

r = redis.StrictRedis(host='172.17.0.16', port=49156, db=0)
r.set('foo', 'bar')
