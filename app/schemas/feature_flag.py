from pydantic import BaseModel


class ConfigResponse(BaseModel):
    flags: dict[str, str]
