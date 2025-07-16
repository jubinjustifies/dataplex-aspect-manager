from logging import info, INFO, error, basicConfig
import requests
from requests import Response
from src.app.helpers.constant import *
from src.app.models.api_responses import APIError, APISuccess
from google.auth import default as google_auth_default
from google.auth.transport.requests import Request as GoogleRequest

basicConfig(level=INFO, format=LOGGING_FORMAT)


def _generate_header(api_type: str):
    if api_type == GOOGLE_API:
        credentials, _ = google_auth_default()
        credentials.refresh(GoogleRequest())
        token = credentials.token
        info("requesting google api")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        return headers


def rest_api_helper(api_type: str, url: str, http_verb: str, request_body: str = None):
    """Calls the REST API"""

    headers = _generate_header(api_type)
    info(f"http_verb: {http_verb}, url: {url}, request_body: {request_body}")

    http_methods = {
        GET: lambda: requests.get(url, headers=headers),
        POST: lambda: requests.post(url, headers=headers, json=request_body),
        PUT: lambda: requests.put(url, headers=headers, json=request_body),
        PATCH: lambda: requests.patch(url, headers=headers, json=request_body),
        DELETE: lambda: requests.delete(url, headers=headers)
    }

    if http_verb not in http_methods:
        raise RuntimeError(f"Unknown HTTP verb: {http_verb}")

    response: Response = http_methods[http_verb]()

    if response.status_code in [200, 201]:
        return APISuccess(200, response.json()).to_json()
    
    error(f"Error rest_api_helper -> ' Status: '{response.status_code}' Text: '{response.text}'")
    raise APIError(response.status_code, {"detail": response.json()})
