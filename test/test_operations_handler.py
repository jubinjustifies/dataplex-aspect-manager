import unittest
from unittest.mock import patch, MagicMock, call
import logging

# Module to be tested
from src.app.services.aspect_manager import (
    create_or_update_aspect_type,
    create_or_update_aspect
)

# Suppress logging during tests
logging.disable(logging.CRITICAL)

class TestOperationsHandler(unittest.TestCase):

    def _create_mock_data_product_list(self, product_id_to_match, gcp_project_id, location_id, assets_config_list):
        """
        Helper to create a list of mock DataProduct objects.
        assets_config_list: e.g., [
            {"asset_type_id": "bq_table", "asset_names": ["ds1.tbl1", "ds1.tbl2"]},
            {"asset_type_id": "gcs_bucket", "asset_names": ["bucket1"]}
        ]
        """
        mock_data_products = []
        
        product_mock = MagicMock()
        product_mock.product_id = product_id_to_match
        
        gcp_projects_list = []
        gcp_project_mock = MagicMock()
        gcp_project_mock.project_id = gcp_project_id
        
        locations_list = []
        location_mock = MagicMock()
        location_mock.location_id = location_id
        
        asset_types_list = []
        for asset_config in assets_config_list:
            asset_type_mock = MagicMock()
            asset_type_mock.asset_type_id = asset_config["asset_type_id"]
            
            current_assets = []
            if asset_config.get("asset_names"):
                for name in asset_config["asset_names"]:
                    asset_item_mock = MagicMock()
                    asset_item_mock.asset_name = name
                    asset_item_mock.flag = "test_flag"
                    current_assets.append(asset_item_mock)
            # Ensure 'assets' attribute exists for hasattr check, even if empty
            asset_type_mock.assets = current_assets
            asset_types_list.append(asset_type_mock)
            
        location_mock.asset_types = asset_types_list
        locations_list.append(location_mock)
        gcp_project_mock.locations = locations_list
        gcp_projects_list.append(gcp_project_mock)
        product_mock.gcp_projects = gcp_projects_list
        
        mock_data_products.append(product_mock)
        return mock_data_products

    @patch('src.app.services.operations_handler.create_aspect_type')
    def test_create_or_update_aspect_type_success(self, mock_create_aspect_type):
        mock_response = {"name": "new_aspect_type"}
        mock_create_aspect_type.return_value = mock_response

        project_id = "test-project"
        aspect_type_id = "customAspect"
        aspect_type_location = "us-central1"
        aspect_type_name = "Custom Aspect"
        aspect_type_description = "A test aspect type"
        metadata_template = {"type": "record", "name": "CustomAspect"}

        response = create_or_update_aspect_type(
            project_id, aspect_type_id, aspect_type_location,
            aspect_type_name, aspect_type_description, metadata_template
        )

        self.assertEqual(response, mock_response)
        mock_create_aspect_type.assert_called_once_with(
            project_id, aspect_type_id, aspect_type_location,
            aspect_type_name, aspect_type_description, metadata_template
        )

    @patch('src.app.services.operations_handler.data_product', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_asset_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_env_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.update_system_entry_gcs_bucket')
    @patch('src.app.services.operations_handler.update_system_entry_spn_table')
    @patch('src.app.services.operations_handler.update_system_entry_spn_schema')
    @patch('src.app.services.operations_handler.update_system_entry_bq_table')
    @patch('src.app.services.operations_handler.update_system_entry_bq_dataset')
    @patch('src.app.services.operations_handler.json_to_aspect_generator')
    @patch('src.app.services.operations_handler.get_gcp_asset_list_from_mapping')
    @patch('src.app.services.operations_handler.get_dataplex_project_id_and_region_from_mapping')
    def test_create_or_update_aspect_success_bq_table_and_gcs_bucket(
            self, mock_get_env_mapping, mock_get_asset_list, mock_json_to_aspect,
            mock_update_bq_dataset, mock_update_bq_table,
            mock_update_spn_schema, mock_update_spn_table, mock_update_gcs_bucket,
            mock_env_map_data, mock_asset_map_data, mock_dp_data):

        # Setup Mocks
        mock_get_env_mapping.return_value = {"dataplex_project_id": "dp-proj", "dataplex_region": "dp-reg"}
        mock_get_asset_list.return_value = ["bq_table", "gcs_bucket"]
        mock_generated_aspects = {"generated_aspect": "value"}
        mock_json_to_aspect.return_value = mock_generated_aspects

        mock_bq_table_response = {"name": "bq_table_aspect_updated"}
        mock_update_bq_table.return_value = mock_bq_table_response
        mock_gcs_bucket_response = {"name": "gcs_bucket_aspect_updated"}
        mock_update_gcs_bucket.return_value = mock_gcs_bucket_response

        data_product_id = "product1"
        gcp_project_id = "gcp-proj1"
        location_id = "loc1"
        
        assets_config = [
            {"asset_type_id": "bq_table", "asset_names": ["dataset1.tableA"]},
            {"asset_type_id": "gcs_bucket", "asset_names": ["my-bucket-name"]},
            {"asset_type_id": "other_type", "asset_names": ["other.asset"]} # Should be ignored
        ]
        mock_dp_data.return_value = self._create_mock_data_product_list(
            data_product_id, gcp_project_id, location_id, assets_config
        )
        # The actual values of these don't matter as the functions using them are mocked
        type(mock_env_map_data).return_value = MagicMock()
        type(mock_asset_map_data).return_value = MagicMock()


        # Call the function
        response = create_or_update_aspect(data_product_id, "aspect_type_A", {"data": "sample"})

        # Assertions
        mock_get_env_mapping.assert_called_once_with(mock_env_map_data, "aspect_type_A")
        mock_get_asset_list.assert_called_once_with(mock_asset_map_data, "aspect_type_A")
        
        self.assertEqual(mock_json_to_aspect.call_count, 2)
        mock_json_to_aspect.assert_any_call("dp-proj", "dp-reg", "aspect_type_A", {"data": "sample"})

        mock_update_bq_table.assert_called_once_with(
            "dp-proj", "dp-reg", gcp_project_id, location_id, "dataset1", "tableA", mock_generated_aspects
        )
        mock_update_gcs_bucket.assert_called_once_with(
            "dp-proj", "dp-reg", gcp_project_id, location_id, "my-bucket-name", mock_generated_aspects
        )
        
        mock_update_bq_dataset.assert_not_called()
        mock_update_spn_schema.assert_not_called()
        mock_update_spn_table.assert_not_called()

        self.assertIsNotNone(response)
        self.assertIn("response", response)
        self.assertEqual(len(response["response"]), 2)
        self.assertIn(mock_bq_table_response, response["response"])
        self.assertIn(mock_gcs_bucket_response, response["response"])

    @patch('src.app.services.operations_handler.data_product', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_asset_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_env_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.update_system_entry_spn_schema')
    @patch('src.app.services.operations_handler.json_to_aspect_generator')
    @patch('src.app.services.operations_handler.get_gcp_asset_list_from_mapping')
    @patch('src.app.services.operations_handler.get_dataplex_project_id_and_region_from_mapping')
    def test_create_or_update_aspect_spanner_schema_call(
            self, mock_get_env_mapping, mock_get_asset_list, mock_json_to_aspect,
            mock_update_spn_schema,
            mock_env_map_data, mock_asset_map_data, mock_dp_data):

        mock_get_env_mapping.return_value = {"dataplex_project_id": "dp-proj", "dataplex_region": "dp-reg"}
        mock_get_asset_list.return_value = ["spn_schema"]
        mock_generated_aspects = {"spanner_aspect": "data"}
        mock_json_to_aspect.return_value = mock_generated_aspects
        mock_spn_schema_response = {"name": "spn_schema_updated"}
        mock_update_spn_schema.return_value = mock_spn_schema_response

        data_product_id = "product_spn"
        gcp_project_id = "gcp-spanner-proj"
        location_id = "spanner-loc"
        spanner_instance_name = "my-spanner-instance"
        spanner_database_name = "my-spanner-db"
        
        assets_config = [
            {"asset_type_id": "spn_schema", "asset_names": [f"{spanner_instance_name}.{spanner_database_name}"]},
        ]
        mock_dp_data.return_value = self._create_mock_data_product_list(
            data_product_id, gcp_project_id, location_id, assets_config
        )
        type(mock_env_map_data).return_value = MagicMock()
        type(mock_asset_map_data).return_value = MagicMock()

        response = create_or_update_aspect(data_product_id, "aspect_spanner", {"key": "val"})

        mock_update_spn_schema.assert_called_once_with(
            "dp-proj", 
            "dp-reg", 
            gcp_project_id, 
            location_id, 
            spanner_instance_name, # This is asset.asset_name.split(".")[0], passed as spannerInstance
            mock_generated_aspects # This is passed as spannerDatabase due to arg mismatch
        )
        self.assertEqual(response["response"], [mock_spn_schema_response])


    @patch('src.app.services.operations_handler.data_product', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_asset_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_env_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.update_system_entry_spn_table')
    @patch('src.app.services.operations_handler.json_to_aspect_generator')
    @patch('src.app.services.operations_handler.get_gcp_asset_list_from_mapping')
    @patch('src.app.services.operations_handler.get_dataplex_project_id_and_region_from_mapping')
    def test_create_or_update_aspect_spanner_table_call(
            self, mock_get_env_mapping, mock_get_asset_list, mock_json_to_aspect,
            mock_update_spn_table,
            mock_env_map_data, mock_asset_map_data, mock_dp_data):

        mock_get_env_mapping.return_value = {"dataplex_project_id": "dp-proj", "dataplex_region": "dp-reg"}
        mock_get_asset_list.return_value = ["spn_table"]
        mock_generated_aspects = {"spanner_aspect_table": "data_table"}
        mock_json_to_aspect.return_value = mock_generated_aspects
        mock_spn_table_response = {"name": "spn_table_updated"}
        mock_update_spn_table.return_value = mock_spn_table_response

        data_product_id = "product_spn_tbl"
        gcp_project_id = "gcp-spanner-proj-tbl"
        location_id = "spanner-loc-tbl"
        spanner_instance_name = "my-spanner-instance-tbl"
        spanner_database_name = "my-spanner-db-tbl"
        spanner_table_name = "my-spanner-table"
        
        assets_config = [
            {"asset_type_id": "spn_table", "asset_names": [f"{spanner_instance_name}.{spanner_database_name}.{spanner_table_name}"]},
        ]
        mock_dp_data.return_value = self._create_mock_data_product_list(
            data_product_id, gcp_project_id, location_id, assets_config
        )
        type(mock_env_map_data).return_value = MagicMock()
        type(mock_asset_map_data).return_value = MagicMock()

        response = create_or_update_aspect(data_product_id, "aspect_spanner_tbl", {"key_tbl": "val_tbl"})

        mock_update_spn_table.assert_called_once_with(
            "dp-proj", 
            "dp-reg", 
            gcp_project_id, 
            location_id, 
            spanner_instance_name, # asset.asset_name.split(".")[0] -> spannerInstance
            spanner_database_name, # asset.asset_name.split(".")[1] -> spannerDatabase
            mock_generated_aspects # aspects -> spannerTable
        )
        self.assertEqual(response["response"], [mock_spn_table_response])


    @patch('src.app.services.operations_handler.get_dataplex_project_id_and_region_from_mapping')
    def test_create_or_update_aspect_no_env_mapping(self, mock_get_env_mapping):
        mock_get_env_mapping.return_value = None # Simulate no mapping found
        
        # Other mocks are not strictly needed as the function should exit early
        with patch('src.app.services.operations_handler.aspect_type_env_mapping', MagicMock()):
             response = create_or_update_aspect("product1", "aspect_type_A", {})
        
        self.assertIsNone(response)
        mock_get_env_mapping.assert_called_once()

    @patch('src.app.services.operations_handler.data_product', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_asset_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_env_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.get_gcp_asset_list_from_mapping')
    @patch('src.app.services.operations_handler.get_dataplex_project_id_and_region_from_mapping')
    def test_create_or_update_aspect_no_matching_product_id(
            self, mock_get_env_mapping, mock_get_asset_list,
            mock_env_map_data, mock_asset_map_data, mock_dp_data):
        
        mock_get_env_mapping.return_value = {"dataplex_project_id": "dp-proj", "dataplex_region": "dp-reg"}
        mock_get_asset_list.return_value = ["bq_table"] # Does not matter much here

        # Create data_product list that does NOT contain "product_to_find"
        mock_dp_data.return_value = self._create_mock_data_product_list(
            "some_other_product", "gcp-proj", "loc", [{"asset_type_id": "bq_table", "asset_names": ["ds.tbl"]}]
        )
        type(mock_env_map_data).return_value = MagicMock()
        type(mock_asset_map_data).return_value = MagicMock()

        response = create_or_update_aspect("product_to_find", "aspect_type_A", {})
        
        self.assertEqual(response, {"response": []})


    @patch('src.app.services.operations_handler.data_product', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_asset_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_env_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.update_system_entry_bq_table')
    @patch('src.app.services.operations_handler.json_to_aspect_generator')
    @patch('src.app.services.operations_handler.get_gcp_asset_list_from_mapping')
    @patch('src.app.services.operations_handler.get_dataplex_project_id_and_region_from_mapping')
    def test_create_or_update_aspect_asset_type_not_in_gcp_list(
            self, mock_get_env_mapping, mock_get_asset_list, mock_json_to_aspect,
            mock_update_bq_table,
            mock_env_map_data, mock_asset_map_data, mock_dp_data):

        mock_get_env_mapping.return_value = {"dataplex_project_id": "dp-proj", "dataplex_region": "dp-reg"}
        # "bq_table" is in data_product, but not in the list returned by mapping
        mock_get_asset_list.return_value = ["some_other_asset_type"] 
        mock_json_to_aspect.return_value = {"aspect": "data"}

        data_product_id = "product1"
        assets_config = [{"asset_type_id": "bq_table", "asset_names": ["dataset1.tableA"]}]
        mock_dp_data.return_value = self._create_mock_data_product_list(
            data_product_id, "gcp-proj", "loc", assets_config
        )
        type(mock_env_map_data).return_value = MagicMock()
        type(mock_asset_map_data).return_value = MagicMock()

        response = create_or_update_aspect(data_product_id, "aspect_type_A", {})
        
        mock_update_bq_table.assert_not_called()
        self.assertEqual(response, {"response": []}) # No updates made

    @patch('src.app.services.operations_handler.data_product', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_asset_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.aspect_type_env_mapping', new_callable=MagicMock)
    @patch('src.app.services.operations_handler.update_system_entry_bq_table')
    @patch('src.app.services.operations_handler.json_to_aspect_generator')
    @patch('src.app.services.operations_handler.get_gcp_asset_list_from_mapping')
    @patch('src.app.services.operations_handler.get_dataplex_project_id_and_region_from_mapping')
    def test_create_or_update_aspect_general_exception(
            self, mock_get_env_mapping, mock_get_asset_list, mock_json_to_aspect,
            mock_update_bq_table,
            mock_env_map_data, mock_asset_map_data, mock_dp_data):

        mock_get_env_mapping.return_value = {"dataplex_project_id": "dp-proj", "dataplex_region": "dp-reg"}
        # Simulate an error during get_gcp_asset_list_from_mapping
        error_message = "Failed to get asset list"
        mock_get_asset_list.side_effect = Exception(error_message)
        
        # These won't be called but need to be part of the patch stack
        mock_json_to_aspect.return_value = {}
        mock_update_bq_table.return_value = {}
        mock_dp_data.return_value = [] 
        type(mock_env_map_data).return_value = MagicMock()
        type(mock_asset_map_data).return_value = MagicMock()


        response = create_or_update_aspect("product1", "aspect_type_A", {})
        
        self.assertIsNotNone(response)
        self.assertIsNone(response["response"])
        self.assertEqual(response["error"], error_message)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
