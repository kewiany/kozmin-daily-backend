import json
import logging

import firebase_admin
from firebase_admin import credentials, messaging

from app.config import settings

logger = logging.getLogger(__name__)

_app: firebase_admin.App | None = None


def init_firebase() -> None:
    import os
    global _app
    raw = os.environ.get("FIREBASE_CREDENTIALS_JSON", "")
    print(f"[firebase] from os.environ: length={len(raw)}")
    if not raw:
        raw = settings.FIREBASE_CREDENTIALS_JSON
    print(f"[firebase] FIREBASE_CREDENTIALS_JSON length={len(raw)}, starts_with={raw[:20]!r}")
    if not raw:
        print("[firebase] FIREBASE_CREDENTIALS_JSON not set — push notifications disabled")
        return
    try:
        cred_dict = json.loads(raw)
        print(f"[firebase] Parsed JSON, project_id={cred_dict.get('project_id')}")
        cred = credentials.Certificate(cred_dict)
        _app = firebase_admin.initialize_app(cred)
        print("[firebase] Firebase Admin SDK initialized")
    except Exception as e:
        print(f"[firebase] Failed to initialize Firebase: {e}")


def send_broadcast(
    tokens: list[str], title: str, body: str
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
