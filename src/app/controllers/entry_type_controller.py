from src.app.helpers.constant import *
from logging import info, error, basicConfig, INFO
from src.app.helpers.api_helper import rest_api_helper
from src.app.models.api_responses import APIError

basicConfig(level=INFO, format=LOGGING_FORMAT)


def exists_entry_type(dataplex_project_id: str, entry_type_location: str, entry_type_id: str):
    url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
          f"locations/{entry_type_location}/entryTypes"
    try:
        json_result = rest_api_helper(GOOGLE_API, url, GET)
        entry_type_name = f"projects/{dataplex_project_id}/locations/{entry_type_location}/entryTypes/{entry_type_id}"
        return any(item["name"] == entry_type_name for item in json_result.get("payload", {}).get("entryTypes", []))
    except APIError as e:
        error(f"Error checking entry type: {e}")
        raise e


def create_custom_entry_type(dataplex_project_id: str, entry_type_location: str, entry_type_id: str,
                             entry_type_name: str, entry_type_description: str, type_aliases: str, platform: str,
                             system: str):
    try:
        if exists_entry_type(dataplex_project_id, entry_type_location, entry_type_id):
            return None
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{entry_type_location}/entryTypes?entryTypeId={entry_type_id}"
        data = {
            "name": entry_type_name,
            "description": entry_type_description,
            "typeAliases": type_aliases,
            "platform": platform,
            "system": system
        }
        api_response = rest_api_helper(GOOGLE_API, url, POST, data)
        return api_response
    except APIError as e:
        error(f"Error creating entry type: {e}")
        return e.to_json()


def delete_custom_entry_type(dataplex_project_id: str, entry_type_location: str, entry_type_id: str):
    try:
        if not exists_entry_type(dataplex_project_id, entry_type_location, entry_type_id):
            return None
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{entry_type_location}/entryTypes/{entry_type_id}"
        api_response = rest_api_helper(GOOGLE_API, url, DELETE)
        return api_response
    except APIError as e:
        error(f"Error deleting entry type: {e}")
        return e.to_json()
