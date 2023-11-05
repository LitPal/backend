import redis

# Connect to Redis
redis_db = redis.Redis(host='localhost', port=6379, db=0)

# Create user table 
redis_db.execute_command('DEL user_table') # clear if exists
redis_db.rpush('user_table', 'user1', 'pw123') 
redis_db.rpush('user_table', 'user2', 'pw456')

