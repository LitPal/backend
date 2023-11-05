import redis

# Connect to Redis
redis_db = redis.Redis(host='localhost', port=6379, db=0)

# Create user table 
redis_db.hset('user:alice', 'password', 'pw123')  
redis_db.hset('user:bob', 'password', 'pw456')