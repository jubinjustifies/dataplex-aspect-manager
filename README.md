* Steps to create or update an aspect.
1. Update the following YAMLs in the project -
    * metadata-enrichment-service\app\configs\aspect_type_asset_mapping.yaml
    * metadata-enrichment-service\app\configs\aspect_type_env_mapping.yaml
    * metadata-enrichment-service\app\configs\product_entry_mapping.yaml
2. Open Postman and provide following configurations -
    * Method - POST
    * URL - http://127.0.0.1:5000/api/aspect
    * Headers - Content-type  |   application/json
    * Body - 
    {
        "data_product_id": "odp_dp_1",
        "aspect_type_id": "data-owner-aspect",
        "aspect_data": {"owner": "Compliance", "email": "compliance@google.com", "domain": "CDP"}
    }
    OR
    {
        "data_product_id": "odp_dp_1",
        "aspect_type_id": "data-quality-aspect",
        "aspect_data": {"last_run": "01-01-2000", "status": "good", "completeness": "90%", "accuracy": "95%"}
    }
3. Hit send and validate the response and resource in gcp console.

* Steps to create an aspect-type.
1. Open Postman and provide following configurations -
    * Method - POST
    * URL - http://127.0.0.1:5000/api/aspect_type
    * Headers - Content-type  |   application/json
    * Body - 
    {
        "project_id": <gcp-project-id>,
        "aspect_type_id": "data-quality-aspect",
        "aspect_type_location": "us-central1",
        "aspect_type_name": "Data Quality Aspect",
        "aspect_type_description": "",
        "metadata_template": {"name": "data-quality-template", "type": "record", "recordFields": [{"name": "last_run", "type": "string", "annotations": {"displayName": "last_run", "description": "Last run date"}, "index": 1, "constraints": {"required": true}}, {"name": "status", "type": "string", "annotations": {"displayName": "status", "description": "Status of the data quality check"}, "index": 2, "constraints": {"required": true}}, {"name": "completeness", "type": "string", "annotations": {"displayName": "completeness", "description": "Completeness percentage"}, "index": 3, "constraints": {"required": true}}, {"name": "accuracy", "type": "string", "annotations": {"displayName": "accuracy", "description": "Accuracy percentage"}, "index": 4, "constraints": {"required": true}}]}
    }
    OR
    {
        "project_id": <gcp-project-id>,
        "aspect_type_id": "data-owner-aspect",
        "aspect_type_location": "us-central1",
        "aspect_type_name": "Data Owner Aspect",
        "aspect_type_description": "",
        "metadata_template": {"name":"data-owner-template","type":"record","recordFields":[{"name":"owner","type":"string","annotations":{"displayName":"Data owner name","description":"Data owner name"},"index":1,"constraints":{"required":true}},{"name":"email","type":"string","annotations":{"displayName":"Data owner email","description":"Data owner email"},"index":2,"constraints":{"required":true}},{"name":"domain","type":"enum","annotations":{"displayName":"domain","description":"Owners domain"},"index":3,"constraints":{"required":true},"enumValues":[{"name":"ODP","index":1},{"name":"FDP","index":2},{"name":"CDP","index":3}]}]}
    }
3. Hit send and validate the response and resource in gcp console.

