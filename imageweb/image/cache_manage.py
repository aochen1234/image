from .models import NewUser, Article
import redis

r = redis.StrictRedis(host='localhost', port='6379', db=0)


