import redis
from rq import Connection, Queue, Worker

from app.core.config import AppConfig


class JobQueue:

    __redis = redis.Redis(host=AppConfig.REDIS_HOST, port=AppConfig.REDIS_PORT)
    __queue = Queue(connection=__redis)
    __worker = Worker(["default"], connection=__redis)


    @classmethod
    def init_workers(cls):
        cls.__worker.work()


    @classmethod
    def enqueue(cls, func, *args):
        cls.__queue.enqueue(func, *args)
