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



metadata-enrichment-framework/
├── helm-charts/                                      # helm charts template for CICD
├── helm-overrides/                                   # configuration for helm charts for CICD
├── src/
│   ├── app/
│   │   ├── config/
│   │   │   ├── aspect_types/                         # Aspect Type YAML definitions/
│   │   │   │   ├── aspect_type_1.yaml                # Aspect Type 1 YAML
│   │   │   │   └── aspect_type_2.yaml                # Aspect Type 2 YAML
│   │   │   ├── config_manager.py                     # Configuration management for Aspect Types
│   │   |   ├── config_loader.py                      # Configuration file loader (YAML/JSON)
│   │   │   └── schema_validators.py                  # Schema validation for configuration files
│   │   ├── core/
│   │   │   ├── appliers/
│   │   │   │   ├── tag_applier.py                    # Logic for applying tags to resources (e.g., BigQuery, GCS)
│   │   │   │   └── aspect_applier.py                 # Logic to apply aspects to GCS/BigQuery assets
│   │   │   ├── collectors/
│   │   │   │   ├── metadata_collector.py             # Collect metadata from pipelines (batch/streaming)
│   │   │   │   └── dlp_collector.py                  # DLP-specific metadata collection (Sensitive Data)
│   │   │   ├── facade/
│   │   │   │   ├── dataplex_facade.py                # Facade for Dataplex API interactions
│   │   │   │   └── api_helper.py                     # Helper functions for interacting with APIs
│   │   │   ├── hooks/
│   │   │   │   ├── batch_hooks.py                    # Hook-based architecture for batch pipelines
│   │   │   │   ├── stream_hooks.py                   # Hook-based architecture for streaming pipelines
│   │   │   │   └── hook_manager.py                   # Manages the execution of hooks within pipelines
│   │   │   ├── metadata_repos/
│   │   │   │   ├── metadata_repository.py            # Centralized repository for storing metadata
│   │   │   │   └── metadata_sync.py                  # Synchronizes metadata across different sources
│   │   │   ├── utils/
│   │   │   │   ├── gcs_utils.py                      # Utilities for GCS interactions
│   │   │   │   ├── bq_utils.py                       # Utilities for BigQuery interactions
│   │   │   │   └── validation_utils.py               # Utilities for metadata validation
│   │   ├── services/
│   │   │   ├── tag_template_manager/                 # Handles the creation and management of tag templates/
│   │   │   │   ├── terraform/
│   │   │   │   │   ├── tag_template.tf               # Terraform script for creating tag templates
│   │   │   │   │   └── variables.tf                  # Terraform variables file
│   │   │   │   ├── tag_template_manager.py           # Core logic for managing tag templates
│   │   │   │   └── tag_template_api.py               # REST API interface for managing templates
│   │   │   ├── api_server/                           # REST API server for exposing metadata services/
│   │   │   │   ├── api.py                            # API endpoint definitions for applying aspects and tags
│   │   │   │   ├── config_service.py                 # API service to handle configuration-related requests
│   │   │   │   ├── tag_service.py                    # API service for handling tag-related operations
│   │   │   │   ├── aspect_service.py                 # API service for handling aspect-related operations
│   │   │   │   └── dlp_service.py                    # DLP service for handling sensitive data tagging
│   │   |   └── event_dispatcher/                     # Event dispatcher for handling metadata updates and tagging/
│   │   |       ├── event_dispatcher.py               # Manages event-driven metadata tagging
│   │   |       └── pubsub_listener.py                # Listens to Pub/Sub messages for metadata updates
│   │   ├── config.yaml                               # Main configuration file for the framework
│   │   └── main.py                                   # Entry point for running the framework
│   └── test/                                         # Tests for each module/
│       ├── core_tests/
│       │   ├── test_tag_applier.py                   # Unit tests for the Tag Applier
│       │   ├── test_metadata_collector.py            # Unit tests for Metadata Collector
│       │   └── test_hooks.py                         # Unit tests for hook-based architecture
│       ├── services_tests/
│       │   ├── test_tag_template_manager.py          # Unit tests for tag template manager
│       │   ├── test_api_server.py                    # Unit tests for API server logic
│       │   └── test_event_dispatcher.py              # Unit tests for event dispatcher
│       ├── utils_tests/
│       │   ├── test_gcs_utils.py                     # Unit tests for GCS utilities
│       │   ├── test_bq_utils.py                      # Unit tests for BigQuery utilities
│       │   └── test_validation_utils.py              # Unit tests for metadata validation
│       └── integration_tests/
│           ├── test_metadata_flow.py                 # End-to-end tests for metadata enrichment
│           ├── test_dlp_integration.py               # Integration tests for DLP metadata collection
│           └── test_tag_applier_integration.py       # Tests integration with the Tag Applier
├── pipelines/
|   └── Jenkinsfile
├── Dockerfile                                        # Dockerfile for POD base image
├── requirements.txt                                  # Dependencies for the framework
└── README.md                                         # Documentation for setting up and using the framework