

ASPECT_TYPE_ENV_MAPPING_FILE = "aspect_type_env_mapping.yaml"
PRODUCT_ENTRY_MAPPING_FILE = "product_entry_mapping.yaml"
ASPECT_TYPE_ASSET_MAPPING_FILE = "aspect_type_asset_mapping.yaml"
ASPECTS_DIRECTORY = "aspect_types"

HTTPS_PATH_PREFIX = "https://"
DATAPLEX_DOMAIN = "dataplex.googleapis.com"
BIGQUERY_DOMAIN = "bigquery.googleapis.com"
SPANNER_DOMAIN = "spanner.googleapis.com"
CLOUD_RESOURCE_MANAGER_DOMAIN = "cloudresourcemanager.googleapis.com"
GOOGLE_API = "google"
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

#https methods
GET = "GET"
POST = "POST"
PUT = "PUT"
PATCH = "PATCH"
DELETE = "DELETE"

ERROR_MESSAGES = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    500: "Internal Server Error",
    503: "Service Unavailable"
}
SUCCESS_MESSAGES = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content"
}
UNEXPECTED_ERROR = "Unexpected Error: Something went wrong."

REQUEST_ID = "request_id"
STATUS_KEY = "status"
CODE_KEY = "code"
MESSAGE_KEY = "message"
RESPONSE_KEY = "response"
PAYLOAD_KEY = "payload"
REASON_KEY = "reason"
ERROR_KEY = "error"
SUCCESS = "success"
FAILED = "failed"
INVALID_INPUT = "invalid input"
FAILURE_AT = "failure at"
ASPECT_TYPE_DATAPLEX_PROJECT_ID = "ASPECT_TYPE_DATAPLEX_PROJECT_ID"
ASPECT_TYPE_DATAPLEX_REGION = "ASPECT_TYPE_DATAPLEX_REGION"
EMPTY_STRING = ""
PIPE_DELIMITER = "|"
PARTIAL_SUCCESS = "partial success"
INVALID_CONFIG = "invalid config"
BQ_TABLE = "bq_table"
BQ_DATASET = "bq_dataset"
GCS_BUCKET = "gcs_bucket"
CUSTOM = "custom"
GCS_BUCKET_CUSTOM_ENTRY_TYPE = "custom-storage-bucket"
BQ_DATASET_SYSTEM_ENTRY_TYPE = "bigquery-dataset"
BQ_TABLE_SYSTEM_ENTRY_TYPE = "bigquery-table"
ODP_PREFIX = "odp-"
CUSTOM_ENTRY_GROUP_SUFFIX = "-entry-group"
ODP = "ODP"
CUSTOM_ENTRY_GROUP = "Custom Entry Group"
CUSTOM_ENTRY_GROUP_DESCRIPTION = "Custom Entry Group for ODP with Data Product Id:"
GCS_BUCKET_CUSTOM_ENTRY_TYPE_NAME = "Custom Storage Bucket"
GCS_BUCKET_CUSTOM_ENTRY_TYPE_DESCRIPTION = "Custom Storage Bucket"
PLATFORM = "Google Cloud"
SYSTEM = "Storage"
GCS_BUCKET_TYPE_ALIASES = "BUCKET"
YAML_FORMAT = ".yaml"
YML_FORMAT = ".yml"
JSON_FORMAT = ".json"
READ_MODE = "r"
ENVIRONMENT = "bld"
DATA_KEY = "data"


BULK_JOB_FAILED = "Bulk job failed. Most common failure reason provided."
ERROR_INVALID_JSON = "Request body must be a valid JSON"
ERROR_MISSING_FIELDS = "Request body must have required fields"
ERROR_EMPTY_VALUES = "Request body must not have empty values"
ERROR_INVALID_CHARS = "Request body must not have special characters"
ERROR_LENGTH_EXCEEDED = "Request body must not have more than 100 characters"
EMPTY_VALUES_KEY = "empty_values"
MISSING_FIELDS_KEY = "missing_fields"
INVALID_VALUES_KEY = "invalid_values"

ASPECT_CREATION_REQUIRED_FIELDS = ['data_product_id', 'aspect_type_id', 'aspect_data']
ASPECT_RETRIEVAL_REQUIRED_FIELDS = ['entry_group_project_id', 'entry_group_location', 'entry_group_id', 'entry_type_id', 'entry_id', 'aspect_type_id']
ASPECT_DELETION_REQUIRED_FIELDS = ['entry_group_project_id', 'entry_group_location', 'entry_group_id', 'entry_type_id', 'entry_id', 'aspect_type_id']
ASPECT_TYPE_RETRIEVAL_REQUIRED_FIELDS = ['aspect_type_id']
ASPECT_TYPE_DELETION_REQUIRED_FIELDS = ['aspect_type_id']
CUSTOM_ENTRY_DELETION_REQUIRED_FIELDS = ['entry_group_project_id', 'entry_group_location', 'data_product_id', 'entry_id']
CUSTOM_ENTRY_GROUP_DELETION_REQUIRED_FIELDS = ['entry_group_project_id', 'entry_group_location', 'data_product_id']
CUSTOM_ENTRY_TYPE_DELETION_REQUIRED_FIELDS = ['entry_type_project_id', 'entry_type_location', 'entry_type_id']

ALPHABET_DIGIT_HYPHEN = r"^[a-zA-Z0-9\-]+$"
FIELD_VALIDATION_PATTERNS = {
    "data_product_id": ALPHABET_DIGIT_HYPHEN,
    "aspect_type_id": ALPHABET_DIGIT_HYPHEN
}




ASPECT_TYPE_DATAPLEX_PROJECT_ID_VALUE = "burner-jubsharm"
ASPECT_TYPE_DATAPLEX_REGION_VALUE = "us-central1"