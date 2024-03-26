from aiogram.contrib.fsm_storage.redis import RedisStorage2


storage = RedisStorage2(
    host='localhost',
    port=6379,
    password=None,
)
