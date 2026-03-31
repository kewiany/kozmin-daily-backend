from pydantic import BaseModel


class FCMTokenRequest(BaseModel):
    fcm_token: str


class BroadcastNotificationRequest(BaseModel):
    title: str
    body: str


class BroadcastNotificationResponse(BaseModel):
    success: int
    failure: int
    total_tokens: int
