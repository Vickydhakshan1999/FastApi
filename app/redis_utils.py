# import redis

# redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# def check_redis_health():
#     try:
#         redis_client.ping()
#         return True
#     except redis.ConnectionError:
#         return False
