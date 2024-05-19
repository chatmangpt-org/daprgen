from pydantic import BaseModel, Field
from typing import List, Optional



class BadRequestDTO(BaseModel):
    status_code: float = Field(0, alias="statusCode",
                               description="The HTTP status code representing the type of error.")
    message: str = Field("", description="A message describing the error.")


class UnauthorizedDTO(BaseModel):
    status_code: float = Field(0, alias="statusCode",
                               description="The HTTP status code representing the type of error.")
    message: str = Field("", description="A message describing the error.")
    error: str = Field("", description="A specific error code or message detailing the unauthorized request.")


class GetAccessCodeBodyDTO(BaseModel):
    client_id: str = Field("", alias="clientId", description="The client ID issued during app registration.")
    client_secret: str = Field("", alias="clientSecret",
                               description="The client secret issued during app registration.")
    grant_type: str = Field("", alias="grantType", description="The type of grant being requested.")
    code: str = Field("", description="The authorization code received from the authorization server.")
    refresh_token: str = Field("", alias="refreshToken", description="The refresh token, if available.")
    user_type: str = Field("", alias="userType", description="The type of user requesting the token.")
    redirect_uri: str = Field("", alias="redirectUri",
                              description="The redirect URI used in the authorization request.")


class GetAccessCodeSuccessfulResponseDTO(BaseModel):
    access_token: str = Field("", alias="accessToken",
                              description="The token that can be used to authenticate API requests.")
    token_type: str = Field("", alias="tokenType", description="The type of token issued, typically 'Bearer'.")
    expires_in: float = Field(0, alias="expiresIn", description="The duration in seconds until the token expires.")
    refresh_token: str = Field("", alias="refreshToken",
                               description="A token that can be used to obtain a new access token.")
    scope: str = Field("", description="The scope of the access granted by the token.")
    user_type: str = Field("", alias="userType", description="The type of user associated with the token.")
    location_id: str = Field("", alias="locationId", description="The ID of the location associated with the token.")
    company_id: str = Field("", alias="companyId", description="The ID of the company associated with the token.")
    approved_locations: List[str] = Field([], alias="approvedLocations",
                                          description="A list of locations approved for access.")
    user_id: str = Field("", alias="userId", description="The ID of the user associated with the token.")
    plan_id: str = Field("", alias="planId", description="The ID of the plan associated with the token.")


class UnprocessableDTO(BaseModel):
    status_code: float = Field(0, alias="statusCode",
                               description="The HTTP status code representing the type of error.")
    message: List[str] = Field([], description="A list of messages describing the errors.")
    error: str = Field("", description="A specific error code or message detailing the unprocessable request.")


class GetLocationAccessCodeBodyDTO(BaseModel):
    company_id: str = Field("", alias="companyId",
                            description="The ID of the company for which access is being requested.")
    location_id: str = Field("", alias="locationId",
                             description="The ID of the location for which access is being requested.")


class GetLocationAccessTokenSuccessfulResponseDTO(BaseModel):
    access_token: str = Field("", alias="accessToken",
                              description="The token that can be used to authenticate API requests.")
    token_type: str = Field("", alias="tokenType", description="The type of token issued, typically 'Bearer'.")
    expires_in: float = Field(0, alias="expiresIn", description="The duration in seconds until the token expires.")
    scope: str = Field("", description="The scope of the access granted by the token.")
    location_id: str = Field("", alias="locationId", description="The ID of the location associated with the token.")
    user_id: str = Field("", alias="userId", description="The ID of the user associated with the token.")


class InstalledLocationSchema(BaseModel):
    id: str = Field("", alias="_id", description="The unique identifier for the installed location.")
    name: str = Field("", description="The name of the installed location.")
    address: str = Field("", description="The address of the installed location.")
    is_installed: bool = Field(True, alias="isInstalled", description="Indicates whether the location is installed.")


class GetInstalledLocationsSuccessfulResponseDTO(BaseModel):
    locations: List[InstalledLocationSchema] = Field([], description="A list of installed locations.")
    count: float = Field(0, description="The number of installed locations.")
    install_to_future_locations: bool = Field(True, alias="installToFutureLocations",
                                              description="Indicates whether the installation applies to future locations.")


class GetAccessTokenPostParams(BaseModel):
    client_id: str = Field(..., title="Client ID", description="The ID provided by GHL for your integration")
    client_secret: str = Field(..., title="Client Secret", description="The secret provided by GHL for your integration")
    grant_type: str = Field(..., title="Grant Type", description="Type of grant requested", example="authorization_code", enum=["authorization_code", "refresh_token"])
    code: Optional[str] = Field(None, title="Authorization Code", description="The authorization code received from the authorization server")
    refresh_token: Optional[str] = Field(None, title="Refresh Token", description="The refresh token received from a previous authorization")
    user_type: Optional[str] = Field(None, title="User Type", description="The type of token to be requested", enum=["Company", "Location"], example="Location")
    redirect_uri: Optional[str] = Field(None, title="Redirect URI", description="The redirect URI for your application", example="https://myapp.com/oauth/callback/gohighlevel")


class GetLocationAccessTokenPostParams(BaseModel):
    companyId: str = Field(..., title="Company ID", description="Company Id of location you want to request token for")
    locationId: str = Field(..., title="Location ID", description="The location ID for which you want to obtain accessToken")
    version: str = Field(..., title="API Version", description="API Version", example="2021-07-28")


class GetInstalledLocationsGetParams(BaseModel):
    appId: str = Field(..., title="App ID", description="Parameter to search by the appId", example="tDtDnQdgm2LXpyiqYvZ6")
    companyId: str = Field(..., title="Company ID", description="Parameter to search by the companyId", example="tDtDnQdgm2LXpyiqYvZ6")
    isInstalled: Optional[bool] = Field(None, title="Is Installed", description="Filters out locations which are installed for specified app under the specified company", example=True)
    limit: Optional[int] = Field(20, title="Limit", description="Parameter to limit the number of installed locations", example=10)
    query: Optional[str] = Field(None, title="Query", description="Parameter to search for the installed location by name", example="location name")
    skip: Optional[int] = Field(0, title="Skip", description="Parameter to skip the number of installed locations", example=1)
