import json
import logging
from typing import Tuple
from cryptography.fernet import Fernet, InvalidToken
from typing import Optional, Union
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

def encrypt_data(data: dict, key: bytes) -> str:
    f = Fernet(key)
    json_string = json.dumps(data)
    encrypted_string = f.encrypt(bytes(json_string, encoding="utf-8"))
    return encrypted_string.decode("utf-8")

def decrypt_string(encrypted: Union[str, bytes], key: bytes) -> Optional[dict]:
    f = Fernet(key)
    if not isinstance(encrypted, bytes):
        encrypted = bytes(encrypted, encoding="utf-8")
    try:
        decrypted_string = f.decrypt(encrypted)
        return json.loads(decrypted_string)
    except InvalidToken:
        return


def create_verification_link(user: User) -> Tuple[str, str]:
    data = {"uid": user.pk}
    key = encrypt_data(data, settings.INVITES_KEY)
    verification_url = f"{settings.FRONTEND_BASE_URL}verification-success?actionType=registration"
    logger.info(f"Verification URL => {verification_url}&token={key}")
    return verification_url, key
