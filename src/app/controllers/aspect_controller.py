from src.app.controllers.entry_group_controller import create_custom_entry_group
from src.app.controllers.entry_type_controller import create_custom_entry_type
from src.app.helpers.utils import *
from src.app.helpers.constant import *
from src.app.helpers.api_helper import rest_api_helper
from src.app.models.api_responses import APIError, APISuccess
from logging import info, error, INFO, basicConfig
from src.app.controllers.entry_controller import get_entry, create_custom_entry

basicConfig(level=INFO, format=LOGGING_FORMAT)


def get_aspect_from_entry(entry_group_project_id: str, entry_group_location: str, entry_group_id: str, entry_resource_path:str,
                          aspect_type_project_id: str, aspect_type_location: str, aspect_type_id: str):
    """Fetches and extracts aspect related information from Dataplex entry"""
    try:
        entry = get_entry(entry_group_project_id, entry_group_location, entry_group_id, entry_resource_path)
        if not aspect_type_id:
            info(f"No aspect_type_id provided, Returning all aspects in {entry_resource_path}")
            return entry
        aspect_resource_path = f"{get_project_number(aspect_type_project_id)}.{aspect_type_location}.{aspect_type_id}"
        info(f"aspect_resource_path: {aspect_resource_path}")
        info(f"entry: {entry}")
        aspect_payload = entry.get("payload", {}).get("aspects").get(aspect_resource_path)
        if not aspect_payload:
            return APIError(404, {ERROR_KEY: INVALID_INPUT, REASON_KEY: f"No aspect_type_id found for {aspect_type_id}"}).to_json()
        return APISuccess(200, {aspect_resource_path: aspect_payload}).to_json()
    except APIError as e:
        error(f"Error fetching aspect: {e}")
        return e.to_json()


def _update_entry(entry_group_project_id: str, entry_group_location: str, entry_group_id: str, entry_resource_path: str,
                  aspects: dict, delete_missing_aspects: bool = False, aspect_keys: list[str] = None):
    """Update information inside the entry"""

    url = f"{HTTPS_PATH_PREFIX}{DATAPLEX_DOMAIN}/v1/projects/{entry_group_project_id}/locations/" \
            f"{entry_group_location}/entryGroups/{entry_group_id}/entries/{entry_resource_path}"

    query_params = ["update_mask=aspects"]
    if delete_missing_aspects and aspect_keys:
        query_params.append("deleteMissingAspects=true")
        for key in aspect_keys:
            query_params.append(f"aspectKeys={key}")

    url = f"{url}?{'&'.join(query_params)}"
    data = {"aspects": aspects}
    try:
        api_response = rest_api_helper(GOOGLE_API, url, PATCH, data)
        return api_response
    except APIError as e:
        error(f"Error updating entry: {e}")
        return e.to_json()


def update_system_entry_bq_table(entry_group_project_id: str, entry_group_location: str, data_product_id: str, bigquery_project_id: str,
                                 bigquery_table_fqn: str, aspects: dict):
    bigquery_dataset, bigquery_table = fully_qualified_name_splitter(bigquery_table_fqn)
    resource_path = f"{BIGQUERY_DOMAIN}/projects/{bigquery_project_id}/datasets/{bigquery_dataset}/tables/{bigquery_table}"
    return _update_entry(entry_group_project_id, entry_group_location, "@bigquery", resource_path, aspects)


def update_system_entry_bq_dataset(entry_group_project_id: str, entry_group_location: str, data_product_id: str, bigquery_project_id: str,
                                 bigquery_dataset_fqn: str, aspects: dict):
    bigquery_dataset = fully_qualified_name_splitter(bigquery_dataset_fqn)[0]
    resource_path = f"{BIGQUERY_DOMAIN}/projects/{bigquery_project_id}/datasets/{bigquery_dataset}"
    return _update_entry(entry_group_project_id, entry_group_location, "@bigquery", resource_path, aspects)


def update_custom_entry_gcs_bucket(entry_group_project_id: str, entry_group_location: str, data_product_id: str, gcs_project_id: str,
                                 gcs_bucket_fqn: str, aspects: dict):
    gcs_bucket = fully_qualified_name_splitter(gcs_bucket_fqn)[0]
    generate_custom_entry_prerequisites(data_product_id, entry_group_project_id, entry_group_location, gcs_bucket)
    return _update_entry(entry_group_project_id, entry_group_location,
                         f"{ODP_PREFIX}{data_product_id}{CUSTOM_ENTRY_GROUP_SUFFIX}", gcs_bucket, aspects)


def delete_aspect_from_entry(entry_group_project_id: str, entry_group_location: str, entry_group_id: str,
                             entry_resource_path: str, aspect_type_project_id: str, aspect_type_location: str,
                             aspect_type_id: str):
    try:
        aspect_key_to_delete = f"{get_project_number(aspect_type_project_id)}.{aspect_type_location}.{aspect_type_id}"
        entry = get_entry(entry_group_project_id, entry_group_location, entry_group_id, entry_resource_path)
        all_aspects = entry.get("payload", {}).get("aspects", {})
        if aspect_key_to_delete not in all_aspects:
            return APIError(404, {ERROR_KEY: INVALID_INPUT,
                                  REASON_KEY: f"Aspect {aspect_key_to_delete} not found in entry."}).to_json()
        del all_aspects[aspect_key_to_delete]
        api_response = _update_entry(entry_group_project_id, entry_group_location, entry_group_id, entry_resource_path,
                                     all_aspects, delete_missing_aspects=True, aspect_keys=[aspect_key_to_delete])
        return api_response
    except APIError as e:
        error(f"Error deleting aspect: {e}")
        return e.to_json()


def generate_custom_entry_prerequisites(data_product_id: str, custom_entry_project_id: str, custom_entry_location: str, entry_id: str):
    entry_group_id = f"{ODP_PREFIX}{data_product_id}{CUSTOM_ENTRY_GROUP_SUFFIX}"
    entry_group_name = f"{ODP} {data_product_id} {CUSTOM_ENTRY_GROUP}"
    entry_group_description = f"{CUSTOM_ENTRY_GROUP_DESCRIPTION} {data_product_id}"

    create_custom_entry_group(custom_entry_project_id, custom_entry_location, entry_group_id, entry_group_name, entry_group_description)
    create_custom_entry_type(custom_entry_project_id, custom_entry_location, GCS_BUCKET_CUSTOM_ENTRY_TYPE, GCS_BUCKET_CUSTOM_ENTRY_TYPE_NAME,
                             GCS_BUCKET_CUSTOM_ENTRY_TYPE_DESCRIPTION, GCS_BUCKET_TYPE_ALIASES, PLATFORM, SYSTEM)
    create_custom_entry(custom_entry_project_id, custom_entry_location, entry_group_id, GCS_BUCKET_CUSTOM_ENTRY_TYPE, custom_entry_location,
                        entry_id, entry_id, EMPTY_STRING, SYSTEM)
