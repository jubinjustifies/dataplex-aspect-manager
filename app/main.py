from services.operations_handler import *
from utils import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# product_id = "odp_dp_1"
# myAspectTypeId = "data-owner-aspect"
# aspect_data = '{"owner": "Compliance", "email": "compliance@google.com", "data_product_type": "ODP"}'

# logging.info(f"Starting Job")
# create_or_update_aspect(product_id, myAspectTypeId, aspect_data)

# aspect_type_id = "data-quality-aspect"
# aspect_type_location = "us-central1"
# aspect_type_name = "Data Quality Aspect"
# aspect_type_description = ""
# metadata_template = '{"name": "data-quality-template", "type": "record", "recordFields": [{"name": "last_run", "type": "string", "annotations": {"displayName": "last_run", "description": "Last run date"}, "index": 1, "constraints": {"required": true}}, {"name": "status", "type": "string", "annotations": {"displayName": "status", "description": "Status of the data quality check"}, "index": 2, "constraints": {"required": true}}, {"name": "completeness", "type": "string", "annotations": {"displayName": "completeness", "description": "Completeness percentage"}, "index": 3, "constraints": {"required": true}}, {"name": "accuracy", "type": "string", "annotations": {"displayName": "accuracy", "description": "Accuracy percentage"}, "index": 4, "constraints": {"required": true}}]}'
# metadata_template = '{"name":"data-owner-template","type":"record","recordFields":[{"name":"owner","type":"string","annotations":{"displayName":"Data owner name","description":"Data owner name"},"index":1,"constraints":{"required":true}},{"name":"email","type":"string","annotations":{"displayName":"Data owner email","description":"Data owner email"},"index":2,"constraints":{"required":true}},{"name":"domain","type":"enum","annotations":{"displayName":"domain","description":"Owners domain"},"index":3,"constraints":{"required":true},"enumValues":[{"name":"ODP","index":1},{"name":"FDP","index":2},{"name":"CDP","index":3}]}]}'
logging.info(f"Starting Job")
# create_or_update_aspect_type(project_id, aspect_type_id, aspect_type_location, aspect_type_name, aspect_type_description, metadata_template)
logging.info(f"Completed Job")