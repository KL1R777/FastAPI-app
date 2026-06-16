from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent # Текущий файл и его предки
print(BASE_DIR)

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes = 1

