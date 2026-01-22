from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str 
    token_type: str | None = None
    expiry: int = Field(gt=0) 
    