import unittest
from unittest.mock import patch, MagicMock
import logging
from src.app.controllers.aspect_controller import (
    update_system_entry_bq_table,
    update_system_entry_bq_dataset,
    update_system_entry_spn_schema,
    update_system_entry_spn_table,
    update_system_entry_gcs_bucket
)

# Suppress logging during tests if not needed, or configure as desired
logging.disable(logging.CRITICAL)

class TestAspectController(unittest.TestCase):

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_bq_table_success(self, mock_rest_api_helper):
        mock_response = {"name": "projects/test-project/locations/us-central1/entryGroups/@bigquery/entries/some_entry_id"}
        mock_rest_api_helper.return_value = mock_response

        dataplex_project_id = "test-dp-project"
        entry_group_location = "us-central1"
        bigquery_project_id = "test-bq-project"
        bigquery_region = "us-central1"
        bigquery_dataset = "my_dataset"
        bigquery_table = "my_table"
        aspects = {"custom_aspect": {"key": "value"}}

        response = update_system_entry_bq_table(
            dataplex_project_id, entry_group_location, bigquery_project_id,
            bigquery_region, bigquery_dataset, bigquery_table, aspects
        )

        self.assertEqual(response, mock_response)
        expected_url = (
            f"https://dataplex.googleapis.com/v1/projects/{dataplex_project_id}/locations/{entry_group_location}/entryGroups/"
            f"@bigquery/entries/bigquery.googleapis.com/projects/{bigquery_project_id}/datasets/{bigquery_dataset}/tables/{bigquery_table}?update_mask=aspects"
        )
        expected_data = {"aspects": aspects}
        mock_rest_api_helper.assert_called_once_with(expected_url, "PATCH", expected_data)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_bq_table_failure(self, mock_rest_api_helper):
        mock_rest_api_helper.side_effect = Exception("API Error")

        response = update_system_entry_bq_table(
            "p", "l", "bp", "br", "bd", "bt", {}
        )
        self.assertIsNone(response)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_bq_dataset_success(self, mock_rest_api_helper):
        mock_response = {"name": "projects/test-project/locations/us-central1/entryGroups/@bigquery/entries/some_dataset_entry_id"}
        mock_rest_api_helper.return_value = mock_response

        dataplex_project_id = "test-dp-project"
        entry_group_location = "us-central1"
        bigquery_project_id = "test-bq-project"
        bigquery_region = "us-central1"
        bigquery_dataset = "my_dataset"
        aspects = {"custom_aspect": {"key": "value"}}

        response = update_system_entry_bq_dataset(
            dataplex_project_id, entry_group_location, bigquery_project_id,
            bigquery_region, bigquery_dataset, aspects
        )

        self.assertEqual(response, mock_response)
        expected_url = (
            f"https://dataplex.googleapis.com/v1/projects/{dataplex_project_id}/locations/{entry_group_location}/entryGroups/"
            f"@bigquery/entries/bigquery.googleapis.com/projects/{bigquery_project_id}/datasets/{bigquery_dataset}?update_mask=aspects"
        )
        expected_data = {"aspects": aspects}
        mock_rest_api_helper.assert_called_once_with(expected_url, "PATCH", expected_data)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_bq_dataset_failure(self, mock_rest_api_helper):
        mock_rest_api_helper.side_effect = Exception("API Error")
        response = update_system_entry_bq_dataset(
            "p", "l", "bp", "br", "bd", {}
        )
        self.assertIsNone(response)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_spn_schema_success(self, mock_rest_api_helper):
        mock_response = {"name": "projects/test-project/locations/us-central1/entryGroups/@spanner/entries/some_spanner_schema_entry_id"}
        mock_rest_api_helper.return_value = mock_response

        dataplex_project_id = "test-dp-project"
        entry_group_location = "us-central1"
        spanner_project_id = "test-sp-project"
        spanner_region = "us-central1" # Note: spannerRegion is not used in URL construction in the original code for schema
        spanner_instance = "my_instance"
        spanner_database = "my_database"
        aspects = {"custom_aspect": {"key": "value"}}

        response = update_system_entry_spn_schema(
            dataplex_project_id, entry_group_location, spanner_project_id,
            spanner_region, spanner_instance, spanner_database, aspects
        )

        self.assertEqual(response, mock_response)
        expected_url = (
            f"https://dataplex.googleapis.com/v1/projects/{dataplex_project_id}/locations/{entry_group_location}/entryGroups/"
            f"@spanner/entries/spanner.googleapis.com/projects/{spanner_project_id}/instances/{spanner_instance}/databases/{spanner_database}?update_mask=aspects"
        )
        expected_data = {"aspects": aspects}
        mock_rest_api_helper.assert_called_once_with(expected_url, "PATCH", expected_data)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_spn_schema_failure(self, mock_rest_api_helper):
        mock_rest_api_helper.side_effect = Exception("API Error")
        response = update_system_entry_spn_schema(
            "p", "l", "sp", "sr", "si", "sd", {}
        )
        self.assertIsNone(response)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_spn_table_success(self, mock_rest_api_helper):
        mock_response = {"name": "projects/test-project/locations/us-central1/entryGroups/@spanner/entries/some_spanner_table_entry_id"}
        mock_rest_api_helper.return_value = mock_response

        dataplex_project_id = "test-dp-project"
        entry_group_location = "us-central1"
        spanner_project_id = "test-sp-project"
        spanner_region = "us-central1" # Note: spannerRegion is not used in URL construction in the original code for table
        spanner_instance = "my_instance"
        spanner_database = "my_database"
        spanner_table = "my_table"
        aspects = {"custom_aspect": {"key": "value"}}

        response = update_system_entry_spn_table(
            dataplex_project_id, entry_group_location, spanner_project_id,
            spanner_region, spanner_instance, spanner_database, spanner_table, aspects
        )

        self.assertEqual(response, mock_response)
        expected_url = (
            f"https://dataplex.googleapis.com/v1/projects/{dataplex_project_id}/locations/{entry_group_location}/entryGroups/"
            f"@spanner/entries/spanner.googleapis.com/projects/{spanner_project_id}/instances/{spanner_instance}/databases/{spanner_database}/tables/{spanner_table}?update_mask=aspects"
        )
        expected_data = {"aspects": aspects}
        mock_rest_api_helper.assert_called_once_with(expected_url, "PATCH", expected_data)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_spn_table_failure(self, mock_rest_api_helper):
        mock_rest_api_helper.side_effect = Exception("API Error")
        response = update_system_entry_spn_table(
            "p", "l", "sp", "sr", "si", "sd", "st", {}
        )
        self.assertIsNone(response)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_gcs_bucket_success(self, mock_rest_api_helper):
        mock_response = {"name": "projects/test-project/locations/us-central1/entryGroups/@storage/entries/some_gcs_entry_id"}
        mock_rest_api_helper.return_value = mock_response

        dataplex_project_id = "test-dp-project"
        entry_group_location = "us-central1"
        gcs_project_id = "test-gcs-project" # Note: gcsProjectId is not used in URL construction in the original code
        gcs_region = "us-central1"       # Note: gcsRegion is not used in URL construction in the original code
        gcs_bucket = "my_bucket"
        aspects = {"custom_aspect": {"key": "value"}}

        response = update_system_entry_gcs_bucket(
            dataplex_project_id, entry_group_location, gcs_project_id,
            gcs_region, gcs_bucket, aspects
        )

        self.assertEqual(response, mock_response)
        expected_url = (
            f"https://dataplex.googleapis.com/v1/projects/{dataplex_project_id}/locations/{entry_group_location}/entryGroups/"
            f"@storage/entries/storage.googleapis.com/{gcs_bucket}?update_mask=aspects"
        )
        expected_data = {"aspects": aspects}
        mock_rest_api_helper.assert_called_once_with(expected_url, "PATCH", expected_data)

    @patch('src.app.services.aspect_controller.rest_api_helper')
    def test_update_system_entry_gcs_bucket_failure(self, mock_rest_api_helper):
        mock_rest_api_helper.side_effect = Exception("API Error")
        response = update_system_entry_gcs_bucket(
            "p", "l", "gp", "gr", "gb", {}
        )
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
# if __name__ == '__main__':
#     unittest.main()