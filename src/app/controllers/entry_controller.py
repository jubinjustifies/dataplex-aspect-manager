from src.app.helpers.utils import *
from src.app.helpers.constant import *
from logging import info, error, basicConfig, INFO
from src.app.helpers.api_helper import rest_api_helper
from src.app.models.api_responses import APIError

basicConfig(level=INFO, format=LOGGING_FORMAT)


def get_entry(dataplex_project_id: str, entry_group_location: str, entry_group_id: str, entry_id: str):
    url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
          f"locations/{entry_group_location}/entryGroups/{entry_group_id}/entries/{entry_id}"
    try:
        json_result = rest_api_helper(GOOGLE_API, url, GET)
        return json_result
    except APIError as e:
        return e.to_json()


def exists_entry(dataplex_project_id: str, entry_group_location: str, entry_group_id: str, entry_id: str):
    url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
          f"locations/{entry_group_location}/entryGroups/{entry_group_id}/entries"
    try:
        json_result = rest_api_helper(GOOGLE_API, url, GET)
        entry_name = f"projects/{dataplex_project_id}/locations/{entry_group_location}/" \
                     f"entryGroups/{entry_group_id}/entries/{entry_id}"
        return any(item["name"] == entry_name for item in json_result.get("payload", {}).get("entries", []))
    except APIError as e:
        raise e


def create_custom_entry(dataplex_project_id: str, entry_group_location: str, entry_group_id: str, entry_type_id: str,
                        entry_type_location: str, entry_id: str, entry_name: str, entry_description: str, system: str):
    try:
        if exists_entry(dataplex_project_id, entry_group_location, entry_group_id, entry_id):
            return None
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{entry_group_location}/entryGroups/{entry_group_id}/entries?entryId={entry_id}"
        data = {
            "entrySource": {
                "displayName": entry_name,
                "description": entry_description,
                "system": system
            },
            "entryType": f"projects/{dataplex_project_id}/locations/{entry_type_location}/entryTypes/{entry_type_id}",
            "fullyQualifiedName": f"gcs:{entry_name}"
        }
        api_response = rest_api_helper(GOOGLE_API, url, POST, data)
        return api_response
    except APIError as e:
        return e.to_json()


def delete_custom_entry(dataplex_project_id: str, entry_group_location: str, entry_group_id: str, entry_id: str):
    try:
        if not exists_entry(dataplex_project_id, entry_group_location, entry_group_id, entry_id ):
            return None
        url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{dataplex_project_id}/" \
              f"locations/{entry_group_location}/entryGroups/{entry_group_id}/entries/{entry_id}"
        api_response = rest_api_helper(GOOGLE_API, url, DELETE)
        return api_response
    except APIError as e:
        return e.to_json()
