from src.app.helpers.utils import *
from src.app.helpers.constant import *
from logging import info, error, basicConfig, INFO
from src.app.helpers.api_helper import rest_api_helper
from src.app.models.api_responses import APIError

basicConfig(level=INFO, format=LOGGING_FORMAT)


def get_aspect_type(dataplex_project_id: str, aspect_type_location: str, aspect_type_id: str):
    url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
          f"locations/{aspect_type_location}/aspectTypes/{aspect_type_id}"
    try:
        json_result = rest_api_helper(GOOGLE_API, url, GET)
        return json_result
    except APIError as e:
        error(f"Error in get_aspect_type: {str(e)}")
        return e.to_json()


def _exists_aspect_type(dataplex_project_id: str, aspect_type_location: str, aspect_type_id: str):
    url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
          f"locations/{aspect_type_location}/aspectTypes"
    try:
        json_result = rest_api_helper(GOOGLE_API, url, GET)
        aspect_type = f"projects/{dataplex_project_id}/locations/{aspect_type_location}/aspectTypes/{aspect_type_id}"
        return any(item["name"] == aspect_type for item in json_result.get("payload", {}).get("aspectTypes", []))
    except APIError as e:
        error(f"Error in exists_aspect_type: {str(e)}")
        raise e


def create_update_aspect_type(dataplex_project_id: str, aspect_type_location: str, aspect_type_id: str,
                              aspect_type_name: str, aspect_type_description: str, metadata_template: dict):
    try:
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{aspect_type_location}/aspectTypes"
        data = {
            "displayName": aspect_type_name,
            "description": aspect_type_description,
            "metadataTemplate": metadata_template
        }
        if _exists_aspect_type(dataplex_project_id, aspect_type_location, aspect_type_id):
            update_url_suffix = f"/{aspect_type_id}?updateMask=displayName,description,metadataTemplate"
            api_response = rest_api_helper(GOOGLE_API, url + update_url_suffix, PATCH, data)
            return api_response
    
        create_url_suffix = f"?aspectTypeId={aspect_type_id}"
        api_response = rest_api_helper(GOOGLE_API, url + create_url_suffix, POST, data)
        return api_response
    except APIError as e:
        error(f"Error creating or updating aspect type: {e}")
        return e.to_json()
  

def delete_aspect_type(dataplex_project_id: str, aspect_type_location: str, aspect_type_id: str):
    try:
        if not _exists_aspect_type(dataplex_project_id, aspect_type_location, aspect_type_id):
            return None
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{aspect_type_location}/aspectTypes/{aspect_type_id}"
        api_response = rest_api_helper(GOOGLE_API, url, DELETE)
        return api_response
    except APIError as e:
        error(f"Error deleting aspect type: {e}")
        return e.to_json()
