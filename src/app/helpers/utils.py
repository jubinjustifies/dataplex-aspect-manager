import os, yaml, traceback, inspect, re, json
from werkzeug.exceptions import BadRequest
from typing import List, Dict, Any
from src.app.models.data_product_model import DataProduct
from src.app.models.aspect_type_asset_mapping_model import AspectTypeAssetMapping
from src.app.models.aspect_type_env_mapping_model import AspectTypeEnvMapping
from src.app.helpers.constant import *
from src.app.helpers.api_helper import rest_api_helper
from src.app.models.api_responses import APIError
from logging import basicConfig, error, INFO, info, warning, debug

basicConfig(level=INFO, format=LOGGING_FORMAT)


def fully_qualified_name_splitter(resource_fqn) -> (str, str):
    resource_parts = resource_fqn.split(".")
    dataset, table = resource_parts[0], (resource_parts[1] if len(resource_parts) > 1 else None)
    # return (resource_fqn.split(".")[0] + [None])[:2]
    return dataset, table


def get_project_number(project_id) -> str:
    url = f"{HTTPS_PATH_PREFIX}{CLOUD_RESOURCE_MANAGER_DOMAIN}/v1/projects/{project_id}"
    api_response = rest_api_helper(GOOGLE_API, url, GET)
    # return str(api_response.get("payload", {}).get("projectNumber"))
    return str(646776580204)


def validate_required_fields(data: dict, fields: list):
    missing = [f for f in fields if f not in data]
    if missing:
        raise APIError(400, {ERROR_KEY: INVALID_INPUT, REASON_KEY: ERROR_MISSING_FIELDS, MISSING_FIELDS_KEY: missing})


def validate_is_json(request):
    if not request.is_json:
        raise APIError(400, {ERROR_KEY: INVALID_INPUT, REASON_KEY: ERROR_INVALID_JSON})
    try:
        _ = request.get_json(force=True)
    except BadRequest:
        raise APIError(400, {ERROR_KEY: INVALID_INPUT, REASON_KEY: ERROR_INVALID_JSON})


def validate_values_are_not_empty(payload: dict):
    empty_values = [k for k, v in payload.items() if v is None or isinstance(v, str) and not v.strip()]
    if empty_values:
        raise APIError(400, {ERROR_KEY: INVALID_INPUT, REASON_KEY: ERROR_EMPTY_VALUES, EMPTY_VALUES_KEY: empty_values})


def validate_values_do_not_have_special_characters(payload: dict):
    invalid_values = [k for k, v in payload if k in FIELD_VALIDATION_PATTERNS and isinstance(payload[k], str) and not re.fullmatch(FIELD_VALIDATION_PATTERNS[k], payload[k])]
    if invalid_values:
        raise APIError(400, {ERROR_KEY: INVALID_INPUT, REASON_KEY: ERROR_INVALID_CHARS, INVALID_VALUES_KEY: invalid_values})


def validate_values_length_do_not_exceed(payload: dict, max_length: int = 100):
    too_long = [k for k, v in payload.items() if isinstance(v, str) and len(v) > max_length]
    if too_long:
        raise APIError(400, {ERROR_KEY: INVALID_INPUT, REASON_KEY: ERROR_LENGTH_EXCEEDED, INVALID_VALUES_KEY: too_long})


def determine_bulk_job_status(api_responses):
    try:
        status_list = [response.get(STATUS_KEY) for response in api_responses if STATUS_KEY in response]
        code_list = [response.get(CODE_KEY) for response in api_responses if CODE_KEY in response]
        message_list = [response.get(MESSAGE_KEY) for response in api_responses if MESSAGE_KEY in response]

        unique_statuses = set(status_list)
        unique_codes = set(code_list)
        unique_messages = set(message_list)

        bulk_status = EMPTY_STRING
        bulk_status_code = 0
        bulk_message = EMPTY_STRING
  
        if len(unique_statuses) == 1 and len(unique_codes) == 1 and len(unique_messages) == 1:
            bulk_status = status_list[0]
            bulk_status_code = code_list[0]
            bulk_message = message_list[0]
        elif 200 in unique_codes and len(unique_codes) > 1:
            bulk_status = PARTIAL_SUCCESS
            bulk_status_code = 207
            bulk_message = SUCCESS_MESSAGES.get(207)
        else:
            failure_codes = [code for code in code_list if code != 200]
            bulk_status = FAILED
            bulk_status_code = max(failure_codes, key=code_list.count)
            bulk_message = BULK_JOB_FAILED

        return {
            STATUS_KEY: bulk_status,
            CODE_KEY: bulk_status_code,
            MESSAGE_KEY: bulk_message,
            RESPONSE_KEY: api_responses
        }
    except ValueError as ve:
        return {
            STATUS_KEY: FAILED,
            CODE_KEY: 501,
            MESSAGE_KEY: str(ve),
            REASON_KEY: api_responses
        }
    except Exception as e:
        return {
            STATUS_KEY: FAILED,
            CODE_KEY: 501,
            MESSAGE_KEY: str(e),
            REASON_KEY: api_responses
        }


def load_multiple_yamls(directory_name):
    yamls = []

    config_path = os.path.abspath(os.path.join(_get_path_for_config(), directory_name))
    for filename in os.listdir(config_path):
        if filename.endswith(YAML_FORMAT) or filename.endswith(YML_FORMAT):
            file_path = os.path.join(config_path, filename)
            filepath = os.path.abspath(file_path)
            with open(filepath, READ_MODE) as file:
                aspect_data = yaml.safe_load(file)
                yamls.append(aspect_data)
    return yamls


def load_multiple_jsons(directory_name: str) -> list:
    jsons = []

    config_path = os.path.abspath(os.path.join(_get_path_for_config(), directory_name))
    for filename in os.listdir(config_path):
        if filename.endswith(JSON_FORMAT):
            file_path = os.path.join(config_path, filename)
            filepath = os.path.abspath(file_path)
            with open(filepath, READ_MODE, encoding="utf-8") as file:
                json_content = json.load(file)
                jsons.append(json_content)
    return jsons


def _get_path_for_config():
    path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "configs"))
    return path


def get_trace_and_log_error(e) -> str:
    frame = inspect.currentframe().f_back
    method_name = frame.f_code.co_name
    line_number = frame.f_lineno
    error(f"Error in {method_name} at line {line_number}: {str(e)}")
    error(traceback.format_exc())
    return f"Line: {line_number}, Method: {method_name}"


def get_config_dir_path(file_name: str, is_global: bool = False) -> str:
    config_path = _get_path_for_config()
    if is_global:
        config_path = os.path.abspath(os.path.join(config_path, file_name))
    else:
        env_name = os.getenv(ENVIRONMENT, "bld")
        config_path = os.path.abspath(os.path.join(config_path, env_name, file_name))
    if not os.path.exists(config_path):
        raise ValueError("Config directory not found")
    return config_path


def get_dataplex_project_id_and_region_from_mapping(aspect_type_env_mapping: AspectTypeEnvMapping, aspect_type_id: str) -> dict:
    for aspect_type in aspect_type_env_mapping.aspect_types:
        if aspect_type.aspect_type_id == aspect_type_id:
            return dict(dataplex_project_id=aspect_type.gcp_project_id, dataplex_region=aspect_type.location_id)
    return None


def get_gcp_asset_list_from_mapping(aspect_type_asset_mapping: AspectTypeAssetMapping, aspect_type_id: str) -> list:
    for aspect_type in aspect_type_asset_mapping.aspect_types:
        if aspect_type.aspect_type_id == aspect_type_id:
            return list(aspect_type.gcp_assets)
    return None


def load_product_entry_mapping(file_path: str) -> List[DataProduct]:
    data = yaml_parser(file_path)
  
    product_list = data.get("data_products", data.get("data_product", []))
    if not product_list:
        raise ValueError("Invalid YAML structure: Missing 'data_products' or 'data_product' key.")
    return [DataProduct(**product) for product in product_list]


def load_aspect_type_env_mapping(file_path: str) -> AspectTypeEnvMapping:
    data = yaml_parser(file_path)
    if "aspect_types" not in data:
        raise ValueError("Invalid YAML structure: Missing 'aspect_types' key.")
    return AspectTypeEnvMapping(aspect_types=data["aspect_types"])


def load_aspect_type_asset_mapping(file_path: str) -> AspectTypeAssetMapping:
    data = yaml_parser(file_path, True)
    if "aspect_types" not in data:
        raise ValueError("Invalid YAML structure: Missing 'aspect_types' key.")
    return AspectTypeAssetMapping(aspect_types=data["aspect_types"])


def yaml_parser(yaml_file_name: str, is_global: bool = False) -> dict:
    config_path = get_config_dir_path(yaml_file_name, is_global)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"YAML file not found: {config_path}")
    with open(config_path, READ_MODE) as file:
        data = yaml.safe_load(file)
    return data


def json_to_aspect_generator(aspect_type_project_id: str, aspect_type_location: str, aspect_type_id: str, aspect_data: Any) -> Dict[str, Dict[str, Any]]:
    aspect_key = f"{aspect_type_project_id}.{aspect_type_location}.{aspect_type_id}"
    aspects = {aspect_key: {DATA_KEY: aspect_data}}
    return aspects
