import redis
import jwt

FAVORITES_ADDITION = ":favorites"

# connect to our redis database
r = redis.Redis(
    host='redis-10075.c228.us-central1-1.gce.cloud.redislabs.com',
    port=10075,
    password='zqSmVqec3tp6G7mlfQC9BkcWvHOnzcmt',
    charset="utf-8", decode_responses=True
)



# returns True ONLY IF this is a valid user AND the password is correct
def authenticate(username: str, password: str) -> bool:
    r.hset("alice", "password", "pw123")
    return r.hget(username, "password") == password

def decode(token: str, secret_key: str) -> bool:
    dec_user = jwt.decode(token, secret_key, algorithms=["HS256"])
    return r.hget(dec_user["username"], "password") != None


# query the database for the user's favorites pdf list, return a list of all the URLs
def getFavorites(username: str) -> list[str]:
    ls = []

    for line in r.smembers(username+FAVORITES_ADDITION):
        ls.append((line))

    return ls

# add a pdf to the user's favorites
def addToFavorites(username: str, url: str):
    r.sadd(username+FAVORITES_ADDITION, url)


# remove a pdf from the user's favorites
def removeFromFavorites(username: str, url: str):
    r.srem(username+FAVORITES_ADDITION, url)
