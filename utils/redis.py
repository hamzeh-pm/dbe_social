import redis


class RedisClient:
    def __init__(self) -> None:
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)
