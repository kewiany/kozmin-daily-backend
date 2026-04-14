from pydantic import BaseModel, Field


class FCMTokenRequest(BaseModel):
    fcm_token: str


class BroadcastNotificationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str = Field(min_length=1, max_length=500)
    event_id: int | None = None
    news_id: int | None = None


class BroadcastNotificationResponse(BaseModel):
    success: int
    failure: int
    total_tokens: int
