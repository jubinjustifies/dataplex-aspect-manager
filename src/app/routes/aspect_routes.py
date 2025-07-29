from flask import Blueprint, request, jsonify
from src.app.models.api_responses import APIError
from src.app.helpers.constant import *
from src.app.helpers.utils import *
from logging import basicConfig, INFO
from src.app.services.aspect_manager import (
    create_update_bulk_aspects_with_yaml, retrieve_aspect, remove_aspect, create_update_bulk_aspect_types_json,
    retrieve_aspect_type, remove_aspect_type, delete_gcs_custom_entry, delete_gcs_custom_entry_group,
    delete_gcs_custom_entry_type
)

basicConfig(level=INFO, format=LOGGING_FORMAT)

aspect_bp = Blueprint('aspect_bp', __name__, url_prefix='/dataplex-management-service/api/v1')


@aspect_bp.route('/', methods=[GET])
def check():
    return jsonify({"status": "success", "message": "dataplex-management-service is running"}), 200


@aspect_bp.route('/aspect', methods=[POST])
def handle_aspect_creation():
    try:
        validate_is_json(request)
        data = request.get_json()
        validate_required_fields(data, ASPECT_CREATION_REQUIRED_FIELDS)
        validate_values_are_not_empty(data)
        # validate_values_do_not_have_special_characters(data)
        validate_values_length_do_not_exceed(data)
        result = create_update_bulk_aspects_with_yaml(data[ASPECT_CREATION_REQUIRED_FIELDS[0]],
                                                      data[ASPECT_CREATION_REQUIRED_FIELDS[1]],
                                                      data[ASPECT_CREATION_REQUIRED_FIELDS[2]])
        return jsonify(result), result.get(CODE_KEY)
    except APIError as e:
        return jsonify(e.to_json()), e.status_code
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501


@aspect_bp.route('/aspect', methods=[GET])
def handle_aspect_retrieval():
    try:
        data = request.args.to_dict()
        validate_required_fields(data, ASPECT_RETRIEVAL_REQUIRED_FIELDS)
        result = retrieve_aspect(data[ASPECT_RETRIEVAL_REQUIRED_FIELDS[0]],
                                 data[ASPECT_RETRIEVAL_REQUIRED_FIELDS[1]],
                                 data[ASPECT_RETRIEVAL_REQUIRED_FIELDS[2]],
                                 data[ASPECT_RETRIEVAL_REQUIRED_FIELDS[3]],
                                 data[ASPECT_RETRIEVAL_REQUIRED_FIELDS[4]],
                                 data[ASPECT_RETRIEVAL_REQUIRED_FIELDS[5]])
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501
    

@aspect_bp.route('/aspect', methods=[DELETE])
def handle_aspect_deletion():
    try:
        data = request.args.to_dict()
        validate_required_fields(data, ASPECT_DELETION_REQUIRED_FIELDS)
        result = remove_aspect(data[ASPECT_DELETION_REQUIRED_FIELDS[0]],
                               data[ASPECT_DELETION_REQUIRED_FIELDS[1]],
                               data[ASPECT_DELETION_REQUIRED_FIELDS[2]],
                               data[ASPECT_DELETION_REQUIRED_FIELDS[3]],
                               data[ASPECT_DELETION_REQUIRED_FIELDS[4]],
                               data[ASPECT_DELETION_REQUIRED_FIELDS[5]])
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501


@aspect_bp.route('/aspect-type', methods=[POST])
def handle_aspect_type_creation_updation():
    try:
        result = create_update_bulk_aspect_types_json()
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501


@aspect_bp.route('/aspect-type', methods=[GET])
def handle_aspect_type_retrieval():
    try:
        data = request.args.to_dict()
        validate_required_fields(data, ASPECT_TYPE_RETRIEVAL_REQUIRED_FIELDS)
        result = retrieve_aspect_type(data[ASPECT_TYPE_RETRIEVAL_REQUIRED_FIELDS[0]])
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501
    

@aspect_bp.route('/aspect-type', methods=[DELETE])
def handle_aspect_type_deletion():
    try:
        data = request.args.to_dict()
        validate_required_fields(data, ASPECT_TYPE_DELETION_REQUIRED_FIELDS)
        result = remove_aspect_type(data[ASPECT_TYPE_DELETION_REQUIRED_FIELDS[0]])
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501


@aspect_bp.route('/entry', methods=[DELETE])
def handle_entry_deletion():
    try:
        data = request.args.to_dict()
        validate_required_fields(data, CUSTOM_ENTRY_DELETION_REQUIRED_FIELDS)
        result = delete_gcs_custom_entry(data[CUSTOM_ENTRY_DELETION_REQUIRED_FIELDS[0]],
                                         data[CUSTOM_ENTRY_DELETION_REQUIRED_FIELDS[1]],
                                         data[CUSTOM_ENTRY_DELETION_REQUIRED_FIELDS[2]],
                                         data[CUSTOM_ENTRY_DELETION_REQUIRED_FIELDS[3]])
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501


@aspect_bp.route('/entry-group', methods=[DELETE])
def handle_entry_group_deletion():
    try:
        data = request.args.to_dict()
        validate_required_fields(data, CUSTOM_ENTRY_GROUP_DELETION_REQUIRED_FIELDS)
        result = delete_gcs_custom_entry_group(data[CUSTOM_ENTRY_GROUP_DELETION_REQUIRED_FIELDS[0]],
                                               data[CUSTOM_ENTRY_GROUP_DELETION_REQUIRED_FIELDS[1]],
                                               data[CUSTOM_ENTRY_GROUP_DELETION_REQUIRED_FIELDS[2]])
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501


@aspect_bp.route('/entry-type', methods=[DELETE])
def handle_entry_type_deletion():
    try:
        data = request.args.to_dict()
        validate_required_fields(data, CUSTOM_ENTRY_TYPE_DELETION_REQUIRED_FIELDS)
        result = delete_gcs_custom_entry_type(data[CUSTOM_ENTRY_TYPE_DELETION_REQUIRED_FIELDS[0]],
                                              data[CUSTOM_ENTRY_TYPE_DELETION_REQUIRED_FIELDS[1]],
                                              data[CUSTOM_ENTRY_TYPE_DELETION_REQUIRED_FIELDS[2]])
        return jsonify(result), result.get(CODE_KEY)
    except Exception as e:
        return jsonify(APIError(501, {ERROR_KEY: str(e),
                                      REASON_KEY: f"{FAILURE_AT} {get_trace_and_log_error(e)}"}).to_json()), 501