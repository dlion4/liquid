
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
    print("set the redis to be blocklist: ", jti)

def token_in_blocklist(jti:str)->bool:
    print("block list in the redis: ", jti)
    return jti in blacklist