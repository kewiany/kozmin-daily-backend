import json
import logging
import os

import firebase_admin
from firebase_admin import auth, credentials, messaging

logger = logging.getLogger(__name__)

_app: firebase_admin.App | None = None


def init_firebase() -> None:
    global _app
    raw = os.environ.get("FIREBASE_CREDENTIALS_JSON", "")
    if not raw:
        logger.warning("FIREBASE_CREDENTIALS_JSON not set — push notifications disabled")
        return
    try:
        cred_dict = json.loads(raw)
        cred = credentials.Certificate(cred_dict)
        _app = firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized")
    except Exception as e:
        logger.error("Failed to initialize Firebase: %s", e)


def send_broadcast(
    tokens: list[str], title: str, body: str, data: dict[str, str] | None = None
) -> tuple[int, int, list[str]]:
    """Send notification to all tokens. Returns (success, failure, bad_tokens)."""
    if _app is None:
        logger.warning("Firebase not initialized — skipping broadcast")
        return 0, 0, []

    success = 0
    failure = 0
    bad_tokens: list[str] = []

    batch_size = 500
    for i in range(0, len(tokens), batch_size):
        batch = tokens[i : i + batch_size]
        messages = [
            messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                data=data,
                token=token,
            )
            for token in batch
        ]
        response = messaging.send_each(messages)

        for j, send_response in enumerate(response.responses):
            if send_response.success:
                success += 1
            else:
                failure += 1
                exc = send_response.exception
                if exc and (
                    "UNREGISTERED" in str(exc)
                    or "INVALID_ARGUMENT" in str(exc)
                ):
                    bad_tokens.append(batch[j])

    return success, failure, bad_tokens


def verify_firebase_token(id_token: str) -> dict:
    """Verify a Firebase ID token and return the decoded payload.

    Raises firebase_admin.auth.InvalidIdTokenError on invalid tokens.
    """
    decoded = auth.verify_id_token(id_token)
    return decoded
