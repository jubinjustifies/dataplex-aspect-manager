from src.app.controllers.aspect_controller import *
from src.app.controllers.aspect_type_controller import *
from src.app.models.aspect_type_asset_mapping_model import AspectTypeAssetMapping
from src.app.models.aspect_type_env_mapping_model import AspectTypeEnvMapping
from src.app.helpers.constant import *
from logging import info, INFO, basicConfig, error
from src.app.controllers.entry_controller import delete_custom_entry
from src.app.controllers.entry_group_controller import delete_custom_entry_group
from src.app.controllers.entry_type_controller import delete_custom_entry_type
from src.app.helpers.utils import *

basicConfig(level=INFO, format=LOGGING_FORMAT)


try:
    aspect_type_env_mapping: AspectTypeEnvMapping = load_aspect_type_env_mapping(ASPECT_TYPE_ENV_MAPPING_FILE)
    aspect_type_asset_mapping: AspectTypeAssetMapping = load_aspect_type_asset_mapping(ASPECT_TYPE_ASSET_MAPPING_FILE)
    data_product = list(DataProduct := load_product_entry_mapping(PRODUCT_ENTRY_MAPPING_FILE))
    aspect_types = load_multiple_yamls(ASPECTS_DIRECTORY)
    aspect_types_json = load_multiple_jsons(ASPECTS_DIRECTORY)
except Exception as e:
    error(f"Error loading mapping files: {e}")
    aspect_type_env_mapping = None
    aspect_type_asset_mapping = None
    data_product = None


def create_update_bulk_aspect_types() -> dict:
    info("Starting bulk aspect type creation process")

    try:
        project_id = os.getenv(ASPECT_TYPE_DATAPLEX_PROJECT_ID, ASPECT_TYPE_DATAPLEX_PROJECT_ID_VALUE)
        location = os.getenv(ASPECT_TYPE_DATAPLEX_REGION, ASPECT_TYPE_DATAPLEX_REGION_VALUE)
        api_responses = []
        
        for aspect_type in aspect_types:
            aspect_type_id = aspect_type["id"]
            aspect_type_name = aspect_type["displayName"]
            aspect_type_description = aspect_type.get("description", EMPTY_STRING)

            metadata_template = {
                "name": aspect_type_id,
                "type": "record",
                "recordFields": []
            }

            for field in aspect_type["fields"]:
                field_annotations = {"displayName": field["displayName"]}
                if "deprecated" in field:
                    field_annotations["deprecated"] = field["deprecated"]
                field_data = {
                    "name": field["name"],
                    "type": field["type"],
                    "annotations": field_annotations,
                    "index": field.get("index", 0),
                    "constraints": {
                        "required": field.get("required", True)
                    },
                    "enumValues": [] 
                }
                if field["type"].lower() == "enum" and "values" in field:
                    i = 1
                    for value in field["values"].split(PIPE_DELIMITER):
                        field_data["enumValues"].append({
                            "name": value,
                            "index": i
                        })
                        i += 1
                
                metadata_template["recordFields"].append(field_data)

            api_response = create_update_aspect_type(project_id, location, aspect_type_id, aspect_type_name,
                                                     aspect_type_description, metadata_template)
            api_responses.append(api_response)
        info("Completed bulk aspect type creation process")
        return determine_bulk_job_status(api_responses)
    except Exception as e:
        error(f"Error in bulk aspect type creation process: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def create_update_bulk_aspect_types_json() -> dict:
    info("Starting bulk aspect type creation process")

    try:
        project_id = os.getenv(ASPECT_TYPE_DATAPLEX_PROJECT_ID, ASPECT_TYPE_DATAPLEX_PROJECT_ID_VALUE)
        location = os.getenv(ASPECT_TYPE_DATAPLEX_REGION, ASPECT_TYPE_DATAPLEX_REGION_VALUE)
        api_responses = []
        
        for aspect_type in aspect_types_json:
            aspect_type_id = aspect_type["name"]
            annotations = aspect_type.get("annotations", {})
            aspect_type_name = annotations.get("displayName", aspect_type_id)
            aspect_type_description = annotations.get("description", EMPTY_STRING)
            metadata_template = aspect_type

            api_response = create_update_aspect_type(project_id, location, aspect_type_id, aspect_type_name,
                                                     aspect_type_description, metadata_template)
            api_responses.append(api_response)
        info("Completed bulk aspect type creation process")
        return determine_bulk_job_status(api_responses)
    except Exception as e:
        error(f"Error in bulk aspect type creation process: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def retrieve_aspect_type(aspect_type_id: str) -> dict:
    info(f"Starting aspect type retrieval process")

    try:
        project_id = os.getenv(ASPECT_TYPE_DATAPLEX_PROJECT_ID, ASPECT_TYPE_DATAPLEX_PROJECT_ID_VALUE)
        location = os.getenv(ASPECT_TYPE_DATAPLEX_REGION, ASPECT_TYPE_DATAPLEX_REGION_VALUE)
        result = get_aspect_type(project_id, location, aspect_type_id)
        info(f"Completed aspect type retrieval process")
        return result
    except Exception as e:
        error(f"Error in aspect type retrieval process: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def remove_aspect_type(aspect_type_id: str) -> dict:
    info(f"Starting aspect type removal process")

    try:
        project_id = os.getenv(ASPECT_TYPE_DATAPLEX_PROJECT_ID, ASPECT_TYPE_DATAPLEX_PROJECT_ID_VALUE)
        location = os.getenv(ASPECT_TYPE_DATAPLEX_REGION, ASPECT_TYPE_DATAPLEX_REGION_VALUE)
        result = delete_aspect_type(project_id, location, aspect_type_id)
        info(f"Completed aspect type removal process")
        return result
    except Exception as e:
        error(f"Error in aspect type removal process: {e}") 
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def create_update_bulk_aspects_with_yaml(data_product_id: str, aspect_type_id: str, aspect_data: dict):
    info(f"Starting create_or_update_aspect for data_product_id: {data_product_id}, aspect_type_id: {aspect_type_id}")
    try:
        if not all([aspect_type_env_mapping, aspect_type_asset_mapping, data_product]):
            return APIError(400, {ERROR_KEY: INVALID_CONFIG, 
                                  REASON_KEY: "Configuration mapping YAML files not found"}).to_json()

        gov_env_dict: dict = get_dataplex_project_id_and_region_from_mapping(aspect_type_env_mapping, aspect_type_id)
        if not gov_env_dict:
            warning(f"No environment mapping found for aspect_type_id: {aspect_type_id}")
            return APIError(404, {ERROR_KEY: INVALID_CONFIG, 
                                  REASON_KEY: f"No environment mapping found for aspect_type_id: {aspect_type_id}"}
                                  ).to_json()

        gcp_asset_list = get_gcp_asset_list_from_mapping(aspect_type_asset_mapping, aspect_type_id)
        if not gcp_asset_list:
            warning(f"No GCP assets found for aspect_type_id: {aspect_type_id}")
            return APIError(404, {ERROR_KEY: INVALID_CONFIG, 
                                  REASON_KEY: f"No asset mapping found for aspect_type_id = {aspect_type_id}"}
                                  ).to_json()

        dataplex_project_id = gov_env_dict["dataplex_project_id"]
        dataplex_region = gov_env_dict["dataplex_region"]
        api_responses = []

        matching_product = next((p for p in data_product if p.product_id == data_product_id), None)
        if not matching_product:
            warning(f"No matching product found for data_product_id: {data_product_id}")
            return APIError(404, {ERROR_KEY: INVALID_CONFIG, 
                                  REASON_KEY: f"No product entry mapping found for data_product_id = {data_product_id}"}
                                  ).to_json()

        for project in matching_product.gcp_projects:
            info(f"Processing project: {project.project_id}")
            for location in project.locations:
                for asset_type in location.asset_types:
                    if asset_type.asset_type_id not in gcp_asset_list or not hasattr(asset_type, "assets"):
                        continue
                    info(f"Processing asset_type: {asset_type.asset_type_id}")
                    for asset in asset_type.assets:
                        info(f"Asset Name: {asset.asset_name}, Flag: {asset.flag}")
                        project_id, region, resource_fqn = project.project_id, location.location_id, asset.asset_name
                        aspects = json_to_aspect_generator(dataplex_project_id, dataplex_region, aspect_type_id,
                                                           aspect_data)

                        update_functions = {
                            BQ_TABLE: update_system_entry_bq_table,
                            BQ_DATASET: update_system_entry_bq_dataset,
                            GCS_BUCKET: update_custom_entry_gcs_bucket
                        }

                        update_fn = update_functions.get(asset_type.asset_type_id)
                        if update_fn:
                            response = update_fn(project_id, region, data_product_id, project_id, resource_fqn, aspects)
                            api_responses.append(response)

        info(f"Completed aspect update for data_product_id: {data_product_id}, aspect_type_id: {aspect_type_id}")
        return determine_bulk_job_status(api_responses)
    except Exception as e:
        error(f"Error updating aspect for data_product_id: {data_product_id}, aspect_type_id: {aspect_type_id}. Error: {str(e)}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def retrieve_aspect(entry_group_project_id: str, entry_group_location: str, entry_group_id: str, entry_type_id: str,
                    entry_id: str, aspect_type_id: str) -> dict:
    info(f"Starting aspect retrieval process")

    try:
        aspect_type_project_id = os.getenv(ASPECT_TYPE_DATAPLEX_PROJECT_ID, ASPECT_TYPE_DATAPLEX_PROJECT_ID_VALUE)
        aspect_type_location = os.getenv(ASPECT_TYPE_DATAPLEX_REGION, ASPECT_TYPE_DATAPLEX_REGION_VALUE)
        resource_path = EMPTY_STRING

        if CUSTOM in entry_type_id:
            resource_path = f"{entry_id}?view=ALL"
        elif BQ_DATASET_SYSTEM_ENTRY_TYPE in entry_type_id:
            resource_path = f"{BIGQUERY_DOMAIN}/projects/{entry_group_project_id}/datasets/{entry_id}?view=ALL"
        elif BQ_TABLE_SYSTEM_ENTRY_TYPE in entry_type_id:
            dataset, table = fully_qualified_name_splitter(entry_id)
            resource_path = f"{BIGQUERY_DOMAIN}/projects/{entry_group_project_id}/datasets/{dataset}/tables/{table}?view=ALL"
        else:
            info(f"Unsupported entry type: {entry_type_id}")
        result = get_aspect_from_entry(entry_group_project_id, entry_group_location, entry_group_id, resource_path,
                                       aspect_type_project_id, aspect_type_location, aspect_type_id)
        info(f"Completed aspect retrieval process")
        return result
    except Exception as e:
        error(f"Error in aspect retrieval process: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def remove_aspect(entry_group_project_id: str, entry_group_location: str, entry_group_id: str, entry_type_id: str,
                  entry_id: str, aspect_type_id: str) -> dict:
    info(f"Starting aspect removal process")

    try:
        aspect_type_project_id = os.getenv(ASPECT_TYPE_DATAPLEX_PROJECT_ID, ASPECT_TYPE_DATAPLEX_PROJECT_ID_VALUE)
        aspect_type_location = os.getenv(ASPECT_TYPE_DATAPLEX_REGION, ASPECT_TYPE_DATAPLEX_REGION_VALUE)
        resource_path = EMPTY_STRING

        if CUSTOM in entry_type_id:
            resource_path = entry_id
        elif BQ_DATASET_SYSTEM_ENTRY_TYPE in entry_type_id:
            resource_path = f"{BIGQUERY_DOMAIN}/projects/{entry_group_project_id}/datasets/{entry_id}"
        elif BQ_TABLE_SYSTEM_ENTRY_TYPE in entry_type_id:
            dataset, table = fully_qualified_name_splitter(entry_id)
            resource_path = f"{BIGQUERY_DOMAIN}/projects/{entry_group_project_id}/datasets/{dataset}/tables/{table}"
        else:
            info(f"Unsupported entry type: {entry_type_id}")
        result = delete_aspect_from_entry(entry_group_project_id, entry_group_location, entry_group_id, resource_path,
                                          aspect_type_project_id, aspect_type_location, aspect_type_id)
        info(f"Completed aspect removal process")
        return result
    except Exception as e:
        error(f"Error in aspect removal process: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def delete_gcs_custom_entry(entry_project_id: str, entry_location: str, data_product_id: str, entry_id: str) -> dict:
    try:
        entry_group_id = f"{ODP_PREFIX}{data_product_id}{CUSTOM_ENTRY_GROUP_SUFFIX}"
        return delete_custom_entry(entry_project_id, entry_location, entry_group_id, entry_id)
    except Exception as e:
        error(f"Error in delete_gcs_custom_entry: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def delete_gcs_custom_entry_group(entry_group_project_id: str, entry_group_location: str, data_product_id: str) -> dict:
    try:
        entry_group_id = f"{ODP_PREFIX}{data_product_id}{CUSTOM_ENTRY_GROUP_SUFFIX}"
        return delete_custom_entry_group(entry_group_project_id, entry_group_location, entry_group_id)
    except Exception as e:
        error(f"Error in delete_gcs_custom_entry_group: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()


def delete_gcs_custom_entry_type(entry_type_project_id: str, entry_type_location: str, entry_type_id: str) -> dict:
    try:
        return delete_custom_entry_type(entry_type_project_id, entry_type_location, entry_type_id)
    except Exception as e:
        error(f"Error in delete_gcs_custom_entry_type: {e}")
        return APIError(501, {ERROR_KEY: str(e), REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()
