import redis

FAVORITES_ADDITION = ":favorites"

# connect to our redis database
r = redis.Redis(
  host='redis-10075.c228.us-central1-1.gce.cloud.redislabs.com',
  port=10075,
  password='zqSmVqec3tp6G7mlfQC9BkcWvHOnzcmt')


# util function for db reformatting
def reformatString(input: str):
    return str(input).split('\'')[1]

# returns True ONLY IF this is a valid user AND the password is correct
def authenticate(username: str, password: str) -> bool:
    return reformatString(r.hget(username, password)) == password


# query the database for the user's favorites pdf list, return a list of all the URLs
def getFavorites(username: str) -> list[str]:
    ls = []

    for line in r.smembers(username+FAVORITES_ADDITION):
        ls.append(reformatString(line))

    return ls

# add a pdf to the user's favorites
def addToFavorites(username: str, url: str):
    r.sadd(username+FAVORITES_ADDITION, url)


# remove a pdf from the user's favorites
def removeFromFavorites(username: str, url: str):
    r.srem(username+FAVORITES_ADDITION, url)