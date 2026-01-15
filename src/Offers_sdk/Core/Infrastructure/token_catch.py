import os
import json

from typing import Optional, Tuple
from datetime import datetime


class TokenCache:
    def __init__(self):
        self._path: str = ".token_cache.json"

    def save(self, token: str, expires_in: datetime):
        data = {
            "token": token,
            "expires_at": expires_in.isoformat()
        }
        with open(self._path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data))

    def load(self) -> Optional[Tuple[str, datetime]]:
        if not os.path.exists(self._path):
            return None

        with open(self._path, "r") as f:
            data = json.load(f)

        try:
            expires_at = datetime.fromisoformat(data["expires_at"])
            token = data["token"]
        except:
            return None

        if datetime.now() >= expires_at:
            return None  # expired
        return token, expires_at


if __name__ == '__main__':
    cache = TokenCache()
    print(cache.load())