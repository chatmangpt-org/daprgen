import json
import os
from typing import Dict, Optional
from pydantic import BaseModel, Field


class AppUserType:
    Company = "Company"
    Location = "Location"


class TokenType:
    Bearer = "Bearer"


class InstallationDetails(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    user_type: str = Field(AppUserType.Company, alias="userType")
    company_id: Optional[str] = Field("", alias="companyId")
    location_id: Optional[str] = Field("", alias="locationId")


class Model:
    def __init__(self):
        self.file_path = 'installationObjects.json'
        self.installation_objects: Dict[str, InstallationDetails] = self.load_installation_objects()

    def load_installation_objects(self):
        try:
            with open(self.file_path, 'r') as f:
                data = f.read()
                return json.loads(data)
        except FileNotFoundError:
            print('JSON file not found, starting with an empty object.')
            return {}
        except Exception as e:
            print(f'Error reading JSON file: {e}')
            return {}

    def save_installation_objects(self):
        try:
            with open(self.file_path, 'w') as f:
                f.write(json.dumps(self.installation_objects, indent=2))
        except Exception as e:
            print(f'Error writing to JSON file: {e}')

    def save_installation_info(self, details: InstallationDetails):
        resource_id = details.location_id or details.company_id
        if resource_id:
            self.installation_objects[resource_id] = details.model_dump()
            self.save_installation_objects()
        else:
            raise ValueError("Resource ID not found in installation details")

    def get_access_token(self, resource_id: str) -> Optional[str]:
        return self.installation_objects.get(resource_id, {}).get("access_token")

    def get_refresh_token(self, resource_id: str) -> Optional[str]:
        return self.installation_objects.get(resource_id, {}).get("refresh_token")

    def set_access_token(self, resource_id: str, token: str):
        if resource_id in self.installation_objects:
            self.installation_objects[resource_id]["access_token"] = token
            self.save_installation_objects()

    def set_refresh_token(self, resource_id: str, token: str):
        if resource_id in self.installation_objects:
            self.installation_objects[resource_id]["refresh_token"] = token
            self.save_installation_objects()
