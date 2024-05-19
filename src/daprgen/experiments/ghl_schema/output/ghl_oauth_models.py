from pydantic import BaseModel, Field
from typing import Optional, List


class BadRequestDTO(BaseModel):
    statusCode: float = Field(0)
    message: str = Field("")


class UnauthorizedDTO(BaseModel):
    statusCode: float = Field(0)
    message: str = Field("")
    error: str = Field("")


class GetAccessCodebodyDto(BaseModel):
    client_id: str = Field("")
    client_secret: str = Field("")
    grant_type: str = Field("")
    code: str = Field("")
    refresh_token: str = Field("")
    user_type: str = Field("")
    redirect_uri: str = Field("")


class GetAccessCodeSuccessfulResponseDto(BaseModel):
    access_token: str = Field("")
    token_type: str = Field("")
    expires_in: float = Field(0)
    refresh_token: str = Field("")
    scope: str = Field("")
    userType: str = Field("")
    locationId: str = Field("")
    companyId: str = Field("")
    approvedLocations: list = Field([])
    userId: str = Field("")
    planId: str = Field("")


class UnprocessableDTO(BaseModel):
    statusCode: float = Field(0)
    message: list = Field([])
    error: str = Field("")


class GetLocationAccessCodeBodyDto(BaseModel):
    companyId: str = Field("")
    locationId: str = Field("")


class GetLocationAccessTokenSuccessfulResponseDto(BaseModel):
    access_token: str = Field("")
    token_type: str = Field("")
    expires_in: float = Field(0)
    scope: str = Field("")
    locationId: str = Field("")
    userId: str = Field("")


class InstalledLocationSchema(BaseModel):
    _id: str = Field("")
    name: str = Field("")
    address: str = Field("")
    isInstalled: bool = Field(True)


class GetInstalledLocationsSuccessfulResponseDto(BaseModel):
    locations: list = Field([])
    count: float = Field(0)
    installToFutureLocations: bool = Field(True)
