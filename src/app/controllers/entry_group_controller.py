from src.app.helpers.utils import *
from src.app.helpers.constant import *
from logging import info, error, basicConfig, INFO
from src.app.helpers.api_helper import rest_api_helper
from src.app.models.api_responses import APIError

basicConfig(level=INFO, format=LOGGING_FORMAT)


def exists_entry_group(dataplex_project_id: str, entry_group_location: str, entry_group_id: str):
    url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
          f"locations/{entry_group_location}/entryGroups"
    try:
        json_result = rest_api_helper(GOOGLE_API, url, GET)
        entry_group = f"projects/{dataplex_project_id}/locations/{entry_group_location}/entryGroups/{entry_group_id}"
        return any(item["name"] == entry_group for item in json_result.get("payload", {}).get("entryGroups", []))
    except APIError as e:
        error(f"Error checking entry group: {e}")
        raise e


def create_custom_entry_group(dataplex_project_id: str, entry_group_location: str, entry_group_id: str,
                              entry_group_name: str, entry_group_description: str):
    try:
        if exists_entry_group(dataplex_project_id, entry_group_location, entry_group_id):
            return None
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{entry_group_location}/entryGroups?entryGroupId={entry_group_id}"
        data = {
            "displayName": entry_group_name,
            "description": entry_group_description
        }
        api_response = rest_api_helper(GOOGLE_API, url, POST, data)
        return api_response
    except APIError as e:
        error(f"Error creating entry group: {e}")
        return e.to_json()
    

def delete_custom_entry_group(dataplex_project_id: str, entry_group_location: str, entry_group_id: str):
    try:
        if not exists_entry_group(dataplex_project_id, entry_group_location, entry_group_id):
            return None
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{entry_group_location}/entryGroups/{entry_group_id}"
        api_response = rest_api_helper(GOOGLE_API, url, DELETE)
        return api_response
    except APIError as e:
        error(f"Error deleting entry group: {e}")
        return e.to_json()
