from pydantic import BaseModel, Field, field_validator
from typing import List


class OAuthToken(BaseModel):
    access_token: str = Field(..., alias='access_token')
    token_type: str = Field(..., alias='token_type')
    expires_in: int = Field(..., alias='expires_in')
    refresh_token: str = Field(..., alias='refresh_token')
    scope: str = Field(..., alias='scope')
    user_type: str = Field(..., alias='userType')
    location_id: str = Field(None, alias='locationId')
    company_id: str = Field(..., alias='companyId')
    approved_locations: List[str] = Field(..., alias='approvedLocations')
    user_id: str = Field(..., alias='userId')
    plan_id: str = Field(None, alias='planId')

    @field_validator('expires_in')
    def validate_expires_in(cls, value):
        if value <= 0:
            raise ValueError('expires_in must be a positive integer')
        return value

    def is_token_valid(self) -> bool:
        # Business logic to check if the token is valid
        return True  # Placeholder for actual logic

    def refresh_needed(self) -> bool:
        # Business logic to determine if a refresh is needed
        return False  # Placeholder for actual logic
