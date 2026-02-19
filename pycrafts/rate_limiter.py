import time


_cooldowns: dict = {}


def is_rate_limited(user_id: int, command: str, seconds: int) -> bool:
    key = f"{user_id}:{command}"
    now = time.time()
    last = _cooldowns.get(key, 0)
    if now - last < seconds:
        return True
    _cooldowns[key] = now
    return False