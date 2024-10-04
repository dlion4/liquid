
from src import config


TOKEN_JTI_EXPIRY=3600

from redis import Redis



token_blocklist = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=0,
    decode_responses=True
)
blacklist = set()
def add_to_blocklist(jti: str) -> None:
    blacklist.add(jti)

def token_in_blocklist(jti:str)->bool:
    return jti in blacklist