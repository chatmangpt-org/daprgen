import json
import os

from dspygen.typetemp.functional import render
from jinja2 import Template


# Load OpenAPI JSON
def load_openapi_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Function to map OpenAPI types to Python types
def map_openapi_to_python_type(openapi_type):
    type_mapping = {
        'integer': 'int',
        'number': 'float',
        'string': 'str',
        'boolean': 'bool',
        'array': 'list',
        'object': 'dict'
    }
    return type_mapping.get(openapi_type, 'Any')


# Preprocess schemas to map OpenAPI types to Python types
def preprocess_schemas(schemas):
    for schema_name, schema_details in schemas.items():
        for prop, prop_details in schema_details.get('properties', {}).items():
            if 'type' in prop_details:
                prop_details['type'] = map_openapi_to_python_type(prop_details['type'])
    return schemas


service_template_str = """
from typing import Any, Dict, Type
import httpx
from pydantic import BaseModel

class {{ service_name }}:
    def __init__(self, base_url: str, auth_token: str, version: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.version = version

    async def request(self, method: str, endpoint: str, data: Any = None, params: Dict[str, Any] = None) -> Any:
        async with httpx.AsyncClient() as client:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'Version': self.version,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            url = f"{self.base_url}{endpoint}"
            response = await client.request(method, url, json=data, params=params, headers=headers)
            response.raise_for_status()
            return response.json()

    def map_response(self, response: httpx.Response, response_map: Dict[int, Type[BaseModel]]) -> Any:
        response_type = response_map.get(response.status_code)
        if response_type:
            return response_type.parse_obj(response.json())
        response.raise_for_status()

    {% for path, methods in paths.items() %}
    {% for method, details in methods.items() %}
    async def {{ details['operationId'] | underscore }}(self{% if 'requestBody' in details and 'application/json' in details['requestBody']['content'] %}, data: {{ details['requestBody']['content']['application/json']['schema']['$ref'].split('/')[-1] | default('Dict[str, Any]') }} = None{% endif %}{% if 'parameters' in details %}, params: Dict[str, Any] = None{% endif %}) -> Any:
        response = await self.request('{{ method }}', '{{ path }}'{% if 'requestBody' in details and 'application/json' in details['requestBody']['content'] %}, data{% endif %}{% if 'parameters' in details %}, params{% endif %})
        response_map = {
            {% for status_code, response_details in details['responses'].items() %}
            {{ status_code }}: {{ response_details['content']['application/json']['schema']['$ref'].split('/')[-1] | default('Any') }},
            {% endfor %}
        }
        return self.map_response(response, response_map)

    {% endfor %}
    {% endfor %}
"""

model_template_str = """
from pydantic import BaseModel
from typing import Optional, List

{% for schema_name, schema_details in schemas.items() %}
class {{ schema_name }}(BaseModel):
    {% for prop, prop_details in schema_details['properties'].items() %}
    {{ prop }}: {{ prop_details['type'] | default('Any') }} = {{ prop_details.get('default', 'None') }}
    {% endfor %}
{% endfor %}
"""


# Render template
def render_template(template_str, context):
    return render(template_str, **context)


def main(openapi_file_path, output_dir):
    # Load OpenAPI JSON
    openapi_data = load_openapi_json(openapi_file_path)

    # Extract paths and schemas
    paths = openapi_data.get('paths', {})
    schemas = openapi_data.get('components', {}).get('schemas', {})

    schemas = preprocess_schemas(schemas)

    # Prepare context for templates
    context = {
        'service_name': 'GHLOAuthService',
        'paths': paths,
        'schemas': schemas
    }

    # Render templates
    service_code = render_template(service_template_str, context)
    model_code = render_template(model_template_str, context)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save rendered code to files
    with open(os.path.join(output_dir, 'ghl_oauth_service.py'), 'w') as f:
        f.write(service_code)

    with open(os.path.join(output_dir, 'ghl_oauth_models.py'), 'w') as f:
        f.write(model_code)


if __name__ == "__main__":
    openapi_file_path = 'oauth.json'  # Replace with your OpenAPI JSON file path
    output_dir = 'output'  # Replace with your desired output directory
    main(openapi_file_path, output_dir)
